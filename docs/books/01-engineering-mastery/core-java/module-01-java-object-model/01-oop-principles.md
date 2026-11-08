---
title: "Lesson 1 — OOP Principles"
description: Abstraction, polymorphism, inheritance, and encapsulation with backend payment examples.
status: covered
audience: practitioner
tags: [java, oop, module-1, lesson-1]
created: 2026-11-07
updated: 2026-11-07
---

# Lesson 1 — OOP Principles

## Overview

The four OOP principles are a design vocabulary, not four independent language features. In backend services they show up as contracts, substitutable implementations, type hierarchies that actually model the domain, and objects that protect their invariants.

**Memory aid — A PIE**

| Letter | Principle | Cue |
| --- | --- | --- |
| **A** | Abstraction | Hide implementation |
| **P** | Polymorphism | Multiple implementations |
| **I** | Inheritance | IS-A |
| **E** | Encapsulation | Protect state |

## 1. Abstraction

Abstraction exposes the operations a caller needs and hides how those operations are performed.

A Java interface is the usual contract at a service boundary. Callers depend on the contract. The class that implements it can change storage, vendor SDKs, or validation rules without forcing every caller to change.

```java
public interface PaymentProcessor {
    PaymentResult process(PaymentRequest request);
}
```

In a backend service, `PaymentService` depends on `PaymentProcessor`. UPI, card, and wallet processors stay behind that contract. Controllers, fraud checks, and audit code do not import a concrete processor. That is abstraction: the necessary operation is visible; the gateway, retries, and payload mapping are not.

Abstraction is not “fewer lines of code.” A leaky abstraction still forces callers to know the implementation (vendor error codes, mutable request objects, connection handles).

## 2. Polymorphism

Polymorphism is one contract with multiple implementations. The caller writes code against the contract. The runtime type supplies the behavior.

```java
public interface PaymentProcessor {
    void process(PaymentRequest request);
}

public final class UpiPaymentProcessor implements PaymentProcessor {
    @Override
    public void process(PaymentRequest request) {
        // UPI collect / intent flow
    }
}

public final class CardPaymentProcessor implements PaymentProcessor {
    @Override
    public void process(PaymentRequest request) {
        // Card authorization and capture
    }
}
```

```java
PaymentProcessor processor = new UpiPaymentProcessor();
processor.process(request); // runtime type is UpiPaymentProcessor
```

This is **runtime polymorphism**: the method that runs is selected from the object's actual class, not from the variable's declared type.

**Interface-based dependency injection** uses the same idea. A Spring (or manual) container injects a `PaymentProcessor`. Production injects `CardPaymentProcessor`. A test injects a fake that records the request and does not call a bank. The service code does not branch on processor class names.

```java
public final class PaymentService {
    private final PaymentProcessor processor;

    public PaymentService(PaymentProcessor processor) {
        this.processor = processor;
    }

    public void pay(PaymentRequest request) {
        processor.process(request);
    }
}
```

Overloading (`process(PaymentRequest)` vs `process(String)`) is compile-time selection. Interview answers about “polymorphism” in service design should mean overriding through a shared contract, not method overloading.

## 3. Inheritance

Inheritance models an **IS-A** relationship: a subclass is a kind of the superclass and can stand in for it (**substitutability**). The subclass reuses and specializes behavior by overriding methods.

```java
public abstract class Notification {
    public final String renderHeader(String title) {
        return "NOTICE: " + title;
    }

    public abstract String body();
}
```

Use inheritance when:

- The subtype truly is a kind of the supertype.
- Callers can use the subtype anywhere the supertype is expected without breaking invariants (Liskov substitution).
- Shared behavior is part of that type's contract, not an accidental helper.

Do not inherit only to reuse a few methods. That couples unrelated types, forces an IS-A story that is false, and makes later changes to the base class break subclasses. Prefer a collaborator (composition) when the relationship is **HAS-A**. Lesson 2 works the payment example in detail.

Method overriding replaces superclass behavior for the runtime type. A subclass that overrides a method and weakens its preconditions or breaks its postconditions is not substitutable, even if the code compiles.

## 4. Encapsulation

Encapsulation keeps state private and changes it only through methods that preserve invariants.

```java
public final class AccountBalance {
    private long minorUnits;

    public AccountBalance(long minorUnits) {
        if (minorUnits < 0) {
            throw new IllegalArgumentException("balance must be >= 0");
        }
        this.minorUnits = minorUnits;
    }

    public long minorUnits() {
        return minorUnits;
    }

    public void debit(long amount) {
        if (amount <= 0 || amount > minorUnits) {
            throw new IllegalArgumentException("invalid debit");
        }
        minorUnits -= amount;
    }
}
```

There is no `setMinorUnits`. A caller cannot put the balance negative or skip the debit rules. Getters that return the raw value are fine here because `long` is a primitive copy. Getters that return internal mutable objects are a separate problem (Lesson 4).

Encapsulation is not “make every field private and generate setters.” Unrestricted setters publish the representation and let callers break invariants the constructor established.

## Interview questions

**Name the four principles with one backend example each.**  
Abstraction: `PaymentProcessor` hides the gateway. Polymorphism: UPI and card processors share that interface. Inheritance: only when a type truly IS-A and stays substitutable. Encapsulation: `AccountBalance` accepts debits only through a method that protects a non-negative balance.

**Where does dependency injection sit?**  
It is a way to supply a polymorphic implementation of an abstraction. The service depends on the contract; the container or test chooses the class.

**When is inheritance the wrong reuse tool?**  
When the new type merely needs a helper method from an existing class and is not substitutable for that class. Composition keeps the reused behavior as a dependency.

**What does encapsulation protect that a public field does not?**  
Invariants. A public `minorUnits` can be set to a negative value with no debit rule applied.

## Misconceptions

| Misconception | Correction |
| --- | --- |
| Four principles are four keywords | They are design obligations; `interface`, `extends`, and `private` are mechanisms |
| Any `extends` is good reuse | Inheritance claims IS-A and substitutability |
| Setters are encapsulation | Setters that accept any value do not protect invariants |

## Key takeaways

- **A PIE:** abstraction hides implementation, polymorphism supplies multiple implementations, inheritance is IS-A, encapsulation protects state.
- Prefer an interface at a service boundary when callers should not know the processor.
- Runtime polymorphism plus constructor injection is how backend code stays testable.
- Inherit for a real subtype relationship. Encapsulate so invariants survive callers.

## See also

- [Lesson 2 — Composition vs inheritance](02-composition-vs-inheritance.md)
- [Lesson 3 — Interfaces vs abstract classes](03-interfaces-vs-abstract-classes.md)
- [Interview Companion](../../../02-interview-companion/core-java/module-01-java-object-model/01-oop-principles.md)
