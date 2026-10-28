---
title: "Lesson 23 — AI-System Concurrency"
description: Fan-out, quotas, timeouts, bounded executors for model calls.
status: covered
audience: advanced
tags: [concurrency, lesson-23, ai]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 23 — AI-System Concurrency

Backend patterns around **concurrent model/provider calls** — not product-specific requirements.

## Typical pressures

- **Fan-out** — RAG retrieves many chunks; parallel embedding or LLM calls.
- **Provider quotas** — tokens/min, concurrent request caps.
- **Long latencies** — threads blocked on HTTP; virtual threads may help **if** pinning is controlled.
- **Cancellation** — client disconnect should cancel in-flight provider calls where supported.

## Patterns

| Concern | Approach |
| --- | --- |
| Concurrency cap | Semaphore / bulkhead per provider ([Lesson 16](16-coordination-primitives.md)) |
| Rate limit | Token bucket (distributed if multi-instance) |
| Timeout | Per-call and overall deadline (`CompletableFuture.orTimeout` JDK 9+) |
| Executor | Isolate blocking HTTP from CPU post-processing ([Lesson 12](12-completable-future.md)) |
| Coalescing | Dedupe identical in-flight prompts ([Lesson 22B](22-backend-concurrency-scenarios.md)) |

## Pitfalls

- Unbounded `parallelStream` over retrieval hits provider limits.
- Ignoring **429** retry-after headers → thundering herd.
- Storing large responses in `ThreadLocal` on many VTs.

## Cross-links

- [Lesson 22 — Rate vs concurrency](22-backend-concurrency-scenarios.md)
