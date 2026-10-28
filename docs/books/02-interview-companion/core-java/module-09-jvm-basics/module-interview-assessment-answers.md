---
title: "JVM Basics — Assessment Answers"
description: Answers for Module 9 interview practice.
status: draft
audience: advanced
tags: [jvm, interview, answers, module-9]
created: 2026-10-18
updated: 2026-10-18
---

# JVM Basics — Assessment Answers

## 1. Frequent GC, stable post-GC occupancy

Suggests **high allocation churn** (many short-lived objects) while the **long-lived set** is stable. GC runs often to recycle young generation, but old-gen footprint after GC is flat. **Not automatically a leak** — confirm with allocation rate in logs and whether old-gen occupancy trends upward over hours/days.

## 2. Rising post-GC occupancy

Possible **growing retention** — objects surviving collections accumulate in old gen. Next: trend GC logs, capture heap dump at similar load, dominator tree + path to GC roots. Still need evidence — could also be new traffic pattern or cache warm-up.

## 3. Large `HashMap` with millions of `byte[]`

Start with **class histogram** (`byte[]`, entry class), then **dominator tree** on the map or dominator of entries, then **retained heap** and **path to GC roots** to the code holding the map.

## 4. Spring singleton with growing `List`

Events are **strongly reachable** from the singleton bean for the JVM lifetime. GC only collects **unreachable** objects. Fix: bound the list, persist and trim, or use a queue with consumption — not `System.gc()`.

## 5. Container limit exceeded, heap below `-Xmx`

Investigate **native memory**: Metaspace, **thread stacks** (count × `-Xss`), **direct buffers**, JNI, code cache, and **RSS vs cgroup limit**. Enable **NMT** if appropriate; check `unable to create native thread`.

## 6. OOM vs SOE

| | Area |
| --- | --- |
| **`OutOfMemoryError`** | Heap, Metaspace, native thread creation, etc. (message-specific) |
| **`StackOverflowError`** | Java thread stack — deep recursion / huge frames |

## 7. Stable heap % but memory pressure

Heap is only part of **process RSS**. Metaspace, stacks, direct memory, and native allocations do not appear in heap metrics — container kills on **total** usage.

## 8. Raising `-Xmx` not always right

Does not fix **retention leaks**; increases GC work; can push **total RSS** over **Kubernetes/cgroup** limit and cause **OOM kill** without Java heap OOM. Buy time only when profiling shows legitimate working set growth.

## 9. GC logs vs heap dump

| Tool | Answers |
| --- | --- |
| **GC logs** | *When* collections happen, pause times, promotion, full GC — **over time** |
| **Heap dump** | *What* objects exist and **who retains them** — **snapshot** |

Use logs for churn vs retention trends; dumps for dominators and paths to roots.

## 10. Shallow vs retained

**Shallow:** object header + its fields. **Retained:** shallow plus objects only this object keeps alive.

Example: `Root → Service → Map (shallow small) → 1M values (large retained)`. Map has large **retained heap**; one value has small shallow size but is dominated by the map.

## 11. GC roots (examples)

Thread stacks/locals, static fields of loaded classes, JNI globals, JVM internal roots.

## 12. `MaxGCPauseMillis`

Does **not** guarantee all pauses stay under the value; does not prevent **full GC**; not applicable to non-G1 collectors.

## 13. `WeakHashMap` trap

**Values are strong.** If a value references its key (or key is pinned by string literal / other strong ref), weak key cleanup does not occur as expected.

## 14. Spark case (facts only)

Production Spark OOM; used GC logs, heap dump, app logs, metrics; dump showed large retention via **Spark SQL optimizer** structures; disabled `spark.sql.constraintPropagation.enabled=false`; resolved. Validate correctness/performance after optimizer change.

## Mini-assessment

**A.**

```bash
jcmd 12345 GC.heap_dump filename=/tmp/app.hprof
```

**B.** `-Xlog:gc*` (with file/tags as needed).

**C.** A Java memory leak is when objects remain **reachable** (usually via strong references) though the application no longer needs them, preventing reclamation.
