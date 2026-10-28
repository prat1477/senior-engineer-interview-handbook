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

## Cross-links

- [Lesson 5 — volatile](05-volatile.md)
- [Lesson 3 — Races](03-race-conditions.md)
