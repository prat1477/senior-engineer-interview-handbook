---
title: "Lesson 12 — Concurrent Collections Overview"
description: "High-level ConcurrentHashMap and why HashMap is not for concurrent structure changes."
status: covered
audience: practitioner
tags: [[collections, concurrent, module-4, lesson-12], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 12 — Concurrent Collections Overview

High-level ConcurrentHashMap and why HashMap is not for concurrent structure changes.

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

Core Java Module 4 — **Collections**. This is the canonical Engineering Mastery
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/12-concurrent-collections-overview.md) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

## Architecture

This lesson sits in **Module 4** of the Core Java track. Service code should treat
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

# Lesson 12 — Concurrent Collections Overview

This lesson records **Collections-level** material from study — not a full concurrency module. Deep internals (CAS, segment details, JMM proofs) are in [Concurrency lesson 9 — Concurrent collections](../../../../concurrency/09-concurrent-collections.md) and the [Concurrency index](../../../../concurrency/index.md).

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


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/12-concurrent-collections-overview.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
