---
title: "Collections — Assessment Answers"
description: Answers for Module 4 interview practice.
status: draft
audience: advanced
tags: [collections, interview, answers, module-4]
created: 2026-10-17
updated: 2026-10-17
---

# Collections — Assessment Answers

## 1. Map vs Collection

`Map` models key–value associations, not a bag of elements. API uses `entrySet` / `keySet` views instead of inheriting `Collection` operations that do not fit.

## 2. Fail-fast ≠ thread-safe

Fail-fast iterators detect concurrent **structural** modification on **one** thread’s iteration and throw `ConcurrentModificationException` — best-effort, not synchronization. Concurrent `put` without `ConcurrentHashMap` risks corruption.

## 3. Comparable vs Comparator

`TreeSet` needs **total order**: natural (`Comparable`) or external (`Comparator` at construction). Inconsistent compare → subtle bugs.

## 4. Mutable key

Entry remains in old bucket; `get` with updated key misses — “lost” entry.

## 5. HashMap vs TreeMap `get`

`HashMap` **O(1)** average; `TreeMap` **O(log n)**.

## 6. ArrayDeque vs LinkedList

`ArrayDeque` — array-backed, better cache locality, no node overhead; preferred for stack/queue on single thread.

## 7. `remove(Object)` on PQ

Must find element in heap array **O(n)** then reheapify.

## 8. Hash codes

No — collisions allowed; `equals` disambiguates.

## 9. LRU LinkedHashMap

`accessOrder = true`, override `removeEldestEntry` when size > capacity.

## 10. Min-heap for K largest

Root is smallest among current K — evict when better candidate arrives. Max-heap of size K keeps K smallest.

## 11. Bounded producer-consumer

`ArrayBlockingQueue` — `put` blocks when full (backpressure). `PriorityBlockingQueue` unbounded — no backpressure on producers.

## 12. containsKey + put

**Not atomic** — race between threads. Use `putIfAbsent` / `computeIfAbsent`.

## 13. Collection picks

(a) `TreeMap`, (b) `LinkedHashSet`, (c) `PriorityBlockingQueue` (or `PriorityQueue` if single-threaded).

## Mini-assessment

**A.** `ConcurrentModificationException` on iterator (fail-fast), not guaranteed in all cases.

**B.** `ArrayList` O(1) index; `LinkedList` O(n) walk.

**C.** `ConcurrentLinkedQueue` — unbounded lock-free FIFO; `ArrayBlockingQueue` — bounded blocking FIFO.
