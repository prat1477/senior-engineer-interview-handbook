---
title: "Lesson 9 — PriorityQueue and Binary Heaps"
description: Heap structure, min/max heap, complexities, and iteration vs poll order.
status: draft
audience: advanced
tags: [collections, priorityqueue, heap, module-4, lesson-9]
created: 2026-10-15
updated: 2026-10-15
---

# Lesson 9 — PriorityQueue and Binary Heaps

`PriorityQueue` orders elements by **priority**, not FIFO arrival. OpenJDK implements it with a **binary heap** in an array.

## 1. Priority vs FIFO

- **FIFO:** first in, first out (`ArrayDeque`, typical `BlockingQueue`).
- **Priority:** smallest (or largest) priority element is always at the **root**.

## 2. Min-heap example (natural ordering)

```java
PriorityQueue<Integer> pq = new PriorityQueue<>();

pq.offer(8);
pq.offer(2);
pq.offer(5);
pq.offer(1);

System.out.println(pq.peek()); // 1 — minimum at root
```

Repeated `poll()` returns `1, 2, 5, 8` — sorted order **only** if you drain the queue.

## 3. Max-heap

```java
PriorityQueue<Integer> maxHeap =
    new PriorityQueue<>(Comparator.reverseOrder());
```

For custom types where **larger number = higher priority**, use a comparator that orders high priority first (often `reverseOrder` on natural order or custom `Comparator`).

## 4. Operations (typical)

| Operation | Complexity |
| --- | ---: |
| `peek()` | O(1) |
| `offer()` / `add()` | O(log n) |
| `poll()` | O(log n) |
| `remove(Object)` | O(n) |
| `contains(Object)` | O(n) |

**`poll()`** removes root, moves last leaf to root, **sifts down** — restores heap property in O(log n).

**`remove(Object)`** must **find** element in heap array (linear scan), then adjust — O(n) search + O(log n) fix.

## 5. Iteration trap

```java
for (Integer x : pq) { ... }  // NOT guaranteed sorted order
```

Iterator walks the **internal array**, not sorted sequence. Only repeated `poll()` yields priority order.

## 6. Restrictions and thread safety

- **No null** elements.
- **Duplicates allowed** (not a set).
- **Not thread-safe** — use `PriorityBlockingQueue` for concurrent consumers ([Lesson 10](10-blocking-queues-and-backpressure.md)).

## 7. Use cases

| Scenario | Why PQ |
| --- | --- |
| Background job scheduling | Always process highest priority next |
| Top-K | Maintain size-K heap |
| Dijkstra | Extract min-distance vertex |
| Merge K sorted lists | Heap of list heads |
| Streaming median | Two heaps technique |

**Not built-in:** efficient cancel-by-job-ID — `remove(Object)` is O(n); indexed heap + map is a custom design ([Lesson 13](13-selecting-the-right-collection.md)).

## Revision notes

- Binary heap: complete tree in array; root = best priority.
- Comparator defines "best".
- Iterate ≠ sorted; `poll` drains in order.

## See also

- [Blocking queues](10-blocking-queues-and-backpressure.md)
- [Comparable and Comparator](06-comparable-and-comparator.md)
