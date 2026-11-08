---
title: Day 14 — Rapid Revision Plan
description: Question banks and timed drills — populate as you study.
status: planned
audience: advanced
tags: [revision, day-14]
created: 2026-10-15
updated: 2026-11-08
---

# Day 14 — Rapid Revision Plan

**Status: Planned.** Question lists grow as topics move to **Covered** in [PROGRESS.md](../PROGRESS.md).

## Targets (from roadmap)

| Bucket | Count | Source when ready |
| --- | ---: | --- |
| Java questions | 50 | Core Java modules + [quick reference](../90-reference/interview-quick-reference.md) |
| Distributed systems | 20 | [distributed-systems](../distributed-systems/index.md) |
| Kafka | 20 | [kafka](../kafka/index.md) |
| Spark / lakehouse | 20 | Spark Handbook + [data-engineering](../data-engineering/index.md) |
| High-level design | 2 | Payment + data-platform scenarios |
| Coding problems | 2 | [DSA tracker](../dsa/index.md) |
| Behavioral | core set | [behavioral](../behavioral/index.md) |

## Revision status legend

- **Confident** — can explain trade-offs without notes
- **Needs another pass** — partial recall
- **Not covered** — still Planned in progress tracker

## Question banks

Banks are **intentionally empty** until authored per topic. Start with Collections via [interview quick reference](../90-reference/interview-quick-reference.md).

### Core Java memory triggers (2026-11-07, 3–5 minutes)

Cues only. Depth: [Module 1](../books/01-engineering-mastery/core-java/module-01-java-object-model/index.md) and [Module 2 contracts](../books/01-engineering-mastery/core-java/module-02-equals-and-hashcode/01-equals-and-hashcode-contracts.md).

- **A PIE** — OOP principles.
- **IS-A vs HAS-A** — inheritance vs composition.
- Interface = contract; abstract class = shared foundation.
- **RSTCN** — equals contract.
- Equal objects must have equal hash codes.
- Never mutate `HashMap` key fields used by equality.
- `final` reference is not an immutable object.
- `List.copyOf()` = unmodifiable shallow copy.
- Immutable nested objects can safely be shared.
- Immutable update = return a new object.
- Record = transparent data carrier.
- Record components = private final fields.
- Compact constructor = validate and normalize.
- Jackson = JSON/object conversion.
- `@Valid` = trigger Bean Validation.
- Entity = persistence model.
- Record DTO = API contract.

### Collections (available now)

Use [Interview Companion — Module 4](../books/02-interview-companion/core-java/module-04-collections/index.md) (**30-second revision** and **Must remember** per lesson), then drill [module practice](../books/02-interview-companion/core-java/module-04-collections/module-interview-practice.md). Depth: [Engineering Mastery — Module 4](../books/01-engineering-mastery/core-java/module-04-collections/index.md).

## Timed drill log

| Date | Activity | Result |
| --- | --- | --- |
| _none_ | | |
