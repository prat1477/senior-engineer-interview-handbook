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

**Last updated:** 2026-11-14
**Current position:** Spring Boot internals, transaction propagation, JPA/Hibernate state, optimistic locking, batch processing, JDBC transactions, and cache consistency are **discussed / conceptually understood**; independent implementation and mixed-mock assessment remain pending. The next technical topic is **Spring Security / OAuth2 Resource Server / JWT verification and authorization**. [DSA arrays and hash maps](docs/dsa/index.md) remain planned. Java Records are **Covered** in [Module 2 Lesson 2](docs/books/01-engineering-mastery/core-java/module-02-equals-and-hashcode/02-inheritance-records-and-equality.md); Core Java Modules 2–9 stay **Covered**. [Java concurrency](docs/concurrency/index.md) lessons **1–24 documented** (handbook pass; not marked newly complete). Week 1 plan: [week-01](docs/week-01-core-java-spring.md). Skill scores: [mastery matrix](docs/tracking/mastery-matrix.md).

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
| 1 | Core Java, Collections, HashMap, DSA arrays/hash maps | **In progress** (Collections, HashMap, object-model lessons, and Java Records **Covered**; DSA arrays/hash maps still **Planned**) |
| 2 | Streams, Optional, JVM basics, two pointers / sliding window | **In progress** (Streams, Optional, JVM basics **Covered**; DSA two pointers / sliding window **Planned**) |
| 3 | Concurrency foundations (JMM, happens-before, race, `synchronized`) | **In progress** (L1–11 handbook **Covered**; study + drill) |
| 4 | Advanced concurrency + high-level system design | **In progress** (L12–24 handbook **Covered**; study + drill) |
| 5 | Spring Boot and backend fundamentals | **In progress** (Spring Core L1 IoC and DI **Covered** conceptually; implementation assessment separate) |
| 6 | Microservice reliability | **Planned** |
| 7 | Kafka deep dive | **In progress** (per-account ordering, consumer coordination, idempotency and outbox reasoning documented; broker tuning and implementation practice remain pending) |
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
| 1 | Java Object Model | **Covered** (Java Records are covered in Module 2 Lesson 2) |
| 2 | **`equals()` and `hashCode()`** | **Covered** (contracts deepened 2026-11-07; module not re-scored as mastered) |
| 3 | **`HashMap` internals (deepening)** | **Covered** (foundational map usage also in Collections M4 L4) |
| 4 | **Collections** | **Covered** |
| 5 | **Generics** | **Covered** |
| 6 | **Java 8 Streams** | **Covered** |
| 7 | **Optional** | **Covered** |
| 8 | **Exception handling** | **Covered** |
| 9 | **JVM basics, GC, and production diagnostics** | **Covered** |

### Module 1 — Java Object Model

Coverage below is lesson status. Scores are in the [mastery matrix](docs/tracking/mastery-matrix.md). Java Records are covered in Module 2 Lesson 2 because that existing lesson owns their equality and immutability context.

| Lesson | Topic | Status |
| --- | --- | --- |
| 01 | OOP principles | **Covered** |
| 02 | Composition vs inheritance | **Covered** |
| 03 | Interfaces vs abstract classes | **Covered** |
| 04 | Immutability and defensive copying | **Covered** |
| 05 | Enums, annotations, reflection, and Spring AOP | **Covered** (enum design and concurrency; annotation metadata, reflection, processing, proxies, and transactional rollback behavior) |
| — | Records (Module 2 Lesson 2) | **Covered** |

### Module 2 — equals / hashCode

| Lesson | Topic | Status |
| --- | --- | --- |
| 01 | Contracts and `hashCode` | **Covered** (2026-11-07 session: `PaymentRequest`, RSTCN, mutable-key nuance, inconsistent `hashCode`) |
| 02 | Inheritance, records, composition | **Covered** (Java Records fundamentals, compact-constructor validation, Jackson, and Spring MVC DTO exercise documented 2026-11-08) |
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
| 2 | Requirement clarification and scope | **Covered** (Mastery + Companion) |
| 3 | Domain modeling and class responsibilities | **Covered** (Mastery + Companion) |
| 4 | Encapsulation, invariants, Tell-Don't-Ask | **Covered** (Mastery + Companion) |
| 5 | Abstraction, composition, pattern selection | **Covered** (Mastery + Companion) |
| 6 | OCP and DIP — pricing rules and payment providers | **Covered** (Mastery + Companion) |
| 7 | State modeling and state transitions | **Covered** (Mastery + Companion) |
| 8 | Error handling and failure modeling | **Covered** (Mastery + Companion) |
| 9 | Practice — curriculum gaps and transfer problems | **In progress** (written; drills not yet done) |
| 10 | Performance, scalability, and optimization | **Covered** (Mastery + Companion) |

**Interview revision:** [Book 2 LLD Companion](docs/books/02-interview-companion/lld/module-05-lld/index.md) including [visual quick reference](docs/books/02-interview-companion/lld/module-05-lld/module-visual-quick-reference.md).

**Book 2 visual pass (2026-10-28):** Core Java M2–M9 companions rewritten with flowcharts, scenario bites, and per-module [cheat sheets](docs/books/02-interview-companion/index.md). Diagrams render under `mkdocs serve`, not in every raw Markdown preview.

---

## Other tracks (roadmap only unless noted)

| Track | Status |
| --- | --- |
| Spring Boot and microservices | **In progress** ([IoC / DI](docs/spring-microservices/01-ioc-and-dependency-injection.md), [production PR review / caching](docs/spring-microservices/02-production-pr-review-caching-and-resilience.md), and [internals / transactions / JPA / JDBC](docs/spring-microservices/03-spring-boot-internals-transactions-jpa.md) **Explained and understood**; Spring Security/JWT and independent validation remain pending) |
| Distributed systems and system design | **In progress** ([DB concurrency](docs/distributed-systems/database-concurrency-and-isolation.md), [locks / Scylla](docs/distributed-systems/distributed-locks-fencing-and-scylladb.md), and [database scaling / CQRS](docs/distributed-systems/database-scaling-replication-and-cqrs.md) **Explained and understood**; broader design track **Planned**) |
| Kafka | **In progress** ([ordering, idempotency, and outbox foundations](docs/kafka/index.md) documented; tuning and implementation practice pending) |
| Data engineering / lakehouse | **Planned** (Spark Modules 1–10 + most of 11 **Covered** in Spark Handbook) |
| AWS and infrastructure | **Planned** |
| DSA and coding | **Planned** (external DSA Handbook not linked yet) |
| Behavioral | **Planned** |
| LLD (module 05) | **In progress** — Lessons 1–8 and 10 **Covered**; Lesson 9 practice set written, drills not done. [Module index](docs/books/02-interview-companion/lld/module-05-lld/index.md) |
| Mock interviews (Day 13) | **Planned** |
| Rapid revision (Day 14) | **Planned** |

---

## November 11–12 practice update

This update records documentation and practice evidence without upgrading all topics to mastery.

| Area | Evidence-based status | Notes |
| --- | --- | --- |
| Stock-trading greedy exercises | **Implemented after guidance** / **independently implemented** | One transaction required guided discovery; unlimited transactions final solution was independently implemented. |
| Streams, collectors, comparators | **Explained and understood** | Needs independent mock validation; sorting terminal-operation mistake logged. |
| JMM, atomics, collections, TPE | **Explained and understood** | Detailed CHM internals and deeper ReentrantLock internals remain **pending** for independent validation. |
| Kafka ordering, SQL debit, idempotency, outbox | **Explained and understood** | Full distributed transaction implementation remains **pending**. |
| JVM memory, G1, MAT, P99 | **Explained and understood** | Advanced G1 tuning, native-memory investigation, production GC-log analysis, and a JVM incident mock remain **pending**. |

## November 12 Spring, caching, and database-scaling update

This is a learning-status update, not a claim of independent production implementation.

| Area | Evidence-based status | What remains |
| --- | --- | --- |
| Spring singleton state, `HashMap` / `ConcurrentHashMap`, DI, 404 handling | **Explained and understood** | Independently correct the complete `OrderService` and complete a timed PR review. |
| Cache patterns, stale-fill races, Caffeine/Redis/DB choice | **Explained and understood** | Design and test strict-freshness and invalidation behaviour independently. |
| Redis outage controls: circuit breaker, bulkhead, rate limit, shedding, queues | **Explained and understood** | Independently size/admit requests and implement a fallback policy. |
| Multi-pod HikariCP budgets and HPA | **Explained and understood** | Perform a capacity calculation and load-test a constrained downstream database. |
| PostgreSQL replicas, WAL, physical/logical replication, CQRS | **Explained and understood** | Configure and validate replication lag/failure behaviour hands-on. |
| Partitioning, sharding, replication, Scylla, ClickHouse | **Explained and understood** | Independently choose a distribution design from workload constraints. |
| Cache retention, mutable values, copy-on-write snapshots | **Explained and understood** | Write a small concurrency test that demonstrates the reference-versus-object distinction. |
| Records, defensive copies, canonical constructors | **Explained and understood** | Complete the canonical-constructor validation exercise independently. |

**Future, not studied or scheduled:** the [LRU cache implementation drill](docs/books/01-engineering-mastery/lld/module-05-lld/09-practice-transfer-problems.md) and [database-selection HLD lesson](docs/distributed-systems/database-scaling-replication-and-cqrs.md) are tracked for later; neither is marked complete.

### Remaining high-priority preparation

- Spring Boot pull-request code review exercise and additional independent concurrency coding.
- Deeper locks and coordination primitives; full JVM production incident mock.
- Additional Java coding/debugging exercises and full system-design interview execution.
- Python and Agentic AI mocks.
- Before the November 17 interview: focused revision of Java 21, Java 25 LTS, and relevant newer Java language/platform features.

## November 14 Spring transactions, JPA, and JDBC update

This documents conceptual work without upgrading it to independently demonstrated mastery.

| Area | Evidence-based status | What remains |
| --- | --- | --- |
| Bean heap/container model, constructor injection, Boot startup, lifecycle and AOP proxies | **Discussed / conceptually understood** | Independently explain a lifecycle/proxy trace and review a configuration. |
| `REQUIRED`, `REQUIRES_NEW`, rollback-only, checked exceptions, and outbox reasoning | **Discussed / conceptually understood** | Mixed propagation mock and independently chosen transaction boundaries. |
| Persistence context, lazy loading, fetch strategy, dirty checking, and `@Version` | **Discussed / conceptually understood** | JPA/Hibernate coding implementation and query/performance review. |
| JPQL bulk DML, Hibernate batching, JdbcTemplate batch counts, chunking | **Discussed / conceptually understood** | Production-grade batch writer, conflict classification, retries, and load testing. |
| Spring JDBC transactions and PostgreSQL error/savepoint semantics | **Discussed / conceptually understood** | Hands-on failure-path implementation and database validation. |
| Caffeine + Redis L1/L2, stale-fill race, and invalidation limits | **Discussed / conceptually understood** | Independently design/test the chosen freshness and fan-out protocol. |

**Next session:** Spring Security / OAuth2 Resource Server / JWT verification and authorization.

## Spark Handbook alignment

| Spark module | Interview handbook status |
| --- | --- |
| Modules 1–10 | **Covered** in [Spark Engineering Handbook](../spark-engineering-handbook/docs/books/01-engineering-mastery/index.md) — reference only |
| Module 11 File formats | **Mostly covered** in Spark Handbook |
| Module 12 Delta Lake | **Planned** here |
| Module 13 Structured Streaming | **Planned** |
| Module 14 Databricks | **Planned** |
