---
title: "Lesson 4 — Map Fundamentals and HashMap Internals"
description: "Key uniqueness, hashing, collisions, nulls, and mutable key hazards."
status: covered
audience: practitioner
tags: [[collections, map, hashmap, module-4, lesson-4], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 4 — Map Fundamentals and HashMap Internals

Key uniqueness, hashing, collisions, nulls, and mutable key hazards.

## Shared domain models

Examples across Modules 4–9 reuse the same records so mental models transfer:

```java
public record Employee(long id, String name, String department, double salary) {}
public record Order(long id, long employeeId, String sku, int quantity, double unitPrice) {}
public record Payment(long orderId, String method, double amount, java.time.Instant paidAt) {}
```

Use them for grouping (`Collectors.groupingBy`), maps (`Map<Long, Employee>`), optional chains
(`Optional<Employee>`), and exception boundaries around payment APIs.

## Big picture

Core Java Module 4 — **Collections**. This is the canonical Engineering Mastery
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/04-map-fundamentals-and-hashmap.md) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

## Architecture

This lesson sits in **Module 4** of the Core Java track. Service code should treat
collection/generics/stream/JVM choices as **capacity and correctness** decisions, not style preferences.

## Internal working

Review the numbered sections in **Core concepts (canonical)** below. For interviews, pair each
fact with **complexity**, **ordering**, and **concurrency** implications.

## Hands-on

```java
// Extend the snippet in the canonical section with Employee / Order / Payment records.
// JDK 17+: compile with your module's test source set or `java Main.java`.
```

## Performance

State average vs worst-case costs for the structures or APIs introduced in this lesson.
Call out allocation hot spots (boxing, autoboxing in streams, defensive copies).

## JDK tools and diagnostic clues

- Watch for lesson-specific exceptions in logs (`ConcurrentModificationException`, `ClassCastException`
  at erasure boundaries, `OutOfMemoryError` subtypes for JVM modules).
- Use **async profiler**, **JFR**, or **heap histogram** (`jcmd <pid> GC.class_histogram`) when
  production symptoms match this topic.

## Failure scenarios

Document one production failure mode tied to misuse of this lesson's API, and the guardrail
(service validation, bounded queues, explicit comparators, try-with-resources).

## Best practices and anti-patterns

- Prefer clear types over clever one-liners.
- Make null and empty collection policies explicit at API edges.

> **Production insight**
> Align collection mutability with transaction boundaries — shared mutable structures between
> threads remain the top source of subtle bugs.

## Staff engineer notes

- Teach the **contract** first (what callers may assume), then the **implementation** (how it is enforced).
- Link forward to Module 12 concurrent collections when discussing multi-threaded mutation.

## Core concepts (canonical)

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


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Module 3 — HashMap internals (deepening)](../module-03-hashmap-internals/index.md)
- [Module 2 — equals / hashCode](../module-02-equals-and-hashcode/index.md)
- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/04-map-fundamentals-and-hashmap.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
