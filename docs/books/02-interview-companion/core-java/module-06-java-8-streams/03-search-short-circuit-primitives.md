---
title: "Companion 3 — Search and primitives"
description: Interview recall for Search and primitives.
status: covered
audience: advanced
tags: [interview, companion, java]
updated: 2026-10-28
---

# Companion 3 — Search and primitives

**Canonical source:** [Mastery lesson](../../../01-engineering-mastery/core-java/module-06-java-8-streams/03-search-short-circuit-primitives.md).

**Cheat sheet:** [Module visual quick reference](module-visual-quick-reference.md).

## Definition

Short-circuit ops stop early; primitive streams avoid boxing on numeric pipelines.

## Must remember

- findFirst, anyMatch, limit short-circuit.
- IntStream for primitive math.
- Boxing in mapToObj costs.
- Order of filter before map can cut work.

## Interview traps

- anyMatch scans everything always — not if it finds a match.

## Interview flow

```mermaid
flowchart LR
  f[filter] --> a[anyMatch stops]

```

## Scenario bite

Stop when any payment is UNKNOWN: anyMatch on status.

## Decision table

| Situation | Prefer |
| --- | --- |
| Exists? | anyMatch |
| First match | findFirst |
| Sum of ints | mapToInt.sum |

## Explain aloud (whiteboard)

1. Short-circuit.
2. Primitive stream.
3. Filter early.

## 30-second revision

- Short-circuit saves work; primitives avoid boxing.

## Memory hook

- **SHORT**.

## Cross-links

- [Module visual quick reference](module-visual-quick-reference.md)
