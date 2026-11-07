---
title: equals and hashCode — Visual Quick Reference
description: Contract and inheritance cheat sheet.
status: covered
audience: advanced
tags: [companion, equals, cheat-sheet]
updated: 2026-10-28
---

# equals / hashCode — Visual Quick Reference

```mermaid
flowchart TD
  eq[equals true] --> same[hashCode must match]
  sub[Subclass extra fields] --> sym[Can break symmetry]
```

| Rule | Line |
| --- | --- |
| Contract | reflexive, symmetric, transitive, consistent |
| Hash | equal ⇒ same hash; unequal may collide |
| Inheritance | prefer composition; records for component equality |

- [01 contracts](01-equals-and-hashcode-contracts.md)
- [02 inheritance and records](02-inheritance-records-and-equality.md)
