---
title: "Lesson 3 — Wildcards and PECS"
description: "? extends", "? super", Producer Extends Consumer Super, assignment traps."
status: covered
audience: practitioner
tags: [[generics, wildcards, pecs, module-5, lesson-3], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 3 — Wildcards and PECS

? extends", "? super", Producer Extends Consumer Super, assignment traps.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-05-generics/03-wildcards-pecs.md) compresses interview signal without
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

# Lesson 3 — Wildcards and PECS

Wildcards (`?`) express **unknown** type arguments at API boundaries while preserving type safety.

## 1. Unbounded wildcard `?`

```java
public static void printSizes(List<?> items) {
    for (Object o : items) {
        System.out.println(o);
    }
}
```

You can read elements as `Object`; you **cannot** add (except `null`) — element type unknown.

## 2. Upper bounded: `? extends T` (producer)

```java
public static double sumNumbers(List<? extends Number> values) {
    double total = 0;
    for (Number n : values) {
        total += n.doubleValue();
    }
    return total;
}

sumNumbers(List.of(1, 2, 3));       // List<Integer> OK
sumNumbers(List.of(1.5, 2.5));    // List<Double> OK
```

**Read-only for adding:** you cannot `values.add(1)` — compiler cannot prove element type.

## 3. Lower bounded: `? super T` (consumer)

```java
public static void addIntegers(List<? super Integer> sink) {
    sink.add(42);
    sink.add(7);
}
```

Accepts `List<Integer>`, `List<Number>`, `List<Object>`. **Read** as `Object` (except `Object` methods); **write** `Integer` (and subtypes).

## 4. PECS — Producer Extends, Consumer Super

| Role | Wildcard | Mnemonic |
| --- | --- | --- |
| **Producer** — you **get** `T` out | `? extends T` | Extends |
| **Consumer** — you **put** `T` in | `? super T` | Super |

```java
public static <T> void copy(List<? extends T> src, List<? super T> dest) {
    for (T item : src) {
        dest.add(item);
    }
}
```

`Collections.copy(List<? super T> dest, List<? extends T> src)` in the JDK follows the same idea (argument order reversed in the API).

## 5. Assignment compatibility traps

```java
List<? extends Number> nums = List.of(1, 2);
// nums.add(1); // compile error

List<? super Integer> sink = new ArrayList<Number>();
sink.add(1); // OK
```

**Wrong answer in interviews:** "`? extends` means read and write both work" — extends is for **reading** `T`; super is for **writing** `T`.

## 6. `Comparable` / `Comparator` with wildcards

```java
public static <T extends Comparable<? super T>> T max(List<T> list) {
    return list.stream().max(Comparable::compareTo).orElseThrow();
}
```

`? super T` on `Comparable` allows `T` that implements `Comparable<Supertype>`.


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-05-generics/03-wildcards-pecs.md)
- [Generics production playbook](../../../03-production-playbook/core-java/module-05-generics-production-playbook.md)
- [Module index](index.md)
