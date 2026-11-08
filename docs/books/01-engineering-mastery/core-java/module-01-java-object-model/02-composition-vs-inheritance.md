---
title: "Lesson 2 — Composition vs Inheritance"
description: IS-A versus HAS-A, payment orchestration, and Template Method versus an interface workflow.
status: covered
audience: practitioner
tags: [java, composition, inheritance, module-1, lesson-2]
created: 2026-11-07
updated: 2026-11-07
---

# Lesson 2 — Composition vs Inheritance

## Overview

Composition and inheritance solve different relationships. Inheritance says the new type **is** the existing type. Composition says the new type **has** collaborators and delegates to them. Payment processing needs both ideas, and neither is universally better.

## 1. IS-A versus HAS-A

| Relationship | Mechanism | Payment example |
| --- | --- | --- |
| IS-A | Inheritance (`extends`) | A card processor is a payment processor only if every caller can treat it as one |
| HAS-A | Composition (fields) | A payment service has a fraud checker and a processor |

If the sentence “a card payment **is a** fraud check” is false, do not extend a fraud-check base class to reuse its code. A payment service **has** a fraud checker.

## 2. Why composition is often more flexible

Collaborators have independent responsibilities. You can replace, decorate, or omit one without rewriting the others.

```java
public interface PaymentProcessor {
    void process(PaymentRequest request);
}

public interface FraudChecker {
    void check(PaymentRequest request);
}
```

`PaymentService` is the orchestrator. It does not implement UPI, card authorization, or fraud rules. It coordinates validation, fraud checking, and payment execution.

```java
public final class PaymentService {
    private final PaymentValidator validator;
    private final FraudChecker fraudChecker;
    private final PaymentProcessor processor;

    public PaymentService(
            PaymentValidator validator,
            FraudChecker fraudChecker,
            PaymentProcessor processor) {
        this.validator = validator;
        this.fraudChecker = fraudChecker;
        this.processor = processor;
    }

    public void pay(PaymentRequest request) {
        validator.validate(request);
        fraudChecker.check(request);
        processor.process(request);
    }
}
```

Dependency injection supplies those three objects. Tests substitute a fake checker that always passes, or a processor that records the call, without subclassing `PaymentService`. A new rail (wallet, net banking) is another `PaymentProcessor`, not a new subclass of the service. That is the extensibility argument: behavior grows by new collaborators, and each collaborator stays testable on its own.

Composition is more flexible when responsibilities vary independently. It is not automatically the better design. A deep pile of one-method delegates can hide a real subtype relationship and scatter a workflow that must not be skipped.

## 3. When inheritance is still appropriate

Use inheritance when all of these hold:

- The subtype is substitutable for the supertype.
- Subtypes share a behavior contract, not just a utility method.
- You need the type system to guarantee a step (a final workflow method that subclasses cannot skip).

“We need three lines from the parent” is not one of those reasons.

## 4. Template Method

An abstract base class can define the workflow and leave the varying steps to subclasses. Mark the workflow `final` so a subclass cannot override it and skip fraud checking.

```java
public abstract class AbstractPaymentProcessor implements PaymentProcessor {
    private final FraudChecker fraudChecker;

    protected AbstractPaymentProcessor(FraudChecker fraudChecker) {
        this.fraudChecker = fraudChecker;
    }

    @Override
    public final void process(PaymentRequest request) {
        validate(request);
        fraudChecker.check(request);
        execute(request);
    }

    protected abstract void validate(PaymentRequest request);

    protected abstract void execute(PaymentRequest request);
}
```

`FraudChecker` is still composition. The base class does not inherit fraud behavior; it **has** a checker. Subclasses such as `CardPaymentProcessor` implement `validate` and `execute` only. Callers still see `PaymentProcessor`.

This fits when every processor in the hierarchy must run the same steps in the same order, and skipping a step would violate the contract.

## 5. Interface plus a separate orchestrator

The alternative is a narrow `PaymentProcessor` interface and a separate `PaymentService` that owns the workflow, as in section 2. Processors stay focused on execution. Validation and fraud stay outside the processor hierarchy.

Choose this when processors should be usable without that workflow (a replay tool that executes a capture without re-running the same checks), or when validation and fraud are cross-cutting services shared by non-processor callers.

| Design | What it locks in | What stays replaceable |
| --- | --- | --- |
| Final template method | Step order inside the processor hierarchy | `FraudChecker` and the abstract steps |
| Interface + orchestrator | Nothing inside the processor | Validator, checker, and processor independently |

## 6. Why a default method cannot be `final`

An interface method cannot be declared `final`. A default method is still overridable. There is no way to publish a default `process` on `PaymentProcessor` and stop an implementor from replacing it and skipping fraud checks.

A `final` instance method is a class feature. If the requirement is “this workflow cannot be overridden,” put it on a class. If the requirement is “callers depend on a contract, and the workflow lives in a service,” keep the interface free of the workflow and orchestrate in `PaymentService`.

## Interview questions

**IS-A or HAS-A for a service that checks fraud and then charges a card?**  
HAS-A. The service has a checker and a processor. A card charge is not a kind of fraud check.

**How do you test the orchestrator?**  
Inject fakes. Assert that `pay` calls validate, then check, then process. You should not need a subclass of `PaymentService` to replace one step.

**When would you still use the abstract processor?**  
When every processor must run a fixed sequence and subclasses are only allowed to fill steps. Composition still supplies `FraudChecker`.

**Can `default void process(...)` plus `final` enforce that sequence?**  
No. Default methods cannot be `final`, so an implementor can override the method and ignore the default body.

## Misconceptions

| Misconception | Correction |
| --- | --- |
| Composition is always better | Choose from substitutability, shared behavior, and what must be extensible |
| Inheritance is only for code reuse | Reuse without IS-A couples unrelated types |
| A default method can freeze a workflow | It can be overridden; a final class method cannot |

## Key takeaways

- IS-A is inheritance. HAS-A is composition.
- `PaymentService` coordinates validation, fraud checking, and `PaymentProcessor` by delegation.
- Template Method uses a **final** workflow and abstract steps; dependencies such as `FraudChecker` are injected.
- An interface cannot mark a default method `final`, so it cannot enforce an unoverrideable workflow.
- The design depends on substitutability, shared behavior, and extension requirements.

## See also

- [Lesson 1 — OOP principles](01-oop-principles.md)
- [Lesson 3 — Interfaces vs abstract classes](03-interfaces-vs-abstract-classes.md)
- [Interview Companion](../../../02-interview-companion/core-java/module-01-java-object-model/02-composition-vs-inheritance.md)
