---
title: "Lesson 6 — Comparable and Comparator"
description: Natural vs custom order, multi-field comparators, and sorted collections.
status: draft
audience: advanced
tags: [collections, comparator, module-4, lesson-6]
created: 2026-10-15
updated: 2026-10-15
---

# Lesson 6 — Comparable and Comparator

Ordering appears in `Collections.sort`, `TreeSet`, `TreeMap`, and `PriorityQueue`. Two mechanisms: **intrinsic** (`Comparable`) and **external** (`Comparator`).

## 1. `Comparable<T>` — natural ordering

```java
public class Employee implements Comparable<Employee> {
    private final long id;
    private final String name;
    private final double salary;

    @Override
    public int compareTo(Employee other) {
        return Long.compare(this.id, other.id);
    }
}
```

- **One** natural order per type.
- Used when the type "has" a default sort (e.g. by ID).

## 2. `Comparator<T>` — custom ordering

```java
Comparator<Employee> byName =
    Comparator.comparing(Employee::getName, String.CASE_INSENSITIVE_ORDER);
```

- Multiple comparators per type.
- Prefer when sort criteria vary by use case (UI vs billing).

## 3. Multi-field and reversed order

```java
List<Employee> employees = loadEmployees();

employees.sort(
    Comparator.comparingDouble(Employee::getSalary)
              .reversed()
              .thenComparing(Employee::getName)
);
```

**Meaning:** higher salary first; for equal salary, **name ascending** (A before Z).

## 4. Sorted sets and maps

- `TreeSet` / `TreeMap` use comparator (or natural order) for **both** sorting **and** key equivalence (compare == 0).
- Tie-break on unique business keys when comparing on non-unique fields ([Lesson 3](03-set-implementations.md)).

## 5. When to use which

| Use `Comparable` | Use `Comparator` |
| --- | --- |
| Single obvious default order | Many sort views |
| Type should always be orderable by ID | Sort by salary for reports only |

## Revision notes

- `compareTo` / `compare` return negative, zero, positive.
- `reversed()` flips primary key; `thenComparing` breaks ties.
- Comparator zero in `TreeSet` ⇒ duplicate for set purposes.

## See also

- [Set implementations](03-set-implementations.md)
- [PriorityQueue](09-priorityqueue-and-heaps.md)
