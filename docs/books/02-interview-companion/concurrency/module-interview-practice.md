---
title: Concurrency — Interview Practice
description: Drill questions across the 24-lesson curriculum.
status: covered
audience: advanced
tags: [interview, concurrency, practice]
updated: 2026-10-25
---

# Concurrency — Interview Practice

Answers: [module-interview-assessment-answers.md](module-interview-assessment-answers.md).  
Full senior mock: [canonical Lesson 24](../../../concurrency/24-senior-interview-assessment.md).

## Foundations (L1–5)

1. Concurrency vs parallelism — one sentence each with a server example.

2. What is **safety** vs **liveness**? Give one failure mode for each.

3. Name three sources of **happens-before** edges without using “time.”

4. Does `volatile` make `count++` thread-safe? Why or why not?

5. Two threads both read `balance`, add 100, write back — what went wrong and name two fixes at different layers.

6. What HB edge does `synchronized` provide? What does it **not** provide across JVMs?

## Building blocks (L6–11)

7. Why must `ReentrantLock.unlock()` live in `finally`?

8. When is `LongAdder` preferable to `AtomicLong`? When is `sum()` misleading?

9. Why is `if (!chm.containsKey(k)) chm.put(k,v)` unsafe? What do you use instead?

10. Explain `corePoolSize`, `maximumPoolSize`, and queue role in `ThreadPoolExecutor`.

11. Why is an unbounded `LinkedBlockingQueue` dangerous under traffic spikes?

12. State **Little’s law** in words and what rising queue depth implies.

## Async, ForkJoin, VT (L12–15)

13. `thenApply` vs `thenCompose` — when is each required? Include a database `executeAsync` example.

14. Why is blocking JDBC on `CompletableFuture.supplyAsync()` without a dedicated executor risky?

15. What runs non-async `thenApply` stages — which thread?

16. Why should blocking I/O not use `ForkJoinPool.commonPool()`?

17. Virtual thread mounts and unmounts — what problem does unmount solve?

18. 5 000 virtual threads and a 50-connection JDBC pool — what happens without a semaphore?

19. Why `ThreadLocal.remove()` in a pooled platform thread? Does it auto-propagate to `supplyAsync`?

## Coordination and queues (L16–17)

20. CountDownLatch vs CyclicBarrier — one use case each.

21. Why is a semaphore not always a mutex? What breaks if you `release()` without `acquire()`?

22. `BlockingQueue.put` vs `offer(timeout)` — when prefer each?

23. Kafka vs `ArrayBlockingQueue` — durability, retention, and consumer groups in three bullets.

## Failure modes and patterns (L18–20)

24. Deadlock vs livelock vs starvation — distinguish in one line each.

25. Name two deadlock prevention tactics used in production services.

26. `final List<String>` in an immutable config class — is the list immutable? What do you do?

27. False sharing vs cache-line bouncing — performance or correctness issue?

28. Ring buffer vs LMAX Disruptor vs Kafka — scope and when to default to `BlockingQueue`.

## Production and backend (L21–23)

29. Why take **multiple** thread dumps minutes apart?

30. Does `RUNNABLE` in a dump prove a thread is using CPU? What do you do next?

31. Double-click Pay, two pods, two different UUIDs — why doesn’t a unique constraint on `request_id` dedupe?

32. What must the client or server provide so retries are safe?

33. Request coalescing — sketch the `ConcurrentHashMap` + `CompletableFuture` pattern and cleanup concern.

34. Rate limiter vs semaphore vs fixed thread pool — what dimension does each cap?

35. Lost update on account debit — write the conditional SQL pattern and how you detect failure.

36. AI RAG fan-out hits provider 429 — name three concurrent controls (not “add threads”).

## Scenario (senior)

37. Design payment capture with external PSP: states, idempotency key placement, and why not one long `@Transactional` around HTTP.

38. `parallelStream()` on common pool while also using default `thenApplyAsync` — symptom and fix.

39. Thread dump shows 200 threads in `TIMED_WAITING` on `getConnection` — likely bottleneck and two fixes.

40. You see `Found one Java-level deadlock` — immediate mitigation vs structural fix.

41. When would you add **both** a thread pool limit and a semaphore around DB access?

42. Explain effectively-once payment outcomes vs exactly-once across PSP + DB + Kafka.

## Mini whiteboard (rapid)

| # | Draw or say in 30s |
| --- | --- |
| A | Happens-before from unlock to lock |
| B | `thenCompose` flattening nested async |
| C | VT mount/unmount on blocking I/O |
| D | Payment state machine PROCESSING → UNKNOWN |
| E | Pick coordination primitive for “max 50 concurrent PSP calls” |

## Full mock

43. Complete [canonical Lesson 24](../../../concurrency/24-senior-interview-assessment.md) under exam conditions.
## Whiteboard (use the cheat sheet)

1. Draw the module flowchart from the visual quick reference without notes.
2. Give one production scenario and the decision-table row you would choose.
3. Name one interview trap and the correction.
