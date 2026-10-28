---
title: "Companion 8 — Heap Dump Analysis"
description: "Interview companion for Histogram, dominator tree, retained heap, path to GC roots, MAT workflow."
status: covered
audience: advanced
tags: [interview, companion, module-9, java]
created: 2026-10-18
updated: 2026-10-18
---

# Companion 8 — Heap Dump Analysis

**Canonical source:** [Lesson 8 — Heap Dump Analysis](../../../01-engineering-mastery/core-java/module-09-jvm-basics/08-heap-dump-analysis.md).

## Definition

Histogram, dominator tree, retained heap, path to GC roots, MAT workflow.

## Why it exists

Backend services need predictable in-memory data semantics; this topic encodes the contract
and the trade-offs senior engineers defend in design reviews.

## Must remember

- Program to interfaces; justify implementations with complexity, ordering, and thread-safety.
- `Employee` / `Order` / `Payment` examples tie this lesson to payroll and commerce flows.

## Interview traps

- | "Retained heap = shallow size" | Retained includes dominated subgraph |
- | "One dump proves leak" | Need trend or reproducible growth |
- | "Dominator = guilty" | Must confirm with roots + code paths |

## Frequently asked questions

- **Q:** What JDK version do examples target?
  **A:** JDK 17+ OpenJDK unless the mastery lesson states otherwise.
- **Q:** Where is the full depth?
  **A:** The [Mastery lesson](../../../01-engineering-mastery/core-java/module-09-jvm-basics/08-heap-dump-analysis.md) is canonical.

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
