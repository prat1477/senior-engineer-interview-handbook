---
title: Streams — Visual Quick Reference
description: Pipeline, collectors, and parallel pitfalls.
status: covered
audience: advanced
tags: [companion, streams, cheat-sheet]
updated: 2026-10-28
---

# Streams — Visual Quick Reference

```mermaid
flowchart LR
  src[Source] --> lazy[filter map flatMap]
  lazy --> term[terminal collect]
  par[parallel] --> pool[Common ForkJoinPool]
```

| Pitfall | Fix |
| --- | --- |
| Assume map runs immediately | Need a terminal op |
| `toMap` duplicate keys | Merge function |
| Blocking work in `parallel()` | Own pool or virtual threads |

- [01 pipeline](01-stream-pipeline-fundamentals.md)
- [02 collectors](02-aggregation-collectors.md)
- [03 short-circuit](03-search-short-circuit-primitives.md)
- [04 parallel](04-correctness-parallel-performance.md)
