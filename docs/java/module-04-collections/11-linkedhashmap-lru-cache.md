---
title: "Lesson 11 — LinkedHashMap Access Order and LRU Caching"
description: accessOrder constructor, get() reordering, and removeEldestEntry patterns.
status: draft
audience: advanced
tags: [collections, linkedhashmap, lru, module-4, lesson-11]
created: 2026-10-15
updated: 2026-10-15
---

# Lesson 11 — LinkedHashMap Access Order and LRU Caching

`LinkedHashMap` extends `HashMap` with a **doubly linked list** through entries to maintain order — either **insertion order** (default) or **access order** for LRU-style caches.

## 1. Enabling access order

```java
LinkedHashMap<Integer, String> products =
    new LinkedHashMap<>(16, 0.75f, true);
//                                      ^^^^ accessOrder = true
```

Default constructor `accessOrder = false` → iteration follows **insertion** order.

## 2. Why `get()` changes order

In access-order mode, **`get(key)`** moves the entry to the **tail** (most recently used). Iteration from head → LRU to MRU.

**Example** (keys): initial insertion `P101`, `P205`, `P310`:

- Order: `P101 → P205 → P310`
- After `get(101)`: `P205 → P310 → P101`

## 3. Bounded cache with `removeEldestEntry`

```java
class RecentProducts extends LinkedHashMap<Integer, String> {

    RecentProducts() {
        super(16, 0.75f, true);
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer, String> eldest) {
        return size() > 100;
    }
}
```

After `put` that exceeds capacity, eldest (LRU head) is removed.

## 4. Capacity-three LRU walkthrough

Access-order list (LRU → MRU):

| Step | Action | Order (LRU → MRU) |
| --- | --- | --- |
| Start | Insert A, B, C | A → B → C |
| Access A | `get(A)` | B → C → A |
| Insert D | `put(D)` | B → C → A → D then evict eldest if over capacity |
| Evict | size > 3, remove eldest B | C → A → D |

## 5. Limitations

- **Not thread-safe** — synchronize externally or use `Collections.synchronizedMap` and sync on wrapper during iteration (per JDK docs).
- **Access order mutates on `get`** — surprising if code assumes stable iteration.
- Multi-step cache logic may need **atomic** compound operations under concurrency.
- High-scale production caches often use dedicated libraries — `LinkedHashMap` is the JDK teaching pattern.

## Revision notes

- Third constructor arg `accessOrder`.
- LRU = evict from head in access-order map.
- `removeEldestEntry` hook after insert.

## See also

- [HashMap vs LinkedHashMap vs TreeMap](05-hashmap-linkedhashmap-treemap.md)
