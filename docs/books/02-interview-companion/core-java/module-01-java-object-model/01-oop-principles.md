---
title: "Companion 1 — OOP Principles"
description: Interview recall for abstraction, polymorphism, inheritance, and encapsulation.
status: covered
audience: advanced
tags: [interview, companion, java]
updated: 2026-11-07
---

# Companion 1 — OOP Principles

**Canonical source:** [Mastery lesson](../../../01-engineering-mastery/core-java/module-01-java-object-model/01-oop-principles.md).

**Cheat sheet:** [Module visual quick reference](module-visual-quick-reference.md).

## Definition

A PIE: hide the implementation, swap implementations, inherit only for IS-A, and protect invariants.

## Must remember

- Abstraction is the contract callers see (`PaymentProcessor`).
- Polymorphism is the runtime implementation (UPI vs card) plus injection.
- Inheritance requires substitutability, not just reuse.
- Encapsulation is private state changed only through invariant-preserving methods.

## Interview traps

- Treating setters as encapsulation.
- Calling overloading the same thing as service-level polymorphism.

## Interview flow

```mermaid
flowchart LR
  api[Abstraction] --> impl[Polymorphic processor]
  impl --> state[Encapsulated invariants]
```

## Scenario bite

`PaymentService` takes a `PaymentProcessor`. Tests pass a fake. Production passes `CardPaymentProcessor` or `UpiPaymentProcessor` without changing `pay`.

## Decision table

| Situation | Prefer |
| --- | --- |
| Callers must not know the gateway | Interface abstraction |
| New behavior is a different gateway | Another implementation |
| Type is not really a subtype | Stop; do not `extends` for reuse |
| Balance must stay non-negative | Method that enforces the rule, no open setter |

## Explain aloud (whiteboard)

1. Name A PIE in one line each.
2. Show interface injection for payments.
3. Say when inheritance fails substitutability.

## 30-second revision

- A PIE. Interface at the boundary. Runtime type does the work. IS-A or don't inherit. Private state, no unrestricted setters.

## Memory hook

- **A PIE** — Abstraction, Polymorphism, Inheritance, Encapsulation.

## Cross-links

- [Module visual quick reference](module-visual-quick-reference.md)
