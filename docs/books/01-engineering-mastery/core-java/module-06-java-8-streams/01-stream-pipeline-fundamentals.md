---
title: "Lesson 1 — Stream Pipeline Fundamentals"
description: "Sources, intermediate/terminal ops, laziness, filter, map, flatMap, sorted."
status: covered
audience: practitioner
tags: [[streams, module-6, lesson-1], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 1 — Stream Pipeline Fundamentals

Sources, intermediate/terminal ops, laziness, filter, map, flatMap, sorted.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-06-java-8-streams/01-stream-pipeline-fundamentals.md) compresses interview signal without
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

# Lesson 1 — Stream Pipeline Fundamentals

**Java 8+** streams process sequences declaratively: describe *what* to compute, not index loops. A stream is **single-use** — see [Lesson 4](04-correctness-parallel-performance.md).

## 1. Pipeline structure

```text
source → intermediate* → terminal
```

| Stage | Examples | Notes |
| --- | --- | --- |
| Source | `collection.stream()`, `Arrays.stream()`, `Stream.of()` | Creates stream |
| Intermediate | `filter`, `map`, `sorted`, `distinct` | Lazy; build pipeline |
| Terminal | `collect`, `reduce`, `forEach`, `count` | Triggers execution |

```java
record Employee(String dept, String title, double salary) {}

List<Employee> engineering = employees.stream()
    .filter(e -> "Engineering".equals(e.dept()))
    .sorted(Comparator.comparingDouble(Employee::salary).reversed())
    .toList(); // Java 16+ — immutable list
```

## 2. Laziness

No intermediate operation runs until a **terminal** operation runs. The stream fuses stages where possible.

```java
employees.stream()
    .filter(e -> { System.out.println("filter " + e); return true; })
    .map(e -> { System.out.println("map " + e); return e; });
// No output — no terminal yet
```

## 3. Core intermediate operations

| Operation | Stateful? | Notes |
| --- | --- | --- |
| `filter(Predicate)` | No | Drops elements |
| `map(Function)` | No | 1:1 transform |
| `flatMap(Function to Stream)` | No | 1:many flatten |
| `distinct()` | **Yes** | Uses `equals`/`hashCode` |
| `sorted()` / `sorted(Comparator)` | **Yes** | Stable sort |
| `skip(n)` / `limit(n)` | `limit` can short-circuit | Useful for pagination patterns |

### `map` vs `flatMap`

```java
List<String> words = List.of("hello", "world");
List<Integer> lengths = words.stream().map(String::length).toList();
// [5, 5]

List<String> letters = words.stream()
    .flatMap(w -> w.chars().mapToObj(c -> String.valueOf((char) c)))
    .toList();
// h,e,l,l,o,w,o,r,l,d
```

**Trap:** `map` returning `List<T>` gives `Stream<List<T>>`; `flatMap` collapses nested streams.

## 4. Encounter order

Streams from ordered sources (`List`, `LinkedHashSet`) have **encounter order**. `sorted()` produces a new order; `distinct()` preserves first occurrence of each element in encounter order.

## 5. Version notes

| API | Since |
| --- | --- |
| `Stream`, `filter`, `map`, `collect` | Java 8 |
| `takeWhile`, `dropWhile` | Java 9 |
| `Stream.toList()` | **Java 16+** (unmodifiable) |
| `Collectors.toList()` | Java 8 (mutable `ArrayList`) |


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-06-java-8-streams/01-stream-pipeline-fundamentals.md)
- [Java 8 Streams production playbook](../../../03-production-playbook/core-java/module-06-java-8-streams-production-playbook.md)
- [Module index](index.md)
