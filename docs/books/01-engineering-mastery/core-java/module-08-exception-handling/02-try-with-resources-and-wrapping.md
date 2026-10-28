---
title: "Lesson 2 — Try-with-Resources and Exception Wrapping"
description: "AutoCloseable, suppressed exceptions, cause chains, logging."
status: covered
audience: practitioner
tags: [[exceptions, module-8, lesson-2], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 2 — Try-with-Resources and Exception Wrapping

AutoCloseable, suppressed exceptions, cause chains, logging.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-08-exception-handling/02-try-with-resources-and-wrapping.md) compresses interview signal without
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

# Lesson 2 — Try-with-Resources and Exception Wrapping

## 1. Try-with-resources (Java 7+)

```java
try (InputStream in = openStream()) {
    return parse(in);
} // in.close() called automatically
```

Resources must implement **`AutoCloseable`**. Close happens after try block, even on exception.

## 2. Suppressed exceptions

If **both** body and `close()` fail, the **primary** exception is thrown; close failure is **suppressed**:

```java
try {
    ...
} catch (IOException e) {
    for (Throwable suppressed : e.getSuppressed()) {
        log.warn("Suppressed during close", suppressed);
    }
    throw e; // preserve primary
}
```

Do not swap primary and suppressed — debugging depends on the main failure.

## 3. Wrapping with cause

```java
try {
    chargeCard(order);
} catch (PaymentProviderException e) {
    throw new OrderProcessingException("Unable to process order", e);
}
```

Preserves stack trace via **`initCause` / constructor with cause**. Avoid wrapping without cause — loses root analysis.

## 4. Logging without duplicate noise

```java
// Good: log once at boundary with stack trace
log.error("Order {} failed", orderId, e);

// Avoid: log and rethrow same exception at every layer
```

At service boundaries: log **or** wrap — not both with full stack at each tier unless policy requires.

## 5. Custom application exceptions

```java
public class OrderProcessingException extends RuntimeException {
    public OrderProcessingException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

Add fields (error codes) when API clients need stable machine-readable codes.

## 6. Catch-all `Exception` trap

```java
catch (Exception e) {
    throw new ServiceException("failed", e);
}
```

Hides **non-retryable** bugs, wraps **InterruptedException** incorrectly, and can turn programming errors into generic 500s. Catch **specific** types; use global handler for unhandled.


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-08-exception-handling/02-try-with-resources-and-wrapping.md)
- [Exception handling production playbook](../../../03-production-playbook/core-java/module-08-exception-handling-production-playbook.md)
- [Module index](index.md)
