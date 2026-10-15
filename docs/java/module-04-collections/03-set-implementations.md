---
title: "Lesson 3 — Set Implementations"
description: HashSet, LinkedHashSet, TreeSet, equality, and comparator membership traps.
status: draft
audience: advanced
tags: [collections, set, module-4, lesson-3]
created: 2026-10-15
updated: 2026-10-15
---

# Lesson 3 — Set Implementations

A `Set` models **mathematical sets**: no duplicate elements. Uniqueness is defined by **`equals()`** (hash-based sets) or by **comparison order** (sorted sets).

## 1. Set vs List

| | `List` | `Set` |
| --- | --- | --- |
| Duplicates | Yes | No |
| Order | Insertion/index | Implementation-dependent |
| `get(index)` | Yes | No |

## 2. Implementations compared

| Implementation | Ordering | `add` / `contains` (typical) |
| --- | --- | --- |
| `HashSet` | No guaranteed iteration order | O(1) average |
| `LinkedHashSet` | Insertion order | O(1) average |
| `TreeSet` | Sorted (red-black tree) | O(log n) |

## 3. `hashCode()` and `equals()`

For `HashSet` / `LinkedHashSet`:

- If `a.equals(b)`, then `a.hashCode() == b.hashCode()` (**required**).
- Buckets use `hashCode`; collisions resolved with `equals`.
- Broken contract → duplicates or lost elements.

## 4. `TreeSet` and comparators

Natural order: elements implement `Comparable`.  
Custom order: `Comparator` at construction.

**Critical:** In `TreeSet`, **comparator compare result 0 means "equal for set membership"** — only one such element is stored, even if `equals()` would distinguish them.

```java
record Employee(long id, String name, double salary) {
    long getId() { return id; }
    String getName() { return name; }
    double getSalary() { return salary; }
}

Set<Employee> bySalary = new TreeSet<>(
    Comparator.comparingDouble(Employee::getSalary)
);

bySalary.add(new Employee(1, "Amit", 80_000));
bySalary.add(new Employee(2, "Priya", 80_000)); // compare → 0 → NOT added
bySalary.add(new Employee(3, "Rahul", 90_000));
// Set size 2: Amit (or Priya — first wins), Rahul
```

Amit and Priya share salary → comparator returns 0 → **equivalent keys** in the tree → one employee dropped.

**Fix — tie-breaker:**

```java
Comparator<Employee> bySalaryThenId =
    Comparator.comparingDouble(Employee::getSalary)
              .thenComparing(Employee::getId);
```

**Best practice:** comparator consistent with `equals()` when possible (`compare(a,b)==0` iff `a.equals(b)`).

## 5. When to use which

- **`HashSet`** — fastest average membership; order irrelevant.
- **`LinkedHashSet`** — dedupe while preserving insertion order (e.g. "seen" order for UI).
- **`TreeSet`** — range queries, `subSet`, sorted iteration — pay log factor.

## Revision notes

- Sets enforce uniqueness; mechanism depends on implementation.
- `TreeSet` membership follows **comparator**, not only `equals()`.
- Always tie-break comparators on business keys (ID) when sorting on non-unique fields.

## See also

- [Comparable and Comparator](06-comparable-and-comparator.md)
- [Map fundamentals](04-map-fundamentals-and-hashmap.md)
