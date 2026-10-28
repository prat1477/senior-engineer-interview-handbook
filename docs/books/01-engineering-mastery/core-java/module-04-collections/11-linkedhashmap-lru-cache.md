---
title: "Lesson 11 — LinkedHashMap Access Order and LRU Caching"
description: "accessOrder constructor, get() reordering, and removeEldestEntry patterns."
status: covered
audience: practitioner
tags: [[collections, linkedhashmap, lru, module-4, lesson-11], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 11 — LinkedHashMap Access Order and LRU Caching

accessOrder constructor, get() reordering, and removeEldestEntry patterns.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/11-linkedhashmap-lru-cache.md) compresses interview signal without
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


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/11-linkedhashmap-lru-cache.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
