---
title: Database Concurrency and Isolation
description: Optimistic/pessimistic locking, MVCC, atomic SQL — complements Lesson 22.
status: covered
audience: advanced
tags: [distributed-systems, database, postgres]
created: 2026-10-25
updated: 2026-10-25
---

# Database Concurrency and Isolation

Application locks do not replace **database** concurrency control in multi-instance deployments.

## Optimistic locking (`@Version`)

JPA increments version on successful update; stale version → `OptimisticLockException`. Good when conflicts are **workload-dependent** (not a universal “5–10%” rule).

## Pessimistic locking

```sql
SELECT * FROM account WHERE id = 42 FOR UPDATE;
```

Holds row lock until transaction ends — prevents concurrent writers; risk of deadlocks and reduced throughput.

## `FOR UPDATE NOWAIT` / `SKIP LOCKED`

- **NOWAIT** — fail fast if row locked.
- **SKIP LOCKED** — queue workers skip rows already locked (job claiming patterns).

## Atomic conditional updates

Prefer DB-native compare-and-set:

```sql
UPDATE account SET balance = balance - 100
WHERE id = 42 AND balance >= 100;
```

Inspect **rows affected** — application-level read-modify-write is racy across instances.

## Lock ordering

Acquire locks in **deterministic order** across tables to reduce deadlock (same principle as Java locks).

## PostgreSQL MVCC (high level)

Readers generally do not block writers; writers create new row versions; `VACUUM` reclaims dead tuples. Long transactions increase bloat and conflict windows.

## When DB atomic ops beat app logic

Single-row conditional updates, ledger postings, inventory decrements — let the engine enforce invariant in one statement.

## Cross-links

- [Concurrency L22 — Scenario D](../concurrency/22-backend-concurrency-scenarios.md)
- [M8 — idempotency](../books/01-engineering-mastery/core-java/module-08-exception-handling/03-production-spring-retries-idempotency.md)

**Verify:** isolation behavior and syntax for your DB version (PostgreSQL docs for `READ COMMITTED` / `REPEATABLE READ`).
