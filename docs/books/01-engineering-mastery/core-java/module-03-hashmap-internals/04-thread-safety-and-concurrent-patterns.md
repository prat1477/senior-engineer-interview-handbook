---
title: "Lesson 4 — Performance, Mutable Keys, and Concurrent Alternatives"
description: Lookup cost, bad hashes, HashMap thread safety, CHM.merge, LongAdder.
status: covered
audience: practitioner
tags: [java, hashmap, concurrency, module-3, lesson-4]
created: 2026-10-20
updated: 2026-10-20
---

# Lesson 4 — Performance, Mutable Keys, and Concurrent Alternatives

## Overview

Expected `get`/`put` is **O(1)** average with a good hash spread; worst case **O(n)** (or tree-bound per bucket) under adversarial hashing. Thread safety requires structures beyond unsynchronized `HashMap`.

## Expected and worst-case performance

| Case | Typical |
| --- | --- |
| Average, well-distributed keys | O(1) `get`/`put` |
| All keys in one bucket | O(n) list walk |
| Treeified bucket | O(log k) for k nodes in **that** bucket — not whole map |

Profile before blaming “HashMap is slow.”

## Mutable keys and poor hash functions

- **Mutable keys:** changing fields used in `hashCode`/`equals` after `put` → lost lookups ([Module 2](../module-02-equals-and-hashcode/01-equals-and-hashcode-contracts.md)).
- **Poor hash:** `hashCode()` returning constant → one bucket → degenerate to list/tree.

## `HashMap` thread safety

`HashMap` is **not** thread-safe for concurrent `put`/`remove` from multiple threads. Undefined behavior can include infinite loops (historical) or lost updates. **Fail-fast iterators** do not fix this.

`Collections.synchronizedMap` serializes every operation — simple but coarse.

## Lost update — non-atomic compound operation

```java
map.put(key, map.getOrDefault(key, 0) + 1); // NOT atomic across threads
```

Two threads can read the same value and both write `old+1`.

## `ConcurrentHashMap.merge()` — per-key atomic update

```java
ConcurrentHashMap<String, Long> counts = new ConcurrentHashMap<>();
counts.merge("hits", 1L, Long::sum);
```

`merge` applies an atomic update for **one key** at a time. Still not a multi-key transaction.

## `ConcurrentHashMap` + `LongAdder` for hot counters

```java
ConcurrentHashMap<String, LongAdder> metrics = new ConcurrentHashMap<>();
metrics.computeIfAbsent("requests", k -> new LongAdder()).increment();
```

Useful when per-key increment contention is high; `LongAdder` reduces CAS contention vs repeated `merge` on boxed `Long`.

## Limits

- `ConcurrentHashMap` does not make `if (!map.containsKey(k)) map.put(k, v)` atomic — use `putIfAbsent`, `computeIfAbsent`, or explicit locking.
- Null keys/values are not allowed in `ConcurrentHashMap`.

Deep concurrency: [Concurrency track](../../../../concurrency/index.md). Collections overview: [M4 L12](../module-04-collections/12-concurrent-collections-overview.md).

## Key takeaways

- Average O(1); worst case can be linear; tree bins help **per bucket** only.
- Mutable keys and bad `hashCode` break correctness and performance.
- Plain `HashMap` + compound read-modify-write loses updates under races.
- Use `merge` / `computeIfAbsent` / `LongAdder` patterns for concurrent counters.

## See also

- [Production Playbook](../../../03-production-playbook/core-java/module-03-hashmap-internals-production-playbook.md)
