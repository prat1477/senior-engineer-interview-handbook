---
title: "Lesson 10 — PriorityBlockingQueue, ArrayBlockingQueue, and Backpressure"
description: "Thread-safe queues, blocking semantics, bounded capacity, and overload."
status: covered
audience: practitioner
tags: [[collections, blockingqueue, backpressure, module-4, lesson-10], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 10 — PriorityBlockingQueue, ArrayBlockingQueue, and Backpressure

Thread-safe queues, blocking semantics, bounded capacity, and overload.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/10-blocking-queues-and-backpressure.md) compresses interview signal without
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


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/10-blocking-queues-and-backpressure.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
