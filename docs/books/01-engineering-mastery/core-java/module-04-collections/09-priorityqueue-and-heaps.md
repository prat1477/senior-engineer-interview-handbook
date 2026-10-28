---
title: "Lesson 9 — PriorityQueue and Binary Heaps"
description: "Heap structure, min/max heap, complexities, and iteration vs poll order."
status: covered
audience: practitioner
tags: [[collections, priorityqueue, heap, module-4, lesson-9], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 9 — PriorityQueue and Binary Heaps

Heap structure, min/max heap, complexities, and iteration vs poll order.

## Shared domain models

Examples across Modules 4–9 reuse the same records so mental models transfer:

```java
public record Employee(long id, String name, String department, double salary) {}
public record Order(long id, long employeeId, String sku, int quantity, double unitPrice) {}
public record Payment(long orderId, String method, double amount, java.time.Instant paidAt) {}
```

Use them for grouping (`Collectors.groupingBy`), maps (`Map<Long, Employee>`), optional chains
(`Optional<Employee>`), and exception boundaries around payment APIs.

## Big picture

Core Java Module 4 — **Collections**. This is the canonical Engineering Mastery
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/09-priorityqueue-and-heaps.md) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

## Architecture

This lesson sits in **Module 4** of the Core Java track. Service code should treat
collection/generics/stream/JVM choices as **capacity and correctness** decisions, not style preferences.

## Internal working

Review the numbered sections in **Core concepts (canonical)** below. For interviews, pair each
fact with **complexity**, **ordering**, and **concurrency** implications.

## Hands-on

```java
// Extend the snippet in the canonical section with Employee / Order / Payment records.
// JDK 17+: compile with your module's test source set or `java Main.java`.
```

## Performance

State average vs worst-case costs for the structures or APIs introduced in this lesson.
Call out allocation hot spots (boxing, autoboxing in streams, defensive copies).

## JDK tools and diagnostic clues

- Watch for lesson-specific exceptions in logs (`ConcurrentModificationException`, `ClassCastException`
  at erasure boundaries, `OutOfMemoryError` subtypes for JVM modules).
- Use **async profiler**, **JFR**, or **heap histogram** (`jcmd <pid> GC.class_histogram`) when
  production symptoms match this topic.

## Failure scenarios

Document one production failure mode tied to misuse of this lesson's API, and the guardrail
(service validation, bounded queues, explicit comparators, try-with-resources).

## Best practices and anti-patterns

- Prefer clear types over clever one-liners.
- Make null and empty collection policies explicit at API edges.

> **Production insight**
> Align collection mutability with transaction boundaries — shared mutable structures between
> threads remain the top source of subtle bugs.

## Staff engineer notes

- Teach the **contract** first (what callers may assume), then the **implementation** (how it is enforced).
- Link forward to Module 12 concurrent collections when discussing multi-threaded mutation.

## Core concepts (canonical)

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
| Top-K | Maintain size-K heap (see below) |
| Dijkstra | Extract min-distance vertex |
| Merge K sorted lists | Heap of list heads |
| Streaming median | Two heaps technique |

**Not built-in:** efficient cancel-by-job-ID — `remove(Object)` is O(n); indexed heap + map is a custom design ([Lesson 13](13-selecting-the-right-collection.md)).

## 8. Top-K largest with a size-K **min-heap**

To retain the **K largest** salaries (or any metric), use a **min-heap** capped at K elements:

- When size `< K`, `offer` every element.
- When size `== K` and a new value is **greater than the heap minimum** (`peek()`), `poll()` the min and `offer` the new value.
- Elements smaller than the current K-th largest are discarded without growing the heap.

```java
record Employee(String name, double salary) {}

List<Employee> topKBySalary(List<Employee> all, int k) {
    PriorityQueue<Employee> minHeap =
        new PriorityQueue<>(Comparator.comparingDouble(Employee::salary));

    for (Employee e : all) {
        if (minHeap.size() < k) {
            minHeap.offer(e);
        } else if (e.salary() > minHeap.peek().salary()) {
            minHeap.poll();
            minHeap.offer(e);
        }
    }
    return new ArrayList<>(minHeap); // iteration order ≠ sorted; sort if needed
}
```

**Why min-heap for largest?** The root is always the **weakest** survivor among the K candidates — the first element you would evict when something better arrives. A max-heap of size K would retain the K **smallest** among seen elements (wrong problem).

**Complexity:** `O(n log k)` time, `O(k)` space vs `O(n log n)` for full sort. For small K on large `n`, the heap wins; for `k ≈ n`, sorting the list may be simpler and competitive.

**Streams tie-in:** full sort vs bounded heap trade-offs are revisited in [Streams lesson 4 — performance](../module-06-java-8-streams/04-correctness-parallel-performance.md).


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/09-priorityqueue-and-heaps.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
