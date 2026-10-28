---
title: "Lesson 13 — ForkJoinPool"
description: Work-stealing, RecursiveTask, common pool, CPU vs blocking.
status: covered
audience: advanced
tags: [concurrency, lesson-13, forkjoin]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 13 — `ForkJoinPool`

## Work-stealing model

Each worker maintains a deque of tasks. Idle workers **steal** from others’ tails — good for **recursive, CPU-bound** divide-and-conquer with uneven subtree cost.

```text
Task split --> subtasks pushed on local deque
Idle worker steals from another deque's tail
```

## `RecursiveTask<V>` vs `RecursiveAction`

| Type | Returns value |
| --- | --- |
| `RecursiveTask<V>` | Yes — `compute()` returns V |
| `RecursiveAction` | No — void side effects only |

## `fork()`, `join()`, `invoke()`

- `fork()` — schedule subtask asynchronously on pool.
- `join()` — wait for result (must be called after forking children; order matters for correctness).
- `invoke()` — fork + join in one call on current thread (often preferred for simplicity).

**Anti-pattern:** `fork(); fork(); join(); join()` on tiny tasks — overhead dominates.

## Common pool vs dedicated pool

`ForkJoinPool.commonPool()` backs `parallelStream()` and default `CompletableFuture` async. **Shared** — blocking work on it harms everyone.

```java
ForkJoinPool custom = new ForkJoinPool(parallelism);
custom.submit(task).get();
```

## CPU-bound vs blocking I/O

| Use ForkJoin | Avoid for |
| --- | --- |
| Parallel array/matrix work | Blocking JDBC, long HTTP |
| Recursive algorithms with split threshold | Tasks that wait on locks/I/O |

For blocking I/O use [virtual threads](14-virtual-threads.md) or blocking thread pools.

## Virtual threads (relationship only)

Virtual threads use **carrier** platform threads scheduled by the JVM. **ForkJoinPool** is a **work-stealing executor for tasks**, not the same as virtual-thread scheduling. `parallelStream` does **not** use virtual threads. Do not equate “many virtual threads” with “ForkJoin common pool.”

## 10+ YOE pitch

“ForkJoin shines for CPU-bound fork/join with minimal blocking. I keep blocking calls off the common pool and size dedicated pools when parallel streams or CF defaults would contend.”

## Cross-links

- [Lesson 6 — Streams parallel (Core Java M6)](../books/01-engineering-mastery/core-java/module-06-java-8-streams/04-correctness-parallel-performance.md)
- [Lesson 14 — Virtual threads](14-virtual-threads.md)
