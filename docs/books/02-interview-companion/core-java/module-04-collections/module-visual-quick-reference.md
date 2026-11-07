---
title: Collections — Visual Quick Reference
description: Last-minute collection picker for interviews.
status: covered
audience: advanced
tags: [companion, collections, cheat-sheet]
updated: 2026-10-28
---

# Collections — Visual Quick Reference

[Module index](index.md). Diagrams render in MkDocs (`mkdocs serve`).

## Picker

```mermaid
flowchart TD
  q{Need}
  q -->|index access| al[ArrayList]
  q -->|unique unordered| hs[HashSet]
  q -->|unique insertion order| lhs[LinkedHashSet]
  q -->|sorted unique| ts[TreeSet]
  q -->|key lookup| hm[HashMap or CHM]
  q -->|LRU| lru[LinkedHashMap access order]
  q -->|FIFO bound| abq[ArrayBlockingQueue]
  q -->|top K| heap[PriorityQueue size K]
```

## Rules to say aloud

| Rule | Line |
| --- | --- |
| LinkedList | Index search is O(n); not the default queue |
| Top-K largest | Size-K **min-heap** |
| Fail-fast | Not a concurrency lock |
| CHM | `merge` / `computeIfAbsent`, not contains+put |
| Queue capacity | Bounds memory, not consumer parallelism |

## Lessons

| # | Page |
| --- | --- |
| 1–13 | Companion files in this folder |
