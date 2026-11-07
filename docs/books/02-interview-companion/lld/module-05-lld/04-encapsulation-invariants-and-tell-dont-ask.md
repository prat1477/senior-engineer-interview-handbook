---
title: "Companion 4 — Encapsulation and Invariants"
description: Interview recall for tryOccupy, release by allocation id, and failure cases.
status: covered
audience: advanced
tags: [interview, companion, lld, lesson-4]
updated: 2026-10-31
---

# Companion 4 — Encapsulation and Invariants

**Canonical source:** [Mastery Lesson 4](../../../01-engineering-mastery/lld/module-05-lld/04-encapsulation-invariants-and-tell-dont-ask.md).

## Must remember

- `tryOccupy()` → allocation id or empty. Id is **this claim**, not the vehicle for life.
- `isOccupied()` is a read. Do not claim with a setter.
- `release(id)` only if it is the current allocation.
- Session create fails → release **that** id.
- Payment fails → stay occupied, same fee.
- Stale cleanup from A must not free B.

```mermaid
stateDiagram-v2
  [*] --> Available
  Available --> Occupied: tryOccupy
  Occupied --> Available: release matching id
```

```mermaid
sequenceDiagram
  participant A
  participant Spot
  participant B
  A->>Spot: tryOccupy idA
  A->>Spot: release idA
  B->>Spot: tryOccupy idB
  A->>Spot: release idA
  Note over Spot: still idB
```

## Explain aloud

1. “Tell the spot to occupy; don’t set flags.”
2. “Empty optional means try the next spot.”
3. “Release checks ownership so a late cleanup is harmless.”

## Practice

1. Why does check-then-set fail?
2. What do you do if the session insert fails?
3. Why is a declined card not a release?
