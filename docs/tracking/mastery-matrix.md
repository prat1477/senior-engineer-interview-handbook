---
title: Mastery Matrix
description: Demonstrated skill scores separate from curriculum coverage and lesson content.
status: in-progress
audience: all
tags: [tracking, mastery]
created: 2026-11-07
updated: 2026-11-08
---

# Mastery Matrix

This page records **demonstrated skill**. It does not replace the other two trackers:

| Tracker | Responsibility |
| --- | --- |
| [PROGRESS.md](../PROGRESS.md) | Curriculum coverage (Covered, In progress, Planned, and the other status words) |
| This matrix | What was actually demonstrated |
| Lessons | Technical knowledge and revision |

Scores:

| Score | Meaning |
| --- | --- |
| 0 | Not assessed |
| 1 | Needs significant help |
| 2 | Understands with some assistance |
| 3 | Independently demonstrates competence |

A topic is **Mastered** only when all four dimensions are 3. One mastered topic does not master a module.

Assessed **2026-11-08**. These scores are that session only. There is no scheduled review date.

| Topic | Concept | Recall | Implementation | Interview | Mastered |
| --- | ---: | ---: | ---: | ---: | --- |
| OOP principles | 3 | 3 | 0 | 2 | No |
| Composition vs inheritance | 3 | 3 | 2 | 2 | No |
| Interfaces vs abstract classes | 3 | 3 | 0 | 2 | No |
| `equals()` and `hashCode()` | 3 | 3 | 3 | 2 | No |
| Immutability and defensive copying | 3 | 3 | 3 | 3 | Yes, for the assessed scope below |
| Java Records | 3 | 3 | 3 | 3 | Yes, for the assessed scope below |

## What each score is based on

- **OOP principles.** Concept and recall were assessed. There was no independent implementation, so Implementation stays 0. Interview score 2 is the questions actually attempted, not every senior follow-up.
- **Composition vs inheritance.** A Spring-style `PaymentService` was applied and reviewed. That is not complete independent implementation mastery, so Implementation stays 2.
- **Interfaces vs abstract classes.** Assessed conceptually. No independent code implementation.
- **`equals()` and `hashCode()`.** An implementation was independently submitted and passed. Interview score 2 does not mean every inheritance or concurrency follow-up was attempted.
- **Immutability and defensive copying.** The immutable `Employee` implementation was independently submitted and passed, including the functional `addRole` update. Interview dimensions reached 3 on the questions and follow-ups actually attempted.
- **Java Records.** The user independently implemented an `Employee` record with compact-constructor validation, request and response records, and a Spring MVC controller using `@Valid` with a `201 Created` response. Runtime application execution and integration testing were not demonstrated.

## Known gaps (not future dates)

- Deep-copying a graph of nested mutable objects was not independently implemented. The immutability implementation score is for the `Employee` / `List<String>` design that passed, not for that graph.
- OOP and interfaces were not implemented independently.
- Composition was reviewed in a Spring-style service, not scored as unaided implementation.
- No topic above is evidence that Module 1 or Module 2 as a whole is mastered.

Lessons: [Module 1](../books/01-engineering-mastery/core-java/module-01-java-object-model/index.md), [Module 2](../books/01-engineering-mastery/core-java/module-02-equals-and-hashcode/index.md).
