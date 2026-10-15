---
title: "Lesson 8 — Queue and Deque Fundamentals"
description: FIFO, deque operations, ArrayDeque vs legacy Stack, and complexity.
status: draft
audience: advanced
tags: [collections, queue, deque, module-4, lesson-8]
created: 2026-10-15
updated: 2026-10-15
---

# Lesson 8 — Queue and Deque Fundamentals

Queues model **producer-consumer** ordering; deques add **both-end** operations. **Ordering depends on implementation** — do not assume every `Queue` is FIFO without checking the type.

## 1. FIFO queues

Typical operations:

| Method | On empty | Action |
| --- | --- | --- |
| `offer(e)` | — | Insert; returns false if bounded full |
| `poll()` | returns `null` | Remove head |
| `peek()` | returns `null` | View head |
| `add(e)` | throws | Insert |
| `remove()` | throws | Remove head |
| `element()` | throws | View head |

Prefer **`offer` / `poll` / `peek`** in services where emptiness is normal.

## 2. `Deque`

- `addFirst` / `addLast`, `pollFirst` / `pollLast`, `peekFirst` / `peekLast`.
- **FIFO queue:** offer at tail, poll from head.
- **LIFO stack:** push/pop at one end (`ArrayDeque` as stack).

## 3. `ArrayDeque`

- Circular **array** backing; resizes as needed.
- **Not thread-safe**; **null elements not allowed**.
- Preferred over legacy **`Stack`** (extends `Vector`, synchronized overhead, legacy API) for single-threaded stacks.

Typical ops: **O(1)** amortized at ends.

## 4. `ConcurrentLinkedQueue` (intro)

Lock-free **unbounded** FIFO linked queue — thread-safe; discussed with blocking queues in [Lesson 10](10-blocking-queues-and-backpressure.md).

## 5. Use cases

| Structure | Use |
| --- | --- |
| `ArrayDeque` | BFS, undo stack, work queue (single-threaded) |
| `BlockingQueue` | Thread pool work handoff |
| `PriorityQueue` | Scheduling by priority ([Lesson 9](09-priorityqueue-and-heaps.md)) |

## Revision notes

- Queue contract ≠ always FIFO (`PriorityQueue` is priority-ordered).
- `ArrayDeque` for stack/queue; not thread-safe, no nulls.
- Exception vs null-returning APIs — choose for control flow.

## See also

- [PriorityQueue](09-priorityqueue-and-heaps.md)
- [Blocking queues](10-blocking-queues-and-backpressure.md)
