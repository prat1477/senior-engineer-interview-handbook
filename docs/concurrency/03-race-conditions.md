---
title: "Lesson 3 — Race Conditions"
description: Read-modify-write, lost updates, data races.
status: covered
audience: advanced
tags: [concurrency, lesson-3]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 3 — Race Conditions

## Data race

Two threads access same variable, at least one write, no happens-before → undefined behavior for non-volatile/non-atomic fields.

## Lost update

```java
count++; // not atomic — read, add, write
```

Fix: `AtomicInteger`, synchronization, or confinement.

## Cross-links

- [Lesson 7 — Atomics](07-atomics-and-cas.md)
- [Lesson 22D — DB lost updates](22-backend-concurrency-scenarios.md)
