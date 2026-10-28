---
title: "Companion 2 — put/get and Treeify"
description: Interview revision for HashMap operations and tree bins.
status: covered
audience: advanced
tags: [interview, companion, module-3]
created: 2026-10-20
updated: 2026-10-20
---

# Companion 2 — `put`/`get` and Treeify

**Canonical source:** [Mastery L2](../../../01-engineering-mastery/core-java/module-03-hashmap-internals/02-put-get-flow-and-treeify.md).

## Must remember

- `put`: hash → index → empty slot or match/replace or collision chain/tree.
- Replace existing key → **no size increase**.
- Treeify (OpenJDK): chain ≥ **8**, table capacity ≥ **64** — not instant for every bucket at 8 entries.
- `get`: match hash + `equals`; walk list or tree.
- Iterator order ≠ sorted.

## Interview traps

- "Bucket with 8 entries always becomes tree" — needs capacity ≥ 64 and JDK rules.
- "Treeify makes whole map O(log n)" — per bucket only.

## FAQ

- **Q:** How does `get` locate an entry?  
  **A:** Compute index, compare hash and `equals` on bucket head, else traverse list/tree.
- **Q:** When can a bucket treeify?  
  **A:** Long collision chain on put when table is large enough (see `TREEIFY_THRESHOLD`, `MIN_TREEIFY_CAPACITY`).

## 30-second revision

- put/get = index + equals; treeify is collision mitigation on big tables.
