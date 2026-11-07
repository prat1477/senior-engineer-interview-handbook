---
title: HashMap — Visual Quick Reference
description: Index, resize, treeify, and thread-safety cheat sheet.
status: covered
audience: advanced
tags: [companion, hashmap, cheat-sheet]
updated: 2026-10-28
---

# HashMap — Visual Quick Reference

```mermaid
flowchart LR
  k[key] --> spread[spread hash]
  spread --> idx["index = n-1 and spread"]
  idx --> eq[equals in bin]
  eq --> put[insert or replace]
  put --> thr{size over threshold?}
  thr -->|yes| resize[double table]
```

| Fact | Recall |
| --- | --- |
| Threshold | capacity × load factor (0.75) |
| Treeify | long chain **and** table large enough |
| Same key put | replace value, size unchanged |
| Threads | HashMap unsafe; CHM single-key atomic |

- [01 indexing](01-internal-table-and-hash-indexing.md)
- [02 put get treeify](02-put-get-flow-and-treeify.md)
- [03 resize](03-resize-load-factor-and-threshold.md)
- [04 concurrency](04-thread-safety-and-concurrent-patterns.md)
