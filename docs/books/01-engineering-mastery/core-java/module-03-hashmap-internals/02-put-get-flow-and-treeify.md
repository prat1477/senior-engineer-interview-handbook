---
title: "Lesson 2 — put(), get(), Collisions, and Tree Bins"
description: OpenJDK insertion/lookup path, linked lists, treeification thresholds.
status: covered
audience: practitioner
tags: [java, hashmap, module-3, lesson-2]
created: 2026-10-20
updated: 2026-10-20
---

# Lesson 2 — `put()`, `get()`, Collisions, and Tree Bins

## Overview

Walkthrough of OpenJDK `HashMap` **put** and **get** at a level suitable for senior interviews. Constants and treeification rules are **JDK implementation** (typically Java 8+); they are not part of the `Map` interface contract.

## OpenJDK constants (implementation)

| Constant | Typical value | Role |
| --- | ---: | --- |
| `TREEIFY_THRESHOLD` | 8 | When a **single bucket** chain length reaches this on put, treeify may occur |
| `UNTREEIFY_THRESHOLD` | 6 | Tree may convert back to linked list on remove/resize |
| `MIN_TREEIFY_CAPACITY` | 64 | Table must be at least this capacity before treeifying a bucket |

**Qualification:** treeification is not “every bucket with 8 entries becomes a tree immediately.” It depends on bucket chain length, table capacity, and the code path (insert vs resize). During resize, chains may be split without hitting treeify on small tables.

## `put(key, value)` — logical flow

1. If `table` is null or too small, **initialize or resize** (lazy allocation).
2. Compute **spread hash** from `key.hashCode()`.
3. Compute **bucket index**.
4. If bucket empty → insert new node.
5. Else walk bucket:
   - If same key (`hash` match and `key.equals`) → **replace value**, return old value; **size unchanged**.
   - Else collision → append to list or insert into tree bin.
6. If chain length triggers treeify **and** `capacity >= MIN_TREEIFY_CAPACITY` → convert bucket to **red-black tree** (implementation detail).
7. If `size > threshold` → **resize** (see Lesson 3).

## `get(key)` — logical flow

1. If `table` null → return `null`.
2. Compute spread hash and index.
3. Inspect first node in bucket:
   - Match `hash` and `equals` → return value.
4. If tree bin → **tree search** (comparison by hash then `equals` / `Comparable` if applicable — see JDK source for tie-breaking).
5. Else walk **linked list** in bucket.
6. No match → `null` (or absent key; distinguish mapped `null` with `containsKey`).

## Collisions and linked lists

Unequal keys may share index and even hash code. List traversal is **O(chain length)** for that bucket.

## Tree bins and complexity

When a bucket treeifies, worst-case lookup in that bucket becomes **O(log n)** in the number of nodes **in that bucket** — not O(log N) for the whole map. Global worst case remains **O(n)** if all keys land in one bucket (broken hash/equality).

Do **not** claim “HashMap is always O(log n)” after treeify.

## Hands-on — replace vs new key

```java
Map<String, Integer> m = new HashMap<>();
m.put("a", 1);
m.put("a", 2); // replace — size still 1
System.out.println(m.size()); // 1
```

## Key takeaways

- `put` replaces value for equal key without increasing `size`.
- Collisions → list; long chains may treeify if capacity ≥ 64 and chain ≥ 8 (OpenJDK).
- `get` checks hash then `equals`; may walk list or tree.

## See also

- [Lesson 3 — Resize and threshold](03-resize-load-factor-and-threshold.md)
