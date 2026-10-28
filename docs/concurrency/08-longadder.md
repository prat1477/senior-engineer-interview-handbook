---
title: "Lesson 8 — LongAdder"
description: Striped counters for high-contention increments.
status: covered
audience: advanced
tags: [concurrency, lesson-8]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 8 — `LongAdder`

## When to use

Many threads incrementing same counter — reduces CAS contention vs single `AtomicLong`.

```java
LongAdder hits = new LongAdder();
hits.increment();
long total = hits.sum(); // not atomic with concurrent adds — approximate for metrics OK
```

## Trade-off

`sum()` is not a global atomic snapshot under heavy concurrent updates — fine for metrics, not for strict financial ledger without stronger model.

## Cross-links

- [Lesson 22 — CHM + LongAdder](22-backend-concurrency-scenarios.md)
