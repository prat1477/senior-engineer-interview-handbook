---
title: Interview Quick Reference
description: Condensed recall — grows with studied modules.
status: draft
audience: advanced
tags: [reference, revision]
created: 2026-10-15
updated: 2026-10-18
---

# Interview Quick Reference

Only **Covered** material is summarized here. Full module revision:
[Interview Companion](../books/02-interview-companion/index.md) (Modules 2–9).
Canonical depth: [Engineering Mastery](../books/01-engineering-mastery/index.md).

## equals / hashCode (M2)

| Rule | Recall |
| --- | --- |
| Contract | Reflexive, symmetric, transitive, consistent, non-null |
| E⇒H | `equals` true ⇒ same `hashCode`; not reversible |
| Override | Both together for hash collections |
| Records | All components; shallow immutability — copy mutable lists |

## HashMap internals (M3)

| Idea | Recall |
| --- | --- |
| Index | `(n-1) & (h ^ (h>>>16))` (OpenJDK) |
| Resize | `size > threshold`; default cap 16 → threshold 12 → 13th distinct key |
| Treeify | 8 / 6 / 64 constants; table capacity must be ≥ 64 |
| Concurrency | Not thread-safe; use `CHM.merge` / `LongAdder` |

## Collections (Covered)

| Type | Pick when | Watch out |
| --- | --- | --- |
| `ArrayList` | Default list, indexed access | Middle insert O(n) |
| `HashMap` | Fast key lookup | Immutable keys; `hashCode`+`equals` |
| `LinkedHashMap` access order | LRU cache | Not thread-safe |
| `TreeMap` / `TreeSet` | Sorted keys / range ops | O(log n); comparator tie-break |
| `PriorityQueue` | Next priority element; Top-K with size-K min-heap | `remove(Object)` O(n); iterate ≠ sorted |
| `ArrayBlockingQueue` | Bounded FIFO + backpressure | `put` blocks when full |
| `PriorityBlockingQueue` | Thread-safe priority | Unbounded — no producer backpressure |
| `ConcurrentHashMap` | Concurrent map ops | No nulls; multi-step ops not atomic |

## Generics (Covered)

| Idea | Recall |
| --- | --- |
| Invariance | `List<Integer>` ≠ `List<Number>` |
| PECS | Producer `? extends T`; consumer `? super T` |
| Erasure | No `new T[]`; runtime is raw + casts |
| Raw types | Compile warnings → `ClassCastException` |

## Streams (Covered)

| Idea | Recall |
| --- | --- |
| Execution | Lazy until terminal op |
| `toList()` | Java 16+ unmodifiable |
| `toMap` | Merge function if duplicate keys |
| Parallel | No shared mutable collect; pool overhead |
| Top-K | `O(n log k)` heap vs `O(n log n)` sort |

## Optional (Covered)

| API | Trap |
| --- | --- |
| `of` vs `ofNullable` | `of(null)` → NPE |
| `orElse` vs `orElseGet` | `orElse(expensive())` always runs |
| `map` | Null result → empty |
| Usage | Return types OK; avoid fields/params |

## Exceptions (Covered)

| Idea | Recall |
| --- | --- |
| TWR | Close failures → suppressed on primary |
| Wrapping | Always pass cause |
| Idempotency key | Persist **before** charge; retries safe |
| Limits | Idempotency ≠ cross-system atomicity |

## Complexity cheat sheet (PriorityQueue)

| `peek` | `offer` | `poll` | `remove(obj)` | `contains` |
| ---: | ---: | ---: | ---: | ---: |
| O(1) | O(log n) | O(log n) | O(n) | O(n) |

## One-liners

- **Map ≠ Collection** — parallel hierarchy.
- **Fail-fast ≠ thread-safe** on `HashMap`.
- **Min-heap size K** → K largest elements.
- **Retry policy** → failure type + operation semantics.

## See also

- [Core Java track](../java/index.md)
- [PROGRESS.md](../PROGRESS.md)
