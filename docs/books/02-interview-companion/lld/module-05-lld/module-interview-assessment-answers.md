---
title: "Module 05 — LLD Assessment Answers"
description: Model answers for LLD Lesson 1 practice.
status: covered
audience: advanced
tags: [lld, interview, answers]
updated: 2026-10-28
---

# Module 05 — LLD Assessment Answers

1. **Clarify:** actors, in/out of scope, persistence, concurrency, money precision, error handling, extensibility expectations, time limit, single vs multi instance.

2. **HLD skip:** single-process/library prompts; state assumptions (one JVM, in-memory) and proceed to classes — don’t design Kafka unless asked.

3. **Workflow:** clarify requirements → scope → domain objects → responsibilities → relationships → trace happy/failure paths → implement APIs → tests → trade-offs (matches Mastery flowchart).

4. **LLD:** class diagram, `quote()` signature. **HLD:** service diagram, DB replication, partition key.

5. **Switch better:** two stable types, rules evolve together, team values clarity, no need for isolated algorithm tests.

6. **Limits:** switch swells with surcharges/discounts; harder to test one rule; calculator keeps changing for combinatorial rules.

7. **OCP:** open for extension, closed for modification **where change is expected** — not a ban on all conditionals.

8. **Not always:** one strategy can cover multiple types, or switch branch suffices; new type might share algorithm with parameter.

9. **Four:** Strategy pattern (interface + impls); selection (pick impl for type); map registry (lookup); Spring DI (discover beans, inject list).

10. **Spring:** component scan registers `@Component` implementations; constructor injection aggregates all `PricingStrategy` beans into `List` at context refresh.

11. **Startup map:** O(1) lookup, validate duplicates once, immutable map for thread-safe reads.

12. **Without editing service:** new `@Component` strategy with unique `supports()` if registry built from injected list.

13. **Fail at startup** — misconfiguration (duplicate key), `IllegalStateException` during registry build.

14. **Request-time** — intentional unsupported capability; map to 400/422 with clear message, not 500 (unless product treats as server misconfig).

15. **Startup** — required capability missing is deploy/config error; fail fast before traffic.

16. **Switch:** few stable rules. **Map registry:** several algorithms, non-Spring or manual wiring. **Spring list:** many beans, plugin-style discovery, startup validation.

17. **Maps cost** indirection and validation; switches are easier to read when change is rare — senior choice matches change rate.

### Whiteboard

| # | Answer |
| --- | --- |
| A | Interface `PricingStrategy`; impls; `ParkingService` holds `Map<VehicleType, PricingStrategy>` |
| B | Scan → inject list → foreach put in map → duplicate → throw → context fails |
| C | Client POST type+duration → service lookup → strategy.calculateFee → return BigDecimal |

18. **Weekend surcharge:** if only fee math changes, extend strategy or add `WeekendPricingStrategy` decorator/wrapper; if cross-cutting, policy object composed into strategy — avoid giant switch. Mention config-driven rules if product toggles often.

19. **Unit test:** instantiate `CarPricingStrategy` directly, assert `calculateFee` for known duration; registry test with manual list, no Spring.

20. **Plugins:** Spring `@Configuration` + `@ComponentScan` on plugin package, or `ServiceLoader`, or conditional beans; still validate duplicate keys at startup; versioned SPI contract.
