---
title: "Lesson 18 — Deadlock, Livelock, and Starvation"
description: Definitions, examples, prevention strategies.
status: covered
audience: advanced
tags: [concurrency, lesson-18]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 18 — Deadlock, Livelock, and Starvation

## Definitions

| Condition | Behavior |
| --- | --- |
| **Deadlock** | Circular wait — no thread can proceed (blocked forever without external action) |
| **Livelock** | Threads keep reacting (retry, yield) but **no useful progress** |
| **Starvation** | Thread persistently denied CPU, lock, or permit while others advance |

## Deadlock example

```java
// Thread1: lock A then B; Thread2: lock B then A — classic cycle
```

**Prevention:** global **lock ordering** (always acquire A before B), timeouts (`tryLock`), reduce lock scope, avoid nested locks.

## Livelock example

Two threads both “politely” back off and retry the same resource at the same time — analogous to corridor standoff. Fix: **randomized exponential backoff**, jitter, or queue mediator.

## Starvation

Unfair lock (`synchronized` no fairness) or high-priority threads monopolize CPU. `ReentrantLock(true)` fairness reduces starvation at throughput cost.

## Unbounded queues

Producers never block → consumers fall behind → latency grows without bound (not deadlock, but **overload**).

## Cross-links

- [Lesson 21 — Thread dumps](21-production-debugging.md)
- [Lesson 16 — Semaphores](16-coordination-primitives.md)
