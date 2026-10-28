---
title: "Lesson 14 — Virtual Threads"
description: Carriers, mounting, pinning, pools, and resource limits (JDK 21+).
status: covered
audience: advanced
tags: [concurrency, lesson-14, virtual-threads]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 14 — Virtual Threads

**Primary target: JDK 21+** (`Thread.ofVirtual()`, JEP 444). Pinning behavior **evolves by release** — verify for your production JDK.

## Concurrency vs parallelism

- **Concurrency:** many tasks in progress (I/O wait, scheduling).
- **Parallelism:** simultaneous CPU execution on multiple cores.

Virtual threads improve **concurrency** for **blocking** workloads; they do **not** add CPU cores.

## Platform vs virtual vs carrier

| Term | Meaning |
| --- | --- |
| **Platform thread** | 1:1 with OS thread (kernel scheduler) |
| **Virtual thread** | Lightweight JVM-managed thread |
| **Carrier** | Platform thread running mounted virtual threads (M:N scheduling) |

```text
[Carrier OS thread] --mounts--> VT1 runs
VT1 blocks on supported JDK I/O --> unmount
Carrier runs VT2 ...
VT1 resumes when I/O completes --> remount (maybe same or other carrier)
```

**OS scheduler** still schedules carrier platform threads onto **CPU cores**. Millions of virtual threads ≠ millions of cores.

## Why virtual threads help

Blocking code can stay **blocking** while carriers switch between thousands of parked virtual threads — practical for request-per-thread servers when work is mostly I/O.

## Why they do not speed CPU-bound work

CPU-saturated work still needs cores; more virtual threads only add scheduling overhead.

## Thread pinning

When a virtual thread cannot unmount during a blocking operation, it **pins** its carrier — reducing scalability.

| JDK era | Notes |
| --- | --- |
| **21–23** | `synchronized` block/method during native/blocking ops could pin carrier (JEP 444) |
| **24+** | JEP 491 reduces pinning for many `synchronized` cases — **re-test** on target JDK |

Also watch **JNI**, **native libraries**, some `FileChannel` operations, and **foreign function** calls — may pin or block carriers.

Use `jcmd <pid> Thread.dump_to_file` and JFR **jdk.VirtualThreadPinned** (where available) for pinning diagnostics.

## Connection pools and semaphores

10 000 virtual threads with **50** JDBC connections → at most ~50 concurrent DB work; rest wait (or timeout). Virtual threads do not enlarge the pool.

Patterns:

- Right-size pools for downstream limits.
- Semaphore/bulkhead around scarce resources ([Lesson 22E](22-backend-concurrency-scenarios.md)).
- Timeouts on acquire and queries.

## Do not pool virtual threads

Create **per task** (`Executors.newVirtualThreadPerTaskExecutor()`). Pooling virtual threads like platform worker threads defeats their model.

## Memory

Each virtual thread has stack/metadata — “unlimited” tasks still mean RAM pressure and downstream limits.

## ThreadLocal caution

Many virtual threads × large `ThreadLocal` values → memory risk ([Lesson 15](15-threadlocal-and-scoped-value.md)).

## 10+ YOE pitch

“Virtual threads are for **high fan-out blocking I/O**, not CPU parallelization. I still enforce DB/HTTP limits with pools and semaphores, monitor pinning on our JDK, and avoid treating carrier count as throughput guarantee.”

## Cross-links

- [JVM M9 — architecture](../books/01-engineering-mastery/core-java/module-09-jvm-basics/01-jvm-architecture-and-execution-lifecycle.md)
- [Distributed DB concurrency](../distributed-systems/database-concurrency-and-isolation.md)

## Interview Q&A

**Q:** Do virtual threads replace thread pools for CPU work?  
**A:** No — use platform pools or parallel streams/ForkJoin for CPU-bound tasks.

**Q:** Why pin?  
**A:** Carrier cannot unmount during some blocking/native/synchronized paths — carrier is tied up until operation completes (version-dependent for `synchronized`).
