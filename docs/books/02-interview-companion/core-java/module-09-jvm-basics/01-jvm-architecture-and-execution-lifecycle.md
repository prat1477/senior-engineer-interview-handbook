---
title: "Companion 1 — JVM Architecture and Java Execution Lifecycle"
description: "Interview companion for Compilation, class loading, linking, initialization, class loaders, interpreter vs JIT."
status: covered
audience: advanced
tags: [interview, companion, module-9, java]
created: 2026-10-18
updated: 2026-10-18
---

# Companion 1 — JVM Architecture and Java Execution Lifecycle

**Canonical source:** [Lesson 1 — JVM Architecture and Java Execution Lifecycle](../../../01-engineering-mastery/core-java/module-09-jvm-basics/01-jvm-architecture-and-execution-lifecycle.md).

## Definition

Compilation, class loading, linking, initialization, class loaders, interpreter vs JIT.

## Why it exists

Backend services need predictable in-memory data semantics; this topic encodes the contract
and the trade-offs senior engineers defend in design reviews.

## Must remember

- Program to interfaces; justify implementations with complexity, ordering, and thread-safety.
- `Employee` / `Order` / `Payment` examples tie this lesson to payroll and commerce flows.

## Interview traps

- | "Bytecode runs directly on the CPU" | JVM interprets or JIT-compiles to native code |
- | "`Class.forName` never runs static blocks" | Default `forName(name)` **initializes** the class |
- | "Failed init is forgotten on next use" | JVM records failed initialization; subsequent uses can fail with `NoClassDefFoundError` |

## Frequently asked questions

- **Q:** What JDK version do examples target?
  **A:** JDK 17+ OpenJDK unless the mastery lesson states otherwise.
- **Q:** Where is the full depth?
  **A:** The [Mastery lesson](../../../01-engineering-mastery/core-java/module-09-jvm-basics/01-jvm-architecture-and-execution-lifecycle.md) is canonical.

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
