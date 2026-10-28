---
title: "Lesson 9 — Concurrent Collections"
description: CHM, queues, atomic single-key ops — deepens Collections L12.
status: covered
audience: advanced
tags: [concurrency, lesson-9]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 9 — Concurrent Collections

Expands [Collections M4 L12](../books/01-engineering-mastery/core-java/module-04-collections/12-concurrent-collections-overview.md).

## `ConcurrentHashMap`

- No null keys/values.
- `putIfAbsent`, `computeIfAbsent`, `merge` — single-key atomicity.
- Weakly consistent iterators.

## Queues

`ConcurrentLinkedQueue`, `ArrayBlockingQueue`, `LinkedBlockingQueue`, `PriorityBlockingQueue` — see Collections lessons 8–10.

## Cross-links

- [M3 — thread safety](../books/01-engineering-mastery/core-java/module-03-hashmap-internals/04-thread-safety-and-concurrent-patterns.md)
- [Lesson 17 — Producer–consumer](17-producer-consumer-patterns.md)
