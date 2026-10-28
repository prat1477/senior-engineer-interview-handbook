---
title: "Lesson 10 — Executors and ThreadPoolExecutor"
description: Executor hierarchy, pool parameters, rejection policies.
status: covered
audience: advanced
tags: [concurrency, lesson-10]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 10 — Executors and `ThreadPoolExecutor`

## Interfaces

| Type | Role |
| --- | --- |
| `Executor` | `execute(Runnable)` |
| `ExecutorService` | lifecycle, `submit`, `invokeAll` |
| `ScheduledExecutorService` | delayed/periodic |

## `ThreadPoolExecutor` knobs

- `corePoolSize`, `maximumPoolSize`, `keepAlive`, **work queue** (bounded vs unbounded), **RejectedExecutionHandler**.

```java
ThreadPoolExecutor pool = new ThreadPoolExecutor(
    8, 16, 60, TimeUnit.SECONDS,
    new ArrayBlockingQueue<>(500),
    new ThreadPoolExecutor.CallerRunsPolicy());
```

**CallerRuns** — backpressure on submitter thread.

## Virtual thread executor

`Executors.newVirtualThreadPerTaskExecutor()` — new VT per task ([Lesson 14](14-virtual-threads.md)).

## Cross-links

- [Lesson 11 — Sizing](11-thread-pool-sizing-and-backpressure.md)
- [Lesson 12 — CompletableFuture](12-completable-future.md)
