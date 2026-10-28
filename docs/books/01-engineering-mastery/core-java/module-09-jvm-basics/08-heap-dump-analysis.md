---
title: "Lesson 8 — Heap Dump Analysis"
description: "Histogram, dominator tree, retained heap, path to GC roots, MAT workflow."
status: covered
audience: practitioner
tags: [[jvm, heap-dump, mat, module-9, lesson-8], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 8 — Heap Dump Analysis

Histogram, dominator tree, retained heap, path to GC roots, MAT workflow.

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

Core Java Module 9 — **JVM basics and GC**. This is the canonical Engineering Mastery
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-09-jvm-basics/08-heap-dump-analysis.md) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

## Architecture

This lesson sits in **Module 9** of the Core Java track. Service code should treat
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

# Lesson 8 — Heap Dump Analysis

A heap dump is a **snapshot** of reachable objects on the Java heap. Analysis connects **retention** to **application code** — not every large object is a leak.

## Investigation workflow

```text
Histogram → Dominator Tree → Retained Heap → Path to GC Roots → Code-Level Root Cause
```

## 1. Core concepts

| Term | Meaning |
| --- | --- |
| **Shallow size** | Memory of the object itself (fields + header), excluding referenced objects |
| **Retained heap** | Memory freed if this object were removed **and** only it kept subgraph alive |
| **Dominator tree** | Each object dominated by the nearest ancestor that must die for it to die — prioritizes “who holds the mass” |
| **Path to GC roots** | Chain of strong references from roots to the object |
| **Object graph** | Objects as nodes, references as edges |

### Small example (conceptual)

```text
Root → ServiceContext → cache (Map) → 1_000_000 Entry objects
```

- One `Entry` may have **small shallow size**.
- The **Map** may have large **retained heap** if it dominates those entries.
- Dominator tree highlights **cache** before individual entries.

## 2. Class histogram

Sort by instance count or shallow size to spot suspicious classes (`byte[]`, `char[]`, domain DTOs, framework internals).

**Caution:** high count alone is not a leak — validate **retained** size and **growth over time**.

## 3. Dominator tree

Identify objects retaining the largest **retained heap**. Ask: is this **legitimate** (e.g. preloaded index) or **unbounded growth**?

The dominator tree **prioritizes** investigation; it does not **prove** a leak without reachability and behavior context.

## 4. Path to GC roots

For a suspicious object:

1. Open **Path to GC Roots** (exclude weak/soft if appropriate for your hypothesis).
2. Walk **strong-reference** chain to static fields, threads, singletons, caches.
3. Map to **source** (field name, Spring bean, collection).

## 5. Eclipse MAT workflow

1. Open the `.hprof` dump.
2. **Histogram** — flag classes with abnormal counts or shallow totals.
3. **Dominator tree** — find top retained objects.
4. Inspect **retained heap** on dominators.
5. **Path to GC Roots** on dominator or suspect instance.
6. Trace chain to **application code** (your package, Spring beans).
7. Form a **hypothesis** (unbounded list, missing eviction, per-request accumulation).
8. **Validate** fix with metrics + representative workload — dumps are one instant.

## 6. Large object vs leak

| Observation | Interpretation |
| --- | --- |
| Single large `byte[]` for one export | May be **legitimate** peak usage |
| Same cache dominator growing across dumps | **Retention** problem likely |
| Optimizer / planner structures (framework) | May be **feature memory**, not classic app leak — see [case study](09-production-oom-case-study-spark-sql-optimizer.md) |

## Common misconceptions

| Myth | Reality |
| --- | --- |
| "Retained heap = shallow size" | Retained includes dominated subgraph |
| "One dump proves leak" | Need trend or reproducible growth |
| "Dominator = guilty" | Must confirm with roots + code paths |


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-09-jvm-basics/08-heap-dump-analysis.md)
- [JVM basics and GC production playbook](../../../03-production-playbook/core-java/module-09-jvm-basics-production-playbook.md)
- [Module index](index.md)
