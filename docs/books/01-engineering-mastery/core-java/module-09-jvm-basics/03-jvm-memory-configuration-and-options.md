---
title: "Lesson 3 — JVM Memory Configuration and Important JVM Options"
description: "-Xms, -Xmx, -Xss, GC flags, Metaspace, heap dumps, unified GC logging."
status: covered
audience: practitioner
tags: [[jvm, flags, module-9, lesson-3], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 3 — JVM Memory Configuration and Important JVM Options

-Xms, -Xmx, -Xss, GC flags, Metaspace, heap dumps, unified GC logging.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-09-jvm-basics/03-jvm-memory-configuration-and-options.md) compresses interview signal without
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

# Lesson 3 — JVM Memory Configuration and Important JVM Options

JVM flags tune **heap**, **stacks**, **class metadata limits**, **collector choice**, and **diagnostics**. Flag names and behavior can differ by **Java version** and **JVM implementation** — examples assume **Java 17+ HotSpot**.

## Quick reference

| Flag | Controls | Area / behavior |
| --- | --- | --- |
| `-Xms512m` | Initial / minimum **configured** heap size | Java heap |
| `-Xmx2g` | Maximum **configured** heap size | Java heap |
| `-Xss1m` | Thread **stack size** (per thread) | Java stacks |
| `-XX:+UseG1GC` | Enable **G1** collector | GC |
| `-XX:+UseParallelGC` | Enable **Parallel** throughput collector | GC |
| `-XX:MaxGCPauseMillis=200` | G1 **pause-time goal** (not a guarantee) | G1 behavior |
| `-XX:MaxMetaspaceSize=256m` | Upper bound on **Metaspace** | Class metadata (native) |
| `-XX:+HeapDumpOnOutOfMemoryError` | Request heap dump on supported Java OOM | Diagnostics |
| `-XX:HeapDumpPath=/path/...` | Dump file location | Diagnostics |
| `-Xlog:gc*` | Unified **GC logging** (JDK 9+) | Diagnostics |

Example startup (illustrative — validate in your environment):

```bash
java -Xms512m -Xmx2g -Xss1m \
  -XX:+UseG1GC -XX:MaxGCPauseMillis=200 \
  -XX:MaxMetaspaceSize=256m \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/var/log/app/heapdumps/ \
  -Xlog:gc*:file=/var/log/app/gc.log:time,uptime,level,tags \
  -jar app.jar
```

## `-Xms` and `-Xmx`

| Flag | Meaning | Production notes |
| --- | --- | --- |
| **`-Xms`** | Initial / minimum configured heap | Setting `-Xms` = `-Xmx` avoids heap **resize** during steady state (trade-off: memory reserved earlier) |
| **`-Xmx`** | Maximum configured heap | Must leave headroom in the **container** for non-heap memory |

**Misunderstanding:** `-Xmx` is not “RAM allocated to the JVM process.” Native memory, stacks, and Metaspace sit outside this cap.

## `-Xss`

- Sets **per-thread** Java stack size (default varies by platform and JDK).
- **Many threads** → large **reserved** address space; committed/resident memory grows with actual stack use, not necessarily full `-Xss` per thread.
- Relevant when you see deep recursion (`StackOverflowError`) or `unable to create native thread` under memory pressure.

## Garbage collector flags

| Flag | When useful | Caveats |
| --- | --- | --- |
| `-XX:+UseG1GC` | Default on many server JDKs; balanced throughput and pauses | Tune with logs; goals are not hard SLAs |
| `-XX:+UseParallelGC` | Batch throughput, pause tolerance | Longer stop-the-world events possible |
| `-XX:MaxGCPauseMillis=200` | **G1 only** — influences pacing | **Not a guarantee**; extreme goals can hurt throughput |

Collector choice should follow **measured** latency, throughput, and heap size — see [Lesson 5](05-garbage-collectors-and-g1.md).

## `-XX:MaxMetaspaceSize`

Caps **Metaspace** growth. Useful to fail fast in misconfigured class-loader scenarios; too low causes `OutOfMemoryError: Metaspace` during legitimate dynamic class generation.

## Heap dump on OOM

| Flag | Role |
| --- | --- |
| `-XX:+HeapDumpOnOutOfMemoryError` | JVM attempts a **heap dump** when a **Java** `OutOfMemoryError` is thrown (supported cases) |
| `-XX:HeapDumpPath=...` | Target path — needs **disk space** and **permissions**; may be multi-GB |

**Production:** dumps can contain **PII/secrets**; restrict file ACLs. Dump creation adds **latency and I/O** at failure time.

**Not triggered:** Linux **OOM killer** / cgroup kill — process may die without Java OOM or dump.

## `-Xlog:gc*`

JDK 9+ **unified logging** replaces legacy `-XX:+PrintGCDetails` patterns.

```bash
-Xlog:gc*:file=gc.log:time,uptime,level,tags
```

Use logs for **temporal** behavior (pause frequency, promotion, full GC events). Pair with [heap dumps](08-heap-dump-analysis.md) for **object retention** snapshots.

## Native Memory Tracking (brief)

```bash
-XX:NativeMemoryTracking=summary
# or detail — higher overhead
```

Then at runtime: `jcmd <pid> VM.native_memory summary` (see [Lesson 7](07-diagnosing-outofmemoryerror-in-production.md)).

NMT does **not** inventory every native allocation; it helps compare categories (heap, class, thread, code, etc.).

## Common misunderstandings

| Myth | Reality |
| --- | --- |
| "`MaxGCPauseMillis` caps all pauses at 200 ms" | It is a **goal** for G1; outliers and full GC still possible |
| "Increase `-Xmx` to fix Metaspace OOM" | Metaspace is **not** heap |
| "Heap dump on every memory problem" | Container kill may leave **no** dump |


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-09-jvm-basics/03-jvm-memory-configuration-and-options.md)
- [JVM basics and GC production playbook](../../../03-production-playbook/core-java/module-09-jvm-basics-production-playbook.md)
- [Module index](index.md)
