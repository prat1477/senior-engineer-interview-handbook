---
title: "Lesson 11 — Thread Pool Sizing and Backpressure"
description: CPU vs I/O bound pools, queue bounds, Little's law intuition.
status: covered
audience: advanced
tags: [concurrency, lesson-11]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 11 — Thread Pool Sizing and Backpressure

## CPU-bound

Pool size ≈ number of cores (or cores − 1) for compute-heavy work — oversubscription adds context switch cost.

## I/O-bound (platform threads)

More threads than cores can help **if** threads block on I/O — bounded by memory and downstream limits. Virtual threads change the trade-off ([Lesson 14](14-virtual-threads.md)).

## Backpressure

Unbounded `LinkedBlockingQueue` → latency grows forever under overload. Prefer bounded queue + measured rejection or caller-runs.

## Little's law (intuition)

`L = λ × W` — average items in system = arrival rate × time in system. Growing queue depth signals need to scale consumers or shed load.

## Cross-links

- [Collections M4 L10 — Blocking queues](../books/01-engineering-mastery/core-java/module-04-collections/10-blocking-queues-and-backpressure.md)
- [Lesson 21 — Debugging saturation](21-production-debugging.md)
