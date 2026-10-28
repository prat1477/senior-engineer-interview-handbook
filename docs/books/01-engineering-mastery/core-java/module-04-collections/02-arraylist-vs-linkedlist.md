---
title: "Lesson 2 — ArrayList vs LinkedList"
description: "Backing structures, complexity, cache locality, and remove overload pitfalls."
status: covered
audience: practitioner
tags: [[collections, list, module-4, lesson-2], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 2 — List Implementations: ArrayList vs LinkedList

Backing structures, complexity, cache locality, and remove overload pitfalls.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/02-arraylist-vs-linkedlist.md) compresses interview signal without
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

# Lesson 2 — List Implementations: ArrayList vs LinkedList

A `List` is an ordered sequence that **allows duplicates** and **preserves insertion order** (unless you sort in place). For interviews, compare `ArrayList` and `LinkedList` on structure, access, mutation, iteration, and memory — not on myths.

## 1. What a List guarantees

- Positional access via `get(int)`, `set(int, E)`.
- `add(E)` appends; `add(int, E)` inserts at index.
- Duplicates allowed; `null` allowed unless implementation forbids (both allow `null`).

## 2. ArrayList internals

- Backing **object array** + `size`.
- **Growth:** when full, allocate larger array (typically ~1.5×), copy elements — **amortized O(1)** append.
- **Indexed access:** `get(i)` / `set(i)` → **O(1)**.
- **Insert/remove in middle:** shift elements → **O(n)**.
- **Iteration:** sequential memory → excellent **CPU cache locality**.

### Amortized append example

Insert `n` elements into an empty `ArrayList` with geometric resizing:

- Most appends are O(1); occasional resize is O(n) but rare.
- Total copying across resizes is O(n), so **n appends → O(n)** overall → **amortized O(1)** per append.

## 3. LinkedList internals

- Doubly linked **nodes** (prev, next, element).
- **Indexed access:** walk from head or tail → **O(n)**.
- **Insert at known node:** O(1) pointer changes — but `list.add(i, e)` must **find** index `i` first → **O(n)**.
- **Memory:** per-element node overhead (pointers + object headers) → worse than compact array for small elements.
- **Iteration:** pointer chasing → poor cache locality vs array scan.

## 4. Comparison table

| Operation | `ArrayList` | `LinkedList` |
| --- | --- | --- |
| `get(i)` / `set(i)` | O(1) | O(n) |
| `add` at end | O(1) amortized | O(1) if tail reference used |
| `add` at index `i` | O(n) shift | O(n) locate + O(1) link |
| `remove` at index `i` | O(n) shift | O(n) locate + O(1) unlink |
| Iterate all | O(n), cache-friendly | O(n), cache-unfriendly |
| Memory | Lower overhead | Higher per element |

**Production default:** prefer `ArrayList` unless you have a measured need for deque-like ops at both ends *and* avoid random access — even then, often `ArrayDeque` beats `LinkedList`.

## 5. `remove(int)` vs `remove(Object)`

```java
List<Integer> numbers = new ArrayList<>(List.of(10, 20, 30));

numbers.remove(1);                 // index 1 → removes 20 → [10, 30]
numbers.remove(Integer.valueOf(20)); // would remove by value if 20 present
```

For `List<Integer>`, `remove(1)` calls **`remove(int index)`** (primitive `int` → index).  
`remove(Integer.valueOf(20))` calls **`remove(Object o)`** (value equality).

**Trap:** `numbers.remove(1)` removes **index** 1, not value `1`. Autoboxing does not apply when the compiler picks `remove(int)`.

## Common misconceptions

| Myth | Reality |
| --- | --- |
| "LinkedList is always faster for insert" | Locating index dominates for `add(i, …)` |
| "ArrayList insert at end is always O(1)" | Worst single append can be O(n) on resize; amortized O(1) |


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/02-arraylist-vs-linkedlist.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
