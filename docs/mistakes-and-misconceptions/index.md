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

## Personal revision queue

| Topic | Status | Notes |
| --- | --- | --- |
| _Add after practice_ | Needs revision | |
