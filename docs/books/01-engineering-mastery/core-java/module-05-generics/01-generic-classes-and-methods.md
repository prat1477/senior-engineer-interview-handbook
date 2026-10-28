---
title: "Lesson 1 — Generic Classes and Methods"
description: "Type parameters, generic methods, and method type inference."
status: covered
audience: practitioner
tags: [[generics, module-5, lesson-1], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 1 — Generic Classes and Methods

Type parameters, generic methods, and method type inference.

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

Core Java Module 5 — **Generics**. This is the canonical Engineering Mastery
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-05-generics/01-generic-classes-and-methods.md) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

## Architecture

This lesson sits in **Module 5** of the Core Java track. Service code should treat
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

# Lesson 1 — Generic Classes and Methods

Generics add **compile-time type parameters** so collections and APIs can be reused without casting. They do not create new runtime types for each `T` — see [type erasure](04-type-erasure-raw-types-arrays.md).

## 1. Generic class

```java
public final class Box<T> {
    private T value;

    public Box(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }
}

Box<String> name = new Box<>("order-42");
String s = name.get(); // no cast
```

`T` is a **type parameter** scoped to the class. Each field/method can use `T` consistently.

## 2. Generic method (on generic or non-generic class)

```java
public static <T> T first(List<T> items) {
    return items.isEmpty() ? null : items.get(0);
}

String head = first(List.of("a", "b")); // T inferred as String
```

Syntax: `<T>` **before** the return type declares method-level type parameters. They can differ from a surrounding class’s `T`.

## 3. Method type inference (Java 8+)

The compiler infers `T` from arguments and context:

```java
List<String> names = List.of("a", "b");
String x = first(names);           // T = String

List<Integer> nums = List.of(1, 2);
Integer y = first(nums);             // T = Integer
```

**Trap:** raw `List` passed to a generic method loses safety and may infer inconsistently — prefer typed collections.

**Explicit type argument** when inference fails:

```java
Collections.<String>emptyList();
```

## 4. Multiple type parameters

```java
public record Pair<K, V>(K key, V value) {}

Map.Entry<Long, String> e = Map.entry(1L, "paid");
```

## 5. Why generics exist (interview)

| Without generics | With generics |
| --- | --- |
| `List` holds `Object`; cast on read | `List<String>` rejects non-`String` at compile time |
| Errors at **runtime** (`ClassCastException`) | Many errors at **compile time** |
| API documents intent poorly | Signatures document element types |

## 6. Backend example

```java
public interface Repository<ID, Entity> {
    Optional<Entity> findById(ID id);
    void save(Entity entity);
}

public class OrderRepository implements Repository<Long, Order> {
    // ID and Entity fixed for this bean
}
```

## Common misconceptions

| Myth | Reality |
| --- | --- |
| "Generics are only for collections" | Any class/method can be generic |
| "`List<String>` and `List` are the same at runtime" | Erasure removes type args; see erasure lesson |
| "I can use `T` in static fields" | Instance type params are not available in static context |


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-05-generics/01-generic-classes-and-methods.md)
- [Generics production playbook](../../../03-production-playbook/core-java/module-05-generics-production-playbook.md)
- [Module index](index.md)
