---
title: "Companion 16 — Coordination Primitives"
description: Latch, barrier, semaphore, phaser — when to use which.
status: covered
audience: advanced
tags: [interview, companion, concurrency, lesson-16]
updated: 2026-10-25
---

# Companion 16 — Coordination Primitives

**Canonical source:** [Lesson 16 — Coordination Primitives](../../../concurrency/16-coordination-primitives.md).

## Definition

JDK utilities coordinate threads at application level — wait for events, rendezvous, limit parallelism, or phase through pipelines.

## Why it exists

Locks protect data; primitives orchestrate **workflow** (startup gates, phased batch jobs, downstream caps).

## Must remember

- **CountDownLatch** — one-shot; `countDown` / `await`.
- **CyclicBarrier** — reusable fixed parties; broken on timeout/interrupt.
- **Semaphore** — N permits; not a mutex unless N=1; release only after acquire.
- **Phaser** — dynamic parties, multi-phase.
- `tryAcquire(timeout)` for bounded wait; interrupt handling matters for permit accounting.

## Interview traps

- Semaphore `release()` without `acquire` — inflates permits.
- Using latch for repeating phases — use barrier or phaser.

## Frequently asked questions

- **Q:** Semaphore vs lock?
  **A:** Semaphore counts N concurrent holders; lock is exclusive ownership with conditions.
- **Q:** Cap DB concurrency?
  **A:** Semaphore(50) around acquire connection — complements pool size ([Companion 22](22-backend-concurrency-scenarios.md)).

## Interview flow

See [Visual quick reference — primitive picker](module-visual-quick-reference.md).

## ASCII / table recall

| Primitive | Reusable? | Typical use |
| --- | --- | --- |
| CountDownLatch | No | Wait for N startups |
| CyclicBarrier | Yes | Phase sync fixed team |
| Semaphore | Yes | Limit concurrent downstream |
| Phaser | Yes | Variable workers, phases |

## Scenario bite

Payments or order processing on more than one instance: apply this lesson at the right layer (JVM primitive vs database vs provider), and say the failure mode aloud before naming the API.

## Explain aloud (whiteboard)

1. “Latch = one-time gate; barrier = repeating team sync.”
2. “Semaphore = capacity limiter, not the same as rate per second.”
3. “Phaser when party count changes between phases.”

## JDK and debug clues

- Threads parked on `Semaphore` — check permit leaks (release count > acquire).

## 30-second revision

- Latch once; barrier phases; semaphore permits; phaser dynamic; release only after acquire.

## Memory hooks

- **LBSP** — **L**atch, **B**arrier, **S**emaphore, **P**haser.

## Cross-links

- [Companion 17 — Producer–consumer](17-producer-consumer-patterns.md)
- [Companion 22 — Rate vs concurrency](22-backend-concurrency-scenarios.md)
