---
title: "Lesson 4 — Correctness, peek, forEach, Parallel Streams"
description: "Single-use streams, side effects, parallel pitfalls, unordered, Top-K trade-offs."
status: covered
audience: practitioner
tags: [[streams, parallel, module-6, lesson-4], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 4 — Correctness, `peek`, Parallel Streams

Single-use streams, side effects, parallel pitfalls, unordered, Top-K trade-offs.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-06-java-8-streams/04-correctness-parallel-performance.md) compresses interview signal without
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

# Lesson 4 — Correctness, `peek`, Parallel Streams

Streams excel at **pure** pipelines. Shared mutation and parallel streams are common interview failure modes.

## 1. Single-use restriction

```java
Stream<String> s = names.stream();
s.count();
s.forEach(System.out::println); // IllegalStateException — stream already consumed
```

## 2. Side effects and shared state

```java
List<Integer> bad = new ArrayList<>();
IntStream.range(0, 10_000).parallel().forEach(bad::add); // data race — undefined results
```

Use **collect** or **reduce** for aggregation — thread-safe by design when used correctly.

## 3. `peek` vs `map` vs `forEach`

| | Role |
| --- | --- |
| `map` | Transform element — part of pipeline result |
| `peek` | Debug/observe — **do not** rely on for business logic |
| `forEach` | Terminal side effect per element |

```java
// Anti-pattern: essential logic in peek
employees.stream()
    .peek(e -> auditLog.add(e)) // may not run if stream short-circuits earlier
    .filter(...)
    .toList();
```

`peek` runs only for elements that reach that stage; short-circuiting may skip it entirely.

## 4. `forEach` vs `forEachOrdered`

On parallel streams, `forEach` may process in arbitrary order; `forEachOrdered` respects encounter order (with cost).

## 5. Parallel streams

`collection.parallelStream()` uses the **common** `ForkJoinPool`.

| Good fit | Poor fit |
| --- | --- |
| Large in-memory data, CPU-heavy pure ops | Small collections (overhead dominates) |
| Per-element independent work | IO-bound tasks blocking pool threads |
| No shared mutable state | Order-sensitive side effects |

**Thread safety:** parallel pipeline stages must not mutate shared structures. **Ordering:** `sorted()` on parallel stream still sorts but pays merge cost.

## 6. `unordered()`

Marks stream **unordered** for optimization — does **not** randomly shuffle. Encounter order may be dropped for parallel ops that preserve nothing order-dependent.

## 7. Top-K: sort vs heap

| Approach | Time | When |
| --- | --- | --- |
| Full `sorted().limit(k)` | O(n log n) | Small `n`, simplicity |
| Size-k min-heap | O(n log k) | Large `n`, small `k` |

Interview answer: pick based on `n`, `k`, and whether you need full ordering of all elements.

## 8. `Optional` in streams

`flatMap(Optional::stream)` (Java 9+) flattens present optionals — ties to [Optional module](../module-07-optional/index.md).


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-06-java-8-streams/04-correctness-parallel-performance.md)
- [Java 8 Streams production playbook](../../../03-production-playbook/core-java/module-06-java-8-streams-production-playbook.md)
- [Module index](index.md)
