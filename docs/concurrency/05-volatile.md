---
title: "Lesson 5 — volatile"
description: Visibility, publication, limits for compound ops.
status: covered
audience: advanced
tags: [concurrency, lesson-5]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 5 — `volatile`

## Guarantees

Writes visible to subsequent reads by other threads (happens-before via volatile semantics).

## Use cases

- Status flags (`shutdown`, `initialized`)
- Single-writer publication patterns (with care)

## Not for

`i++` on volatile — still racy. Use atomics or locks.

## Why `volatile int count` still loses increments

```java
private volatile int count;

void increment() {
    count++; // read count, add one, write count
}
```

Two threads can both read `10`, each calculate `11`, and both write `11`. Volatile makes each
read/write visible with ordering rules; it does not turn the read-modify-write sequence into one
indivisible action. Use `AtomicInteger.incrementAndGet()` for a single atomic counter operation
or a lock when the invariant spans several fields/actions.

`synchronized` combines mutual exclusion with memory semantics: an unlock happens-before a
later lock of the same monitor. A synchronized writer alone does not establish a complete
visibility contract for an unsynchronized reader:

```java
public synchronized void increment() { count++; }
public int getCount() { return count; } // reader does not acquire the same monitor
```

Synchronize `getCount`, make its read governed by another valid publication design, or use an
atomic counter. Do not reason from “the write happened first in real time”; reason from the
specified happens-before edge.

## Cross-links

- [Lesson 2 — JMM](02-java-memory-model.md)
