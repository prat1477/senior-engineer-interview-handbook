---
title: The Three Books — Core Java
description: Map of Engineering Mastery, Interview Companion, and Production Playbook for Core Java.
status: stable
audience: all
tags: [books, architecture, java]
created: 2026-10-18
updated: 2026-10-18
---

# The Three Books — Core Java

Modules **4–9** are delivered as three complementary books (Spark-aligned layout):

| # | Book | Purpose |
| --- | --- | --- |
| 1 | [Engineering Mastery](01-engineering-mastery/index.md) | Canonical depth — concepts, internals, hands-on Java |
| 2 | [Interview Companion](02-interview-companion/index.md) | Derived high-signal revision; practice + answers per module |
| 3 | [Production Playbook](03-production-playbook/index.md) | Runbooks for JVM services (diagnostics, incidents) |

**Canonical rule:** Book 2 never introduces new concepts; it links to Book 1. Book 3 owns procedures.

## Layout

```text
docs/books/
  01-engineering-mastery/core-java/module-NN-slug/NN-lesson.md
  02-interview-companion/core-java/module-NN-slug/   (mirror + practice)
  03-production-playbook/core-java/module-NN-*-production-playbook.md
```

Legacy paths under [`docs/java/`](../java/index.md) are **stubs** that point here.

## Shared domain

Module indexes reference `Employee`, `Order`, and `Payment` records for consistent examples.

## Learning order

1. Read Mastery lessons in module order (4 → 9).
2. Revise with the Companion before mocks.
3. Skim the module Playbook for production debugging scenarios.
