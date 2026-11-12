---
title: "Lesson 6 — Comparable and Comparator"
description: "Natural vs custom order, multi-field comparators, and sorted collections."
status: covered
audience: practitioner
tags: [[collections, comparator, module-4, lesson-6], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 6 — Comparable and Comparator

Natural vs custom order, multi-field comparators, and sorted collections.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/06-comparable-and-comparator.md) compresses interview signal without
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

# Lesson 6 — Comparable and Comparator

Ordering appears in `Collections.sort`, `TreeSet`, `TreeMap`, and `PriorityQueue`. Two mechanisms: **intrinsic** (`Comparable`) and **external** (`Comparator`).

## 1. `Comparable<T>` — natural ordering

```java
public class Employee implements Comparable<Employee> {
    private final long id;
    private final String name;
    private final double salary;

    @Override
    public int compareTo(Employee other) {
        return Long.compare(this.id, other.id);
    }
}
```

- **One** natural order per type.
- Used when the type "has" a default sort (e.g. by ID).

## 2. `Comparator<T>` — custom ordering

```java
Comparator<Employee> byName =
    Comparator.comparing(Employee::getName, String.CASE_INSENSITIVE_ORDER);
```

- Multiple comparators per type.
- Prefer when sort criteria vary by use case (UI vs billing).

## 3. Multi-field and reversed order

```java
List<Employee> employees = loadEmployees();

employees.sort(
    Comparator.comparingDouble(Employee::getSalary)
              .reversed()
              .thenComparing(Employee::getName)
);
```

**Meaning:** higher salary first; for equal salary, **name ascending** (A before Z).

## 4. Sorted sets and maps

- `TreeSet` / `TreeMap` use comparator (or natural order) for **both** sorting **and** key equivalence (compare == 0).
- Tie-break on unique business keys when comparing on non-unique fields ([Lesson 3](03-set-implementations.md)).

## 5. When to use which

| Use `Comparable` | Use `Comparator` |
| --- | --- |
| Single obvious default order | Many sort views |
| Type should always be orderable by ID | Sort by salary for reports only |


## Practice extension — comparator composition and mutation

```java
List<Employee> ranked = employees.stream()
    .sorted(Comparator.comparingInt(Employee::salary)
        .reversed()
        .thenComparing(Employee::name))
    .toList();
```

This means salary descending, then name ascending for equal salaries. Put `reversed()` directly
after the salary comparator: calling it after `thenComparing` reverses the *entire* composed
comparator, including the name tie-break. `List.sort()` mutates its list; `Stream.sorted()`
returns a new ordered stream, and Java 17 `toList()` creates an unmodifiable result list.

A comparator must be antisymmetric, transitive, and consistent enough for its target collection;
do not subtract integers to compare them because overflow can violate the ordering contract.
Use `comparingInt`, `Long.compare`, or `Comparator.comparing`. Practice note: the initial sorting
pipeline omitted its terminal `toList()`; `sorted()` is still an intermediate operation.

### What I should say in an interview

“`Comparable` declares the one natural order on the type; `Comparator` expresses a caller's
ordering policy. For a report I use a composed Comparator so the domain model is not forced to
adopt report-specific ordering.”

### What not to say

- “`sorted()` returns a list.” It returns a lazy stream.
- “`reversed()` reverses only the last criterion.” It reverses the comparator built so far.

## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/06-comparable-and-comparator.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
