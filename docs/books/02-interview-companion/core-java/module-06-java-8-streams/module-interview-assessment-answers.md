---
title: "Streams — Assessment Answers"
description: Answers for Module 6 interview practice.
status: draft
audience: advanced
tags: [streams, interview, answers, module-6]
created: 2026-10-17
updated: 2026-10-17
---

# Streams — Assessment Answers

## 1. Execution timing

When a **terminal** operation runs (e.g. `collect`, `count`, `forEach`). Intermediates are lazy.

## 2. Empty `allMatch`

Vacuous truth: every element (zero elements) satisfies the predicate. Confirm product semantics for empty input.

## 3. `unordered()` vs `sorted()`

`unordered()` relaxes ordering guarantees for optimization — not a shuffle. `sorted()` computes a total order (expensive).

## 4. Parallel `forEach` + shared list

Concurrent `add` on `ArrayList` is a data race — lost updates or exceptions. Use `collect(toList())` or concurrent collector.

## 5. Engineering payroll

```java
double total = employees.stream()
    .filter(e -> "Engineering".equals(e.dept()))
    .mapToDouble(Employee::salary)
    .sum();
```

## 6. Nested grouping

```java
employees.stream().collect(Collectors.groupingBy(
    Employee::dept,
    Collectors.groupingBy(Employee::title)));
```

## 7. Duplicate names in `toMap`

Supply merge function: `(a, b) -> ...` or use `groupingBy` if multiple per key expected.

## 8. `map` vs `flatMap`

`map(line -> Arrays.stream(line.split(" ")))` → `Stream<Stream<String>>`. `flatMap(line -> Arrays.stream(line.split(" ")))` → `Stream<String>`.

## 9. `peek` + `filter`

Records failing `filter` never reach `peek` if `peek` is after filter; if before filter, rejected records still logged — but `peek` is not guaranteed for all pipeline shapes under optimization/short-circuit. Do not use `peek` for compliance logging — use explicit processing.

## 10. Top 3 at scale

Heap `O(n log k)` with k=3 usually beats full sort `O(n log n)` for large n. Mention constant factors and that partial sort / `partialSort` alternatives exist in other libraries.

## Mini-assessment

**A.**

```java
employees.stream()
    .filter(e -> "Engineering".equals(e.dept()) && e.salary() > 200_000)
    .findFirst();
```

**B.**

```java
employees.stream().collect(Collectors.partitioningBy(e -> e.salary() > 100_000, Collectors.counting()));
```

**C.** Internal state consumed; second terminal throws `IllegalStateException`.
