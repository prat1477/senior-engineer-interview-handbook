---
title: "Companion 9 — OOM case study"
description: Interview recall for OOM case study.
status: covered
audience: advanced
tags: [interview, companion, java]
updated: 2026-10-28
---

# Companion 9 — OOM case study

**Canonical source:** [Mastery lesson](../../../01-engineering-mastery/core-java/module-09-jvm-basics/09-production-oom-case-study-spark-sql-optimizer.md).

**Cheat sheet:** [Module visual quick reference](module-visual-quick-reference.md).

## Definition

Large query plans can exhaust memory during optimization — a production pattern of unbounded in-memory structures.

## Must remember

- Symptom, evidence, cause, fix.
- Bound plan complexity or memory.
- Don't only raise heap.
- Separate this story from generic leaks.

## Interview traps

- The only fix is a bigger cluster.

## Interview flow

```mermaid
flowchart LR
  query[Huge SQL] --> opt[Optimizer structures]
  opt --> oom[Heap OOM]

```

## Scenario bite

A generated query with huge IN lists builds a giant plan; bound inputs and simplify SQL.

## Decision table

| Situation | Prefer |
| --- | --- |
| Unbounded structure | Cap input |
| Need capacity | Size after the cap |

## Explain aloud (whiteboard)

1. Tell symptom then cause.
2. Bound the input.
3. Heap increase is secondary.

## 30-second revision

- OOM case studies need a retainer and a bound.

## Memory hook

- **CAP** — Cap the input.

## Cross-links

- [Module visual quick reference](module-visual-quick-reference.md)
