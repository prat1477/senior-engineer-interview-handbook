---
title: "Lesson 3 — Production Handling, Retries, and Idempotency"
description: "Spring services, retryable failures, payment idempotency scenario."
status: covered
audience: practitioner
tags: [[exceptions, spring, idempotency, module-8, lesson-3], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 3 — Production Handling, Retries, and Idempotency

Spring services, retryable failures, payment idempotency scenario.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-08-exception-handling/03-production-spring-retries-idempotency.md) compresses interview signal without
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

# Lesson 3 — Production Handling, Retries, and Idempotency

Exception handling in services is one layer of **reliability** — not a substitute for distributed consistency patterns ([Distributed systems](../../../../distributed-systems/index.md)).

## 1. Spring Boot service practices

| Practice | Rationale |
| --- | --- |
| `@ControllerAdvice` maps exceptions → HTTP | Single translation layer |
| Domain exceptions → 4xx vs 5xx | Client error vs server/dependency |
| Do not leak provider stack traces | Security + noise |
| Validate at boundary | Fail fast before transactions |

```java
@RestControllerAdvice
class ApiErrors {
    @ExceptionHandler(OrderNotFoundException.class)
    ResponseEntity<ProblemDetail> notFound(OrderNotFoundException ex) {
        return ResponseEntity.status(404).body(ProblemDetail.forStatus(404));
    }
}
```

## 2. Retryable vs non-retryable

| Retry maybe | Do not blind-retry |
| --- | --- |
| Transient timeout, 503, connection reset | `IllegalArgumentException`, 400 validation |
| Idempotent read | Non-idempotent POST without key |
| Bounded attempts + backoff | Infinite retry on bug |

**Caveat:** retry policy must match **operation semantics** and failure type — same exception class can be retryable in one context and fatal in another.

## 3. Timeouts, backoff, uncertain outcomes

- **Timeout** → outcome unknown (payment may have succeeded).
- **Bounded retries** with exponential backoff reduce thundering herds.
- After max retries, surface failure and rely on **reconciliation** / support playbooks.

## 4. Idempotency scenario (payment + order status)

**Sequence discussed in prep:**

1. Client submits payment with **idempotency key** `pay-{orderId}`.
2. Service **persists** idempotency record / order intent **before** calling payment provider.
3. Payment provider **succeeds**.
4. Saving order status to DB **fails** (network, deadlock).
5. API returns **5xx**; customer **retries** with same key.

**With stable idempotency key:**

- Second request recognizes in-flight/completed payment for that key → **does not charge again**; may retry status update or return cached outcome.

**What idempotency does not guarantee:**

- **Atomic** consistency between provider ledger and your DB — two systems without distributed transaction.
- You still need **outbox**, **reconciliation jobs**, or provider queries to heal partial states.

```java
@Transactional
public PaymentResult pay(Order order, String idempotencyKey) {
    IdempotencyRecord record = idempotencyStore.begin(idempotencyKey, order.getId());
    if (record.isCompleted()) {
        return record.result();
    }
    PaymentResult charged = paymentClient.charge(order, idempotencyKey);
    order.markPaid(charged);
    orderRepository.save(order); // if this throws, client retries — key prevents double charge
    idempotencyStore.complete(idempotencyKey, charged);
    return charged;
}
```

## 5. Exception handling ≠ distributed recovery

| Layer | Handles |
| --- | --- |
| try/catch, `@ExceptionHandler` | Single request thread, translate failure |
| Idempotency, sagas, outbox | Cross-service consistency over time |

Link: [Spring microservices track](../../../../spring-microservices/index.md) for circuit breakers and outbox (planned lessons).


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-08-exception-handling/03-production-spring-retries-idempotency.md)
- [Exception handling production playbook](../../../03-production-playbook/core-java/module-08-exception-handling-production-playbook.md)
- [Module index](index.md)
