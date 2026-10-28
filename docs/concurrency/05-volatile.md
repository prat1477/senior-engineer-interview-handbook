---
title: "Lesson 5 — volatile"
description: Visibility, publication, limits for compound ops.
status: covered
audience: advanced
tags: [concurrency, lesson-5]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 5 — `volatile`

## Guarantees

Writes visible to subsequent reads by other threads (happens-before via volatile semantics).

## Use cases

- Status flags (`shutdown`, `initialized`)
- Single-writer publication patterns (with care)

## Not for

`i++` on volatile — still racy. Use atomics or locks.

## Cross-links

- [Lesson 2 — JMM](02-java-memory-model.md)
