---
title: "Lesson 13 — Selecting the Right Collection"
description: "Decision guide by access pattern, scale, concurrency, and job scheduling."
status: covered
audience: practitioner
tags: [[collections, design, module-4, lesson-13], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 13 — Selecting the Right Collection

Decision guide by access pattern, scale, concurrency, and job scheduling.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/13-selecting-the-right-collection.md) compresses interview signal without
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

# Lesson 13 — Selecting the Right Collection

Senior interviews ask you to **justify** structures against dominant operations, ordering, memory, and concurrency — not to recite class names.

## 1. Quick decision guide

| Need | Often choose |
| --- | --- |
| Fast key lookup; sorted report rare | `HashMap` + sort on demand |
| Fast lookup + frequent sorted key walk | `TreeMap` |
| Fast lookup + LRU / access tracking | Access-order `LinkedHashMap` |
| Unique, unordered | `HashSet` |
| Unique, insertion order | `LinkedHashSet` |
| Unique, sorted | `TreeSet` |
| Next best priority repeatedly | `PriorityQueue` |
| Thread-safe priority + block on empty | `PriorityBlockingQueue` |
| Bounded FIFO producer-consumer | `ArrayBlockingQueue` |
| Stack / deque, single-threaded | `ArrayDeque` |
| Default sequential list | `ArrayList` |

## 2. One million employees

**Pattern A:** ID lookups all day; salary-sorted report nightly.

- `HashMap<Long, Employee>` for hot path.
- Nightly: stream values, sort by salary, export — O(n log n) acceptable once per day.
- Avoid second sorted structure updated on every salary change.

**Pattern B:** ID lookups **and** constant salary-ordered traversal.

- Option 1: `TreeMap` keyed by salary — only if salary is truly the key (duplicate salaries collide — need composite key).
- Option 2: `HashMap` + secondary sorted index — every update maintains both → engineering cost and bug risk.

## 3. Job scheduling and cancellation

| Requirement | Tool | Caveat |
| --- | --- | --- |
| Poll highest priority job | `PriorityQueue` | O(log n) poll |
| Lookup job metadata by ID | `HashMap<ID, Job>` | Does not remove from heap |
| Cancel arbitrary job by ID | `PriorityQueue.remove(job)` | **O(n)** search |
| Fast arbitrary cancel | Indexed priority queue (custom) | Map ID → heap index; complex |

**Practical answer:** PQ + map for metadata; cancellation either marks job cancelled (lazy skip on poll) or pays O(n) remove — state trade-off in design discussion, not a required implementation lesson.

## 4. Dimensions to articulate

- **Dominant operations** — read vs write ratio.
- **Ordering guarantees** — none, insertion, access, sorted.
- **Memory** — linked structures vs arrays; unbounded queues.
- **Concurrency** — single-threaded vs `Concurrent*` vs blocking queues.
- **Update frequency** — cost of maintaining auxiliary indexes.


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/13-selecting-the-right-collection.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
