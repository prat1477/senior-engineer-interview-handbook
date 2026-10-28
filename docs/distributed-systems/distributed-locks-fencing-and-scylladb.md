---
title: Distributed Locks, Fencing, and ScyllaDB Patterns
description: Leases, fencing tokens, LWT, shard-per-core — high-level accurate patterns.
status: covered
audience: advanced
tags: [distributed-systems, scylladb, locks]
created: 2026-10-25
updated: 2026-10-25
---

# Distributed Locks, Fencing, and ScyllaDB Patterns

## Distributed locks and leases

Locks with **TTL/lease** expire if holder crashes — but delayed holder can still write after lease expires unless storage **rejects stale tokens**.

## Fencing tokens

Monotonic token issued with lock; storage accepts writes only if `token > last_seen`. **Protection requires the resource to check the token** — a lock alone (e.g. naive Redis lock) does not automatically fence downstream storage.

## Sagas, at-least-once, idempotency

Event delivery is often **at-least-once** — consumers must be **idempotent**. Aligns with [Concurrency L22](../concurrency/22-backend-concurrency-scenarios.md).

## ScyllaDB / Cassandra-family (conceptual)

- **Shard-per-core** architecture — partitions map to tokens; each CPU handles subset of data.
- **CommitLog → MemTable → SSTable** — write path; **compaction** merges SSTables (operational cost).
- **Lightweight transactions (LWT)** — conditional writes for compare-and-set at partition level (latency cost — use deliberately).
- **Hot partitions** — one key dominates traffic; **synthetic sharding** splits logical key (`user#bucket`) but complicates reads/aggregations — not free performance.

## Driver routing

Use **token-aware** / **shard-aware** drivers per current ScyllaDB documentation for your version — **do not** document unverified `token % cores` formulas here.

## Cross-links

- [Distributed systems index](index.md)
- [Kafka track](../kafka/index.md)

**Verify:** LWT semantics, driver APIs, and routing against official ScyllaDB docs for deployed version.
