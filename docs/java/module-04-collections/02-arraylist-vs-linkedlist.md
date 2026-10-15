---
title: "Lesson 2 — ArrayList vs LinkedList"
description: Backing structures, complexity, cache locality, and remove overload pitfalls.
status: draft
audience: advanced
tags: [collections, list, module-4, lesson-2]
created: 2026-10-15
updated: 2026-10-15
---

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

## Revision notes

- Lists: ordered, duplicates OK.
- `ArrayList`: array, O(1) index, amortized append, best iteration.
- `LinkedList`: rarely the right choice vs `ArrayList` / `ArrayDeque`.
- Overloaded `remove` — index vs object.

## See also

- [Collections overview](01-collections-framework-overview.md)
- [Queue and Deque](08-queue-and-deque.md)
