---
title: Mistakes, Misconceptions, and Revision Items
description: Corrections from interactive study — add after each session.
status: draft
audience: advanced
tags: [revision, misconceptions]
created: 2026-10-15
updated: 2026-11-08
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

## Personal revision queue

| Topic | Status | Notes |
| --- | --- | --- |
| _Add after practice_ | Needs revision | |
