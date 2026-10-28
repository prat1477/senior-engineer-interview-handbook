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

**Last updated:** 2026-10-25  
**Current position:** Core Java Modules 2–9 **Covered** in the [three-book layout](docs/books/index.md). [Java concurrency](docs/concurrency/index.md) lessons **1–24 documented** (handbook pass; deepen L1–11 as you study). Distributed-systems support pages: [DB concurrency](docs/distributed-systems/database-concurrency-and-isolation.md), [locks / Scylla](docs/distributed-systems/distributed-locks-fencing-and-scylladb.md). Module 1 object model still **Planned**.

### Three-book rewrite (layout vs depth)

| Module | Mastery + Companion + Playbook layout | Hand-expanded Mastery depth |
| --- | --- | --- |
| 4 Collections | **Done** | L1 pilot expanded; L2–L13 use migrated body + template supplement — **Needs revision** for full Spark-style depth |
| 5–9 | **Done** | Same pattern — expand lesson-by-lesson in Book 1 as you study |

Companion chapters and playbooks are in place; deepening is incremental in [Engineering Mastery](docs/books/01-engineering-mastery/index.md) only.

---

## 14-day roadmap

| Day | Theme | Status |
| --- | --- | --- |
| 1 | Core Java, Collections, HashMap, DSA arrays/hash maps | **In progress** (Collections **Covered**; Object model / dedicated HashMap module still **Planned**) |
| 2 | Streams, Optional, JVM basics, two pointers / sliding window | **In progress** (Streams, Optional, JVM basics **Covered**; DSA two pointers / sliding window **Planned**) |
| 3 | Concurrency foundations (JMM, happens-before, race, `synchronized`) | **In progress** (L1–11 handbook **Covered**; study + drill) |
| 4 | Advanced concurrency + high-level system design | **In progress** (L12–24 handbook **Covered**; study + drill) |
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

## Core Java track (fixed order + extensions)

| # | Module | Status |
| --- | --- | --- |
| 1 | Java Object Model | **Planned** |
| 2 | **`equals()` and `hashCode()`** | **Covered** |
| 3 | **`HashMap` internals (deepening)** | **Covered** (foundational map usage also in Collections M4 L4) |
| 4 | **Collections** | **Covered** |
| 5 | **Generics** | **Covered** |
| 6 | **Java 8 Streams** | **Covered** |
| 7 | **Optional** | **Covered** |
| 8 | **Exception handling** | **Covered** |
| 9 | **JVM basics, GC, and production diagnostics** | **Covered** |

### Module 2 — equals / hashCode

| Lesson | Topic | Status |
| --- | --- | --- |
| 01 | Contracts and `hashCode` | **Covered** |
| 02 | Inheritance, records, composition | **Covered** |
| — | Companion practice + answers | **Covered** |

### Module 3 — HashMap internals

| Lesson | Topic | Status |
| --- | --- | --- |
| 01 | Table, spread hash, index | **Covered** |
| 02 | put/get, treeify | **Covered** |
| 03 | Resize, load factor, threshold | **Covered** |
| 04 | Performance, concurrency | **Covered** |
| — | Companion practice + answers | **Covered** |

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
| 14–15 | Interview practice + answers | **Covered** |

### Module 5 — Generics lessons

| Lesson | Topic | Status |
| --- | --- | --- |
| 01–04 | Classes, bounds, PECS, erasure | **Covered** |
| 05–06 | Interview practice + answers | **Covered** |

### Module 6 — Streams lessons

| Lesson | Topic | Status |
| --- | --- | --- |
| 01–04 | Pipeline, collectors, short-circuit, parallel | **Covered** |
| 05–06 | Interview practice + answers | **Covered** |

### Module 7 — Optional lessons

| Lesson | Topic | Status |
| --- | --- | --- |
| 01–02 | Fundamentals, composition, anti-patterns | **Covered** |
| 03–04 | Interview practice + answers | **Covered** |

### Module 8 — Exception handling lessons

| Lesson | Topic | Status |
| --- | --- | --- |
| 01–03 | Hierarchy, TWR, Spring/retries/idempotency | **Covered** |
| 04–05 | Interview practice + answers | **Covered** |

### Module 9 — JVM basics and GC lessons

| Lesson | Topic | Status |
| --- | --- | --- |
| 01 | JVM architecture and execution lifecycle | **Covered** |
| 02 | Runtime memory areas | **Covered** |
| 03 | JVM memory configuration and options | **Covered** |
| 04 | Garbage collection fundamentals | **Covered** |
| 05 | Garbage collectors and G1 GC | **Covered** |
| 06 | Java reference types and memory retention | **Covered** |
| 07 | Diagnosing `OutOfMemoryError` in production | **Covered** |
| 08 | Heap dump analysis | **Covered** |
| 09 | Production OOM case study (Spark SQL optimizer) | **Covered** |
| 10–11 | Interview practice + answers | **Covered** |

---

## Java concurrency (24-lesson curriculum)

| # | Lesson | Status |
| --- | --- | --- |
| 1 | Concurrency fundamentals | **Covered** (handbook) |
| 2 | Java Memory Model | **Covered** (handbook) |
| 3 | Race conditions | **Covered** (handbook) |
| 4 | `synchronized` | **Covered** (handbook) |
| 5 | `volatile` | **Covered** (handbook) |
| 6 | Locks | **Covered** (handbook) |
| 7 | Atomics and CAS | **Covered** (handbook) |
| 8 | `LongAdder` | **Covered** (handbook) |
| 9 | Concurrent collections | **Covered** (handbook; see also Collections M4 L12) |
| 10 | Executors and `ThreadPoolExecutor` | **Covered** (handbook) |
| 11 | Thread pool sizing and backpressure | **Covered** (handbook) |
| 12 | `CompletableFuture` | **Covered** (handbook) |
| 13 | `ForkJoinPool` | **Covered** (handbook) |
| 14 | Virtual threads | **Covered** (handbook; JDK 21+ notes) |
| 15 | `ThreadLocal` and `ScopedValue` | **Covered** (handbook) |
| 16 | Coordination primitives | **Covered** (handbook) |
| 17 | Producer-consumer patterns | **Covered** (handbook) |
| 18 | Deadlock, livelock, starvation | **Covered** (handbook) |
| 19 | Thread-safety patterns | **Covered** (handbook) |
| 20 | Advanced concurrency | **Covered** (handbook) |
| 21 | Production debugging | **Covered** (handbook) |
| 22 | Backend concurrency scenarios | **Covered** (handbook) |
| 23 | AI-system concurrency | **Covered** (handbook) |
| 24 | Senior interview assessment | **Covered** (handbook) |

**Book 2 Interview Companion** for all 24 lessons: [concurrency companion](docs/books/02-interview-companion/concurrency/index.md) — **Covered** (handbook; includes [visual quick reference](docs/books/02-interview-companion/concurrency/module-visual-quick-reference.md)).

---

## LLD — module 05-lld

| Lesson | Topic | Status |
| --- | --- | --- |
| 1 | LLD foundations — senior interview evaluation | **Covered** (Mastery + Companion + Playbook) |

**Interview revision:** [Book 2 LLD Companion](docs/books/02-interview-companion/lld/module-05-lld/index.md).

---

## Other tracks (roadmap only unless noted)

| Track | Status |
| --- | --- |
| Spring Boot and microservices | **Planned** |
| Distributed systems and system design | **In progress** ([DB concurrency](docs/distributed-systems/database-concurrency-and-isolation.md), [locks / Scylla](docs/distributed-systems/distributed-locks-fencing-and-scylladb.md); broader design track **Planned**) |
| Kafka | **Planned** |
| Data engineering / lakehouse | **Planned** (Spark Modules 1–10 + most of 11 **Covered** in Spark Handbook) |
| AWS and infrastructure | **Planned** |
| DSA and coding | **Planned** (external DSA Handbook not linked yet) |
| Behavioral | **Planned** |
| LLD (module 05) | **In progress** — [L1 Companion](docs/books/02-interview-companion/lld/module-05-lld/index.md) |
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
