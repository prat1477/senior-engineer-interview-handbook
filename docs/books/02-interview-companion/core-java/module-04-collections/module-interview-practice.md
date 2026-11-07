---
title: "Lesson 14 — Collections Interview Practice"
description: Hierarchy, complexity, equals/hashCode, concurrent and heap scenarios.
status: draft
audience: advanced
tags: [collections, interview, module-4, lesson-14]
created: 2026-10-17
updated: 2026-10-17
---

# Lesson 14 — Collections Interview Practice

Answers: [module-interview-assessment-answers.md](module-interview-assessment-answers.md).

## Conceptual

1. Why does `Map` not extend `Collection`?

2. Does fail-fast iteration make `HashMap` safe for concurrent `put` from two threads? Explain.

3. `Comparable` vs `Comparator` — when is each required for `TreeSet`?

4. What breaks if a mutable key’s `hashCode` changes after `put`?

## Complexity / comparison

5. Average-case `get` for `HashMap` vs `TreeMap`?

6. When prefer `ArrayDeque` over `LinkedList` for queue operations?

7. Why is `PriorityQueue.remove(Object)` costly?

## Code / debugging

8. Two equal keys must have equal hash codes — must two unequal keys have unequal hash codes?

9. Implement LRU with `LinkedHashMap` — which constructor flag matters?

10. **Top-K:** Why does a size-K **min-heap** track the K **largest** values?

## Scenario (senior)

11. Producer-consumer with bounded memory — which queue type and why?

12. `ConcurrentHashMap` — is `if (!map.containsKey(k)) map.put(k, v)` atomic?

13. Choose collection for: (a) sorted range scan on keys, (b) dedupe with insertion order, (c) thread-safe priority scheduling.

## Mini-assessment

| # | Task |
| --- | --- |
| A | Name fail-fast behavior on structural modify during iteration. |
| B | `ArrayList` vs `LinkedList` for random access by index. |
| C | One concurrent queue: unbounded lock-free vs bounded blocking. |
## Whiteboard (use the cheat sheet)

1. Draw the module flowchart from the visual quick reference without notes.
2. Give one production scenario and the decision-table row you would choose.
3. Name one interview trap and the correction.
