---
title: "Lesson 4 — Map Fundamentals and HashMap Internals"
description: Key uniqueness, hashing, collisions, nulls, and mutable key hazards.
status: draft
audience: advanced
tags: [collections, map, hashmap, module-4, lesson-4]
created: 2026-10-15
updated: 2026-10-15
---

# Lesson 4 — Map Fundamentals and HashMap Internals

A `Map` associates **unique keys** with values. It is central to employee directories, caches, and indexes — interviews focus on **contract**, **hashing**, and **what breaks in production**.

## 1. Basic behavior

```java
Map<Integer, String> employees = new HashMap<>();

employees.put(101, "Amit");
employees.put(102, "Priya");
employees.put(101, "Rahul");  // same key → replaces value

// Key 101 maps to "Rahul" (not "Amit")
```

- **`put(k, v)`** — insert or **replace** value for key `k`.
- **`get(k)`** — returns value or **`null`** if key absent (for `HashMap`).

```java
employees.get(999); // null — key not present
```

If `null` is a **legal value**, use **`containsKey(999)`** to distinguish missing key from mapped `null`.

## 2. `HashMap` at a high level (OpenJDK)

1. Compute bucket index from `key.hashCode()` (spread / mask).
2. Locate entry in bucket; compare keys with **`equals()`**.
3. **Collisions:** chain entries in bucket; from Java 8+, long chains may **treeify** to tree bins (implementation detail, not API guarantee).
4. **Resize** when load exceeds threshold (default load factor 0.75) — rehash — **amortized** cost.

| Rule | Why |
| --- | --- |
| Equal keys → equal hash codes | Required for correct lookup |
| Unequal keys → may share hash code | Collisions OK; `equals` disambiguates |
| Override `equals` → override `hashCode` compatibly | Or buckets break |

## 3. Mutable keys

If a key field used in `equals`/`hashCode` changes after `put`, the entry may live in the **wrong bucket** — `get` fails silently. **Use immutable keys** (e.g. `Integer`, `String`, record with final id).

## 4. `HashMap` vs `LinkedHashMap` vs `TreeMap` (preview)

| | Iteration order | `get` typical |
| --- | --- | --- |
| `HashMap` | Unpredictable | O(1) avg |
| `LinkedHashMap` | Insertion or access order | O(1) avg |
| `TreeMap` | Sorted by key | O(log n) |

Detail: [Lesson 5](05-hashmap-linkedhashmap-treemap.md).

## 5. Production example

```java
Map<Long, Employee> byId = new HashMap<>();
byId.put(emp.getId(), emp);

Employee found = byId.get(order.getEmployeeId());
if (found == null) {
    // absent OR mapped null — use containsKey if null values allowed
}
```

## Common misconceptions

| Myth | Reality |
| --- | --- |
| "`get` null always means missing" | Could be mapped `null` |
| "Hash code uniqueness" | Hash codes need not be unique; equality decides |
| "TreeMap sorts by value" | Sorts by **key** ordering |

## Revision notes

- Keys unique; repeat `put` replaces value.
- `hashCode` → bucket; `equals` → exact key match.
- Immutable keys; `containsKey` when `null` values exist.

## See also

- [HashMap vs LinkedHashMap vs TreeMap](05-hashmap-linkedhashmap-treemap.md)
- Module 3 (planned): dedicated `HashMap` internals lesson
