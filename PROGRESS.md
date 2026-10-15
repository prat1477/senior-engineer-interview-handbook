# Progress Tracker

Update this file after each study session. Status meanings:

| Status | Meaning |
| --- | --- |
| **Covered** | Studied with examples, trade-offs, and follow-up Q&A |
| **In progress** | Partially studied; handbook reflects work so far |
| **Introduced** | High-level exposure only; not interview-ready |
| **Planned** | On the roadmap; no substantive lesson yet |
| **Deferred** | Belongs to a later curriculum (e.g. deep concurrency internals during Collections) |
| **Needs revision** | Studied but you want another pass |

**Last updated:** 2026-10-15  
**Current position:** Core Java — Module 4 Collections (**In progress** — lessons documented; finish any remaining drill before marking Covered)

---

## 14-day roadmap

| Day | Theme | Status |
| --- | --- | --- |
| 1 | Core Java, Collections, HashMap, DSA arrays/hash maps | **Planned** (Collections content **In progress**) |
| 2 | Streams, Optional, JVM basics, two pointers / sliding window | **Planned** |
| 3 | Concurrency foundations (JMM, happens-before, race, `synchronized`) | **Planned** |
| 4 | Advanced concurrency + high-level system design | **Planned** |
| 5 | Spring Boot and backend fundamentals | **Planned** |
| 6 | Microservice reliability | **Planned** |
| 7 | Kafka deep dive | **Planned** |
| 8 | Distributed system design (payments, fraud, idempotency) | **Planned** |
| 9 | Lakehouse and Spark (remaining modules) | **Planned** |
| 10 | Databricks, orchestration, SQL | **Planned** |
| 11 | AWS data platform | **Planned** |
| 12 | Data-platform system design and debugging | **Planned** |
| 13 | Full mock interview | **Planned** |
| 14 | Rapid revision | **Planned** |

---

## Core Java track (fixed order)

| # | Module | Status |
| --- | --- | --- |
| 1 | Java Object Model | **Planned** |
| 2 | `equals()` and `hashCode()` | **Planned** |
| 3 | `HashMap` internals | **Planned** (map behavior also in Collections lessons) |
| 4 | **Collections** | **In progress** → lessons 01–13 documented |
| 5 | Generics | **Planned** |
| 6 | Java 8 Streams | **Planned** |

### Module 4 — Collections lessons

| Lesson | Topic | Status |
| --- | --- | --- |
| 01 | Collections Framework overview | **Covered** |
| 02 | `ArrayList` vs `LinkedList` | **Covered** |
| 03 | Set implementations | **Covered** |
| 04 | Map fundamentals and `HashMap` internals | **Covered** |
| 05 | `HashMap` vs `LinkedHashMap` vs `TreeMap` | **Covered** |
| 06 | `Comparable` and `Comparator` | **Covered** |
| 07 | Iterators and modification during iteration | **Covered** |
| 08 | Queue and `Deque` fundamentals | **Covered** |
| 09 | `PriorityQueue` and binary heaps | **Covered** |
| 10 | Blocking queues and backpressure | **Covered** |
| 11 | `LinkedHashMap` access order and LRU | **Covered** |
| 12 | Concurrent collections overview | **Covered** (high level; deep internals **Deferred**) |
| 13 | Selecting the right collection | **Covered** |

---

## Java concurrency (24-lesson curriculum)

| # | Lesson | Status |
| --- | --- | --- |
| 1 | Concurrency fundamentals | **Planned** |
| 2 | Java Memory Model | **Introduced** (touched during Collections detour) |
| 3 | Race conditions | **Planned** |
| 4 | `synchronized` | **Planned** |
| 5 | `volatile` | **Introduced** |
| 6 | Locks | **Planned** |
| 7 | Atomics and CAS | **Introduced** |
| 8 | `LongAdder` | **Planned** |
| 9 | Concurrent collections | **Introduced** (see Collections lesson 12) |
| 10 | Executors and `ThreadPoolExecutor` | **Planned** |
| 11 | Thread pool sizing and backpressure | **Planned** |
| 12 | `CompletableFuture` | **Planned** |
| 13 | `ForkJoinPool` | **Planned** |
| 14 | Virtual threads | **Planned** |
| 15 | `ThreadLocal` and `ScopedValue` | **Planned** |
| 16 | Coordination primitives | **Planned** |
| 17 | Producer-consumer patterns | **Planned** |
| 18 | Deadlock, livelock, starvation | **Planned** |
| 19 | Thread-safety patterns | **Planned** |
| 20 | Advanced concurrency | **Planned** |
| 21 | Production debugging | **Planned** |
| 22 | Backend concurrency scenarios | **Planned** |
| 23 | AI-system concurrency | **Planned** |
| 24 | Senior interview assessment | **Planned** |

---

## Other tracks (roadmap only unless noted)

| Track | Status |
| --- | --- |
| Spring Boot and microservices | **Planned** |
| Distributed systems and system design | **Planned** |
| Kafka | **Planned** |
| Data engineering / lakehouse | **Planned** (Spark Modules 1–10 + most of 11 **Covered** in Spark Handbook) |
| AWS and infrastructure | **Planned** |
| DSA and coding | **Planned** (external DSA Handbook not linked yet) |
| Behavioral | **Planned** |
| Mock interviews (Day 13) | **Planned** |
| Rapid revision (Day 14) | **Planned** |

---

## Spark Handbook alignment

| Spark module | Interview handbook status |
| --- | --- |
| Modules 1–10 | **Covered** in [Spark Engineering Handbook](../spark-engineering-handbook/docs/books/01-engineering-mastery/index.md) — reference only |
| Module 11 File formats | **Mostly covered** in Spark Handbook |
| Module 12 Delta Lake | **Planned** here |
| Module 13 Structured Streaming | **Planned** |
| Module 14 Databricks | **Planned** |
