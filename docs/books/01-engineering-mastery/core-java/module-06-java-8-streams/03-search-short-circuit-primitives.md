---
title: "Lesson 3 — Search, Short-Circuiting, and Primitive Streams"
description: "findFirst, match ops, mapToInt, Stream.generate/iterate, takeWhile."
status: covered
audience: practitioner
tags: [[streams, module-6, lesson-3], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 3 — Search, Short-Circuiting, and Primitive Streams

findFirst, match ops, mapToInt, Stream.generate/iterate, takeWhile.

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

Core Java Module 6 — **Java 8 Streams**. This is the canonical Engineering Mastery
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-06-java-8-streams/03-search-short-circuit-primitives.md) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

## Architecture

This lesson sits in **Module 6** of the Core Java track. Service code should treat
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

# Lesson 3 — Search, Short-Circuiting, and Primitive Streams

```java
record Employee(String name, String dept, String title, double salary) {}
```

Short-circuiting terminals stop processing once an answer is known — important for infinite or large streams.

## 1. `findFirst` vs `findAny`

| Method | Ordered stream | Parallel stream |
| --- | --- | --- |
| `findFirst()` | First in encounter order | First in encounter order (coordination cost) |
| `findAny()` | Any match | Often faster — any thread’s match |

```java
Optional<Employee> firstEng = employees.stream()
    .filter(e -> "Engineering".equals(e.dept()))
    .findFirst();
```

## 2. Match operations

```java
boolean anyVip = employees.stream().anyMatch(e -> e.salary() > 500_000);
boolean allPaid = employees.stream().allMatch(e -> e.salary() > 0);
boolean noneNegative = employees.stream().noneMatch(e -> e.salary() < 0);
```

**Empty stream:**

| Op | Result |
| --- | --- |
| `anyMatch` | `false` |
| `allMatch` | `true` (vacuous truth) |
| `noneMatch` | `true` |

**Trap:** `allMatch` on empty returns `true` — confirm business meaning.

## 3. Primitive streams

```java
int total = employees.stream()
    .mapToInt(e -> (int) e.salary()) // prefer mapToDouble for money
    .sum();

OptionalDouble avg = employees.stream()
    .mapToDouble(Employee::salary)
    .average();
```

Boxing `Stream<Integer>` for arithmetic adds allocation; primitive streams expose `sum`, `max`, `average` directly.

## 4. `Stream.generate` and `Stream.iterate`

```java
Stream<Double> randoms = Stream.generate(Math::random).limit(5);

Stream<Integer> powers = Stream.iterate(1, n -> n * 2).limit(10);
```

Java 9+ `iterate` with predicate:

```java
Stream<Integer> bounded = Stream.iterate(1, n -> n < 1000, n -> n * 2);
```

## 5. `takeWhile` / `dropWhile` (Java 9+)

```java
List<Integer> nums = List.of(1, 2, 3, 4, 1, 2);
List<Integer> prefix = nums.stream().takeWhile(n -> n < 4).toList();
// [1, 2, 3] — stops at first 4, does not skip later 1,2
```

For **sorted** inputs, `takeWhile` behaves like a prefix scan; on unordered data, semantics are still “stop at first failing element in encounter order.”

## 6. Top three salaries (stream sort approach)

```java
List<Employee> top3 = employees.stream()
    .sorted(Comparator.comparingDouble(Employee::salary).reversed())
    .limit(3)
    .toList();
```

`O(n log n)` — compare with `O(n log k)` heap in [Collections lesson 9](../module-04-collections/09-priorityqueue-and-heaps.md).


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-06-java-8-streams/03-search-short-circuit-primitives.md)
- [Java 8 Streams production playbook](../../../03-production-playbook/core-java/module-06-java-8-streams-production-playbook.md)
- [Module index](index.md)
