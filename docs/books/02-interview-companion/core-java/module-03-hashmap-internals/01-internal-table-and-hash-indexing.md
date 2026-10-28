---
title: "Companion 1 — Table, Spread Hash, Index"
description: Interview revision for HashMap indexing.
status: covered
audience: advanced
tags: [interview, companion, module-3]
created: 2026-10-20
updated: 2026-10-20
---

# Companion 1 — Table, Spread Hash, Index

**Canonical source:** [Mastery L1](../../../01-engineering-mastery/core-java/module-03-hashmap-internals/01-internal-table-and-hash-indexing.md).

## Definition

OpenJDK `HashMap` maps keys to buckets via spread `hashCode` and bitmask index `(capacity - 1) & hash`.

## Must remember

- **Capacity** = bucket array length (power of 2).
- **Size** = mapping count.
- Spread: `h ^ (h >>> 16)` (implementation).
- Index: `(n - 1) & spread`.

## Interview traps

- Confusing **size** with **capacity** or occupied buckets.
- Treating spread/index formulas as public API guarantees.

## FAQ

- **Q:** How is bucket index calculated?  
  **A:** `(table.length - 1) & spreadHash`, with spread mixing high bits of `hashCode()`.
- **Q:** Why spread bits?  
  **A:** Better distribution when only low bits select buckets.

## 30-second revision

- power-of-two capacity → bitmask index; spread before mask.
