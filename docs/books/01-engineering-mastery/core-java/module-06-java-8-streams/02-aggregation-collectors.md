---
title: "Lesson 2 — Aggregation and Collectors"
description: "reduce, collect, groupingBy, toMap merge, downstream collectors."
status: covered
audience: practitioner
tags: [[streams, collectors, module-6, lesson-2], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 2 — Aggregation and Collectors

reduce, collect, groupingBy, toMap merge, downstream collectors.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-06-java-8-streams/02-aggregation-collectors.md) compresses interview signal without
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

# Lesson 2 — Aggregation and Collectors

```java
record Employee(String name, String dept, String title, double salary) {}
```

Terminal aggregation turns a stream into a value or mutable container. **`collect`** is mutable reduction; **`reduce`** is often immutable folding.

## 1. `reduce()` overloads

```java
// Optional — no identity
Optional<Integer> sum = Stream.of(1, 2, 3)
    .reduce((a, b) -> a + b);

// With identity — never empty result
int total = Stream.of(1, 2, 3).reduce(0, Integer::sum);
```

Parallel streams use **combiner** overload:

```java
int parallelSum = numbers.parallelStream()
    .reduce(0, Integer::sum, Integer::sum);
```

Identity must be a true zero for the operation — wrong identity breaks parallel `reduce`.

## 2. `collect` and `Collectors`

```java
List<String> names = employees.stream()
    .map(Employee::name)
    .collect(Collectors.toList()); // mutable ArrayList
```

### `Collectors.toList()` vs `Stream.toList()` (Java 16+)

| | `collect(toList())` | `.toList()` |
| --- | --- | --- |
| Mutability | Mutable list | **Unmodifiable** |
| Null elements | Allowed in list | **Not allowed** (NPE if present) |
| Since | Java 8 | Java 16+ |

## 3. `Collectors.toMap()` and duplicate keys

```java
// Duplicate key without merge → IllegalStateException
Map<String, Employee> byName = employees.stream()
    .collect(Collectors.toMap(Employee::name, e -> e));
```

With **merge function**:

```java
Map<String, Employee> latestByName = employees.stream()
    .collect(Collectors.toMap(
        Employee::name,
        e -> e,
        (existing, replacement) -> replacement)); // or keep higher salary, etc.
```

## 4. Grouping and partitioning

```java
Map<String, List<Employee>> byDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::dept));

Map<String, Map<String, List<Employee>>> byDeptAndTitle = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::dept,
        Collectors.groupingBy(Employee::title)));
```

```java
Map<Boolean, List<Employee>> partitioned = employees.stream()
    .collect(Collectors.partitioningBy(e -> e.salary() > 100_000));
```

## 5. Downstream collectors

```java
Map<String, Long> headcount = employees.stream()
    .collect(Collectors.groupingBy(Employee::dept, Collectors.counting()));

Map<String, Double> avgSalary = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::dept,
        Collectors.averagingDouble(Employee::salary)));

Map<String, Optional<Employee>> topEarner = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::dept,
        Collectors.maxBy(Comparator.comparingDouble(Employee::salary))));
```

`collectingAndThen` — post-process:

```java
Map<String, List<String>> namesByDept = employees.stream()
    .collect(Collectors.collectingAndThen(
        Collectors.groupingBy(Employee::dept, Collectors.mapping(Employee::name, Collectors.toList())),
        map -> map)); // transform map if needed
```

## 6. `summaryStatistics` and min/max

```java
DoubleSummaryStatistics stats = employees.stream()
    .mapToDouble(Employee::salary)
    .summaryStatistics();

Optional<Employee> richest = employees.stream()
    .max(Comparator.comparingDouble(Employee::salary));
```

## 7. Engineering salaries example

```java
double engPayroll = employees.stream()
    .filter(e -> "Engineering".equals(e.dept()))
    .mapToDouble(Employee::salary)
    .sum();
```

Primitive `mapToDouble` avoids boxing in the aggregation path.


## Practice extension — maximum salary per department

```java
Map<String, Optional<Employee>> topByDepartment = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::department,
        Collectors.maxBy(Comparator.comparingInt(Employee::salary))));

Map<String, Employee> requiredTopByDepartment = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::department,
        Collectors.collectingAndThen(
            Collectors.maxBy(Comparator.comparingInt(Employee::salary)),
            Optional::orElseThrow)));
```

The downstream collector runs separately for each group. `maxBy` returns `Optional` because it
is a general collector and an empty input has no maximum. Every group created by ordinary
`groupingBy` received at least one employee, so unwrapping inside `collectingAndThen` is sound
for this particular pipeline; it is not a claim that arbitrary `maxBy` results are nonempty.
`collectingAndThen` performs a finishing conversion after the downstream collector completes.

This is **O(n)** time and **O(g)** result space, where `g` is the number of departments; it does
not sort each group. Ties return one encountered maximum (do not claim a deterministic business
tie-break unless the comparator or a secondary rule specifies one). Add an explicit tie-breaker
or collect all tied candidates when the domain requires it.

### What I should say in an interview

“`groupingBy` builds the department buckets and `maxBy` is the downstream reduction. I avoid
sorting because a running maximum is linear; I only unwrap the Optional after explaining why each
group is known to be nonempty.”

### What not to say

- “`maxBy` cannot be empty because I grouped first.” It can be empty in other collector contexts.
- “A maximum resolves equal salaries.” It selects one unless the business rule handles ties.

## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-06-java-8-streams/02-aggregation-collectors.md)
- [Java 8 Streams production playbook](../../../03-production-playbook/core-java/module-06-java-8-streams-production-playbook.md)
- [Module index](index.md)
