---
title: "Lesson 12 — Concurrent Collections Overview"
description: High-level ConcurrentHashMap and why HashMap is not for concurrent structure changes.
status: draft
audience: advanced
tags: [collections, concurrent, module-4, lesson-12]
created: 2026-10-15
updated: 2026-10-15
---

# Lesson 12 — Concurrent Collections Overview

This lesson records **Collections-level** material from study — not a full concurrency module. Deep internals (CAS, segment details, JMM proofs) are **deferred** to the [Concurrency track](../../concurrency/index.md).

## 1. Why not `HashMap` under concurrency?

`HashMap` is **not** designed for concurrent **structural** modification (multiple threads putting/removing). Without external synchronization, races can corrupt the table or lose updates. Fail-fast iterators do not make it safe.

`Collections.synchronizedMap` wraps every method — coarse locking, lower scalability.

## 2. `ConcurrentHashMap` (high level)

- Thread-safe map for concurrent `get`/`put`/compute-style operations.
- Finer-grained locking / CAS (implementation evolves by JDK) — **not** "lock entire map per op" like synchronized wrapper.
- **No null keys or values** — avoids ambiguity in concurrent `get`/`contains`.
- **`putIfAbsent(k, v)`** — atomic "insert if missing" — useful for caches and dedup keys.
- Iterators are **weakly consistent** — may reflect partial updates; no `ConcurrentModificationException` guarantee like fail-fast.

## 3. Atomicity limits

A single `putIfAbsent` is atomic. A workflow such as:

```text
if (!map.containsKey(k)) { map.put(k, expensiveCompute()); }
```

is **not** atomic across threads — use `putIfAbsent`, `computeIfAbsent`, or higher-level coordination.

## 4. Introduced during Collections (defer depth)

| Topic | Status in handbook |
| --- | --- |
| `volatile`, happens-before | **Introduced** — see concurrency lessons 2, 5 |
| CAS | **Introduced** — see concurrency lesson 7 |
| `ConcurrentHashMap` internals | **Deferred** |

## Revision notes

- Concurrent structure changes → `ConcurrentHashMap` (or appropriate concurrent structure).
- `putIfAbsent` / `computeIfAbsent` for atomic single-key patterns.
- Thread-safe map ≠ atomic multi-step business transaction.

## See also

- [Concurrency curriculum](../../concurrency/index.md)
- [Blocking queues](10-blocking-queues-and-backpressure.md)
