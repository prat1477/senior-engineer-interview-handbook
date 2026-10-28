---
title: "Companion 6 — Java Reference Types and Memory Retention"
description: "Interview companion for Strong, soft, weak, phantom, ReferenceQueue, WeakHashMap, caches."
status: covered
audience: advanced
tags: [interview, companion, module-9, java]
created: 2026-10-18
updated: 2026-10-18
---

# Companion 6 — Java Reference Types and Memory Retention

**Canonical source:** [Lesson 6 — Java Reference Types and Memory Retention](../../../01-engineering-mastery/core-java/module-09-jvm-basics/06-java-reference-types-and-memory-retention.md).

## Definition

Strong, soft, weak, phantom, ReferenceQueue, WeakHashMap, caches.

## Why it exists

Backend services need predictable in-memory data semantics; this topic encodes the contract
and the trade-offs senior engineers defend in design reviews.

## Must remember

- Program to interfaces; justify implementations with complexity, ordering, and thread-safety.
- `Employee` / `Order` / `Payment` examples tie this lesson to payroll and commerce flows.

## Interview traps

- | "`WeakHashMap` frees entries automatically" | Values must not strongly retain keys |
- | "`PhantomReference.get()` returns the object" | Always **null** by design |
- | "Soft refs = LRU cache" | No ordering guarantee; pressure-dependent clearing |

## Frequently asked questions

- **Q:** What JDK version do examples target?
  **A:** JDK 17+ OpenJDK unless the mastery lesson states otherwise.
- **Q:** Where is the full depth?
  **A:** The [Mastery lesson](../../../01-engineering-mastery/core-java/module-09-jvm-basics/06-java-reference-types-and-memory-retention.md) is canonical.

## JDK and debug clues

- GC logs (`-Xlog:gc*`) and `jcmd GC.heap_info` for heap pressure.
- Heap dump dominators for `char[]`, `byte[]`, or collection backings tied to retention.

## Performance notes

- Name the dominant operation before naming a concrete class.
- Watch hidden `O(n)` scans (`contains`, `indexOf`) inside loops.

## Production notes

- Bound in-memory maps and caches; log size metrics where feasible.
- Document nullability and ordering guarantees on public APIs.

## Staff engineer notes

- Separate **semantic requirements** (unique keys, sorted traversal) from **favorite classes**.

## 30-second revision

- Read the mastery tables once, then rehearse answering "why this implementation?" aloud.

## Memory hooks

- **LOMS** — **L**ist order, **O**rdering mode, **M**ap vs Collection, **S**election by access pattern.
