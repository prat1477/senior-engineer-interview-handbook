---
title: "Lesson 7 — Atomics and CAS"
description: Compare-and-swap, AtomicInteger, ABA caveat.
status: covered
audience: advanced
tags: [concurrency, lesson-7]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 7 — Atomics and CAS

## CAS loop

```java
AtomicInteger counter = new AtomicInteger();
counter.incrementAndGet(); // CAS-based
```

Hardware compares memory, swaps if expected value matches — retry on failure.

## Limits

- Only safe for **well-defined** atomic variables — not arbitrary invariants spanning fields.
- High contention → CAS spin waste — consider `LongAdder`.

## Cross-links

- [Lesson 8 — LongAdder](08-longadder.md)
- [Lesson 19 — Patterns](19-thread-safety-patterns.md)
