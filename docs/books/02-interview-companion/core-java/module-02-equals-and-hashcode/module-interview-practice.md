---
title: Module 2 — Interview Practice
description: equals/hashCode drills for senior interviews.
status: covered
audience: advanced
tags: [interview, module-2]
created: 2026-10-20
updated: 2026-10-20
---

# Module 2 — Interview Practice

Answers: [module-interview-assessment-answers.md](module-interview-assessment-answers.md). Depth: [Mastery](../../../01-engineering-mastery/core-java/module-02-equals-and-hashcode/index.md).

## Quick-revision checklist

- [ ] Five `equals` contract properties
- [ ] `equals` ⇒ equal `hashCode` (not converse)
- [ ] Override both methods together
- [ ] `Objects.equals` for fields
- [ ] Immutable map keys
- [ ] Record shallow immutability

## Conceptual

1. What is the contract of `equals()`?
2. Why must equal objects have equal hash codes?
3. Can unequal objects share a hash code?
4. What happens when `equals()` is overridden but `hashCode()` is not?
5. Why are mutable `HashMap` keys dangerous?
6. How can inheritance violate symmetry?
7. What equality do records generate by default?

## Output prediction

8. After `BadKey` example (Lesson 1), what does `map.get(k2)` return when `k1.equals(k2)` but `hashCode` not overridden?

9. Given `record R(List<String> xs)`, caller mutates list after insert into `HashSet` — what can go wrong?

## Scenario

10. Team uses `Order` entity with `@Id Long id` as `HashMap` key but `equals` includes mutable `status`. What production symptom do you expect?
