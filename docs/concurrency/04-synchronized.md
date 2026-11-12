---
title: "Lesson 4 — synchronized"
description: Monitors, reentrancy, intrinsic locks.
status: covered
audience: advanced
tags: [concurrency, lesson-4]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 4 — `synchronized`

## Mechanics

Monitor lock — one thread per object monitor; **reentrant** (same thread can re-enter).

```java
synchronized (lock) {
    // mutual exclusion + unlock happens-before next lock
}
```

## Limits

- Coarse-grained — contention hurts throughput.
- No try/timeout (use `ReentrantLock`).
- On virtual threads: may **pin** carrier during blocking (JDK-dependent) — [Lesson 14](14-virtual-threads.md).

## Compound operations and collection wrappers

`Collections.synchronizedList` serializes its individual methods on a common monitor. It does
not make a check-then-act sequence atomic, and its iterator must be used under that monitor:

```java
List<Integer> numbers = Collections.synchronizedList(new ArrayList<>());

synchronized (numbers) {
    if (!numbers.contains(100)) {
        numbers.add(100);
    }
}
```

The same lock covers the check and update, preventing two threads from both seeing absence and
adding. Iteration uses the same pattern: `synchronized (numbers) { for (...) { ... } }`.

## Cross-links

- [Lesson 6 — Locks](06-locks.md)
