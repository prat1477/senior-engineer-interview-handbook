---
title: Mistakes, Misconceptions, and Revision Items
description: Corrections from interactive study — add after each session.
status: draft
audience: advanced
tags: [revision, misconceptions]
created: 2026-10-15
updated: 2026-11-14
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

## Object model, equality, records, and runtime metadata (2026-11-07 and 2026-11-08)

Corrections from that session only. Correct answers are not listed here.

| Topic | Initial misunderstanding | Correct understanding | Memory trigger |
| --- | --- | --- | --- |
| Composition | Composition is always better | Choose based on relationship, substitutability, and design needs | IS-A vs HAS-A |
| Interfaces | Confusion around default methods and conflicts | Conflicting defaults require explicit resolution | Contract evolution |
| `hashCode` | Assuming `HashSet` detects all equal objects even with inconsistent hashes | Equal objects must have equal hashes | Equals first, hash consistency |
| Mutable keys | Assuming lookup always fails after mutation | Lookup may fail depending on bucket and hash behaviour | Never mutate key fields |
| `final` reference | Assuming `final List` makes its contents immutable | `final` prevents reassignment, not mutation | Reference vs object |
| `List.copyOf` | Assuming it performs deep copying | It copies the collection structure, not nested mutable objects | Shallow copy |
| Immutable updates | Attempting to reassign a `final` field | Return a new object with updated state | New object, same original |
| Records | Assuming record components make the full object graph immutable | Records are shallowly immutable; nested mutable objects need defensive copies or immutable designs | Final reference != frozen graph |
| Jackson and validation | Assuming JSON deserialization proves Bean Validation succeeded | Jackson calls the canonical constructor; `@Valid` triggers Jakarta Bean Validation | Convert != validate |
| Serialization | Treating serialization as network transmission | Serialization converts to JSON (or another representation); HTTP transports it | Convert != transmit |
| Record DTOs | Treating records as replacements for every regular class or conventional JPA entity | Use record DTOs as API contracts; persistence entities have different lifecycle and ORM needs | DTO != entity |
| Enum singleton | Assuming one enum instance makes its mutable fields thread-safe | Mutable enum fields are shared state; `count++` has races | Singleton != thread-safe |
| Enum persistence | Persisting `ordinal()` as a business identifier | Persist explicit stable codes; declaration order can change | Position != identity |
| Annotation | Assuming an annotation runs business logic by itself | Metadata needs a framework, processor, interceptor, or custom reader | Metadata != behavior |
| Retention | Treating `@Inherited` as interface or method inheritance | It applies only to class annotations through superclasses | Superclass only |
| Transactions | Assuming reflection performs rollback or every annotated call is intercepted | A Spring proxy/interceptor and transaction manager act; self-invocation bypasses the proxy | `this` skips proxy |

Lessons: [composition](../books/01-engineering-mastery/core-java/module-01-java-object-model/02-composition-vs-inheritance.md), [interfaces](../books/01-engineering-mastery/core-java/module-01-java-object-model/03-interfaces-vs-abstract-classes.md), [immutability](../books/01-engineering-mastery/core-java/module-01-java-object-model/04-immutability-and-defensive-copying.md), [`equals` / `hashCode`](../books/01-engineering-mastery/core-java/module-02-equals-and-hashcode/01-equals-and-hashcode-contracts.md), and [Java Records](../books/01-engineering-mastery/core-java/module-02-equals-and-hashcode/02-inheritance-records-and-equality.md).

## Java, concurrency, JVM, and production practice corrections (2026-11-11 to 2026-11-12)

These are constructive recall prompts, not severity labels. “Implemented after guidance” is not
the same as independent algorithm discovery.

| Topic | Earlier misunderstanding | Correct understanding | Revision link |
| --- | --- | --- | --- |
| One-transaction stock | Changed buy after a profitable sale; nested scan called O(n) | Buy changes only at a new minimum; nested scan is O(n²) | [DSA practice](../dsa/index.md) |
| Unlimited stock trades | More splits always create more profit | Adjacent positive rises telescope across an increasing run | [DSA practice](../dsa/index.md) |
| Streams | Omitted terminal `toList()` | `sorted()` is intermediate and returns a Stream | [Comparator](../books/01-engineering-mastery/core-java/module-04-collections/06-comparable-and-comparator.md) |
| Thread pool | `maximumPoolSize=20` meant 20 extra threads | It is a total cap: 5 core + 15 additional in the scenario | [TPE](../concurrency/10-executors-and-thread-pool-executor.md) |
| Kafka key | Proposed `transactionId` for account ordering | Use `accountId`; Kafka order is per partition | [Kafka](../kafka/index.md) |
| CHM | Atomic mapping made `ArrayList` mutation safe | `computeIfAbsent` protects mapping, not returned mutable value | [Concurrent collections](../concurrency/09-concurrent-collections.md) |
| Copy-on-write | Considered it for transaction appends | It is for read-heavy, write-light snapshot iteration | [Concurrent collections](../concurrency/09-concurrent-collections.md) |
| `volatile` | Visibility understood but JIT mechanism unclear | Optimizations may reuse nonvolatile reads when the JMM permits | [JMM](../concurrency/02-java-memory-model.md) |
| `LongAdder` | `sum()` sounded inaccurate | It is not an atomic snapshot; quiescent totals are maintained | [LongAdder](../concurrency/08-longadder.md) |
| JVM memory | Identified only Metaspace outside heap | Stacks, code cache, direct/native memory and GC structures affect RSS | [Memory areas](../books/01-engineering-mastery/core-java/module-09-jvm-basics/02-jvm-runtime-memory-areas.md) |
| Young GC | Frequent GC automatically meant severe pressure | Inspect pause time and allocation rate | [G1](../books/01-engineering-mastery/core-java/module-09-jvm-basics/05-garbage-collectors-and-g1.md) |
| P99 | Treated P99 as average/percentage improvement; reversed qualifying/exceeding counts | It is a percentile; for 10,000 measurements, about 9,900 qualify and up to 100 exceed | [Performance](../books/01-engineering-mastery/lld/module-05-lld/10-performance-scalability-and-optimization.md) |
| Full GC / SATB | Unclear why marking can run again | Concurrent SATB marking and Full-GC marking are different work | [G1](../books/01-engineering-mastery/core-java/module-09-jvm-basics/05-garbage-collectors-and-g1.md) |
| Native memory | Assumed one reclaimer manages non-heap | Reclamation depends on area: GC, thread lifecycle, class unloading, Cleaner, or native free | [Memory areas](../books/01-engineering-mastery/core-java/module-09-jvm-basics/02-jvm-runtime-memory-areas.md) |

## Caching, database scaling, and immutable-value corrections (2026-11-12)

| Topic | Misconception / uncertainty | Correct understanding | Revision link |
| --- | --- | --- | --- |
| GET caching | One fresh DB read guarantees later GET accuracy | A cached value can become stale after the read | [Cache review](../spring-microservices/02-production-pr-review-caching-and-resilience.md) |
| Redis | Redis is always non-durable | RDB/AOF persistence is configurable; durability remains a policy/trade-off | [Cache review](../spring-microservices/02-production-pr-review-caching-and-resilience.md) |
| TTL | 30-second TTL always means at most 30 seconds stale versus DB | Delayed in-flight fills can repopulate older data after invalidation | [Stale-fill race](../spring-microservices/02-production-pr-review-caching-and-resilience.md) |
| Write-through | Cache invalidation automatically is write-through | Write-through and cache-aside invalidation have different write contracts | [Cache strategies](../spring-microservices/02-production-pr-review-caching-and-resilience.md) |
| HikariCP | Each pod pool limits cluster-wide DB concurrency | Local pools multiply across pods and rolling-deployment/HPA capacity | [DB protection](../spring-microservices/02-production-pr-review-caching-and-resilience.md) |
| HPA | More pods necessarily increase system throughput | A downstream database can be the bottleneck and need budgets/shedding | [HPA](../spring-microservices/02-production-pr-review-caching-and-resilience.md) |
| Queueing | Queueing fixes sustained database overload | It only absorbs a burst; sustainable throughput is unchanged | [Resilience](../spring-microservices/02-production-pr-review-caching-and-resilience.md) |
| Read replica | Replica equals an independently modeled CQRS database | Physical replicas retain the same physical schema/index design; CQRS changes the model | [Replication/CQRS](../distributed-systems/database-scaling-replication-and-cqrs.md) |
| PostgreSQL partitioning | Table partitions distribute automatically over machines | Native partitions are not distributed sharding | [Distribution](../distributed-systems/database-scaling-replication-and-cqrs.md) |
| ClickHouse `PARTITION BY` | It determines machine-level distribution | Partitioning and shard distribution are separate | [Distribution](../distributed-systems/database-scaling-replication-and-cqrs.md) |
| Thread-safe cache | Safe cache internals imply safe mutable cached object state | Element state, visibility, and immutability are separate | [Cache values](../spring-microservices/02-production-pr-review-caching-and-resilience.md) |
| Copy-on-write | Snapshot iterator freezes the stored object | It snapshots array references, not mutable element state | [COW list](../concurrency/09-concurrent-collections.md) |
| Record | Record is automatically deeply immutable | Records are shallowly immutable unless nested values are immutable/copied | [Records](../books/01-engineering-mastery/core-java/module-02-equals-and-hashcode/02-inheritance-records-and-equality.md) |
| `List.copyOf` | It deep-copies mutable elements | It makes an unmodifiable structural copy, not an element deep copy | [Records](../books/01-engineering-mastery/core-java/module-02-equals-and-hashcode/02-inheritance-records-and-equality.md) |
| Canonical constructor | New record concept requiring revision | It initializes all components; compact form validates/normalizes before implicit assignment | [Constructor forms](../books/01-engineering-mastery/core-java/module-02-equals-and-hashcode/02-inheritance-records-and-equality.md) |

The record discussion correctly recognized that a `List` component can be mutable. The later
nested-object explanation deepened that point; it is not recorded as a fabricated misconception.

## Spring transactions, JPA, and JDBC corrections (2026-11-14)

These entries distinguish attention-to-code-review details from genuine gaps and preserve correct
reasoning from the session.

| Topic | What happened in practice | Correct understanding | Revision link |
| --- | --- | --- | --- |
| `REQUIRES_NEW` | Initially overlooked that the two methods were in the same class. | The annotation needs a call crossing the transactional proxy; self-invocation bypasses it. | [Proxy invocation](../spring-microservices/03-spring-boot-internals-transactions-jpa.md#self-invocation-annotation-present-advice-absent) |
| Transaction scopes | Initially described an internally invoked method as a child transaction. | An internal call does not create a separately proxied transaction scope. | [Propagation](../spring-microservices/03-spring-boot-internals-transactions-jpa.md#3-propagation-rollback-rules-and-exception-paths) |
| `UnexpectedRollbackException` | Initially expected normal outer completion after catching an inner failure. | A separate `REQUIRED` inner scope can mark the shared transaction rollback-only. | [Rollback-only](../spring-microservices/03-spring-boot-internals-transactions-jpa.md#3-propagation-rollback-rules-and-exception-paths) |
| Spring proxy implementation | Assumed proxy creation necessarily requires a custom classloader. | JDK/CGLIB proxy infrastructure is the defining mechanism, not a custom classloader. | [AOP proxies](../spring-microservices/03-spring-boot-internals-transactions-jpa.md#2-aop-proxies-and-transaction-interception) |
| Bean storage | Asked where a bean lives. | It is a heap object managed by `ApplicationContext`; the context is not separate heap memory. | [Beans](../spring-microservices/03-spring-boot-internals-transactions-jpa.md#1-beans-the-container-and-boot-startup) |
| Fetch plans | `EntityGraph` and DTO projection were unfamiliar. | They deliberately control entity loading or select API fields rather than relying on accidental lazy loading. | [Fetch design](../spring-microservices/03-spring-boot-internals-transactions-jpa.md#4-persistence-context-lazy-loading-and-fetch-design) |
| Dirty checking | Asked whether `@Transactional` itself causes dirty checking. | A managed entity/persistence context supplies change tracking; transaction scope usually keeps it usable. | [Persistence context](../spring-microservices/03-spring-boot-internals-transactions-jpa.md#4-persistence-context-lazy-loading-and-fetch-design) |
| JDBC transactions | Initially thought `@Transactional` might be JPA-only. | Spring transaction abstraction also coordinates JDBC/JdbcTemplate. | [Transactional JDBC](../spring-microservices/03-spring-boot-internals-transactions-jpa.md#7-transactional-jdbc-chunking-and-postgresql-errors) |
| PostgreSQL failures | Clarified zero-row conditional update versus constraint error. | A constraint error normally aborts the active PostgreSQL transaction; a zero count need not. | [PostgreSQL errors](../spring-microservices/03-spring-boot-internals-transactions-jpa.md#7-transactional-jdbc-chunking-and-postgresql-errors) |
| Cache invalidation | Expected shared Redis deletion to make the next read fresh. | A late in-flight fill can write an older value after `DEL`. | [Stale fill](../spring-microservices/02-production-pr-review-caching-and-resilience.md) |

Correctly reasoned after clarification: debit and credit share one JDBC transaction and roll back
together on a database error; checked exceptions commit by default; managed entities do not need
an extra `save()` for dirty checking; Hibernate `@Version` uses a version predicate; and a
cross-bean `REQUIRES_NEW` scope has an independent physical outcome.

## Personal revision queue

| Topic | Status | Notes |
| --- | --- | --- |
| _Add after practice_ | Needs revision | |
