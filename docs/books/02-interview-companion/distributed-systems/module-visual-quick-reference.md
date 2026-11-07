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
