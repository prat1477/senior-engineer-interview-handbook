---
title: "Generics — Assessment Answers"
description: Answers and explanations for Module 5 interview practice.
status: draft
audience: advanced
tags: [generics, interview, answers, module-5]
created: 2026-10-17
updated: 2026-10-17
---

# Generics — Assessment Answers

## 1. `List<Integer>` vs `List<Number>`

Generics are **invariant**. Allowing the assignment would let you `add(3.14)` to a list that is actually `List<Integer>`, breaking type safety. Use `List<? extends Number>` to **read** numbers from a `List<Integer>`.

## 2. PECS + JDK example

**Producer Extends, Consumer Super.** `Collections.copy(List<? super T> dest, List<? extends T> src)` — read from `src` (producer), write to `dest` (consumer).

## 3. Runtime

Both are `ArrayList` (or other raw implementation) at runtime; type arguments are erased. `instanceof List<String>` is illegal; casts inserted by compiler enforce types.

## 4. `new T[10]`

Arrays carry runtime element type; `T` is erased to `Object` or bound — creating `T[]` would allow storing wrong types and break the heap. Use `ArrayList` or `toArray(IntFunction)`.

## 5. `nums.add(3)`

**Does not compile.** `? extends Number` is read-only for adds (except `null`).

## 6. `fill(numbers)`

**Compiles.** `List<Number>` is a valid `List<? super Integer>` (consumer super).

## 7. `addAll` with `List<Object>`

`List<String>` is not a `List<Object>` (invariance). Fix:

```java
public static <T> void addAll(List<? super T> dest, List<? extends T> src) {
    dest.addAll(src);
}
```

## 8. Raw map cast

Unchecked cast from `Object`; erasure hides bugs until runtime. Prefer `Map<K,V>` with typed keys/values.

## 9. Raw list + `ClassCastException`

Raw `List` allows any element type; reading as `String` after `add(42)` fails at runtime. Generics move failure to compile time.

## 10. Wildcard parameter

When callers pass lists of **unknown but bounded** subtypes and you only **read** events (or only **write** if super). Example: `void audit(List<? extends PaymentEvent> events)` if you never add to the list.

## Mini-assessment

**A.**

```java
public static <T> void copy(List<? extends T> src, List<? super T> dest) {
    for (T item : src) {
        dest.add(item);
    }
}
```

**B.** No. `Box<Integer>` is not a `Box<Number>` — invariance again (`Comparable` bound does not change that).

**C.** Examples: `new T()`, `T.class`, `instanceof List<String>`, overload on `List<String>` vs `List<Integer>`.
