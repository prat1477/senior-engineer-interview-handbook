---
title: "Lesson 10 — PriorityBlockingQueue, ArrayBlockingQueue, and Backpressure"
description: Thread-safe queues, blocking semantics, bounded capacity, and overload.
status: draft
audience: advanced
tags: [collections, blockingqueue, backpressure, module-4, lesson-10]
created: 2026-10-15
updated: 2026-10-15
---

# Lesson 10 — PriorityBlockingQueue, ArrayBlockingQueue, and Backpressure

Blocking queues connect **producers** and **consumers** across threads. They differ in **ordering**, **bounds**, and **backpressure** — critical for senior system design answers.

## 1. Comparison

| | `PriorityQueue` | `PriorityBlockingQueue` | `ArrayBlockingQueue` | `ConcurrentLinkedQueue` |
| --- | --- | --- | --- | --- |
| Thread-safe | No | Yes | Yes | Yes |
| Ordering | Priority | Priority | FIFO | FIFO |
| Bounded | No | **Logically unbounded** | Fixed capacity | Unbounded |
| Blocking `take`/`put` | No | Yes (`take` blocks if empty) | Yes | Non-blocking (`poll`) |

## 2. `PriorityBlockingQueue`

- **Unbounded** — `initialCapacity` is only array growth hint, **not** a max size.
- `take()` **blocks** until an element is available.
- `put(e)` does not block for capacity (unbounded) — **no producer backpressure** from queue size.
- Thread-safe priority ordering for consumer pools.

**Design gap:** If you need **strict priority** and **hard max capacity**, ordinary `PriorityBlockingQueue` is insufficient — you need a custom bounded-priority structure or layered design (semaphore + queue, etc.).

## 3. `ArrayBlockingQueue`

- **Fixed capacity** at construction.
- `put(e)` **blocks** when full — applies **backpressure** to producers.
- `take()` blocks when empty.
- FIFO — fair optional constructor for threads.

## 4. Overload scenario

**Arrival:** 1,000 jobs/s. **Database processing:** 200 jobs/s. **Sustained deficit:** 800 jobs/s accumulates.

| Design | Behavior |
| --- | --- |
| Unbounded `PriorityBlockingQueue` | Memory grows; latency from head-of-line and GC; producers never slow |
| `ArrayBlockingQueue` (capacity N) | Producers block or fail when full; forces drop, scale consumers, or shed load |

Increasing unbounded queue size **delays** pain; it does **not** increase downstream throughput.

## 5. When to use what

- **Priority + blocking consumer, overload acceptable in memory** → `PriorityBlockingQueue` with monitoring and shedding elsewhere.
- **FIFO + enforce capacity** → `ArrayBlockingQueue` + thread pools.
- **Non-blocking handoff** → `ConcurrentLinkedQueue` with your own backpressure policy.

## Revision notes

- `take()` blocks on empty blocking queues.
- `put()` blocks on full **bounded** queue.
- `PriorityBlockingQueue` ≠ bounded; no capacity backpressure.
- Backpressure protects latency and memory.

## See also

- [PriorityQueue](09-priorityqueue-and-heaps.md)
- [Concurrent collections](12-concurrent-collections-overview.md)
- Concurrency track: thread pools (planned)
