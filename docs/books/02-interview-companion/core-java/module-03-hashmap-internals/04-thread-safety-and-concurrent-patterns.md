---
title: "Companion 4 — Concurrency and Performance"
description: Interview revision for HashMap thread safety and CHM patterns.
status: covered
audience: advanced
tags: [interview, companion, module-3]
created: 2026-10-20
updated: 2026-10-20
---

# Companion 4 — Concurrency and Performance

**Canonical source:** [Mastery L4](../../../01-engineering-mastery/core-java/module-03-hashmap-internals/04-thread-safety-and-concurrent-patterns.md).

## Must remember

- Average O(1) `get`/`put`; worst case can be O(n) or long chains.
- `HashMap` not thread-safe; compound get+put not atomic.
- `ConcurrentHashMap.merge` / `computeIfAbsent` for single-key atomicity.
- `LongAdder` in CHM for hot per-key counters.
- CHM ≠ multi-key transactions.

## FAQ

- **Q:** Why is `HashMap` not thread-safe?  
  **A:** Concurrent structural mutation without synchronization can corrupt table or lose updates.
- **Q:** Fix `map.put(k, map.get(k)+1)`?  
  **A:** `merge`, `AtomicInteger`, or `LongAdder` patterns on `ConcurrentHashMap`.

## 30-second revision

- plain HashMap + races = lost updates; use CHM atomic single-key ops.
