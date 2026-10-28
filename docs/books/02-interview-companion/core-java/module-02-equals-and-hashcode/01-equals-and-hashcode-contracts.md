---
title: "Companion 1 — equals() and hashCode() Contracts"
description: Interview revision for equality contracts and hashing.
status: covered
audience: advanced
tags: [interview, companion, module-2]
created: 2026-10-20
updated: 2026-10-20
---

# Companion 1 — `equals()` and `hashCode()` Contracts

**Canonical source:** [Mastery L1](../../../01-engineering-mastery/core-java/module-02-equals-and-hashcode/01-equals-and-hashcode-contracts.md).

## Definition

`equals` defines logical sameness; `hashCode` supports hash buckets. If `a.equals(b)`, then `a.hashCode() == b.hashCode()`.

## Why it exists

Hash maps and sets must place equal keys in the same bucket and find them with `equals` after hashing.

## Must remember

- `==` is identity; `equals` is value semantics (when overridden).
- Five properties: reflexive, symmetric, transitive, consistent, non-null.
- Override **both** `equals` and `hashCode` for value types used in hash collections.
- Equal hash codes **do not** imply equal objects.
- Mutable key fields → broken lookups after mutation.

## Interview traps

- "`get` null means missing" — mapped `null` possible; use `containsKey`.
- "Unequal objects must have different hash codes" — **false** (collisions).
- "Only override `equals`" — breaks `HashMap`/`HashSet`.

## Frequently asked questions

- **Q:** What is the contract of `equals()`?  
  **A:** Reflexive, symmetric, transitive, consistent, and `false` for `null`.
- **Q:** Why must equal objects have equal hash codes?  
  **A:** So hash-based structures store and retrieve them in the same bucket.
- **Q:** What if `equals` is overridden but not `hashCode`?  
  **A:** Equal logical keys can land in different buckets; `get`/`Set` behavior breaks.

## JDK and debug clues

- `ClassCastException` rarely from equality itself; look for raw types in collections.
- Unit tests: assert symmetry with swapped operands.

## Performance notes

- Keep `hashCode` cheap; cache if needed (`String` does).

## Production notes

- Use immutable keys (`Long`, `String`, records with final components).

## Staff engineer notes

- Equality fields are a **product** decision (id vs id+version).

## 30-second revision

- `equals` contract ×5; `equals` ⇒ same `hashCode`; collisions OK; never mutable map keys.

## ASCII diagram

```text
key --> hashCode() --> bucket index
              \--> equals() resolves chain/tree in bucket
```

## Memory hooks

- **E⇒H** — Equal objects, equal hash codes (not the reverse).
