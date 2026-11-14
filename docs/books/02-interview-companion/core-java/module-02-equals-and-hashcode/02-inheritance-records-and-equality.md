---
title: "Companion 2 - Inheritance and records"
description: Interview recall for inheritance, records, validation, and DTOs.
status: covered
audience: advanced
tags: [interview, companion, java]
updated: 2026-11-08
---

# Companion 2 - Inheritance and records

**Canonical source:** [Mastery lesson](../../../01-engineering-mastery/core-java/module-02-equals-and-hashcode/02-inheritance-records-and-equality.md).

**Cheat sheet:** [Module visual quick reference](module-visual-quick-reference.md).

## Definition

Equality across inheritance is fragile; records generate `equals` and `hashCode` from components.

Records are **transparent data carriers**: the header defines their state and API. Component fields are `private final`; the compiler provides accessors, a canonical constructor, and component-based `equals`, `hashCode`, and `toString`.

## Must remember

- Subclass fields can break equality symmetry; prefer composition.
- Records are shallowly immutable. `List.copyOf()` is an unmodifiable shallow copy, not a deep copy.
- A record is implicitly final, extends `java.lang.Record`, can implement interfaces, and cannot extend an abstract class.
- Jackson conversion and Bean Validation are separate operations.

## Interview traps

- Parent and child `instanceof` equality can break symmetry.
- Final component references do not make nested mutable objects immutable.
- Jackson deserialization does not prove Bean Validation ran.
- Serialization converts an object to JSON; HTTP transport sends that JSON.
- `Collections.unmodifiableList(input)` is a view; `List.copyOf(input)` is an unmodifiable structural snapshot.

## Decision table

| Situation | Prefer |
| --- | --- |
| Need a fixed API contract / DTO | Record |
| Need a conventional JPA entity | Regular entity class; map to a record DTO |
| Need a subclass hierarchy | Composition, sealed types, or a regular class hierarchy |

## Records interview revision

| Question | Concise answer | Memory trigger |
| --- | --- | --- |
| Why were records introduced? | To model transparent data carriers without repetitive value-class boilerplate. | Header = state/API |
| Are records deeply immutable? | No. Fields are final, but referenced mutable objects can change. | Final reference != frozen graph |
| Can records implement interfaces? | Yes. They cannot extend arbitrary or abstract classes. | Implements yes; extends no |
| Why use records for DTOs? | Fixed API contract, concise accessors, value semantics, and Jackson support. | DTO = boundary value |
| Why avoid conventional JPA entity mapping with records? | Entities usually need ORM lifecycle, proxies, identity, and mutable relationships. | Entity = persistence model |
| How does Jackson deserialize a record? | It binds JSON component names and invokes the canonical constructor. | JSON -> canonical constructor |
| Constructor validation vs Bean Validation? | Constructor checks invariants whenever constructed; Bean Validation checks annotations when explicitly triggered. | Constructor always; `@Valid` triggers |
| What does `@Valid` do? | In Spring MVC it triggers Jakarta Bean Validation for the request object. | `@Valid` = validate now |
| Serialization vs network transmission? | Serialization creates JSON; HTTP transport sends it. | Convert != transmit |

`@NotNull` and `@Positive` are both needed for a required positive `BigDecimal`: `@Positive` does not make a missing value present.

## Explain aloud

1. Show the inheritance symmetry break and recommend composition.
2. Describe records as final transparent data carriers with component equality.
3. Explain shallow immutability and `List.copyOf()`.
4. Trace Spring MVC: Jackson deserializes, `@Valid` validates, Jackson serializes the response.

## 30-second revision

- Inheritance plus `equals` is a trap; records fit simple values and DTO contracts.
- Compact constructor validates and normalizes. `@Valid` triggers Bean Validation.
- DTO is an API contract; entity is a persistence model.

## Canonical-constructor recall

| Form | Remember |
| --- | --- |
| Implicit canonical | Compiler takes every component, in declaration order. |
| Explicit canonical | Repeat full signature and assign every component field. |
| Compact canonical | Validate/normalize parameters; compiler assigns component fields after body. |

**Exercise — attempt independently:**

```java
public record Employee(String name, int age) {
    public Employee {
        if (age < 18) throw new IllegalArgumentException("Underage");
        age = 18;
    }
}
System.out.println(new Employee("John", 25).age());
```

Explain the output and why parameter reassignment is legal while direct component-field assignment
is not. Do not look up the answer before attempting it.

**Memory tricks:**

- **Final fields do not make referenced objects immutable.**
- **Copy the collection, then make its elements immutable for deep immutability.**

## Memory hook

- **SYM** - Symmetry first.
- **RECORD** - Representation, Equality, Canonical constructor, Object graph shallow, Request DTO.

## Cross-links

- [Module visual quick reference](module-visual-quick-reference.md)
