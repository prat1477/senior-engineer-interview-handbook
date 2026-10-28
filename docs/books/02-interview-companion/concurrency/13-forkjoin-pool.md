---
title: "Companion 13 — ForkJoinPool"
description: Work-stealing, RecursiveTask, common pool pitfalls.
status: covered
audience: advanced
tags: [interview, companion, concurrency, lesson-13]
updated: 2026-10-25
---

# Companion 13 — `ForkJoinPool`

**Canonical source:** [Lesson 13 — ForkJoinPool](../../../concurrency/13-forkjoin-pool.md).

## Definition

`ForkJoinPool` is a work-stealing executor for divide-and-conquer tasks — workers steal from deque tails when idle.

## Why it exists

Efficient CPU-bound parallel recursion (`parallelStream`, custom splits) with load balancing across uneven subtrees.

## Must remember

- `RecursiveTask<V>` returns value; `RecursiveAction` void.
- `fork()` schedule; `join()` wait; `invoke()` fork+join together.
- Split threshold — too-small tasks → overhead dominates.
- **Common pool** shared — blocking JDBC on it hurts all `parallelStream`/default CF async.
- **Not** virtual-thread scheduling — VT uses carriers; FJP steals **tasks**, different roles.
- Blocking I/O → VT or blocking pool, not FJP.

## Interview traps

- `parallelStream()` for blocking HTTP — ties up common pool.
- Equating “many virtual threads” with ForkJoin.

## Frequently asked questions

- **Q:** `fork(); join();` order?
  **A:** Often fork all then join all; `invoke` for simpler single-subtask paths.
- **Q:** Dedicated FJP?
  **A:** When you need isolation from common pool or custom parallelism.

## Interview flow

```mermaid
flowchart LR
  w1[Worker 1 deque]
  w2[Worker 2 idle]
  w2 -->|steal tail| w1
```

## ASCII / table recall

```text
Local deque: push subtasks on head, steal from tail
CPU split/merge OK | blocking wait NOT OK
```

## Explain aloud (whiteboard)

1. “Work-stealing balances uneven recursive CPU work.”
2. “Common pool is a shared resource — no blocking I/O there.”
3. “Virtual threads solve blocking fan-out; ForkJoin solves CPU divide-and-conquer.”

## JDK and debug clues

- `ForkJoinPool.commonPool-worker-*` threads in dumps during parallel streams.

## 30-second revision

- Steal from deque; RecursiveTask; common pool sacred; CPU yes blocking no; VT ≠ FJP.

## Memory hooks

- **SPLIT** — **S**teal **P**arallel **L**ocal **I**/O **T**asks forbidden.

## Cross-links

- [Companion 12 — CF](12-completable-future.md)
- [Companion 14 — VT](14-virtual-threads.md)
- [M6 parallel streams](../../../books/01-engineering-mastery/core-java/module-06-java-8-streams/04-correctness-parallel-performance.md)
