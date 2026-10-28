---
title: "Lesson 3 — Capacity, Load Factor, Threshold, and Resize"
description: Default 16/0.75, 13th distinct mapping, redistribution on double.
status: covered
audience: practitioner
tags: [java, hashmap, module-3, lesson-3]
created: 2026-10-20
updated: 2026-10-20
---

# Lesson 3 — Capacity, Load Factor, Threshold, and Resize

## Overview

Resize is driven by **mapping count (`size`)** versus **threshold**, not by how many buckets are occupied and not by a collision alone.

## Terminology

| Term | Meaning |
| --- | --- |
| **Capacity** | Length of internal bucket array (`table.length`) |
| **Size** | Number of key-value mappings |
| **Load factor** | Sizing factor (default **0.75f**) |
| **Threshold** | `capacity * loadFactor` (integer math in OpenJDK) — resize when `size > threshold` after insert |

## Defaults (OpenJDK `HashMap`)

- Default initial capacity: **16** buckets (after first allocation).
- Default load factor: **0.75**.
- Initial threshold: `16 * 0.75 = 12`.

## The 13th distinct insertion

On the normal insertion path, adding a **13th distinct key** when capacity is 16 and load factor 0.75:

- After 12 distinct puts, `size == 12`, `size > threshold` is false (12 > 12 is false).
- 13th distinct put increases `size` to 13; then `size > threshold` (13 > 12) → **resize** before or as part of growth logic.

**Clarifications:**

- The **13th mapping** is not bucket index 13.
- **Threshold is not** “number of occupied buckets.”
- A **collision** on put does not by itself increase `size` if the key already exists (value replace).
- **Replacing** a value for an existing key does not increase `size` and does not trigger resize for that reason alone.

## Lazy table allocation

Empty `HashMap` may hold `table == null` until first `put`. First allocation typically uses default capacity 16 (implementation detail).

## Resize behavior

1. New capacity ≈ **double** old capacity (power of two).
2. Recompute threshold for new capacity.
3. **Redistribute** entries into new table.

OpenJDK optimization: when capacity doubles, each entry either **stays at the same index** or moves by **+ oldCapacity** (bit in spread hash determines which). This avoids rehashing from scratch in the general case.

## Why collisions alone do not resize

Resize is tied to **size vs threshold**. Many keys can share a bucket (collisions) while `size` stays below threshold — you get long chains (or tree) instead of immediate resize.

## Performance note

Frequent resize while growing a map copies entries — if you know expected `size`, `new HashMap<>(expectedSize)` reduces resize churn (constructor computes capacity from expected mappings and load factor).

## Key takeaways

- Threshold = capacity × load factor; default threshold 12 at capacity 16.
- 13th **distinct** key triggers resize on default map.
- Size, not occupied bucket count, drives threshold.
- Resize doubles capacity and redistributes entries.

## See also

- [Lesson 4 — Performance and concurrency](04-thread-safety-and-concurrent-patterns.md)
