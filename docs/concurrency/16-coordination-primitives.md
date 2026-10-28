---
title: "Lesson 16 — Coordination Primitives"
description: CountDownLatch, CyclicBarrier, Semaphore, Phaser comparison.
status: covered
audience: advanced
tags: [concurrency, lesson-16]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 16 — Coordination Primitives

## Comparison table

| Primitive | Reusable? | Typical use |
| --- | --- | --- |
| **CountDownLatch** | One-shot | Wait for N events / startup gate |
| **CyclicBarrier** | Yes | Fixed parties rendezvous per phase |
| **Semaphore** | Yes | Limit concurrent access to N resources |
| **Phaser** | Yes | Multi-phase, dynamic party count |

## CountDownLatch

```java
CountDownLatch ready = new CountDownLatch(3);
// each service: ready.countDown();
ready.await(); // blocks until count hits 0
```

`countDown()` is idempotent past zero; `await()` unblocks all waiters once.

## CyclicBarrier

```java
CyclicBarrier barrier = new CyclicBarrier(3, () -> mergePhase());
worker.run(); // await() at phase end; barrier action runs by one thread
```

**Broken barrier** on timeout/interrupt — `BrokenBarrierException`; reset or fail job.

## Semaphore

```java
Semaphore dbSlots = new Semaphore(50);
dbSlots.acquire();
try {
    query();
} finally {
    dbSlots.release(); // only after successful acquire
}
```

- **Not a mutex** unless permits=1 — multiple permits = N concurrent holders.
- `tryAcquire(timeout)` for bounded wait.
- **Release without acquire** inflates permits → breaks limit.
- On interrupt during `acquire`, handle `InterruptedException` and permit accounting.

## Phaser

Dynamic register/deregister; phases advance when parties arrive — useful for staged pipelines with variable workers.

## 10+ YOE pitch

“Latch for one-time startup; barrier for phased batch compute; semaphore for downstream capacity; phaser when party count shifts between phases.”

## Cross-links

- [Lesson 17 — Producer–consumer](17-producer-consumer-patterns.md)
- [Lesson 22 — Rate vs concurrency](22-backend-concurrency-scenarios.md)
