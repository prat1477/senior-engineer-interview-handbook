---
title: Interview Quick Reference
description: Condensed recall — grows with studied modules.
status: draft
audience: advanced
tags: [reference, revision]
created: 2026-10-15
updated: 2026-10-15
---

# Interview Quick Reference

Only **Covered** material is summarized here. Expand after Generics, Streams, and other modules.

## Collections (Covered)

| Type | Pick when | Watch out |
| --- | --- | --- |
| `ArrayList` | Default list, indexed access | Middle insert O(n) |
| `HashMap` | Fast key lookup | Immutable keys; `hashCode`+`equals` |
| `LinkedHashMap` access order | LRU cache | Not thread-safe |
| `TreeMap` / `TreeSet` | Sorted keys / range ops | O(log n); comparator tie-break |
| `PriorityQueue` | Next priority element | `remove(Object)` O(n); iterate ≠ sorted |
| `ArrayBlockingQueue` | Bounded FIFO + backpressure | `put` blocks when full |
| `PriorityBlockingQueue` | Thread-safe priority | Unbounded — no producer backpressure |
| `ConcurrentHashMap` | Concurrent map ops | No nulls; multi-step ops not atomic |

## Complexity cheat sheet (PriorityQueue)

| `peek` | `offer` | `poll` | `remove(obj)` | `contains` |
| ---: | ---: | ---: | ---: | ---: |
| O(1) | O(log n) | O(log n) | O(n) | O(n) |

## One-liners

- **Map ≠ Collection** — parallel hierarchy.
- **Sort values on demand** vs **TreeMap** — nightly report vs continuous sorted index.
- **PQ + HashMap** — fast poll + metadata; cancel by ID is still hard without extra design.

## See also

- [Module 4 lessons](../java/module-04-collections/index.md)
- [PROGRESS.md](../../PROGRESS.md)
