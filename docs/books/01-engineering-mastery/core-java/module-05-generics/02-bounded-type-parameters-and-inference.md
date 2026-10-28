---
title: "Lesson 2 — Bounded Type Parameters"
description: "extends bounds, multiple bounds, and invariance of generic types."
status: covered
audience: practitioner
tags: [[generics, module-5, lesson-2], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 2 — Bounded Type Parameters and Invariance

extends bounds, multiple bounds, and invariance of generic types.

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

Core Java Module 5 — **Generics**. This is the canonical Engineering Mastery
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-05-generics/02-bounded-type-parameters-and-inference.md) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

## Architecture

This lesson sits in **Module 5** of the Core Java track. Service code should treat
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

# Lesson 2 — Bounded Type Parameters and Invariance

Bounded type parameters restrict `T` to a subtype range so you can call methods on the bound.

## 1. Upper bound: `<T extends Number>`

```java
public static <T extends Number> double sum(List<T> values) {
    double total = 0;
    for (T v : values) {
        total += v.doubleValue(); // Number API available
    }
    return total;
}
```

`T` must be `Number` or a subclass (`Integer`, `Double`, …).

## 2. Multiple bounds

```java
public static <T extends Number & Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}
```

- Use **`&`** between interfaces/classes (class first if any).
- All bounds must be satisfied by the actual type argument.

## 3. Invariance: `List<Integer>` is not a `List<Number>`

```java
List<Integer> ints = List.of(1, 2, 3);
// List<Number> nums = ints; // COMPILE ERROR
```

**Why:** if assignment were allowed, you could do:

```java
nums.add(3.14); // would break Integer list at runtime without generics
```

Generic types are **invariant** in Java: `G<A>` is not a subtype of `G<B>` even when `A` extends `B`. Use wildcards for flexibility — [Lesson 3](03-wildcards-pecs.md).

| Relationship | Holds? |
| --- | --- |
| `Integer` extends `Number` | Yes |
| `List<Integer>` extends `List<Number>` | **No** |
| `List<? extends Number>` accepts `List<Integer>` | Yes (read-only producer view) |

## 4. When to bound `T`

| Pattern | Bound |
| --- | --- |
| Numeric aggregation | `<T extends Number>` |
| Sortable domain types | `<T extends Comparable<T>>` |
| Entity with ID | `<T extends Identifiable<ID>>` |

## 5. Interview trap: arrays vs generics

```java
Number[] nums = new Integer[10]; // arrays are covariant — legal but unsafe
nums[0] = 3.14; // ArrayStoreException at runtime
```

Generics were designed **invariant** partly to avoid this class of runtime failures.


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-05-generics/02-bounded-type-parameters-and-inference.md)
- [Generics production playbook](../../../03-production-playbook/core-java/module-05-generics-production-playbook.md)
- [Module index](index.md)
