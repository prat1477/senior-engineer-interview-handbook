---
title: "Lesson 21 — Production Debugging"
description: Thread dumps, executor saturation, pinning, correlation with metrics.
status: covered
audience: advanced
tags: [concurrency, lesson-21]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 21 — Production Debugging

## Workflow

1. **Symptom** — latency, errors, CPU, pool wait times.
2. **Metrics** — thread pool queue depth, DB pool active, GC, request rate.
3. **Multiple thread dumps** (30–60s apart) — `jcmd <pid> Thread.print`, JFR, `jstack`.
4. **Correlate** — same threads blocked on same lock? Growing pool queue?
5. **Hypothesis** → targeted fix (pool size, lock order, semaphore, query).

## Thread states (snapshot semantics)

| State | Meaning in dump |
| --- | --- |
| `BLOCKED` | Waiting to enter monitor |
| `WAITING` | `wait()`, park without timeout |
| `TIMED_WAITING` | `sleep`, timed `wait`, `park` with deadline |
| `RUNNABLE` | **Eligible** to run — **not proof** of active CPU at dump instant (can be running or ready) |

## Common signatures

- **Deadlock** — “Found one Java-level deadlock” section.
- **Pool exhaustion** — many threads in `TIMED_WAITING` on pool queue or JDBC `getConnection`.
- **Virtual thread pinning** — carriers blocked while many VTs pinned (JDK-specific events).
- **ThreadLocal leak** — heap dominators show `ThreadLocal$Entry` chains.

## Distinguish evidence vs guess

High CPU + many `RUNNABLE` in JDBC driver → might be **busy** queries, not necessarily deadlock. Validate with profiler.

## Cross-links

- [M9 — JVM diagnostics](../books/01-engineering-mastery/core-java/module-09-jvm-basics/07-diagnosing-outofmemoryerror-in-production.md)
- [Lesson 18 — Deadlock](18-deadlock-livelock-starvation.md)
