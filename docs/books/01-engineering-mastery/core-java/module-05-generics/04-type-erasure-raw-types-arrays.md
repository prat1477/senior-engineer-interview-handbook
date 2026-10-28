---
title: "Lesson 4 — Type Erasure, Raw Types, and Generic Arrays"
description: "Compile-time checks, runtime casts, raw types, and why new T[] is forbidden."
status: covered
audience: practitioner
tags: [[generics, erasure, module-5, lesson-4], mastery]
created: 2026-10-15
updated: 2026-10-18
---

# Lesson 4 — Type Erasure, Raw Types, and Generic Arrays

Compile-time checks, runtime casts, raw types, and why new T[] is forbidden.

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
lesson; the [Interview Companion](../../../02-interview-companion/core-java/module-05-generics/04-type-erasure-raw-types-arrays.md) compresses interview signal without
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

# Lesson 4 — Type Erasure, Raw Types, and Generic Arrays

Java generics are implemented by **type erasure**: type parameters are stripped at compile time; bytecode uses **raw types** and casts inserted by the compiler.

## 1. What erasure means

```java
List<String> names = new ArrayList<>();
// At runtime: ArrayList — no "String" field on the list object
```

The JVM does not retain `List<String>` vs `List<Integer>` as distinct classes (except via reflection metadata on some constructs).

**Implications:**

- Cannot `new T()` or `T.class` without workarounds (`Class<T>` parameter).
- Cannot use `instanceof List<String>` — use `instanceof List<?>` then check elements separately.
- Overloads differing only by type argument are illegal after erasure.

## 2. Bridge methods

The compiler may synthesize bridge methods so overriding respects generic signatures — relevant when overriding generic interfaces.

## 3. Raw types and warnings

```java
List raw = new ArrayList();
raw.add("text");
raw.add(42); // allowed — no compile-time check

Integer n = (Integer) raw.get(0); // ClassCastException at runtime
```

**Raw type** = generic type used without type arguments. Still compiles (legacy) but loses safety.

**Interview trap:** mixing raw and parameterized types can compile with warnings then fail at runtime.

## 4. Why `new T[n]` is generally forbidden

Arrays are **reified** (know element type at runtime); generics are **erased**. Creating `T[]` would break heap integrity:

```java
// Object[] arr = new String[10]; // OK
// String[] s = (String[]) new Object[10]; // generic array creation problem
```

Workarounds: `ArrayList<T>`, or pass `Class<T>` / `IntFunction<T[]>`:

```java
List<String> list = List.of("a", "b");
String[] arr = list.toArray(String[]::new);
```

## 5. Arrays of lists vs lists of arrays

```java
List<String>[] arrayOfLists = new List[10]; // unchecked warning — avoid

List<String[]> listOfArrays = new ArrayList<>();
listOfArrays.add(new String[] {"a", "b"}); // legal, rarely ideal
```

`List<String>[]` is possible with warnings but breaks if you store `List<Integer>` in a slot — erasure vs array component type clash.

## 6. Heap pollution and `@SafeVarargs`

Varargs + generics can create unsafe array types; JDK uses `@SafeVarargs` on trusted APIs like `List.of()`.


## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter](../../../02-interview-companion/core-java/module-05-generics/04-type-erasure-raw-types-arrays.md)
- [Generics production playbook](../../../03-production-playbook/core-java/module-05-generics-production-playbook.md)
- [Module index](index.md)
