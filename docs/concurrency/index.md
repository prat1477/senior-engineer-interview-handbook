---
title: Java Concurrency Curriculum
description: 24-lesson fixed sequence for senior Java concurrency interviews.
status: covered
audience: advanced
tags: [concurrency]
created: 2026-10-15
updated: 2026-10-25
---

# Java Concurrency Curriculum

Study **after** [Core Java Modules 2–9](../books/01-engineering-mastery/index.md). Lesson order is **fixed** — do not reorder.

**Interview revision:** [Book 2 — Concurrency Companion](../books/02-interview-companion/concurrency/index.md) (diagrams, whiteboard scripts, [visual quick reference](../books/02-interview-companion/concurrency/module-visual-quick-reference.md), [practice](../books/02-interview-companion/concurrency/module-interview-practice.md)).

| # | Lesson | File | Status |
| --- | --- | --- | --- |
| 1 | Concurrency fundamentals | [01-concurrency-fundamentals.md](01-concurrency-fundamentals.md) | Covered |
| 2 | Java Memory Model | [02-java-memory-model.md](02-java-memory-model.md) | Covered |
| 3 | Race conditions | [03-race-conditions.md](03-race-conditions.md) | Covered |
| 4 | `synchronized` | [04-synchronized.md](04-synchronized.md) | Covered |
| 5 | `volatile` | [05-volatile.md](05-volatile.md) | Covered |
| 6 | Locks | [06-locks.md](06-locks.md) | Covered |
| 7 | Atomics / CAS | [07-atomics-and-cas.md](07-atomics-and-cas.md) | Covered |
| 8 | `LongAdder` | [08-longadder.md](08-longadder.md) | Covered |
| 9 | Concurrent collections | [09-concurrent-collections.md](09-concurrent-collections.md) | Covered |
| 10 | Executors / `ThreadPoolExecutor` | [10-executors-and-thread-pool-executor.md](10-executors-and-thread-pool-executor.md) | Covered |
| 11 | Thread pool sizing + backpressure | [11-thread-pool-sizing-and-backpressure.md](11-thread-pool-sizing-and-backpressure.md) | Covered |
| 12 | `CompletableFuture` | [12-completable-future.md](12-completable-future.md) | Covered |
| 13 | `ForkJoinPool` | [13-forkjoin-pool.md](13-forkjoin-pool.md) | Covered |
| 14 | Virtual threads | [14-virtual-threads.md](14-virtual-threads.md) | Covered |
| 15 | `ThreadLocal` + `ScopedValue` | [15-threadlocal-and-scoped-value.md](15-threadlocal-and-scoped-value.md) | Covered |
| 16 | Coordination primitives | [16-coordination-primitives.md](16-coordination-primitives.md) | Covered |
| 17 | Producer–consumer | [17-producer-consumer-patterns.md](17-producer-consumer-patterns.md) | Covered |
| 18 | Deadlock / livelock / starvation | [18-deadlock-livelock-starvation.md](18-deadlock-livelock-starvation.md) | Covered |
| 19 | Thread-safety patterns | [19-thread-safety-patterns.md](19-thread-safety-patterns.md) | Covered |
| 20 | Advanced concurrency | [20-advanced-concurrency.md](20-advanced-concurrency.md) | Covered |
| 21 | Production debugging | [21-production-debugging.md](21-production-debugging.md) | Covered |
| 22 | Backend scenarios | [22-backend-concurrency-scenarios.md](22-backend-concurrency-scenarios.md) | Covered |
| 23 | AI-system concurrency | [23-ai-system-concurrency.md](23-ai-system-concurrency.md) | Covered |
| 24 | Senior interview assessment | [24-senior-interview-assessment.md](24-senior-interview-assessment.md) | Covered |

## Related handbook material

- [Database concurrency](../distributed-systems/database-concurrency-and-isolation.md)
- [Distributed locks & ScyllaDB](../distributed-systems/distributed-locks-fencing-and-scylladb.md)
- [Collections M4 L12](../books/01-engineering-mastery/core-java/module-04-collections/12-concurrent-collections-overview.md) — introductory CHM (Lesson 9 deepens)

Days 3–4 of the [14-day roadmap](../14-day-roadmap.md) align with lessons 1–11+.

**Note:** `senior_java_virtual_threads_jvm_memory_handbook.md` was **not found** in this repository; virtual-thread content is integrated in [Lesson 14](14-virtual-threads.md).
