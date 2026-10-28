---
title: "Exception Handling — Assessment Answers"
description: Answers for Module 8 interview practice.
status: draft
audience: advanced
tags: [exceptions, interview, answers, module-8]
created: 2026-10-17
updated: 2026-10-17
---

# Exception Handling — Assessment Answers

## 1. Checked exceptions in libraries

When callers **must** handle recoverable environmental failures (I/O) and you want compile-time enforcement. Many modern Java APIs avoid checked exceptions for ergonomics — be ready to defend either choice.

## 2. Double failure in TWR

Primary exception from try; close exception **suppressed** on primary via `addSuppressed`. Thrown exception is try-block failure.

## 3. Catch-all wrapping

Masks specific handling, duplicates logs, may wrap **InterruptedException** without restoring interrupt flag, turns bugs into generic failures.

## 4. `bad()` return value

**2** — `finally` return overrides try return.

## 5. Try-with-resources

```java
try (Connection conn = dataSource.getConnection()) {
    // use conn
}
```

## 6. Wrapping with cause

Constructor `OrderProcessingException(String, Throwable)` passes `e` to `super(message, cause)` — full chain in stack trace.

## 7. Idempotency key before charge

First request stores key → charge runs once. Retry with same key hits stored state → skip duplicate charge while completing or returning prior result.

## 8. Limits of idempotency

Two independent systems — payment may commit while DB rolls back. Need reconciliation, provider status API, outbox, or manual repair — not single try/catch.

## 9. Retry examples

**Reasonable:** transient 503, socket timeout on idempotent GET, deadlock on retryable transaction (with limit). **Not:** validation error, insufficient funds, duplicate non-idempotent POST without key, `NullPointerException`.

## 10. Exception vs saga/outbox

Exceptions end **one request’s** control flow. Sagas/outbox coordinate **multiple services over time** with durable messages and compensations.

## Mini-assessment

**A.** `SQLException` catch must come **before** `Exception` (subclass first).

**B.** `e.getSuppressed()` on caught exception.

**C.** Failure **type** and operation **semantics** (idempotency, side effects).
