---
title: "Lesson 5 — Generics Interview Practice"
description: Conceptual, code, and scenario questions for senior backend interviews.
status: draft
audience: advanced
tags: [generics, interview, module-5, lesson-5]
created: 2026-10-17
updated: 2026-10-17
---

# Lesson 5 — Generics Interview Practice

Attempt each question before opening [answers](module-interview-assessment-answers.md).

## Conceptual

1. Why is `List<Integer>` not assignable to `List<Number>`?
2. State PECS in one sentence and give a JDK example method that uses both extends and super wildcards.
3. What happens at runtime for `List<String>` vs `List<Integer>`?
4. Why does Java forbid `new T[10]` in a generic class?

## Code output / compile-time

5. Will this compile? If yes, what prints?

```java
List<? extends Number> nums = List.of(1, 2);
nums.add(3);
```

6. Will this compile?

```java
void fill(List<? super Integer> sink) {
    sink.add(1);
}
List<Number> numbers = new ArrayList<>();
fill(numbers);
```

7. What is wrong with this API and how would you fix it?

```java
public static void addAll(List<Object> dest, List<Object> src) {
    dest.addAll(src);
}
// Caller has List<String> strings ...
```

## Debugging / traps

8. A method returns `(T) map.get(key)` from a raw `HashMap`. What interview concern do you raise?

9. Explain why `Arrays.asList(1, 2, 3)` infers `List<Integer>` but mixing with raw `List` in legacy code caused production `ClassCastException`.

## Scenario (senior)

10. You expose `void process(List<PaymentEvent> events)` but callers have `List<? extends PaymentEvent>` from different modules. When do you change the parameter to a wildcard?

## Mini-assessment (10 minutes)

| # | Question |
| --- | --- |
| A | Write `copy` with PECS: source list of subtypes of `T`, destination that accepts `T`. |
| B | Given `class Box<T extends Comparable<T>>`, can `Box<Integer>` be used where `Box<Number>` is expected? Why? |
| C | Name one thing you **cannot** do because of erasure. |

Answers: [06-interview-assessment-answers.md](module-interview-assessment-answers.md).
## Whiteboard (use the cheat sheet)

1. Draw the module flowchart from the visual quick reference without notes.
2. Give one production scenario and the decision-table row you would choose.
3. Name one interview trap and the correction.
