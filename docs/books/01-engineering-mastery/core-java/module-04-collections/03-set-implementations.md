---
title: "Lesson 3 — Set Implementations"
description: "HashSet, LinkedHashSet, TreeSet, equality, and comparator membership traps."
status: covered
audience: practitioner
tags: [[collections, set, module-4, lesson-3], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 3 — Set Implementations

HashSet, LinkedHashSet, TreeSet, equality, and comparator membership traps.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/03-set-implementations.md) compresses interview signal without
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

# Lesson 3 — Set Implementations

A `Set` models **mathematical sets**: no duplicate elements. Uniqueness is defined by **`equals()`** (hash-based sets) or by **comparison order** (sorted sets).

## 1. Set vs List

| | `List` | `Set` |
| --- | --- | --- |
| Duplicates | Yes | No |
| Order | Insertion/index | Implementation-dependent |
| `get(index)` | Yes | No |

## 2. Implementations compared

| Implementation | Ordering | `add` / `contains` (typical) |
| --- | --- | --- |
| `HashSet` | No guaranteed iteration order | O(1) average |
| `LinkedHashSet` | Insertion order | O(1) average |
| `TreeSet` | Sorted (red-black tree) | O(log n) |

## 3. `hashCode()` and `equals()`

For `HashSet` / `LinkedHashSet`:

- If `a.equals(b)`, then `a.hashCode() == b.hashCode()` (**required**).
- Buckets use `hashCode`; collisions resolved with `equals`.
- Broken contract → duplicates or lost elements.

## 4. `TreeSet` and comparators

Natural order: elements implement `Comparable`.  
Custom order: `Comparator` at construction.

**Critical:** In `TreeSet`, **comparator compare result 0 means "equal for set membership"** — only one such element is stored, even if `equals()` would distinguish them.

```java
record Employee(long id, String name, double salary) {
    long getId() { return id; }
    String getName() { return name; }
    double getSalary() { return salary; }
}

Set<Employee> bySalary = new TreeSet<>(
    Comparator.comparingDouble(Employee::getSalary)
);

bySalary.add(new Employee(1, "Amit", 80_000));
bySalary.add(new Employee(2, "Priya", 80_000)); // compare → 0 → NOT added
bySalary.add(new Employee(3, "Rahul", 90_000));
// Set size 2: Amit (or Priya — first wins), Rahul
```

Amit and Priya share salary → comparator returns 0 → **equivalent keys** in the tree → one employee dropped.

**Fix — tie-breaker:**

```java
Comparator<Employee> bySalaryThenId =
    Comparator.comparingDouble(Employee::getSalary)
              .thenComparing(Employee::getId);
```

**Best practice:** comparator consistent with `equals()` when possible (`compare(a,b)==0` iff `a.equals(b)`).

## 5. When to use which

- **`HashSet`** — fastest average membership; order irrelevant.
- **`LinkedHashSet`** — dedupe while preserving insertion order (e.g. "seen" order for UI).
- **`TreeSet`** — range queries, `subSet`, sorted iteration — pay log factor.


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/03-set-implementations.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
