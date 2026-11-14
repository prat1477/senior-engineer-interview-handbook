---
title: Spring Boot Caching and Resilience Quick Reference
description: PR review, cache correctness, Redis failure, and multi-pod database protection.
status: covered
audience: advanced
tags: [companion, spring-boot, caching, redis, resilience]
created: 2026-11-12
updated: 2026-11-12
---

# Spring Boot Caching and Resilience Quick Reference

**Canonical source:** [production PR review and resilience](../../../spring-microservices/02-production-pr-review-caching-and-resilience.md).

## 1. Spring Boot PR-review checklist

| Check | Say this | Trap |
| --- | --- | --- |
| Singleton field | One bean instance is shared by concurrent requests in a pod. | Singleton means thread-safe. |
| `HashMap` | Concurrent mutation is unsafe; start with `ConcurrentHashMap` or a cache. | Concurrent map solves cache consistency. |
| `containsKey` + `get` | Two operations; often harmless for a cache read, but avoid needless race. | Every non-atomic read pair is a business bug. |
| Cache miss | Coalesce/limit expensive loads; `computeIfAbsent` is per-key mapping atomicity. | It coordinates DB work across pods. |
| Injection | Constructor injection makes requirements/test seams explicit. | Field injection is equivalent for testing. |
| Missing order | Domain exception + `@ControllerAdvice` -> 404. | Normal absence becomes accidental 500. |

**30-second answer:** “I identify the singleton's shared mutable `HashMap`, make dependencies and
404 behavior explicit, then review cache bounds, stale-data policy, cross-pod scope, and outage
behavior. Thread safety is necessary but not sufficient.”

## 2. Cache strategy picker

| Pattern | Read | Write | Memory cue |
| --- | --- | --- | --- |
| Cache-aside | app loads DB on miss | commit DB, then invalidate/update | app owns cache |
| Read-through | cache layer loads on miss | separate policy | Redis alone is not read-through |
| Write-through | cache-facing read | synchronously attempt store + cache | not one atomic transaction |
| Write-behind | cache serves write | durable async persistence | fast, but recovery matters |
| Write-around | normal cache reads | direct DB write/no warm | bypass is not invalidation |

**Most common misconception:** Cache hit rate alone means correct caching.

**Memory trick:** **Freshness + invalidation + failure policy = cache correctness.**

## 3. Stale-fill race

```text
Reader: miss -> reads PENDING
Writer: commits SHIPPED -> invalidates key
Reader: delayed write PENDING with TTL
```

TTL starts at the delayed fill, so it does not bound staleness from the newest database commit.
Use version-aware writes, coordination, ordered invalidation/event processing, or primary reads
when a strict freshness contract matters.

## 4. Redis, Caffeine, or database?

| Need | Prefer | Caveat |
| --- | --- | --- |
| Pod-local hot, bounded reads | Caffeine | no cross-pod coherence |
| Shared cache / TTL / coordinated state | Redis | network/failure/invalidation design |
| Same relational schema, read scale | PostgreSQL read replica | replication lag |
| Different denormalized query | CQRS projection | replay/lag/operations |
| Cheap or strict-freshness read | primary DB / no cache | protect with query/pool design |

Redis can use RDB/AOF persistence; it is not universally non-durable. Local `ConcurrentHashMap`
is per pod and unbounded unless a policy is added.

## 5. Redis failure controls

| Control | Controls | Not |
| --- | --- | --- |
| Circuit breaker | calls to an unhealthy dependency | throughput |
| Bulkhead / semaphore | concurrent in-flight work | request rate |
| Rate limiter | request starts per interval | concurrency |
| Bounded queue | burst absorption | sustainable DB throughput |
| Load shedding | protects service/downstream | an unexpected 500 |

Use short Redis timeouts, bounded retries/backoff/jitter where useful, half-open probes, and fast
fallback while the breaker is open. Return 429 for a client quota, 503 for temporary incapacity,
and 500 for unexpected errors.

## 6. HikariCP, pods, and HPA

```text
10 pods x 20 pool connections = 200 possible connections
```

Pool size is local. Checked-out connections, executing queries, RPS, and completed throughput are
different metrics. Budget against maximum pods and deployment surge; reserve DB headroom. HPA adds
application workers, not PostgreSQL capacity.

**Interview line:** “I set per-pod pool budgets from a measured cluster-wide DB budget and cap
replicas; I do not let CPU-only autoscaling multiply downstream concurrency.”

## 7. Cache memory and values

- Unbounded singleton caches retain strong references, increase old-gen/GC pressure, and can OOM.
- Caffeine: choose `maximumSize`/expiry from heap and workload; observe hit/miss, evictions, load latency, and old-gen.
- **Thread-safe container != thread-safe elements.** Cache immutable DTOs or protect mutable state.
- FIFO = oldest insertion; LRU = least recent access; LFU = least frequent use; TTL = time expiry.

**Follow-ups:** How would you stop a stale fill? Why can a semaphore not enforce a cluster-wide
limit? What cache state belongs in Redis versus a per-pod Caffeine cache?
