---
title: "Lesson 5 — HashMap vs LinkedHashMap vs TreeMap"
description: "Ordering modes, complexity trade-offs, and when to sort on demand."
status: covered
audience: practitioner
tags: [[collections, map, module-4, lesson-5], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 5 — HashMap vs LinkedHashMap vs TreeMap

Ordering modes, complexity trade-offs, and when to sort on demand.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/05-hashmap-linkedhashmap-treemap.md) compresses interview signal without
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

# Lesson 5 — HashMap vs LinkedHashMap vs TreeMap

Choose a map by **lookup frequency**, **iteration order needs**, and **whether sorted structure is worth continuous maintenance**.

## 1. Comparison

| | `HashMap` | `LinkedHashMap` | `TreeMap` |
| --- | --- | --- | --- |
| Key order (iteration) | Not guaranteed | Insertion or **access** order | Sorted by key |
| `get` / `put` typical | O(1) avg | O(1) avg | O(log n) |
| Extra memory | Baseline | Doubly-linked entries | Tree structure |
| Null keys | One null key allowed | Same | No null keys (natural order) |

**`TreeMap` sorts by key**, not by value. Salary-ranked employees require sorting **values** or entries explicitly:

```java
employees.values().stream()
    .sorted(Comparator.comparingDouble(Employee::getSalary))
    .forEach(System.out::println);
```

## 2. Selection scenarios

1. **Frequent lookup by employee ID; salary report once nightly**  
   → `HashMap<Long, Employee>` for O(1) lookups; build sorted report by copying values and sorting — **O(n log n)** once per night beats maintaining `TreeMap` if sorted traversal is rare.

2. **Frequent lookup + frequent ascending ID traversal**  
   → `TreeMap<Long, Employee>` or `HashMap` + separate sorted index — second structure adds **consistency cost** on every update.

3. **Unique elements in sorted order**  
   → `TreeSet` (not a map) or `TreeMap` keyed by sort key.

4. **Bounded recent-products cache, fast lookup by product ID**  
   → Access-order `LinkedHashMap` + `removeEldestEntry` (see [Lesson 11](11-linkedhashmap-lru-cache.md)).

## 3. One million employees design

| Requirement | Structure |
| --- | --- |
| Hot path: `get(id)` | `HashMap` |
| Nightly salary report | Sort snapshot of values or stream to report DB |
| Hot path: salary-ordered iteration all day | Consider `TreeMap` keyed by salary (only if salary is key — unusual) or secondary index + sync on write |

Maintaining **HashMap + TreeMap** on every salary change is O(log n) per update vs O(1) for map alone — justified only if sorted traversal is as hot as lookup.


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/05-hashmap-linkedhashmap-treemap.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
