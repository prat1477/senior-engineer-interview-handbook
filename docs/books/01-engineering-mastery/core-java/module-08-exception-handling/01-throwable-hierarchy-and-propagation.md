---
title: "Lesson 1 — Throwable Hierarchy and Propagation"
description: "Checked vs unchecked, throw vs throws, catch ordering, finally traps."
status: covered
audience: practitioner
tags: [[exceptions, module-8, lesson-1], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 1 — Throwable Hierarchy and Propagation

Checked vs unchecked, throw vs throws, catch ordering, finally traps.

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

Core Java Module 8 — **Exception handling**. This is the canonical Engineering Mastery
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-08-exception-handling/01-throwable-hierarchy-and-propagation.md) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

## Architecture

This lesson sits in **Module 8** of the Core Java track. Service code should treat
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

# Lesson 1 — Throwable Hierarchy and Propagation

Exceptions signal **recoverable failures**; errors often indicate serious JVM/resource problems you usually do not catch.

## 1. Hierarchy (simplified)

```text
Throwable
├── Error (e.g. OutOfMemoryError) — typically do not catch
└── Exception
    ├── RuntimeException (unchecked)
    └── other Exception subclasses (checked)
```

| Category | Compile-time | Examples |
| --- | --- | --- |
| **Checked** | Must handle or declare | `IOException`, `SQLException` |
| **Unchecked** | No `throws` required | `IllegalArgumentException`, `NullPointerException` |
| **Error** | Unchecked | `StackOverflowError` |

**Design stance (interviews):** use **unchecked** for programming bugs and non-recoverable API misuse; **checked** for recoverable external failures callers should handle — many Spring codebases lean unchecked + global handler.

## 2. `throw` vs `throws`

```java
void readFile() throws IOException { // declares checked exception
    throw new IOException("disk full"); // throws instance
}
```

`throws` on signature; `throw` at throw site.

## 3. Propagation and catch order

```java
try {
    process();
} catch (FileNotFoundException e) {
    // specific first
} catch (IOException e) {
    // broader
}
```

Subclass catches must appear **before** superclass catches.

## 4. `finally` and return trap

```java
int bad() {
    try {
        return 1;
    } finally {
        return 2; // finally wins — hides try return — NEVER do this
    }
}
```

`finally` runs on normal or exceptional exit — except `System.exit` / JVM halt.


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-08-exception-handling/01-throwable-hierarchy-and-propagation.md)
- [Exception handling production playbook](../../../03-production-playbook/core-java/module-08-exception-handling-production-playbook.md)
- [Module index](index.md)
