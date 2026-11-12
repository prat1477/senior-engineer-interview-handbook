---
title: "Lesson 6 — Locks"
description: ReentrantLock, fairness, tryLock, Condition.
status: covered
audience: advanced
tags: [concurrency, lesson-6]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 6 — Locks

## `ReentrantLock`

```java
lock.lock();
try {
    // critical section
} finally {
    lock.unlock();
}
```

`tryLock(timeout)` avoids indefinite deadlock; **always** unlock in `finally`.

## Fairness

`new ReentrantLock(true)` — reduces starvation, lowers throughput.

## vs `synchronized`

Explicit timeouts, multiple `Condition` objects, lock interruptibility.

## Foundation-level decision guide

`ReentrantLock` offers the same mutual-exclusion role as an intrinsic monitor while adding
timed `tryLock`, interruptible acquisition (`lockInterruptibly`), optional fairness, and multiple
`Condition` queues. Fair locks reduce barging/starvation risk but usually reduce throughput.
Use a `Condition` only with its owning lock and await in a predicate loop. This is foundation
coverage; deeper lock internals and coordination practice remain **pending**.

| Need | Prefer |
| --- | --- |
| Simple scoped mutual exclusion | `synchronized` |
| Timeout / cancellation while acquiring | `ReentrantLock` |
| Separate wait sets / advanced coordination | `ReentrantLock` + `Condition` |

## Cross-links

- [Lesson 18 — Deadlock](18-deadlock-livelock-starvation.md)
