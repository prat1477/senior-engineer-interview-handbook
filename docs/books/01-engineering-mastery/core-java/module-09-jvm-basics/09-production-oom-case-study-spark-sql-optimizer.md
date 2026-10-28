---
title: "Lesson 9 — Production OOM Case Study: Spark SQL Optimizer"
description: "Documented Spark workload OOM investigation and constraint propagation mitigation."
status: covered
audience: practitioner
tags: [[jvm, spark, oom, case-study, module-9, lesson-9], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 9 — Production OOM Case Study: Spark SQL Optimizer

Documented Spark workload OOM investigation and constraint propagation mitigation.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-09-jvm-basics/09-production-oom-case-study-spark-sql-optimizer.md) compresses interview signal without
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

# Lesson 9 — Production OOM Case Study: Spark SQL Optimizer

This lesson records a **documented investigation** using only the facts below. It illustrates that OOM on data platforms may involve **optimizer/planner memory**, not only application collections.

## Known facts (only)

- A production **Spark workload** experienced an **`OutOfMemoryError`**.
- Investigation used **GC logs**, a **heap dump**, **application logs**, and **application metrics**.
- The heap dump showed a **large object graph retained through Spark SQL optimizer structures**.
- Disabling Spark SQL constraint propagation **resolved** the issue:

```properties
spark.sql.constraintPropagation.enabled=false
```

**Not recorded** (do not assume in interviews): exact OOM subtype, driver vs executor, Spark version, class names, heap sizes, GC timings, percentages, or measured performance after the change.

## Investigation narrative

### 1. Production symptom

Spark workload failed with **OutOfMemoryError** under production load.

### 2. Evidence collected

| Evidence | Role |
| --- | --- |
| GC logs | Temporal GC behavior during failure window |
| Heap dump | **Retention snapshot** — optimizer-related graph |
| Application logs | Workload context |
| Metrics | Correlation with memory pressure |

### 3. Heap-dump finding

Dominant retention tied to **Spark SQL optimizer structures** — not a typical unbounded `HashMap` in application code.

### 4. Investigation direction

Focus on **query-optimization memory** and planner/optimizer retention rather than assuming a conventional application leak first.

### 5. Configuration change

```properties
spark.sql.constraintPropagation.enabled=false
```

### 6. Outcome

Issue **resolved** after disabling constraint propagation.

### 7. Engineering trade-off

Disabling an optimizer feature may reduce **optimization opportunities**. Validate **correctness** and **performance** on **representative workloads** after the change.

**General context (not an additional incident fact):** complex logical plans can consume substantial memory during optimization — useful when explaining *why* optimizer memory matters, separate from this specific deployment.

## Senior interview answer (model)

> We had a production OutOfMemoryError in a Spark workload. I investigated it using GC logs, a heap dump, application logs, and metrics. The heap dump showed a large object graph retained through Spark SQL optimizer structures, so I investigated query-optimization memory rather than assuming a conventional application memory leak. We disabled Spark SQL constraint propagation using `spark.sql.constraintPropagation.enabled=false`, and the issue was resolved. The key lesson was that query optimization itself can consume substantial memory for complex logical plans. Because this configuration changes optimizer behavior, its correctness and performance impact should be validated against representative workloads.

## What this case does not cover

- Step-by-step MAT screenshots (workflow is in [Lesson 8](08-heap-dump-analysis.md)).
- Executor vs driver tuning — not specified in known facts.
- Expanding the Spark curriculum — see [Spark cross-reference](../../../../data-engineering/spark-cross-reference.md).


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-09-jvm-basics/09-production-oom-case-study-spark-sql-optimizer.md)
- [JVM basics and GC production playbook](../../../03-production-playbook/core-java/module-09-jvm-basics-production-playbook.md)
- [Module index](index.md)
