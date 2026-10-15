---
title: "Lesson 5 — HashMap vs LinkedHashMap vs TreeMap"
description: Ordering modes, complexity trade-offs, and when to sort on demand.
status: draft
audience: advanced
tags: [collections, map, module-4, lesson-5]
created: 2026-10-15
updated: 2026-10-15
---

# Lesson 5 — HashMap vs LinkedHashMap vs TreeMap

Choose a map by **lookup frequency**, **iteration order needs**, and **whether sorted structure is worth continuous maintenance**.

## 1. Comparison

| | `HashMap` | `LinkedHashMap` | `TreeMap` |
| --- | --- | --- | --- |
| Key order (iteration) | Not guaranteed | Insertion or **access** order | Sorted by key |
| `get` / `put` typical | O(1) avg | O(1) avg | O(log n) |
| Extra memory | Baseline | Doubly-linked entries | Tree structure |
| Null keys | One null key allowed | Same | No null keys (natural order) |

**`TreeMap` sorts by key**, not by value. Salary-ranked employees require sorting **values** or entries explicitly:

```java
employees.values().stream()
    .sorted(Comparator.comparingDouble(Employee::getSalary))
    .forEach(System.out::println);
```

## 2. Selection scenarios

1. **Frequent lookup by employee ID; salary report once nightly**  
   → `HashMap<Long, Employee>` for O(1) lookups; build sorted report by copying values and sorting — **O(n log n)** once per night beats maintaining `TreeMap` if sorted traversal is rare.

2. **Frequent lookup + frequent ascending ID traversal**  
   → `TreeMap<Long, Employee>` or `HashMap` + separate sorted index — second structure adds **consistency cost** on every update.

3. **Unique elements in sorted order**  
   → `TreeSet` (not a map) or `TreeMap` keyed by sort key.

4. **Bounded recent-products cache, fast lookup by product ID**  
   → Access-order `LinkedHashMap` + `removeEldestEntry` (see [Lesson 11](11-linkedhashmap-lru-cache.md)).

## 3. One million employees design

| Requirement | Structure |
| --- | --- |
| Hot path: `get(id)` | `HashMap` |
| Nightly salary report | Sort snapshot of values or stream to report DB |
| Hot path: salary-ordered iteration all day | Consider `TreeMap` keyed by salary (only if salary is key — unusual) or secondary index + sync on write |

Maintaining **HashMap + TreeMap** on every salary change is O(log n) per update vs O(1) for map alone — justified only if sorted traversal is as hot as lookup.

## Revision notes

- Continuous sorted index vs sort-on-demand = **update cost vs read pattern**.
- `TreeMap` ≠ sort by value.

## See also

- [LinkedHashMap LRU](11-linkedhashmap-lru-cache.md)
- [Selecting collections](13-selecting-the-right-collection.md)
