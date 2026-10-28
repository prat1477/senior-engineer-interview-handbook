---
title: "Lesson 24 — Senior Interview Assessment"
description: Scenario questions across concurrency curriculum with model answers.
status: covered
audience: advanced
tags: [concurrency, lesson-24, assessment]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 24 — Senior Interview Assessment

Attempt without notes, then compare to model reasoning.

## 1. Payment double-submit

Two API instances, two different UUIDs, same user double-clicks Pay. Why does DB unique on `request_id` fail? What do you require instead?

<details>
<summary>Model answer</summary>

Different UUIDs = different rows — not the same logical operation. Require **stable client idempotency key** or **shared payment intent id** reused across submits/retries; unique constraint on that business key; state machine + PSP idempotency.
</details>

## 2. CompletableFuture + JDBC

Team wraps blocking JDBC in `supplyAsync` on common pool. Symptom?

<details>
<summary>Model answer</summary>

Common pool starvation — latency spikes for all parallel streams/CF users. Dedicated blocking pool or virtual threads; keep driver async path light in `thenCompose`.
</details>

## 3. Virtual threads + DB

50-connection pool, 5k virtual threads all query at once. Outcome?

<details>
<summary>Model answer</summary>

Most wait on pool; timeouts if misconfigured; not 5k concurrent queries. Semaphore/bulkhead, timeouts, right-size pool and instances.
</details>

## 4. Kafka vs queue

When is in-memory `BlockingQueue` enough vs Kafka?

<details>
<summary>Model answer</summary>

Queue: single-process decoupling/backpressure. Kafka: durable cross-service log, replay, multiple consumer groups, retention — see [Lesson 17](17-producer-consumer-patterns.md).
</details>

## 5. False sharing

Two atomic counters on same cache line — problem?

<details>
<summary>Model answer</summary>

Performance degradation from cache coherence — not necessarily incorrect results. Padding/`@Contended` (where available), separate objects, benchmark.
</details>

## 6. Thread dump

Many threads `RUNNABLE` in socket read — deadlock?

<details>
<summary>Model answer</summary>

Not necessarily — likely I/O wait or runnable-ready. Check for deadlock section, pool metrics, repeated stacks over multiple dumps.
</details>

## Cross-links

Full curriculum: [index](index.md).
