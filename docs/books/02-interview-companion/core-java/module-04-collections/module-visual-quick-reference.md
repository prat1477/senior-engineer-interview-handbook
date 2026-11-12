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

## Comparator recall

```java
employees.stream()
    .sorted(Comparator.comparingInt(Employee::salary)
        .reversed()
        .thenComparing(Employee::name))
    .toList();
```

| Concept | Interview line |
| --- | --- |
| `Comparable` | One natural order, declared by the type via `compareTo`. |
| `Comparator` | External, use-case-specific order via `compare`. |
| `List.sort()` | Mutates the existing list. |
| `Stream.sorted()` | Returns a stream; add a terminal operation. |
| Reversal trap | Reverse salary before `thenComparing`; otherwise both criteria reverse. |

**Memory trick:** **Natural = Comparable; custom = Comparator.**

## Lessons

| # | Page |
| --- | --- |
| 1–13 | Companion files in this folder |
