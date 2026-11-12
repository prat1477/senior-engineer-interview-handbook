---
title: "Lesson 2 — Java Memory Model"
description: Happens-before, visibility, ordering.
status: covered
audience: advanced
tags: [concurrency, lesson-2, jmm]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 2 — Java Memory Model (JMM)

## Happens-before

If action A *happens-before* B, B observes A’s effects. Without HB, compilers/CPUs may reorder; other threads may see stale values.

**Sources:** `synchronized` unlock→lock, `volatile` write→read, `Thread.start/join`, `Concurrent` utilities, etc.

## Visibility vs atomicity

`volatile` ensures visibility of writes — **not** compound read-modify-write atomicity (`count++` still races).

## 10+ YOE pitch

“I reason in happens-before edges, not ‘it should be fine on my laptop.’”

## Shared memory, data races, and the JIT

Threads share heap objects but have no permission to assume that another thread immediately sees
an ordinary field write. The Java Memory Model (JMM) defines **visibility**, **ordering**, and
which actions are **atomic**. It deliberately does not promise a physical RAM read on every
access: CPUs cache, processors reorder, and the JIT may reuse or move reads when the JMM permits.

```java
private boolean running = true;

void start() {
    while (running) {
        // work
    }
}

void stop() {
    running = false;
}
```

Without a happens-before edge, this has a data race. Conceptually, a HotSpot optimization may
load `running` once and reuse that value (or hoist an equivalent read out of the loop), because
the observing thread has no synchronization proving another thread's write must be observed.
Hardware cache intuition is useful but incomplete: the JMM is the portable language-level
contract that constrains compiler and CPU transformations.

Make the flag `volatile` when it is an independently written/read state flag. A volatile write
happens-before a subsequent volatile read of the same field, providing visibility and ordering
around that publication. It does not make a multi-step invariant atomic.

| Concern | Question | Typical tool |
| --- | --- | --- |
| Visibility | Will this thread observe a completed write? | `volatile`, monitor, atomic, start/join |
| Atomicity | Can two updates interleave and lose work? | lock or atomic RMW |
| Ordering | May reads/writes be observed in an unsafe order? | happens-before edge |

### What I should say in an interview

“I start with happens-before, not cache folklore. Ordinary shared-field reads racing with writes
have no visibility or ordering guarantee; volatile creates a publication edge, while locks also
provide mutual exclusion.”

### What not to say

- “`volatile` reads directly from RAM.” It is a JMM guarantee, not that physical implementation.
- “A data race merely returns an old value.” It permits surprising visibility and ordering outcomes.

## Cross-links

- [Lesson 5 — volatile](05-volatile.md)
- [Lesson 3 — Races](03-race-conditions.md)
