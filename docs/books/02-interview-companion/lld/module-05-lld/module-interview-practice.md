---
title: "Module 05 — LLD Interview Practice"
description: Drill questions for LLD Lesson 1.
status: covered
audience: advanced
tags: [lld, interview, practice]
updated: 2026-10-28
---

# Module 05 — LLD Interview Practice (Lesson 1)

Answers: [module-interview-assessment-answers.md](module-interview-assessment-answers.md).

## Scope and workflow

1. List five things you clarify in the first five minutes of an LLD interview.

2. When is a full HLD **unnecessary** before LLD?

3. Draw or describe the LLD workflow from requirements to trade-offs (nine steps).

4. LLD vs HLD — give one artifact each that belongs only on that side.

## Abstraction and Strategy

5. When is a `switch` on `VehicleType` the **better** choice than Strategy?

6. Name two limitations of a growing switch-based parking fee calculator.

7. State the Open/Closed Principle without claiming every `if` violates it.

8. Does every new `VehicleType` **require** a new strategy class? Explain.

## Spring and registry

9. What four concepts are often confused? (Strategy, selection, map, Spring)

10. How does Spring provide `List<PricingStrategy>` to `ParkingService`?

11. Why build `Map<VehicleType, PricingStrategy>` at startup instead of iterating the list per request?

12. When can you add a new pricing rule **without** editing `ParkingService`?

## Validation

13. Duplicate `CarPricingStrategy` and `CarPromoPricingStrategy` both returning `CAR` — when should the app fail?

14. Request for `TRUCK` when only CAR and MOTORCYCLE are supported — startup failure or request-time? HTTP shape?

15. Missing required `MOTORCYCLE` strategy in config — prefer startup or first request failure? Why?

## Judgment

16. Complete the table: switch vs map registry vs Spring-discovered strategies — one row each for “when prefer.”

17. Why are maps not automatically better than switches?

## Whiteboard (30s each)

| # | Task |
| --- | --- |
| A | Mermaid or boxes: Strategy + registry + ParkingService |
| B | Startup validation flow for duplicate keys |
| C | Sequence: client → ParkingService → strategy → BigDecimal quote |

## Scenario

18. Interviewer asks “Design parking fees with weekend surcharge.” Where do you put weekend logic — switch, new strategy, decorator, or config? Defend trade-offs.

19. How do you unit-test pricing without `@SpringBootTest`?

20. Senior follow-up: “We deploy plugins as separate JARs.” What changes in your design?
