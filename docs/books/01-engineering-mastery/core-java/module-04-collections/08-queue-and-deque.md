---
title: "Lesson 8 — Queue and Deque Fundamentals"
description: "FIFO, deque operations, ArrayDeque vs legacy Stack, and complexity."
status: covered
audience: practitioner
tags: [[collections, queue, deque, module-4, lesson-8], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 8 — Queue and Deque Fundamentals

FIFO, deque operations, ArrayDeque vs legacy Stack, and complexity.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/08-queue-and-deque.md) compresses interview signal without
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


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/08-queue-and-deque.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
