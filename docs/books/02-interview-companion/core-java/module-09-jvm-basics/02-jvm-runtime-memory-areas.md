---
title: "Companion 2 — JVM Runtime Memory Areas"
description: "Interview companion for Heap, stacks, method area, Metaspace, PC registers, native stacks, OOM vs SOE."
status: covered
audience: advanced
tags: [interview, companion, module-9, java]
created: 2026-10-18
updated: 2026-10-18
---

# Companion 2 — JVM Runtime Memory Areas

**Canonical source:** [Lesson 2 — JVM Runtime Memory Areas](../../../01-engineering-mastery/core-java/module-09-jvm-basics/02-jvm-runtime-memory-areas.md).

## Definition

Heap, stacks, method area, Metaspace, PC registers, native stacks, OOM vs SOE.

## Why it exists

Backend services need predictable in-memory data semantics; this topic encodes the contract
and the trade-offs senior engineers defend in design reviews.

## Must remember

- Program to interfaces; justify implementations with complexity, ordering, and thread-safety.
- `Employee` / `Order` / `Payment` examples tie this lesson to payroll and commerce flows.

## Interview traps

- | "All variables live on the heap" | Locals and parameters live in **stack frames**; objects live on heap |
- | "Static fields are on the stack" | Static fields are associated with the class (method area / Metaspace + heap objects they reference) |
- | "Heap OOM means buy more RAM" | Classify OOM type and **retention** first |

## Frequently asked questions

- **Q:** What JDK version do examples target?
  **A:** JDK 17+ OpenJDK unless the mastery lesson states otherwise.
- **Q:** Where is the full depth?
  **A:** The [Mastery lesson](../../../01-engineering-mastery/core-java/module-09-jvm-basics/02-jvm-runtime-memory-areas.md) is canonical.

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
