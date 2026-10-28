---
title: "Lesson 19 — Thread-Safety Patterns"
description: Immutability, confinement, atomics, check-then-act, compound invariants.
status: covered
audience: advanced
tags: [concurrency, lesson-19]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 19 — Thread-Safety Patterns

## Pattern catalog

| Pattern | Idea |
| --- | --- |
| **Immutability** | No mutation after publish — safest sharing |
| **Thread confinement** | Only one thread touches mutable state |
| **Synchronization** | `synchronized` / locks around invariants |
| **Atomics / concurrent collections** | Single-variable or map-level atomic ops |
| **Defensive copy** | Copy on ingress/egress |
| **Safe publication** | `volatile`, locks, or concurrent utilities before readers see object |

## `final` does not deep-immutable

```java
public final class Config {
    private final List<String> hosts; // final ref — list contents can still mutate if shared
}
```

Defensive `List.copyOf` in constructor.

## Check-then-act

```java
if (!map.containsKey(k)) map.put(k, v); // race
map.putIfAbsent(k, v); // single op atomic on CHM
map.merge(k, 1L, Long::sum);
```

## Compound invariants

Method-level thread safety (`synchronized void transfer`) does not make **workflow** atomic across services without transactions or distributed coordination ([Lesson 22](22-backend-concurrency-scenarios.md)).

## Cross-links

- [M3 — CHM patterns](../books/01-engineering-mastery/core-java/module-03-hashmap-internals/04-thread-safety-and-concurrent-patterns.md)
- [Collections M4 L12](../books/01-engineering-mastery/core-java/module-04-collections/12-concurrent-collections-overview.md)
