---
title: "Lesson 3 — Interfaces vs Abstract Classes"
description: Contracts, shared foundations, default methods, and conflict resolution.
status: covered
audience: practitioner
tags: [java, interfaces, abstract-class, module-1, lesson-3]
created: 2026-11-07
updated: 2026-11-07
---

# Lesson 3 — Interfaces vs Abstract Classes

## Overview

An interface publishes a contract. An abstract class is a shared foundation: it can hold state, constructors, and concrete methods, including `final` methods. Java 8 and 9 made interfaces able to carry code, but they did not turn interfaces into classes.

**Memory cues**

- Interface = contract.
- Abstract class = shared foundation.
- Default method = evolving contract.

## Comparison

| Feature | Interface | Abstract class |
| --- | --- | --- |
| Contract | Yes | Can provide one |
| Instance state | No | Yes |
| Constructors | No | Yes |
| Abstract methods | Yes | Yes |
| Concrete methods | Default, static, and private methods | Yes |
| Multiple inheritance | A class may implement multiple interfaces | One superclass |
| Fields | Implicitly `public static final` | Normal instance and static fields |
| Final methods | Not allowed, including default methods | Supported |

## 1. Interface as a contract

```java
public interface PaymentProcessor {
    void process(PaymentRequest request);
}
```

Implementors must provide `process` unless a default method supplies it. Callers can depend on the interface without a shared base class. A type can implement `PaymentProcessor` and `Auditable` together.

## 2. Abstract class as a shared foundation

Use an abstract class when subtypes share fields, construction rules, or a method that must stay `final`.

```java
public abstract class AbstractPaymentProcessor implements PaymentProcessor {
    private final String gatewayId;

    protected AbstractPaymentProcessor(String gatewayId) {
        this.gatewayId = gatewayId;
    }

    public final String gatewayId() {
        return gatewayId;
    }

    @Override
    public abstract void process(PaymentRequest request);
}
```

Instance state and constructors are class features. An interface cannot store `gatewayId` per object.

## 3. Java 8 default and static methods

A **default method** is an instance method with a body on an interface. Existing implementors inherit that body. A **static method** on an interface is called as `InterfaceName.method(...)`. It is not inherited as an overridable instance method.

```java
public interface PaymentProcessor {
    void process(PaymentRequest request);

    default boolean supports(String rail) {
        return false;
    }

    static PaymentProcessor noop() {
        return request -> { };
    }
}
```

## 4. Java 9 private interface methods

Private methods on an interface let default methods share a helper without adding it to the public contract.

```java
public interface PaymentProcessor {
    default void process(PaymentRequest request) {
        trace(request);
    }

    private void trace(PaymentRequest request) {
        // visible only inside this interface
    }
}
```

`private` here means “not part of the API other types implement,” not “instance field.”

## 5. Evolving a contract

**Scenario:** `PaymentProcessor` is implemented by about 100 classes, and you need `supports(String rail)`.

| Change | Result |
| --- | --- |
| New abstract method | Every implementor fails to compile until it implements the method |
| New default method | Existing classes keep compiling and inherit the default; classes that care override it |

That is the backward-compatible use of a default method: extend the contract without a source break. The default must be a sensible behavior for old implementors. A default that silently no-ops a new security check is a bad evolution.

## 6. Conflicting default methods

If two interfaces declare the same default method, a class that implements both must resolve the conflict. The compiler will not pick a winner.

```java
public interface Auditable {
    default String description() {
        return "audit";
    }
}

public interface Loggable {
    default String description() {
        return "log";
    }
}

public final class CardAudit implements Auditable, Loggable {
    @Override
    public String description() {
        return Auditable.super.description();
    }
}
```

`Auditable.super.description()` is the explicit choice. Overriding without calling `super` replaces both defaults.

If one interface is a subinterface and overrides the default, that more specific default can win without a class-level override. Two unrelated interfaces at the same level do not have a more specific method; the class must override.

## 7. One superclass, many interfaces

A class extends one class. It may implement any number of interfaces. That is why payment, audit, and retry policies are often interfaces: a card processor can implement all three without a diamond of superclasses. Shared mutable setup, when it is truly shared, still belongs on one abstract superclass or on a composed collaborator.

## Choosing for payment processors

| Need | Prefer |
| --- | --- |
| Callers and tests depend on “can process a payment” | `PaymentProcessor` interface |
| Several processors must share a `final` workflow and instance fields | Abstract class that implements the interface |
| Add an optional operation without editing 100 classes | Default method, with a safe default |
| Two interfaces already default the same method | Override in the class and call `InterfaceName.super.method()` if one default should be kept |

A common senior shape is both: the interface is the contract injected into `PaymentService`, and an abstract class is an optional foundation for processors that share construction and a locked workflow. Processors that do not share that foundation implement the interface directly.

## Interview questions

**You add a method to an interface with 100 implementors. What breaks?**  
An abstract method breaks compilation of every implementor. A default method does not, as long as the signature does not collide with an existing method.

**Two interfaces define `default void audit()`. The class implements both. What does the compiler require?**  
An overriding `audit()` in the class. Inside it, `InterfaceName.super.audit()` selects one default.

**Interface or abstract class for payment processors?**  
Interface for the substitutable contract. Abstract class only if those processors share state, construction, or a `final` method. Default methods cannot be `final`, so they cannot lock the workflow.

## Misconceptions

| Misconception | Correction |
| --- | --- |
| Interfaces cannot contain code | They can contain default, static, and private methods; they still cannot have instance fields |
| A default method is a final template | It remains overridable, and `final` is illegal on it |
| The compiler merges two default methods | Unrelated conflicts must be overridden |

## Key takeaways

- Interface = contract. Abstract class = shared foundation. Default method = evolving contract.
- Multiple interfaces are allowed; one superclass is allowed.
- Resolve colliding defaults with an override and `InterfaceName.super.method()`.
- Choose the interface, the abstract class, or both from the payment-processor needs above.

## See also

- [Lesson 2 — Composition vs inheritance](02-composition-vs-inheritance.md)
- [Lesson 4 — Immutability and defensive copying](04-immutability-and-defensive-copying.md)
- [Interview Companion](../../../02-interview-companion/core-java/module-01-java-object-model/03-interfaces-vs-abstract-classes.md)
