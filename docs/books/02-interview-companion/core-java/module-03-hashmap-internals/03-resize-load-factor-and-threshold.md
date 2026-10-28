---
title: "Companion 3 — Resize and Threshold"
description: Interview revision for load factor and 13th insertion.
status: covered
audience: advanced
tags: [interview, companion, module-3]
created: 2026-10-20
updated: 2026-10-20
---

# Companion 3 — Resize and Threshold

**Canonical source:** [Mastery L3](../../../01-engineering-mastery/core-java/module-03-hashmap-internals/03-resize-load-factor-and-threshold.md).

## Must remember

- Default capacity **16**, load factor **0.75**, threshold **12**.
- **13th distinct** mapping can trigger resize (not bucket 13).
- Threshold uses **size**, not occupied bucket count.
- Collision alone ≠ resize; replace value ≠ size++.

## FAQ

- **Q:** Why 13th insertion resize?  
  **A:** After 12 mappings `size ≤ threshold`; 13th distinct key makes `size > 12`.
- **Q:** What happens on resize?  
  **A:** Capacity doubles; entries reindexed (often same index or + oldCapacity).

## 30-second revision

- resize when size > threshold; threshold = capacity × load factor.
