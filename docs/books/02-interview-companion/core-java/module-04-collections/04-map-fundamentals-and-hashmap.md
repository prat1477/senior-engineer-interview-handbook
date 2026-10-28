---
title: "Companion 4 — Map Fundamentals and HashMap Internals"
description: "Interview companion for Key uniqueness, hashing, collisions, nulls, and mutable key hazards."
status: covered
audience: advanced
tags: [interview, companion, module-4, java]
created: 2026-10-18
updated: 2026-10-18
---

# Companion 4 — Map Fundamentals and HashMap Internals

**Canonical source:** [Lesson 4 — Map Fundamentals and HashMap Internals](../../../01-engineering-mastery/core-java/module-04-collections/04-map-fundamentals-and-hashmap.md).

## Definition

Key uniqueness, hashing, collisions, nulls, and mutable key hazards.

## Why it exists

Backend services need predictable in-memory data semantics; this topic encodes the contract
and the trade-offs senior engineers defend in design reviews.

## Must remember

- Program to interfaces; justify implementations with complexity, ordering, and thread-safety.
- `Employee` / `Order` / `Payment` examples tie this lesson to payroll and commerce flows.

## Interview traps

- | "`get` null always means missing" | Could be mapped `null` |
- | "Hash code uniqueness" | Hash codes need not be unique; equality decides |
- | "TreeMap sorts by value" | Sorts by **key** ordering |

## Frequently asked questions

- **Q:** What JDK version do examples target?
  **A:** JDK 17+ OpenJDK unless the mastery lesson states otherwise.
- **Q:** Where is the full depth?
  **A:** The [Mastery lesson](../../../01-engineering-mastery/core-java/module-04-collections/04-map-fundamentals-and-hashmap.md) is canonical.

## JDK and debug clues

- Stack traces mentioning this lesson's types (`java.util.*`, `java.lang.*`) — map frame to contract violation.
- Enable `-XX:+HeapDumpOnOutOfMemoryError` when symptoms involve unbounded structures from this module.

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
