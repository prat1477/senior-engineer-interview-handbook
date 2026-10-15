---
title: Spark Handbook Cross-Reference
description: Links to canonical Spark lessons already completed in the Spark Engineering Handbook.
status: stable
audience: advanced
tags: [spark, cross-reference]
created: 2026-10-15
updated: 2026-10-15
---

# Spark Handbook Cross-Reference

Canonical content lives in the parent repo Spark Handbook. Paths are relative to this file.

## Completed modules (reference during interview prep)

| Module | Topic | Entry |
| --- | --- | --- |
| 1 | Spark architecture & execution | [Module 1 index](../../../spark-engineering-handbook/docs/books/01-engineering-mastery/module-01-spark-architecture/index.md) |
| 2 | APIs & execution internals | [Module 2 index](../../../spark-engineering-handbook/docs/books/01-engineering-mastery/module-02-apis-and-execution-internals/index.md) |

Modules 3–10 in your study plan align with lessons across Module 1–2 and extended mastery TOC — use [Engineering Mastery book index](../../../spark-engineering-handbook/docs/books/01-engineering-mastery/index.md) as the authoritative map for:

- Data abstractions, execution engine, Catalyst, shuffle, joins, partitioning, AQE, memory, caching/checkpointing.

## Remaining interview focus (author in this handbook)

- [Delta Lake](index.md) — Module 12
- Structured Streaming — Module 13
- Databricks / Unity Catalog — Module 14

## Production debugging scenarios (planned here)

- Driver memory pressure during wide collects or broadcast misuse
- Reading physical plans (`explain`) for unexpected shuffles
- Too many concurrent Spark jobs on shared cluster
- Shuffle-heavy stages and spill to disk
- Executor failures and stage retries
- Dynamic allocation oscillation

Do not copy Spark lesson bodies — link and add **interview framing** only when lessons are written.
