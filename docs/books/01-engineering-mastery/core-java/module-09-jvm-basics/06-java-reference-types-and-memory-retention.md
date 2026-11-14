---
title: "Lesson 6 — Java Reference Types and Memory Retention"
description: "Strong, soft, weak, phantom, ReferenceQueue, WeakHashMap, caches."
status: covered
audience: practitioner
tags: [[jvm, references, module-9, lesson-6], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 6 — Java Reference Types and Memory Retention

Strong, soft, weak, phantom, ReferenceQueue, WeakHashMap, caches.

## Shared domain models

Examples across Modules 4–9 reuse the same records so mental models transfer:

```java
public record Employee(long id, String name, String department, double salary) {}
public record Order(long id, long employeeId, String sku, int quantity, double unitPrice) {}
public record Payment(long orderId, String method, double amount, java.time.Instant paidAt) {}
```

Use them for grouping (`Collectors.groupingBy`), maps (`Map<Long, Employee>`), optional chains
(`Optional<Employee>`), and exception boundaries around payment APIs.

## Big picture

Core Java Module 9 — **JVM basics and GC**. This is the canonical Engineering Mastery
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-09-jvm-basics/06-java-reference-types-and-memory-retention.md) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

## Architecture

This lesson sits in **Module 9** of the Core Java track. Service code should treat
collection/generics/stream/JVM choices as **capacity and correctness** decisions, not style preferences.

## Internal working

Review the numbered sections in **Core concepts (canonical)** below. For interviews, pair each
fact with **complexity**, **ordering**, and **concurrency** implications.

## Hands-on

```java
// Extend the snippet in the canonical section with Employee / Order / Payment records.
// JDK 17+: compile with your module's test source set or `java Main.java`.
```

## Performance

State average vs worst-case costs for the structures or APIs introduced in this lesson.
Call out allocation hot spots (boxing, autoboxing in streams, defensive copies).

## JDK tools and diagnostic clues

- Watch for lesson-specific exceptions in logs (`ConcurrentModificationException`, `ClassCastException`
  at erasure boundaries, `OutOfMemoryError` subtypes for JVM modules).
- Use **async profiler**, **JFR**, or **heap histogram** (`jcmd <pid> GC.class_histogram`) when
  production symptoms match this topic.

## Failure scenarios

Document one production failure mode tied to misuse of this lesson's API, and the guardrail
(service validation, bounded queues, explicit comparators, try-with-resources).

## Best practices and anti-patterns

- Prefer clear types over clever one-liners.
- Make null and empty collection policies explicit at API edges.

> **Production insight**
> Align collection mutability with transaction boundaries — shared mutable structures between
> threads remain the top source of subtle bugs.

## Staff engineer notes

- Teach the **contract** first (what callers may assume), then the **implementation** (how it is enforced).
- Link forward to Module 12 concurrent collections when discussing multi-threaded mutation.

## Core concepts (canonical)

# Lesson 6 — Java Reference Types and Memory Retention

Beyond ordinary strong references, `java.lang.ref` provides **soft**, **weak**, and **phantom** references for lifecycle-sensitive structures. Semantics interact with GC; they are **not** a substitute for bounded application caches.

## Comparison table

| Type | Reachability | `get()` | Typical use |
| --- | --- | --- | --- |
| **Strong** | Keeps object alive while reachable | Returns referent | Default references |
| **Soft** | Cleared when memory **pressure** warrants (timing not guaranteed) | Returns referent until cleared | Memory-sensitive cache (legacy) |
| **Weak** | Cleared when only weakly reachable | Returns referent until cleared | Canonical mappings, listeners |
| **Phantom** | After finalization/cleaner semantics; `get()` always **null** | Always `null` | Post-mortem cleanup via `ReferenceQueue` |

## 1. Strong references

```java
List<String> list = new ArrayList<>();
```

While `list` is reachable from roots, the `ArrayList` and its elements (if strongly referenced) stay alive.

**Static fields:** a `static` or `static final` **reference** keeps the **referenced object** reachable — not “every object in the graph is immortal forever,” but anything strongly reachable from that static chain remains alive until the reference is cleared and the object becomes unreachable.

## 2. Weak references

```java
WeakReference<LargeObject> weak = new WeakReference<>(new LargeObject());
LargeObject obj = weak.get(); // may return null after GC clears weak referent
```

Weakly reachable objects may be cleared during GC processing.

## 3. Soft references

```java
SoftReference<byte[]> soft = new SoftReference<>(new byte[1_000_000]);
byte[] data = soft.get(); // may be null under memory pressure
```

May survive longer than weak refs; **eviction timing is not guaranteed** — poor fit for strict SLAs.

## 4. Phantom references and `ReferenceQueue`

```java
ReferenceQueue<Connection> queue = new ReferenceQueue<>();
PhantomReference<Connection> phantom =
    new PhantomReference<>(conn, queue);
// phantom.get() is always null
```

Used to learn when an object is **phantom reachable** so native resources can be released **after** related cleanup — not for fetching the object.

**`ReferenceQueue` does not** automatically close files, sockets, or pools — you still run a **consumer thread** or cleaner that reacts to enqueued references.

## 5. `WeakHashMap`

- **Keys** are weak; **values** are **strong**.
- If a value references its key (directly or indirectly), the key may stay strongly reachable → **expected weak-key cleanup may not occur**.

```java
Map<Key, Value> map = new WeakHashMap<>();
// Danger: value holds strong ref back to key → key not collectable
```

**String literals** and other strong references elsewhere also keep keys alive.

## 6. Caches: soft references vs Caffeine

For production caches, **bounded** structures with explicit eviction (size, TTL, weight) — e.g. **Caffeine** — are more **predictable** than soft-reference caches.

| Approach | Predictability |
| --- | --- |
| Soft-reference map | GC-driven, timing unspecified |
| Bounded cache (Caffeine) | Defined max size / TTL / policy |

## Common misconceptions

| Myth | Reality |
| --- | --- |
| "`WeakHashMap` frees entries automatically" | Values must not strongly retain keys |
| "`PhantomReference.get()` returns the object" | Always **null** by design |
| "Soft refs = LRU cache" | No ordering guarantee; pressure-dependent clearing |

## 7. Singleton cache retention in a service

```java
private final ConcurrentHashMap<String, Order> cache = new ConcurrentHashMap<>();
```

An application singleton is long-lived; every strongly reachable key/value chain remains live to
the GC. Millions of unique keys in an unbounded cache increase old-generation occupancy, GC work,
and can cause `OutOfMemoryError` within each pod's heap budget. A concurrent map fixes neither
retention nor an eviction policy. Bound cache size/weight/TTL, measure evictions and hit/miss/load
latency, and correlate cache growth with old-gen and process RSS. See the [Spring cache review](../../../../spring-microservices/02-production-pr-review-caching-and-resilience.md).


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-09-jvm-basics/06-java-reference-types-and-memory-retention.md)
- [JVM basics and GC production playbook](../../../03-production-playbook/core-java/module-09-jvm-basics-production-playbook.md)
- [Module index](index.md)
