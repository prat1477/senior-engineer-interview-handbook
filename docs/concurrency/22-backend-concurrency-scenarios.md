---
title: "Lesson 22 — Backend Concurrency Scenarios"
description: Payments idempotency, coalescing, rate limits, lost updates, VT limits.
status: covered
audience: advanced
tags: [concurrency, lesson-22, payments]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 22 — Backend Concurrency Scenarios

Interview-grade scenarios — correctness under concurrency, retries, and horizontal scale.

## Scenario A — Duplicate payment prevention

### Flawed check-then-act

```java
if (!paymentRepository.existsById(requestId)) {
    paymentGateway.charge(payment);
    paymentRepository.save(payment);
}
```

Two threads (or two **instances**) can both pass `exists` before either saves → **double charge**.

`synchronized` on one JVM does **not** help across instances.

### UUID per click trap

Client double-clicks; each request generates a **new UUID**. Unique constraint on `request_id` allows **two rows** — not the same logical payment.

**Idempotency key must be reused** for the same logical operation:

- Client sends stable `Idempotency-Key` header on retries, or
- Server creates durable **payment intent** first; both submits reference same intent id.

Matching “same customer + amount + timestamp” is **not** reliable dedup — legitimate duplicate purchases exist.

### Durable design elements

| Mechanism | Role |
| --- | --- |
| Unique constraint on idempotency key | At-most-one row per logical op |
| States `PROCESSING`, `SUCCEEDED`, `FAILED`, `UNKNOWN` | Safe retries & queries |
| Provider idempotency key | PSP dedupes charge on retry |
| Webhooks (idempotent handlers) | Async completion |
| Reconciliation jobs | Heal ambiguous `UNKNOWN` |

### Timeout after provider success

Network fails after charge — client retries with **same** idempotency key → return stored outcome or query PSP with same operation id — **not** a new charge.

### Transactions vs external systems

DB transaction **cannot roll back** an external charge. Do **not** hold DB transactions open across slow HTTP to PSP — persist intent, call provider, update state in short transactions.

**Exactly-once** across independent systems is not universal — aim for **effectively-once** business outcomes with idempotency + reconciliation.

Cross-link: [M8 — idempotency](../books/01-engineering-mastery/core-java/module-08-exception-handling/03-production-spring-retries-idempotency.md).

### Crash between PROCESSING and provider

Recovery: resume from persisted state; query provider or rely on webhook; expire stale `PROCESSING` with policy.

---

## Scenario B — Request coalescing

Hundreds of threads request same cache key while compute is in flight — run **one** load, share result.

```java
ConcurrentHashMap<String, CompletableFuture<Data>> inFlight = new ConcurrentHashMap<>();

CompletableFuture<Data> load(String key) {
    return inFlight.computeIfAbsent(key, k ->
        CompletableFuture.supplyAsync(() -> expensive(k), executor)
            .whenComplete((r, t) -> inFlight.remove(k)));
}
```

Handle failures (remove on error), cancellation, and executor rejection. **Coalescing** ≠ long-term **caching** — only dedupes concurrent misses.

---

## Scenario C — Rate limiting vs concurrency limiting

| Tool | Limits |
| --- | --- |
| **Semaphore / bulkhead** | Concurrent in-flight calls |
| **Rate limiter (token bucket)** | Operations per time window |
| **Fixed thread pool** | Active worker threads |
| **Bounded queue** | Queued work before rejection |

Distributed rate limits need shared store (Redis, etc.) — per-instance semaphores are insufficient for global caps.

---

## Scenario D — Database lost updates

Application read-modify-write races even with Java locks if two instances update DB.

**Atomic conditional SQL:**

```sql
UPDATE account
SET balance = balance - 100
WHERE id = 42
  AND balance >= 100;
-- rows affected = 0 => insufficient funds or lost race
```

Also: optimistic `@Version`, pessimistic `FOR UPDATE`, isolation level awareness — see [database concurrency](../distributed-systems/database-concurrency-and-isolation.md).

---

## Scenario E — Virtual threads vs connection pool

10 000 virtual threads, **50** JDBC connections — most tasks wait on pool acquire. Add **timeouts**, **semaphore(50)** around DB section, right-size pool, bulkhead per dependency.

Second limiter helps when you must cap concurrent **blocking** calls regardless of VT count.

## 10+ YOE pitch

“Concurrency in payments is about **durable idempotency keys**, state machines, and PSP alignment — not single-JVM locks. I separate coalescing, rate limits, and DB atomic updates.”

## Cross-links

- [Distributed locks & Scylla](../distributed-systems/distributed-locks-fencing-and-scylladb.md)
