---
title: "Lesson 1 — Optional Fundamentals"
description: "Creating Optional, presence checks, orElse vs orElseGet, orElseThrow."
status: covered
audience: practitioner
tags: [[optional, module-7, lesson-1], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 1 — Optional Fundamentals

Creating Optional, presence checks, orElse vs orElseGet, orElseThrow.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-07-optional/01-optional-fundamentals.md) compresses interview signal without
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

# Lesson 1 — Optional Fundamentals

**Java 8+** `Optional<T>` models a value that may be **absent** without using `null` in return types. It is a **container**, not a general-purpose field type.

## 1. Factory methods

```java
Optional<String> definite = Optional.of("paid");           // null → NPE
Optional<String> maybe = Optional.ofNullable(getName()); // null → empty
Optional<String> empty = Optional.empty();
```

| Method | `null` argument |
| --- | --- |
| `Optional.of(null)` | **NullPointerException** |
| `Optional.ofNullable(null)` | `Optional.empty()` |

## 2. Presence API

```java
if (opt.isPresent()) { ... }
if (opt.isEmpty()) { ... } // Java 11+

opt.ifPresent(v -> log.info("{}", v));
opt.ifPresentOrElse(
    v -> process(v),
    () -> handleMissing()); // Java 9+
```

## 3. `orElse` vs `orElseGet` (eager vs lazy)

```java
User u = optionalUser.orElse(loadDefaultUser());       // loadDefaultUser() ALWAYS runs
User u2 = optionalUser.orElseGet(User::loadDefault); // supplier only if empty
```

**Trap:** passing expensive `orElse(compute())` — argument evaluated **before** `orElse` checks presence.

## 4. `orElseThrow`

```java
Order order = findOrder(id)
    .orElseThrow(() -> new OrderNotFoundException(id));

// Java 10+: orElseThrow() with no arg → NoSuchElementException
```

## 5. `get()` — avoid in production code

```java
optional.get(); // NoSuchElementException if empty — use orElseThrow with domain exception
```

## 6. Service-layer return type

```java
public Optional<Customer> findByEmail(String email) {
    return repository.findByEmail(email); // absent ≠ error
}

public Customer requireByEmail(String email) {
    return findByEmail(email)
        .orElseThrow(() -> new CustomerNotFoundException(email));
}
```

`Optional` documents **optional result**; do not use for every nullable parameter.


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-07-optional/01-optional-fundamentals.md)
- [Optional production playbook](../../../03-production-playbook/core-java/module-07-optional-production-playbook.md)
- [Module index](index.md)
