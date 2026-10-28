---
title: Module 2 — Equality and Map Keys Playbook
description: Operational guidance for equals/hashCode in services.
status: covered
audience: operator
tags: [playbook, module-2]
created: 2026-10-20
updated: 2026-10-20
---

# Module 2 — Equality and Map Keys Playbook

Lightweight companion to [Case 1 in Module 3 playbook](module-03-hashmap-internals-production-playbook.md). Theory: [Mastery Module 2](../../01-engineering-mastery/core-java/module-02-equals-and-hashcode/index.md).

## When to use

- Designing cache keys or in-memory indexes
- Code review flags entity objects used as `HashMap` keys

## Procedure

1. List fields used in `equals`/`hashCode` — must be **immutable** after insert.
2. Prefer `Long`/`String`/record business keys over mutable entities.
3. Add unit tests for symmetry: `a.equals(b)` ⇔ `b.equals(a)`.
4. If using records with collections, **defensive copy** in compact constructor (`List.copyOf`).

## Incident checklist

- [ ] Key type overrides both `equals` and `hashCode`
- [ ] No mutable fields in equality
- [ ] Record components immutable or copied
