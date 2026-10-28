---
title: "Lesson 2 — Inheritance, Records, and Equality Design"
description: Subclass equality traps, composition over inheritance, records, shallow immutability.
status: covered
audience: practitioner
tags: [java, equals, records, module-2, lesson-2]
created: 2026-10-20
updated: 2026-10-20
---

# Lesson 2 — Inheritance, Records, and Equality Design

## Overview

Equality is easy on `final` classes with fixed fields. **Inheritance** and **mutable components** are where contracts break in production. **Records** generate `equals`/`hashCode` from components — but shallow immutability still allows bugs.

## 1. Inheritance breaks symmetry or transitivity

Classic `Point` / `ColorPoint` problem (Joshua Bloch):

```java
class Point {
    private final int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Point p)) return false;
        return x == p.x && y == p.y;
    }
    @Override public int hashCode() { return Objects.hash(x, y); }
}

class ColorPoint extends Point {
    private final Color color;
    ColorPoint(int x, int y, Color color) {
        super(x, y);
        this.color = color;
    }
    @Override
    public boolean equals(Object o) {
        if (!(o instanceof ColorPoint cp)) return false;
        return super.equals(o) && color == cp.color;
    }
}
```

```java
Point p = new Point(1, 2);
ColorPoint cp = new ColorPoint(1, 2, Color.RED);
p.equals(cp);  // true — Point sees same coordinates
cp.equals(p);  // false — ColorPoint requires ColorPoint type
// Symmetry violated
```

**Interview point:** do not use inheritance for value equality unless you design a careful `canEqual` / `getClass` strategy. Prefer **composition**.

## 2. Composition over inheritance for value types

```java
record ColoredPoint(Point point, Color color) {}
```

Equality is one level; no subclass asymmetry. Domain models for map keys are often `record OrderKey(long tenantId, String id)`.

## 3. `getClass()` versus `instanceof` in `equals`

| Style | Effect |
| --- | --- |
| `getClass() != obj.getClass()` | Rejects subclasses — symmetric if both sides use same class |
| `instanceof MyType` | Allows subclasses — risky unless `canEqual` pattern used |

For **entity keys**, `final` class + `instanceof` is common.

## 4. Java records — generated equality

```java
public record Employee(long id, String name) {}
```

Compiler generates `equals`/`hashCode` using all components. **All components participate** — you cannot omit a field without wrapping.

```java
var a = new Employee(1L, "Amit");
var b = new Employee(1L, "Amit");
a.equals(b); // true
```

## 5. Shallow immutability and mutable components

```java
public record Team(String name, List<String> members) {
    public Team {
        members = List.copyOf(members); // defensive copy at construction
    }
}
```

Without copying, callers can mutate the list after the record is created:

```java
var list = new ArrayList<>(List.of("a"));
var team = new Team("eng", list);
list.add("b"); // mutates internal state if not copied — equals/hash may change
```

`List.copyOf()` yields an **unmodifiable** list; elements themselves can still be mutable objects if the list holds mutable types.

## 6. Defensive copying and map keys

Do not use mutable objects as record components for **keys** unless fully immutable. Prefer `String`, `Long`, or immutable value types.

## 7. When not to override equality

- Singletons where identity matters.
- Types where only JVM identity should gate synchronization (rare in domain code).
- Entities where ORM manages identity — still use stable **business keys** in APIs.

## Failure scenarios

| Trap | Outcome |
| --- | --- |
| Record with mutable `List` field, no copy | Changed hash/equality after insert into `HashSet` |
| Subclass `equals` without symmetry | Intermittent cache/set bugs |
| Equality includes derived/computed field that changes | Unstable `hashCode` |

## Key takeaways

- Inheritance + `equals` is fragile; prefer composition or `final` classes.
- Records: equality on **all** components; shallow immutability only.
- `List.copyOf` does not deep-freeze mutable elements.
- Choose equality fields deliberately per domain — not every class uses all fields.

## See also

- [Lesson 1 — Contracts](01-equals-and-hashcode-contracts.md)
- [Module 3 — Mutable keys](../module-03-hashmap-internals/04-thread-safety-and-concurrent-patterns.md)
