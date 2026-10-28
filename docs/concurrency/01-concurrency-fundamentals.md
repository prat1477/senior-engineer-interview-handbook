---
title: "Lesson 1 — Concurrency Fundamentals"
description: Threads, tasks, safety, liveness, JDK 17+ baseline.
status: covered
audience: advanced
tags: [concurrency, lesson-1]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 1 — Concurrency Fundamentals

## Concepts

- **Process** vs **thread** — shared memory within a process.
- **Concurrency** — multiple tasks in progress; **parallelism** — simultaneous CPU execution.
- **Safety** — no corrupted state; **liveness** — system makes progress (no deadlock/starvation).

## Java threading models

- **Platform threads** — `Thread`, `ExecutorService`.
- **Virtual threads (21+)** — [Lesson 14](14-virtual-threads.md).

## Shared mutable state

Default assumption: **unsafe** unless proven thread-safe via confinement, immutability, or synchronization.

## Cross-links

- Next: [Lesson 2 — JMM](02-java-memory-model.md)
