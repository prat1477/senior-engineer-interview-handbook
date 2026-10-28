---
title: Mistakes, Misconceptions, and Revision Items
description: Corrections from interactive study — add after each session.
status: draft
audience: advanced
tags: [revision, misconceptions]
created: 2026-10-15
updated: 2026-10-18
---

# Mistakes, Misconceptions, and Revision Items

Log items here when practice reveals gaps. Link to the **Engineering Mastery** lesson that corrects them (canonical depth in [Book 1](../books/01-engineering-mastery/index.md)).

## Collections (from study sessions)

| Misconception | Correction | Lesson |
| --- | --- | --- |
| `List.remove(1)` removes value `1` on `List<Integer>` | It removes **index** 1; use `remove(Integer.valueOf(1))` for value | [L2](../books/01-engineering-mastery/core-java/module-04-collections/02-arraylist-vs-linkedlist.md) |
| Iterating `PriorityQueue` is sorted | Only repeated `poll()` drains in priority order | [L9](../books/01-engineering-mastery/core-java/module-04-collections/09-priorityqueue-and-heaps.md) |
| `TreeSet` uses only `equals()` | Comparator compare `== 0` defines set membership | [L3](../books/01-engineering-mastery/core-java/module-04-collections/03-set-implementations.md) |
| `get()` returning null always means missing key | Mapped null possible — use `containsKey` | [L4](../books/01-engineering-mastery/core-java/module-04-collections/04-map-fundamentals-and-hashmap.md) |
| `PriorityBlockingQueue` capacity limits producers | Logically unbounded — no capacity backpressure | [L10](../books/01-engineering-mastery/core-java/module-04-collections/10-blocking-queues-and-backpressure.md) |
| Fail-fast guarantees thread safety | Fail-fast is best-effort single-threaded detection | [L7](../books/01-engineering-mastery/core-java/module-04-collections/07-iterators-and-modification.md) |
| Concurrency detour during Collections = concurrency module done | JMM/CAS/volatile only **Introduced** | [L12](../books/01-engineering-mastery/core-java/module-04-collections/12-concurrent-collections-overview.md) |

## Personal revision queue

| Topic | Status | Notes |
| --- | --- | --- |
| _Add after practice_ | Needs revision | |
