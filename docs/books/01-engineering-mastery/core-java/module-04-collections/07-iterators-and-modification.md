---
title: "Lesson 7 — Iterators and Modifying Collections During Iteration"
description: "Fail-fast behavior, safe removal, and ConcurrentModificationException."
status: covered
audience: practitioner
tags: [[collections, iterator, module-4, lesson-7], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 7 — Iterators and Modifying Collections During Iteration

Fail-fast behavior, safe removal, and ConcurrentModificationException.

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

Core Java Module 4 — **Collections**. This is the canonical Engineering Mastery
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-04-collections/07-iterators-and-modification.md) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

## Architecture

This lesson sits in **Module 4** of the Core Java track. Service code should treat
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

# Lesson 7 — Iterators and Modifying Collections During Iteration

Iteration is how you process collections in business logic. Structural changes during iteration require discipline — **fail-fast** iterators detect many illegal patterns but are **not** a correctness or concurrency guarantee.

## 1. Iterator API

```java
Iterator<String> it = names.iterator();
while (it.hasNext()) {
    String name = it.next();
    if (name.isEmpty()) {
        it.remove(); // safe: updates iterator state
    }
}
```

- **`hasNext()`** / **`next()`** — walk elements.
- **`remove()`** — removes last returned element via iterator.

## 2. Enhanced for-loop

```java
for (String name : names) { ... }
```

Uses an iterator under the hood — same structural modification rules apply.

## 3. Unsafe: modify collection directly

```java
for (String name : names) {
    if (name.isEmpty()) {
        names.remove(name); // often ConcurrentModificationException
    }
}
```

Direct `Collection.remove` while iterating can leave iterator state inconsistent → **`ConcurrentModificationException`** (best-effort).

## 4. Safe alternatives

- **`iterator.remove()`** during explicit iteration.
- **`removeIf(Predicate)`** — bulk remove with defined behavior.
- **Copy-on-write** or **concurrent** collections for concurrent access (different rules — see [Lesson 12](12-concurrent-collections-overview.md)).

## 5. Fail-fast limitations

| Fact | Implication |
| --- | --- |
| Not guaranteed in all cases | Do not rely on CME for program logic |
| Single-threaded structural change | Typical trigger |
| Not thread safety | Use concurrent collections or synchronization for threads |

Multiple threads modifying a non-concurrent collection can corrupt state **without** CME.

## Incorrect vs correct pattern

```java
// Incorrect for ArrayList during foreach
list.forEach(x -> { if (bad(x)) list.remove(x); });

// Correct
list.removeIf(bad);
```


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-04-collections/07-iterators-and-modification.md)
- [Collections production playbook](../../../03-production-playbook/core-java/module-04-collections-production-playbook.md)
- [Module index](index.md)
