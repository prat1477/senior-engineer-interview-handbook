---
title: "Lesson 20 — Advanced Concurrency"
description: Ring buffer, false sharing, cache-line bouncing, Disruptor vs queues.
status: covered
audience: advanced
tags: [concurrency, lesson-20]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 20 — Advanced Concurrency

Low-latency patterns — **not** default replacements for `BlockingQueue` or Kafka.

## A. Ring buffer pattern

Fixed-capacity array; producer/consumer indices wrap with sequence numbers.

```text
slots[0..N-1]  producerSeq --> claim slot
                 consumerSeq --> process & advance
```

**Not automatically thread-safe** — requires memory barriers, single-writer rules, or external synchronization. Overwrite without coordination = data loss.

**Trade-offs:** low allocation, cache-friendly; complex correctness.

## B. False sharing

Independent variables on same **cache line** (~64 bytes typical on x86 — **architecture-dependent**) cause coherence traffic when cores update different fields — **performance** issue, not necessarily a Java data race.

## C. Cache-line bouncing

True sharing: threads fight for ownership of one hot variable — repeated invalidate/miss.

## D. Padding and `@Contended`

`@jdk.internal.vm.annotation.Contended` (internal) / `sun.misc.Contended` patterns in JDK for known hotspots — **not** a general app annotation in all JDKs. Manual padding with `long` fields is fragile (JVM layout, object headers). **Benchmark** before relying on padding.

## E. LMAX Disruptor

Framework: ring buffer + sequence barriers + event processors; dependency graphs between handlers; wait strategies (busy-spin vs block).

| | Disruptor | BlockingQueue | Kafka |
| --- | --- | --- | --- |
| Scope | In-process JVM | In-process | Distributed log |
| Durability | Process memory | Process memory | Persistent/replicated |
| Complexity | High | Moderate | Ops + protocol |

Use when microsecond-level latency and allocation control justify engineering cost — payments hot paths, matching engines — not typical CRUD services.

## 10+ YOE pitch

“Ring buffer is a coordination/storage pattern; Disruptor is a framework implementing it; Kafka is cross-service streaming. I’d default to queues and only escalate after measured contention on the hot path.”

## Cross-links

- [Lesson 17 — Producer–consumer](17-producer-consumer-patterns.md)
