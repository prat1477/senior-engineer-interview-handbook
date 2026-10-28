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

## Cross-links

- [Lesson 18 — Deadlock](18-deadlock-livelock-starvation.md)
