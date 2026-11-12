---
title: Distributed systems — Visual Quick Reference
description: Interview cheat sheet for DB concurrency and distributed locks.
status: covered
audience: advanced
tags: [companion, distributed, cheat-sheet]
updated: 2026-10-28
---

# Distributed systems — Visual Quick Reference

Canonical pages:

- [Database concurrency and isolation](../../../distributed-systems/database-concurrency-and-isolation.md)
- [Locks, fencing, ScyllaDB](../../../distributed-systems/distributed-locks-fencing-and-scylladb.md)

## Lost update vs lock

```mermaid
flowchart TD
  debit[Debit account] --> sql["UPDATE balance WHERE balance >= amount"]
  sql --> rows{rows updated?}
  rows -->|1| ok[Success]
  rows -->|0| retry[Conflict or insufficient funds]
```

| Mechanism | Say this |
| --- | --- |
| Optimistic `@Version` | Retry on conflict; rate is workload-specific |
| `SELECT FOR UPDATE` | Pessimistic row lock; watch lock order |
| JVM `synchronized` | Does not cover other instances |
| Fencing token | Works only if storage rejects stale tokens |
| Synthetic sharding | Changes query shape; not a free speedup |

## When both appear

Kafka between services; database conditional update for money; in-process queue only inside one JVM.

## Kafka, idempotency, and outbox recall

| Topic | 30-second interview line | Trap |
| --- | --- | --- |
| Kafka ordering | Order is per partition; key by `accountId` for an account sequence. | `transactionId` usually disperses one account's events. |
| Debit | One conditional `UPDATE ... WHERE balance >= amount`; check row count. | SELECT then UPDATE races across instances. |
| Duplicate replay | Unique `transactionId` claim makes retry/replay idempotent. | Exactly-once business effect is not exactly-once delivery. |
| Flush | Sends deferred SQL; does not commit. | `save()` always proves unique claim now. |
| Outbox | Business update and event intent commit together; CDC publishes later. | CDC outage rolls back an already committed DB transaction. |

```mermaid
sequenceDiagram
  participant K as Kafka
  participant C as Consumer
  participant D as PostgreSQL
  participant O as Outbox/CDC
  K->>C: record (accountId, transactionId)
  C->>D: claim id + conditional debit + outbox row
  D-->>C: commit
  C->>K: acknowledge input offset
  D->>O: committed outbox captured
```

**Memory trick:** **Key -> Claim -> Debit -> Outbox -> Ack.**
