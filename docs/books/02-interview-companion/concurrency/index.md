---
title: Java Concurrency — Interview Companion
description: Book 2 recall pages for the 24-lesson concurrency curriculum.
status: covered
audience: advanced
tags: [companion, concurrency]
updated: 2026-10-25
---

# Java Concurrency — Interview Companion

Derived from the canonical [Concurrency curriculum](../../../concurrency/index.md). Lesson order is **fixed** — same as Book 1 study path.

| # | Companion | Canonical | Visual focus |
| --- | --- | --- | --- |
| 1 | [01-fundamentals](01-concurrency-fundamentals.md) | [L1](../../../concurrency/01-concurrency-fundamentals.md) | Thread states, safety vs liveness |
| 2 | [02-jmm](02-java-memory-model.md) | [L2](../../../concurrency/02-java-memory-model.md) | Happens-before edges |
| 3 | [03-races](03-race-conditions.md) | [L3](../../../concurrency/03-race-conditions.md) | Lost-update timeline |
| 4 | [04-synchronized](04-synchronized.md) | [L4](../../../concurrency/04-synchronized.md) | Monitor enter/exit |
| 5 | [05-volatile](05-volatile.md) | [L5](../../../concurrency/05-volatile.md) | Visibility vs atomicity |
| 6 | [06-locks](06-locks.md) | [L6](../../../concurrency/06-locks.md) | `ReentrantLock` try/finally |
| 7 | [07-atomics](07-atomics-and-cas.md) | [L7](../../../concurrency/07-atomics-and-cas.md) | CAS retry loop |
| 8 | [08-longadder](08-longadder.md) | [L8](../../../concurrency/08-longadder.md) | Cells vs hot `AtomicLong` |
| 9 | [09-chm](09-concurrent-collections.md) | [L9](../../../concurrency/09-concurrent-collections.md) | `merge` / `computeIfAbsent` |
| 10 | [10-executors](10-executors-and-thread-pool-executor.md) | [L10](../../../concurrency/10-executors-and-thread-pool-executor.md) | Submit → queue → worker |
| 11 | [11-pool-sizing](11-thread-pool-sizing-and-backpressure.md) | [L11](../../../concurrency/11-thread-pool-sizing-and-backpressure.md) | Saturation & rejection |
| 12 | [12-cf](12-completable-future.md) | [L12](../../../concurrency/12-completable-future.md) | `thenCompose` flatten |
| 13 | [13-fjp](13-forkjoin-pool.md) | [L13](../../../concurrency/13-forkjoin-pool.md) | Work-stealing |
| 14 | [14-vt](14-virtual-threads.md) | [L14](../../../concurrency/14-virtual-threads.md) | Mount / unmount |
| 15 | [15-threadlocal](15-threadlocal-and-scoped-value.md) | [L15](../../../concurrency/15-threadlocal-and-scoped-value.md) | Pool leak vs `remove()` |
| 16 | [16-coordination](16-coordination-primitives.md) | [L16](../../../concurrency/16-coordination-primitives.md) | Primitive picker table |
| 17 | [17-producer-consumer](17-producer-consumer-patterns.md) | [L17](../../../concurrency/17-producer-consumer-patterns.md) | Queue vs Kafka |
| 18 | [18-deadlock](18-deadlock-livelock-starvation.md) | [L18](../../../concurrency/18-deadlock-livelock-starvation.md) | Cycle vs livelock |
| 19 | [19-patterns](19-thread-safety-patterns.md) | [L19](../../../concurrency/19-thread-safety-patterns.md) | Pattern decision tree |
| 20 | [20-advanced](20-advanced-concurrency.md) | [L20](../../../concurrency/20-advanced-concurrency.md) | Ring buffer / false sharing |
| 21 | [21-debug](21-production-debugging.md) | [L21](../../../concurrency/21-production-debugging.md) | Dump → hypothesis |
| 22 | [22-backend](22-backend-concurrency-scenarios.md) | [L22](../../../concurrency/22-backend-concurrency-scenarios.md) | Payment state machine |
| 23 | [23-ai](23-ai-system-concurrency.md) | [L23](../../../concurrency/23-ai-system-concurrency.md) | Fan-out + bulkhead |
| 24 | [24-assessment](24-senior-interview-assessment.md) | [L24](../../../concurrency/24-senior-interview-assessment.md) | Topic matrix → full mock |

## Module tools

- [Visual quick reference](module-visual-quick-reference.md) — last-minute diagrams before interviews
- [Interview practice](module-interview-practice.md)
- [Assessment answers](module-interview-assessment-answers.md)
