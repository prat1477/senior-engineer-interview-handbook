---
title: "Lesson 2 - Inheritance, Records, and Equality Design"
description: Subclass equality traps, Java Records, validation, DTOs, and shallow immutability.
status: covered
audience: practitioner
tags: [java, equals, records, module-2, lesson-2]
created: 2026-10-20
updated: 2026-11-08
---

# Lesson 2 - Inheritance, Records, and Equality Design

## Overview

Equality is easy on `final` classes with fixed fields. **Inheritance** and **mutable components** are where contracts break in production. **Records** generate `equals` and `hashCode` from components, but shallow immutability still allows bugs.

This lesson documents the completed Java Records exercise: a validated `Employee` value plus Spring MVC payment request and response DTOs. The implementation was reviewed; runtime application execution and integration testing were not demonstrated.

## 1. Inheritance breaks symmetry or transitivity

Classic `Point` / `ColorPoint` problem:

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
p.equals(cp);  // true
cp.equals(p);  // false: symmetry violated
```

**Interview point:** avoid inheritance for value equality unless a careful `canEqual` / `getClass` strategy is required. Prefer composition.

## 2. Composition over inheritance for value types

```java
record ColoredPoint(Point point, Color color) {}
```

Equality is one level; there is no subclass asymmetry. Domain models for map keys are often `record OrderKey(long tenantId, String id)`.

## 3. `getClass()` versus `instanceof` in `equals`

| Style | Effect |
| --- | --- |
| `getClass() != obj.getClass()` | Rejects subclasses; symmetric if both sides use the same class |
| `instanceof MyType` | Allows subclasses; risky unless a `canEqual` strategy is used |

## 4. Record fundamentals

Java introduced records to make **transparent data carriers** concise and explicit. A record declares that its state is its API: it names the components that describe a value rather than repeating field, constructor, accessor, `equals`, `hashCode`, and `toString` code. Records became a permanent Java feature in Java 16.

```java
public record Employee(long id, String name) {}
```

For each component, the compiler provides a `private final` field, a public accessor with the component name (`id()` and `name()`, not `getId()`), and a canonical constructor whose parameters are all components in declaration order. It also generates `equals()`, `hashCode()`, and `toString()` from those components.

Every record implicitly extends `java.lang.Record`, is implicitly `final`, and cannot extend an arbitrary class. It may implement one or more interfaces. A record therefore suits a stable value or DTO, not an inheritance hierarchy that needs an abstract base class.

### Generated equality

```java
public record Employee(long id, String name) {}

var a = new Employee(1L, "Amit");
var b = new Employee(1L, "Amit");
a.equals(b); // true
```

All components participate in generated equality. Do not use a record when its equality must intentionally omit part of its represented state without first designing that distinction explicitly.

## 5. Immutability is shallow by default

A record's component fields are final, so the record cannot later point a component at a different object. That is **shallow immutability**, not deep immutability: a referenced mutable object can still change.

```java
public record Team(String name, List<String> members) {
    public Team {
        members = List.copyOf(members);
    }
}
```

Without the copy, callers can mutate the list after the record is created:

```java
var list = new ArrayList<>(List.of("a"));
var team = new Team("eng", list);
list.add("b"); // would change internal state without copying
```

`List.copyOf()` produces an unmodifiable list, but it is a **shallow** copy: the list structure is protected, while mutable elements remain mutable.

```java
final class Address {
    private String city;

    Address(String city) { this.city = city; }
    String city() { return city; }
    void moveTo(String city) { this.city = city; }
}

record EmployeeDirectory(List<Address> addresses) {
    EmployeeDirectory {
        addresses = List.copyOf(addresses);
    }
}
```

The list cannot be structurally changed through `addresses()`, but a caller holding an `Address` can call `moveTo`; the record's observable state changes. Deep immutability needs defensive copying of each nested mutable object on input (and, where needed, output), or an immutable nested design. Immutable nested values such as `String`, `BigDecimal`, or an immutable `Address` record can safely be shared.

### Completed `Employee` record

The compact canonical constructor below validates the domain and replaces constructor parameters before the compiler assigns them to component fields. `List.copyOf()` gives the roles list an unmodifiable, shallow defensive copy.

```java
public record Employee(
    int id,
    String name,
    List<String> roles
) {
    public Employee {
        if (id <= 0) {
            throw new IllegalArgumentException(
                "ID must be greater than zero."
            );
        }

        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException(
                "Name cannot be null or blank."
            );
        }

        name = name.strip();

        roles = List.copyOf(
            Objects.requireNonNull(roles, "Roles cannot be null")
        );
    }
}
```

Import `java.util.List` and `java.util.Objects` for this code. `id > 0`, a nonblank `name`, and a non-null `roles` collection are domain invariants. `String.strip()` normalizes surrounding Unicode whitespace after validation.

### Canonical and compact canonical constructors

The generated canonical constructor assigns every component. A developer may declare the full canonical constructor with the same component list and assign fields explicitly, or a **compact canonical constructor** (`public Employee { ... }`) when validation or normalization is sufficient. In a compact constructor, component fields are assigned automatically after the body, so reassigning `name` or `roles` changes the stored value. Constructor validation protects the record wherever Java code constructs it.

## 6. Jackson serialization and deserialization

**Serialization** converts a Java object to a representation such as JSON. **Deserialization** converts JSON into a Java object. Neither word means network transmission: HTTP may carry JSON, but conversion and transport are separate concerns.

Jackson's `ObjectMapper` performs these conversions. In Spring MVC, `HttpMessageConverter` integration selects Jackson for JSON request and response bodies. Jackson supports records: when deserializing, it binds JSON properties to record components and invokes the canonical constructor; when serializing, it reads component accessors.

Useful Jackson annotations include `@JsonProperty` (map a JSON name), `@JsonCreator` (identify a creator when configuration requires it), `@JsonIgnore` (exclude a property), and `@JsonFormat` (control a representation such as a date). These express JSON mapping, not business rules.

Jackson constructing a record does **not** mean Bean Validation passed. Constructor validation enforces Java-level invariants during construction; Jakarta Bean Validation annotations are evaluated only when a validation mechanism is invoked, such as Spring MVC's `@Valid`.

## 7. Spring Boot integration

Records are a natural fit for request and response DTOs: their fixed component list expresses an API contract, and generated accessors keep controller code compact. Spring MVC uses `@RequestBody` to deserialize JSON into a request record, then `@Valid` to trigger Jakarta Bean Validation on its component annotations. Typical constraints are `@NotBlank` for required text, `@NotNull` for a required reference, and `@Positive` for a positive numeric value.

Validation failures use Spring's normal HTTP error handling; a successful controller can choose an explicit status such as `201 Created`. This validation requires `spring-boot-starter-validation`.

Keep persistence separate. Conventional JPA entities usually need an identity lifecycle, ORM proxies, no-argument construction, and mutable relationship management. A record is not a general replacement for them. Map between a persistence entity and record DTOs at the API boundary.

### Completed payment DTOs and controller

```java
public record CreatePaymentRequest(
    @NotBlank(message = "transactionId must not be blank")
    String transactionId,

    @NotNull(message = "amount is required")
    @Positive(message = "amount must be positive")
    BigDecimal amount,

    @NotBlank(message = "paymentMethod must not be blank")
    String paymentMethod
) {}
```

```java
public record PaymentResponse(
    String transactionId,
    String status,
    BigDecimal amount
) {}
```

```java
@PostMapping("/payments")
public ResponseEntity<PaymentResponse> createPayment(
        @Valid @RequestBody CreatePaymentRequest request) {

    PaymentResponse response = new PaymentResponse(
        request.transactionId(),
        "ACCEPTED",
        request.amount()
    );

    return ResponseEntity
        .status(HttpStatus.CREATED)
        .body(response);
}
```

Request flow: Jackson deserializes JSON into `CreatePaymentRequest`; `@Valid` triggers Bean Validation; the controller creates a response; Jackson serializes `PaymentResponse` to JSON. `HttpStatus.CREATED` makes the successful response HTTP **201 Created**. `@Positive` rejects non-positive non-null values, but does not establish presence, so `@NotNull` is required alongside it for `amount`.

## 8. Defensive copying and map keys

Do not use mutable objects as record components for **keys** unless they are fully immutable. Prefer `String`, `Long`, or immutable value types.

## Failure scenarios

| Trap | Outcome |
| --- | --- |
| Record with mutable `List` field, no copy | Changed hash/equality after insert into `HashSet` |
| Nested mutable object behind a copied list | Record state can still change |
| Subclass `equals` without symmetry | Intermittent cache/set bugs |
| Jackson conversion assumed to be validation | Invalid data reaches business logic without `@Valid` |

## Key takeaways

- Inheritance plus `equals` is fragile; prefer composition or final classes.
- Records are final transparent data carriers with equality on all components.
- `List.copyOf()` does not deep-freeze mutable elements.
- Use compact constructors for record-level invariants and `@Valid` for request Bean Validation; they are complementary checks.
- A record DTO is an API contract, not automatically a JPA entity or a deeply immutable object.

## See also

- [Lesson 1 - Contracts](01-equals-and-hashcode-contracts.md)
- [Module 3 - Mutable keys](../module-03-hashmap-internals/04-thread-safety-and-concurrent-patterns.md)
