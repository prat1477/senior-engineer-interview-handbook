---
title: "Lesson 12 — CompletableFuture"
description: Async pipelines, executors, thenCompose, and database CompletionStage integration.
status: covered
audience: advanced
tags: [concurrency, lesson-12, completablefuture]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 12 — `CompletableFuture`

**JDK 17+** examples. `CompletableFuture` models asynchronous computation with composable stages.

## Concept and motivation

Non-blocking **I/O** (kernel waits without holding a thread) differs from **asynchronous execution** (work continues on another thread or later on the same executor). `CompletableFuture` is about **async task composition**, not magic network efficiency.

## Core API map

| Method | Role |
| --- | --- |
| `thenApply(fn)` | Map result; returns `CompletableFuture<U>` |
| `thenCompose(fn)` | Flatten nested `CompletionStage` — `thenApply` that returns CF would nest |
| `thenCombine(other, fn)` | Combine two completed values |
| `thenApplyAsync` / `thenComposeAsync` | Run on default or supplied `Executor` |

**Default executor:** `ForkJoinPool.commonPool()` for `*Async` without executor — fine for CPU work, risky for blocking I/O unless isolated.

## Sync vs async continuations

```java
CompletableFuture<String> stage = CompletableFuture.supplyAsync(() -> fetchOrderId());

// Runs on SAME thread that completes the previous stage (often common pool worker)
stage.thenApply(id -> enrich(id));

// Runs on explicit executor
stage.thenApplyAsync(id -> enrich(id), ioExecutor);
```

Non-async stages run on the thread that **completes** the predecessor — if that thread is a scarce pool thread, heavy work in `thenApply` blocks that worker.

## `thenCompose` and database drivers

Many async drivers return `CompletionStage`:

```java
CompletionStage<RowSet<Row>> queryAsync =
    session.executeAsync(boundStatement);

return queryAsync.thenCompose(rs -> mapRows(rs));
```

`thenCompose` **flattens** so the outer pipeline is one stage, not `CF<CF<T>>`.

**Why not always add another executor?** If `executeAsync` already schedules I/O on the driver’s event loop / internal pool, an extra `thenComposeAsync` per stage can add thread hops without benefit. Add executors when work is **CPU-heavy** or **blocking** and must not run on the driver’s completion thread.

```java
return session.executeAsync(stmt)
    .thenCompose(rs -> CompletableFuture.supplyAsync(
        () -> heavyTransform(rs), computeExecutor));
```

## `join()` vs `get()`

| | `join()` | `get()` |
| --- | --- | --- |
| Checked exception | Unchecked `CompletionException` | `ExecutionException` (checked) |
| Interrupt | Does not declare interrupt | `InterruptedException` |

Both unwrap `CompletionException` cause chain. Prefer `join()` in internal code; `get()` at boundaries where you handle interrupts explicitly.

## Cancellation and exceptions

Failed stages complete exceptionally; later stages skip unless `handle` / `exceptionally`. `cancel(true)` may not stop underlying I/O — depends on driver/task cooperation.

## Executor isolation pattern

| Workload | Executor |
| --- | --- |
| CPU-bound transforms | Fixed `ThreadPoolExecutor` sized ~ cores |
| Blocking JDBC (legacy) | Dedicated blocking pool — **not** common pool |
| Async driver callbacks | Often driver thread — keep callbacks light |

## Failure cases

- Blocking HTTP inside `thenApply` on common pool → stalls all `supplyAsync` users.
- Lost exception if `exceptionally` swallows without logging.
- `join()` in reactive request thread under load → hides backpressure.

## 10+ YOE pitch

“`CompletableFuture` separates **composition** from **scheduling**. I use `thenCompose` for async DB stages, isolate blocking and CPU work onto named executors, and never assume async I/O just because the API returns a `CompletionStage`.”

## Cross-links

- [Lesson 10 — ThreadPoolExecutor](10-executors-and-thread-pool-executor.md)
- [Lesson 13 — ForkJoinPool](13-forkjoin-pool.md)
- [Lesson 22 — Backend scenarios](22-backend-concurrency-scenarios.md)

## Interview Q&A

**Q:** `thenApply` vs `thenCompose`?  
**A:** `thenApply` maps T→U; use `thenCompose` when the function returns another `CompletionStage` to avoid nested futures.

**Q:** Does async DB mean I need `thenApplyAsync` everywhere?  
**A:** No — run heavy or blocking work off the completion thread; light mapping can stay synchronous on the driver’s completion path.
