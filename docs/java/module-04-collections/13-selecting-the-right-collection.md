---
title: "Lesson 13 — Selecting the Right Collection"
description: Decision guide by access pattern, scale, concurrency, and job scheduling.
status: draft
audience: advanced
tags: [collections, design, module-4, lesson-13]
created: 2026-10-15
updated: 2026-10-15
---

# Lesson 13 — Selecting the Right Collection

Senior interviews ask you to **justify** structures against dominant operations, ordering, memory, and concurrency — not to recite class names.

## 1. Quick decision guide

| Need | Often choose |
| --- | --- |
| Fast key lookup; sorted report rare | `HashMap` + sort on demand |
| Fast lookup + frequent sorted key walk | `TreeMap` |
| Fast lookup + LRU / access tracking | Access-order `LinkedHashMap` |
| Unique, unordered | `HashSet` |
| Unique, insertion order | `LinkedHashSet` |
| Unique, sorted | `TreeSet` |
| Next best priority repeatedly | `PriorityQueue` |
| Thread-safe priority + block on empty | `PriorityBlockingQueue` |
| Bounded FIFO producer-consumer | `ArrayBlockingQueue` |
| Stack / deque, single-threaded | `ArrayDeque` |
| Default sequential list | `ArrayList` |

## 2. One million employees

**Pattern A:** ID lookups all day; salary-sorted report nightly.

- `HashMap<Long, Employee>` for hot path.
- Nightly: stream values, sort by salary, export — O(n log n) acceptable once per day.
- Avoid second sorted structure updated on every salary change.

**Pattern B:** ID lookups **and** constant salary-ordered traversal.

- Option 1: `TreeMap` keyed by salary — only if salary is truly the key (duplicate salaries collide — need composite key).
- Option 2: `HashMap` + secondary sorted index — every update maintains both → engineering cost and bug risk.

## 3. Job scheduling and cancellation

| Requirement | Tool | Caveat |
| --- | --- | --- |
| Poll highest priority job | `PriorityQueue` | O(log n) poll |
| Lookup job metadata by ID | `HashMap<ID, Job>` | Does not remove from heap |
| Cancel arbitrary job by ID | `PriorityQueue.remove(job)` | **O(n)** search |
| Fast arbitrary cancel | Indexed priority queue (custom) | Map ID → heap index; complex |

**Practical answer:** PQ + map for metadata; cancellation either marks job cancelled (lazy skip on poll) or pays O(n) remove — state trade-off in design discussion, not a required implementation lesson.

## 4. Dimensions to articulate

- **Dominant operations** — read vs write ratio.
- **Ordering guarantees** — none, insertion, access, sorted.
- **Memory** — linked structures vs arrays; unbounded queues.
- **Concurrency** — single-threaded vs `Concurrent*` vs blocking queues.
- **Update frequency** — cost of maintaining auxiliary indexes.

## Revision notes

- No single "best" collection — match structure to access pattern.
- Sort on demand vs continuous index = classic trade-off.
- PQ + map does not imply O(1) heap removal by ID.

## See also

- [Collections overview](01-collections-framework-overview.md)
- [90-reference interview quick reference](../../90-reference/interview-quick-reference.md)
