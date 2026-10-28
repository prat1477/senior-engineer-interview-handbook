---
title: "Lesson 2 — Optional Composition and Anti-Patterns"
description: "map, flatMap, filter, or(), null mapping traps, interview anti-patterns."
status: covered
audience: practitioner
tags: [[optional, module-7, lesson-2], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 2 — Optional Composition and Anti-Patterns

map, flatMap, filter, or(), null mapping traps, interview anti-patterns.

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

Core Java Module 7 — **Optional**. This is the canonical Engineering Mastery
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-07-optional/02-optional-composition-and-antipatterns.md) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

## Architecture

This lesson sits in **Module 7** of the Core Java track. Service code should treat
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

# Lesson 2 — Optional Composition and Anti-Patterns

Optional chains express sequential lookups without nested null checks — when used on **return values**, not everywhere.

## 1. `map`, `flatMap`, `filter`

```java
Optional<String> city = findUser(id)
    .map(User::getAddress)
    .map(Address::getCity);

Optional<Order> order = findUser(id)
    .flatMap(User::getLatestOrder); // method returns Optional<Order>
```

**Null from mapping function:** `map` wraps with `ofNullable` — mapping function returning `null` yields **empty** Optional (Java 9+ behavior documented in API).

```java
optional.map(x -> null); // becomes empty, not Optional.of(null)
```

## 2. `filter`

```java
optional.filter(v -> v.isActive()); // empty if predicate false
```

## 3. `or()` — alternative Optional (Java 9+)

```java
return primary.lookup(key)
    .or(() -> fallback.lookup(key));
```

Lazy alternative supplier — runs only if primary empty.

## 4. What Optional does **not** guarantee

- Does not stop callers from passing `null` where a non-optional reference is expected.
- Does not replace validation on input DTOs.
- Serialization: `Optional` as JSON field is awkward — use DTOs without Optional for REST bodies.

## 5. Anti-patterns (interview favorites)

| Anti-pattern | Prefer |
| --- | --- |
| `Optional` method parameter | Overloads or `@Nullable` + validation |
| `Optional` fields on entities | Plain nullable or separate presence model |
| `if (opt.isPresent()) return opt.get(); else ...` | `orElse`, `map`, `ifPresent` |
| `Optional.ofNullable(x).orElse(null)` | Just use `x` |
| Collection of `Optional<T>` | `flatMap` / filter present |

## 6. Streams integration (Java 9+)

```java
List<String> cities = users.stream()
    .map(User::getAddress)
    .flatMap(Optional::stream)
    .map(Address::getCity)
    .toList();
```


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-07-optional/02-optional-composition-and-antipatterns.md)
- [Optional production playbook](../../../03-production-playbook/core-java/module-07-optional-production-playbook.md)
- [Module index](index.md)
