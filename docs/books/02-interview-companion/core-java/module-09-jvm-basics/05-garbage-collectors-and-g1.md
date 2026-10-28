---
title: "Companion 5 — Garbage Collectors and G1 GC"
description: "Interview companion for STW pauses, Parallel vs G1 vs ZGC, regions, mixed GC, humongous objects."
status: covered
audience: advanced
tags: [interview, companion, module-9, java]
created: 2026-10-18
updated: 2026-10-18
---

# Companion 5 — Garbage Collectors and G1 GC

**Canonical source:** [Lesson 5 — Garbage Collectors and G1 GC](../../../01-engineering-mastery/core-java/module-09-jvm-basics/05-garbage-collectors-and-g1.md).

## Definition

STW pauses, Parallel vs G1 vs ZGC, regions, mixed GC, humongous objects.

## Why it exists

Backend services need predictable in-memory data semantics; this topic encodes the contract
and the trade-offs senior engineers defend in design reviews.

## Must remember

- Program to interfaces; justify implementations with complexity, ordering, and thread-safety.
- `Employee` / `Order` / `Payment` examples tie this lesson to payroll and commerce flows.

## Interview traps

- | "Switch to ZGC for every service" | Measure pause vs throughput vs JDK support |
- | "G1 never does full GC" | Full GC can still occur under pressure or mis-tuning |
- | "Humongous regions are rare in business apps" | Large `byte[]`, serialized plans, buffers can trigger them |

## Frequently asked questions

- **Q:** What JDK version do examples target?
  **A:** JDK 17+ OpenJDK unless the mastery lesson states otherwise.
- **Q:** Where is the full depth?
  **A:** The [Mastery lesson](../../../01-engineering-mastery/core-java/module-09-jvm-basics/05-garbage-collectors-and-g1.md) is canonical.

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
