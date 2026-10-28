---
title: "Companion 2 — Inheritance, Records, and Equality"
description: Interview revision for subclass traps and records.
status: covered
audience: advanced
tags: [interview, companion, module-2]
created: 2026-10-20
updated: 2026-10-20
---

# Companion 2 — Inheritance, Records, and Equality

**Canonical source:** [Mastery L2](../../../01-engineering-mastery/core-java/module-02-equals-and-hashcode/02-inheritance-records-and-equality.md).

## Definition

Subclass `equals` can violate symmetry; records generate component-wise equality with **shallow** immutability.

## Must remember

- `ColorPoint` / `Point` breaks symmetry if `equals` uses `instanceof` asymmetrically.
- Prefer composition or `final` classes for value keys.
- Records: all components in `equals`/`hashCode`.
- `List.copyOf` — unmodifiable list, not deep freeze of elements.

## Interview traps

- "Records are always safe as HashMap keys" — only if components are immutable.
- "Inheritance is fine for DTO equality" — often breaks contract.

## Frequently asked questions

- **Q:** How can inheritance violate symmetry?  
  **A:** Parent accepts child type in `equals`; child rejects parent type.
- **Q:** What do records generate?  
  **A:** `equals`/`hashCode`/`toString` from all record components.

## 30-second revision

- Avoid inherited `equals`; defensive-copy mutable record fields; shallow immutability.

## Memory hooks

- **Compose, don't subclass** value equality.
