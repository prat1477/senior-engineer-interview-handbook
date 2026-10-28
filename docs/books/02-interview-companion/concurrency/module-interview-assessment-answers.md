---
title: Concurrency — Assessment Answers
description: Model answers for concurrency interview practice.
status: covered
audience: advanced
tags: [interview, concurrency, answers]
updated: 2026-10-25
---

# Concurrency — Assessment Answers

1. **Concurrency** — many requests in flight (threads waiting on I/O). **Parallelism** — multiple cores executing simultaneously (CPU-bound work). Example: 1 000 concurrent HTTP handlers vs 8 cores running matrix math.

2. **Safety** — no corrupted shared state (lost updates). **Liveness** — system progresses (no permanent deadlock/starvation). Safety failure: double charge; liveness failure: all threads blocked in a lock cycle.

3. Program order within a thread; `synchronized` unlock→lock; `volatile` write→read; `Thread.start` before child actions; `Thread.join` after child completion; `java.util.concurrent` actions per spec.

4. **No.** `volatile` gives visibility of individual reads/writes, not atomic read-modify-write. Use `AtomicInteger`, locks, or confinement.

5. **Lost update** — both read same value, both write incremented value once. Fixes: `AtomicInteger` / synchronized debit in JVM; conditional SQL `UPDATE ... WHERE balance >= 100` in DB for cross-instance.

6. Unlock on monitor M **happens-before** subsequent lock on M (visibility + mutual exclusion for guarded region). Does **not** coordinate across JVM instances or external systems.

7. If the critical section throws, `unlock` in `finally` still runs — otherwise the lock is held forever and other threads starve or deadlock.

8. **LongAdder** when many threads increment the same counter (reduces CAS hot spot). `sum()` under concurrent increments is not a strict global snapshot — fine for metrics, not authoritative ledger totals without quiescence or DB truth.

9. Two threads can both see absent key and both put — duplicate work or inconsistent state. Use `putIfAbsent`, `computeIfAbsent`, or `merge` for single-key atomicity.

10. **Core** threads stay alive; above core, tasks queue until **max** threads spawn; beyond max with full queue → **rejected**. Queue bounds latency/memory and enables backpressure.

11. Accepts unlimited tasks while consumers lag — p99 latency grows without bound, memory pressure, no early rejection signal. Prefer bounded queue + rejection or caller-runs.

12. Average items in system L ≈ arrival rate λ × time in system W. Growing queue depth → tasks spending longer waiting — scale consumers, shed load, or fix slow downstream.

13. **`thenApply`** maps `T→U`. **`thenCompose`** when function returns `CompletionStage` — flattens `CF<CF<U>>`. DB: `session.executeAsync(stmt).thenCompose(rs -> mapRows(rs))` not `thenApply` if inner is async.

14. Default `supplyAsync` uses **common ForkJoin pool** — blocking JDBC starves parallel streams and other CF async work. Use dedicated blocking pool or virtual threads.

15. The thread that **completes** the previous stage (often a common-pool worker or driver completion thread). Heavy work there blocks that scarce thread.

16. Common pool is for short CPU tasks; blocking holds workers idle while work queues stall — hurts everyone using parallel streams/default async.

17. Unmount frees the **carrier** platform thread to run other virtual threads while one waits on supported blocking I/O — many blocked requests without one OS thread each.

18. At most ~50 concurrent DB operations; rest block on pool acquire or timeout. VTs don’t enlarge the pool — add semaphore/timeouts/bulkhead and right-size pool.

19. **remove** prevents next task on same pooled thread seeing stale request/trace ID. **No** automatic propagation to async workers — copy context explicitly or use framework/ScopedValue integration.

20. **Latch** — one-shot wait for N services to finish startup. **Barrier** — fixed team repeats synchronized phases (e.g. batch pipeline rounds).

21. Semaphore with N>1 allows N concurrent holders — not exclusive. Extra **release** inflates permits → limit broken, possible over-subscription to downstream.

22. **`put`** blocks indefinitely when full — strong backpressure. **`offer(timeout)`** — bounded wait, fail fast or degrade when overloaded; handle interrupt for shutdown.

23. **Queue** — single JVM, elements removed on take, lost on crash. **Kafka** — replicated log, records retained by policy, **offsets** per consumer group, replay via reset/new group; not deleted merely because read.

24. **Deadlock** — circular wait, blocked. **Livelock** — threads keep reacting, no useful completion. **Starvation** — one thread never acquires lock/CPU while others proceed.

25. Global **lock ordering**; **`tryLock` with timeout**; reduce lock scope; avoid nested locks; bulkhead/timeouts on external calls.

26. **No** — `final` is reference only; mutable list contents can change if reference leaks. Use `List.copyOf` in constructor and never expose mutable backing.

27. **Performance** (cache coherence), not Java memory model data race (unless actual unsynchronized shared mutation).

28. **Ring buffer** — in-process pattern; **Disruptor** — framework implementing sequenced ring processing; **Kafka** — distributed streaming. Default **BlockingQueue** until profiling proves microsecond path needs Disruptor.

29. Single dump is a snapshot — races and transient blocks differ over time; two dumps show stuck vs moving threads and growing lock chains.

30. **No** — RUNNABLE means eligible to run. Confirm with CPU profiler/async profiler; may be runnable but not scheduled yet.

31. Each click sent a **different** id — unique constraint treats them as distinct operations. Need **stable idempotency key** or shared **payment intent** id for the same logical purchase.

32. **Stable idempotency key** reused on retries/double-submit, or server-issued intent id both requests reference; store outcome keyed by that business identity.

33. `inFlight.computeIfAbsent(key, k -> supplyAsync(...).whenComplete((r,t) -> inFlight.remove(k)))` — ensures one load; cleanup on complete/fail so map doesn’t leak; handle failures so waiters see exception.

34. **Rate limiter** — requests per time window. **Semaphore** — concurrent in-flight operations. **Fixed pool** — active worker threads executing tasks. **Bounded queue** — queued work waiting for workers.

35. `UPDATE account SET balance = balance - 100 WHERE id = 42 AND balance >= 100` — **0 rows affected** means insufficient funds or lost race; retry or abort based on isolation.

36. Semaphore on provider concurrency; distributed **rate limiter** for RPS; **deadlines/cancellation**; dedicated executor; **coalescing** duplicate prompts; exponential backoff on 429 with jitter.

37. Persist row with **unique idempotency key** + `PROCESSING`; short txn; call PSP with same key; update `SUCCEEDED`/`FAILED`/`UNKNOWN` in new txn; webhook idempotent handler; reconciliation for UNKNOWN. Long txn around HTTP holds locks and cannot roll back charge.

38. **Pool starvation** / latency spikes on all parallel work. Move blocking to dedicated pool or VT; use explicit executors on `*Async`; don’t block common pool.

39. **DB pool exhaustion** — too many concurrent borrowers vs pool size or slow queries. Fix: right-size pool, query tuning, semaphore to match downstream, reduce concurrent borrowers, timeouts.

40. **Mitigation** — restart may break hold (last resort) or kill stuck thread (dangerous). **Structural** — lock ordering, smaller locks, tryLock timeouts, remove cycle.

41. Pool limits **threads executing**; DB pool limits **connections**; if many tasks each need connection, threads can exceed useful DB concurrency — semaphore aligns in-flight DB work with 50 connections.

42. **Exactly-once** end-to-end across PSP+DB+broker is not generally guaranteed. **Effectively-once** — idempotent APIs, dedup keys, outbox, reconciliation so customer charged once and ledger matches.

### Mini whiteboard

| # | Answer |
| --- | --- |
| A | Thread A unlock(m) → HB → Thread B lock(m) sees A’s writes in critical section |
| B | Outer stage is `CompletionStage<U>` not nested `CF<CF<U>>` — one pipeline |
| C | VT runs on carrier → blocks on I/O → unmount → carrier serves other VTs |
| D | Timeout after PSP success leaves UNKNOWN → query PSP/webhook before retry charge |
| E | **Semaphore(50)** around PSP calls (concurrency cap) |

43. See model answers in [canonical Lesson 24](../../../concurrency/24-senior-interview-assessment.md).
