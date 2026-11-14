---
title: "Lesson 9 — Practice: transfer the design"
description: Coverage against the LLD curriculum, the gaps to drill, and the problems worth practicing after the parking lot.
status: in_progress
audience: practitioner
tags: [lld, module-05, lesson-9, practice, mastery]
updated: 2026-11-02
---

# Lesson 9 — Practice: transfer the design

Lessons 1–8 and 10 already walk one parking lot from requirements through `SKIP LOCKED`. This lesson does not redesign that lot. It records what the curriculum asked for, what those lessons already cover, and the drills that exercise a **different** skill.

**Companion:** [Book 2 — Lesson 9](../../../02-interview-companion/lld/module-05-lld/09-practice-transfer-problems.md)

**Use with:** [Lesson 5 pattern guide](05-abstraction-composition-and-pattern-selection.md), [Lesson 7 state](07-state-modeling-and-transitions.md), [Lesson 8 failure](08-error-handling-and-failure-modeling.md), [Lesson 10 performance](10-performance-scalability-and-optimization.md). Concurrency mechanics stay in the [concurrency track](../../../../concurrency/index.md). REST, JPA, and API versioning stay on the [Spring roadmap](../../../../spring-microservices/index.md).

---

## Learning outcomes

- Reconstruct the parking lot in one sitting without opening Lessons 2–8.
- Name which SOLID points and patterns the parking lot never forced, and when each is justified.
- Run one new problem (rate limiter, notifications, or inventory) through the same ten-step review.
- Refuse a second full design that only renames parking spots.

---

## 1. Curriculum versus this handbook

The pasted curriculum numbers lessons differently. This module split foundations across Lessons 1–4 and taught the parking lot as the running example instead of saving it for a final chapter.

| Curriculum | What it asks | Handbook | Status |
| --- | --- | --- | --- |
| Phase 1 — LLD fundamentals | What interviews score, LLD vs HLD, requirements, scope, assumptions | [Lesson 1](01-lld-foundations-what-senior-lld-interviews-evaluate.md), [Lesson 2](02-requirement-clarification-and-scope.md) | Covered |
| Phase 1 — domain modeling | Entities, value data, responsibilities, composition vs inheritance, interfaces | [Lesson 3](03-domain-modeling-and-class-responsibilities.md), [Lesson 4](04-encapsulation-invariants-and-tell-dont-ask.md), [Lesson 5](05-abstraction-composition-and-pattern-selection.md) | Covered. UML relationship names are in §3 below, not a separate diagramming lesson |
| Phase 2 — SOLID | All five principles, cohesion, coupling, smells, extensibility without theater | SRP and cohesion in Lesson 3. Encapsulation in Lesson 4. OCP and DIP in [Lesson 6](06-ocp-and-dip.md). LSP and ISP in §2 | Partial — drill LSP and ISP here |
| Phase 3 — patterns I | Strategy, Factory Method, Abstract Factory, Builder, Observer | Strategy in Lessons 1 and 5–6. Factory, Builder, Observer as short entries in Lesson 5 | Partial — Abstract Factory is in §4 |
| Phase 3 — patterns II | Adapter, Decorator, Template Method, State, Command, Chain of Responsibility, Proxy, Repository | Adapter, Decorator, State, registry in Lesson 5. State machines in Lesson 7. Repository as a persistence boundary in Lesson 8 | Partial — Template Method, Command, chain, and Proxy are in §4 |
| Phase 4 — REST and Spring | Resources, status codes, DTOs, layers, validation, auth boundary, pagination | HTTP mapping of domain failures in Lesson 8. Layer talk in Lessons 3 and 8 | Boundary only. Full API design is the Spring track, not a second LLD course |
| Phase 4 — persistence and tests | Transactions, JPA, versioning, idempotency, unit vs integration tests | Transactions, optimistic and pessimistic locks, idempotency keys, outbox, saga in Lessons 7, 8, and 10 | Covered for interview LLD. JPA pitfalls, versioning, and the test pyramid stay on the Spring track |
| Phase 5 — concurrency in LLD | Invariants, races, one JVM vs many instances, locks, duplicate requests | Lessons 4, 7, 8, and 10, plus concurrency Lessons 1–24 | Covered. Do not restudy the concurrency module inside LLD |
| Phase 6 — end-to-end problems | Parking lot plus a curated set, not every famous problem | Parking lot is Lessons 2–8 and 10. Other problems are §6 | This lesson |
| Phase 7 — performance | Bottlenecks, indexing, `SKIP LOCKED`, short transactions, ordering trade-off | [Lesson 10](10-performance-scalability-and-optimization.md) | Covered |

---

## 2. LSP and ISP

The parking lot used SRP, OCP, and DIP. These two are the ones an interviewer can still catch you on.

**Liskov Substitution.** A subtype must be usable anywhere the supertype is expected, including the failure behavior. `CarSpot extends ParkingSpot` that throws on `release` for bikes breaks callers that only know `ParkingSpot`. Prefer one `ParkingSpot` and a `canFit` rule (Lesson 5). Subclass only when every caller of the parent is still correct.

**Interface Segregation.** Do not make a payer depend on card vaulting. Split a wide `PaymentGateway` that also has `saveCard` and `parseWebhook` into the operations a caller actually uses. A fake in a unit test should not implement methods the test never calls. ISP is a reason to split interfaces. It is not a reason to create an interface with one implementation and no second caller.

---

## 3. Relationship words

Use these names if the interviewer asks for a class diagram. The parking model already has the shapes.

| Word | Meaning here | Parking example |
| --- | --- | --- |
| Association | A knows B and uses it | `ParkingLot` orders `ParkingSpot`s |
| Composition | B's lifecycle is inside A | The allocation id on a spot dies with that occupancy |
| Aggregation | A groups B; B outlives A | A lot lists vehicles that exist before entry |
| Dependency | A uses B temporarily | `ParkingService` calls `PaymentGateway` at exit |
| Inheritance | A is a B for every caller | Avoid `CarSpot`. Behavior does not diverge |

---

## 4. Patterns Lesson 5 did not spell out

Same rule as Lesson 5: name the problem, skip the pattern when a simpler shape works, and say the misuse.

| Pattern | Justified when | Skip when | Misuse |
| --- | --- | --- | --- |
| **Factory Method** | A subclass or strategy must choose the concrete product (`Receipt` vs `SmsReceipt`) | `new ParkingSession(...)` after a successful claim | A factory whose body is only `new` |
| **Abstract Factory** | A **family** must match: a region's ticket layout and its receipt template are created together | You need one object. Use a constructor or Factory Method | A factory of `Vehicle` and `Spot` that do not vary as a pair |
| **Template Method** | The step order is stable and one hook changes (`quote → pay → release`, receipt hook) | The steps themselves change per vehicle. That is Strategy, or still one method | An abstract class with a single subclass |
| **Command** | The work must be stored, queued, or retried as data (exit request with the same idempotency key) | The caller can invoke the method now | A command object per setter |
| **Chain of Responsibility** | Independent checks can be reordered or added (`vehicle present`, `already parked`, `spot fits`) and each may stop the chain | Three checks read clearly as early returns in one method | A chain of one handler |
| **Proxy** | You control access, lazy loading, or a remote stand-in for an interface you already own | The foreign API has a different shape. That is an Adapter | A logging proxy “in case we add metrics” when one orchestrator can log |
| **Repository** | Domain code needs to load and save an aggregate without seeing SQL | You are designing the in-memory model and nobody asked about the database | A repository interface that copies every table column into the domain |

---

## 5. How to practice one problem

Forty-five to sixty minutes. Write this sequence. Stop when the next step would only add classes.

1. Clarify scope, assumptions, and what you will not build.
2. Name entities, value data, and who owns each invariant.
3. Say what you composed and what you refused to subclass.
4. Pick a pattern only where §4 or Lesson 5 says the problem matches.
5. Sketch the few types whose methods enforce the invariant. No full Spring app.
6. Name the HTTP resource and one status code only if the prompt is an API.
7. Say whether correctness is one JVM or many instances, and which write is atomic.
8. Name one failure that must not be retried as a new operation.
9. Name one test that would fail if the invariant broke.
10. State one trade-off you accepted.

A critical flaw is a broken invariant (double spend, double occupy, lost money). A missing cache or a missing pattern name is optional.

---

## 6. What to practice

Do these in order. Each one fails if you only rename the parking lot.

### 6.1 Reconstruct the parking lot (do this first)

From memory, one whiteboard:

- Session starts only after a claim. The entry rate is snapshotted. Payment failure keeps the spot.
- The spot owns occupancy. `release` requires the allocation id.
- Same hourly formula for car, bike, and bus is configuration. A different formula is Strategy.
- Timeout is `UNKNOWN`, same idempotency key. `SKIP LOCKED` is best-effort nearest, not strict order.

If you cannot do this, restudy Lessons 2–8 and 10. Do not start another problem.

### 6.2 Rate limiter (practice now)

**Skills:** state, atomics versus a shared store, what “exact” costs.

**Assume** a per-API-key limit of N requests per window. One service, then several instances. No distributed consensus lecture.

**Invariant:** over the window, accepted calls are at most N per key, or you explicitly allow a small overshoot and say so.

**Design:** a `RateLimiter` with `tryAcquire(key) -> boolean`. Fixed window is a counter and a window start. Sliding log is a queue of timestamps and more memory. Token bucket allows bursts and needs a refill rule.

**Senior point:** a `ConcurrentHashMap` of counters is correct on **one** JVM and wrong across instances. A second instance needs Redis, the database, or a gateway limit. Say which, and what happens when the store times out (fail open vs fail closed). Do not hide the policy in a filter before you have the decision.

**Skip:** a Strategy per customer, and a leaky-bucket class hierarchy.

### 6.3 Notification system (practice now)

**Skills:** Strategy, Factory Method, Observer — and when a channel list is enough.

**Assume** email, SMS, and push. A user can opt into some channels. Delivery can fail per channel. No campaign builder.

**Invariant:** a failed SMS does not cancel an email that already succeeded. Preferences are data.

**Design:** `Notification` is the message. `ChannelSender` is the vendor boundary (Adapter if the vendor SDK is awkward). A registry maps channel id → sender. The orchestrator loops the user’s enabled channels.

**Senior point:** Observer fits when new subscribers appear and the sender must not list them. It is the wrong tool for “send these three and report which failed.” Prefer an explicit list of senders and a result per channel. Factory Method is justified when the product (email body vs SMS body) really differs, not when the body is a template string.

### 6.4 Inventory and order reservation (practice now)

**Skills:** transactions, idempotency, state, partial failure. This is the parking claim moved to stock.

**Assume** one warehouse row per SKU, `available` count, reserve-then-pay, expire unpaid reservations. Several app instances.

**Invariant:** `available` never goes negative. One client retry does not reserve twice. An expired reservation returns stock once.

**Design:** `Reservation` with `HELD → CONFIRMED | RELEASED`. The atomic write is `UPDATE inventory SET available = available - :qty WHERE sku = :sku AND available >= :qty`. Zero rows means sold out. Idempotency key on the reserve call. Expiry is a worker that releases `HELD` rows older than the TTL, guarded so two workers cannot both return the same units.

**Senior point:** a JVM lock around the repository call does not protect a second instance. Do not hold a database transaction open across the payment HTTP call (Lesson 7). Payment timeout leaves the reservation `HELD` until expiry or a confirmed capture. That is the same `UNKNOWN` rule as the parking fee.

**Skip:** a saga across three services until the prompt has a second service. One database can do reserve and confirm.

### 6.5 Thread-safe LRU cache (next)

**Skills:** encapsulation, data structure, single-JVM concurrency.

`LinkedHashMap` access-order LRU is already [Collections — access order](../../core-java/module-04-collections/11-linkedhashmap-lru-cache.md). The LLD drill is the **object boundary**: `get` and `put` are the only mutators, capacity is fixed, and the map is not returned to callers. Synchronization on one cache is enough for one process. It does not make a shared Redis LRU. State that limit in the first minute.

#### Future implementation checklist (not yet studied)

When this drill is scheduled, build the cache twice: first with an access-order `LinkedHashMap`, then with a `HashMap<K, Node>` plus a doubly linked list with head/tail sentinels. The second version should keep every operation `O(1)`:

- `get`: find the node, move it to the most-recent end, and return its value (or miss);
- `put`: update an existing key without changing size, or insert a new most-recent node and evict the least-recent node at capacity;
- `remove`: unlink the node and remove its map entry;
- list helpers: `unlink`, `appendMostRecent`, and `evictLeastRecent`; sentinels eliminate null endpoint cases.

Explain the trade-off: `LinkedHashMap` is concise and appropriate when its behavior is enough; the explicit node list is useful for interview data-structure reasoning or custom policy hooks. Then discuss synchronization, read/write contention, bounded memory/weight/expiry, loader stampedes, metrics, and why production Java services usually prefer Caffeine rather than an interview cache. This is a future exercise, not a completed implementation.

### 6.6 Connection pool (next)

**Skills:** resource lifecycle, thread safety, a hard cap.

**Invariant:** borrowed connections are at most the pool size. `close` returns a connection to the pool or closes it once, never twice. A caller that forgets to return a connection is a leak you can detect with a timeout.

**Senior point:** the pool limits **waiting callers** as well as connections. A larger pool does not fix a slow query (Lesson 10). Virtual threads waiting on a small pool is a concurrency-track topic; do not re-derive it here. Proxy fits if you hand out a wrapper whose `close` returns the connection. It does not fit as a substitute for the pool’s accounting.

### 6.7 Do these only to transfer, not to learn a new idea

| Problem | Why it is optional | The one difference from parking |
| --- | --- | --- |
| Movie ticket booking | Same claim, expiry, and unique seat | The seat is the spot. A held seat expires; say who may buy it next |
| Payment processing | Lessons 7 and 8 | Duplicate capture with a **new** idempotency key is the bug. Show the stored outcome |
| Elevator system | State and scheduling, easy to overbuild | One cabin, one direction, requests as data. No multi-elevator optimization unless asked |
| Splitwise | Money and rounding | Integer minor units, balances sum to zero, simplify debts without “almost equal” floats |
| Task scheduler / pub-sub | Concurrency Lesson 17 already covers the queue | A task is a Command with a state (`PENDING`, `RUNNING`, `DEAD`). At-least-once means the handler is idempotent |

---

## 7. What not to add as new LLD lessons

- Another pass over JMM, locks, or executors.
- A Spring Boot tutorial inside this module. When you study Days 5–6, attach pagination, bean scopes, N+1, and API versioning there, and link back to Lessons 6–8 for the domain decisions.
- Full Java for every row in §6.7. The curriculum asks for different skills, not a catalog of implementations.

---

## Revision checklist

- Parking reconstruction hits claim-then-session, snapshotted rate, allocation id, `UNKNOWN`, and `SKIP LOCKED`.
- LSP example is a subtype that throws where the parent does not. ISP example is a payer forced to implement `saveCard`.
- You can reject Abstract Factory, Template Method, Command, a chain, and Proxy with a concrete simpler alternative.
- Rate limiter states one-JVM versus shared store and fail open versus fail closed.
- Inventory reservation is an atomic conditional `UPDATE`, not a synchronized block, when two instances share the database.

## Key takeaways

The handbook already contains the parking-lot LLD and the performance lesson. Practice is transfer: one reconstruction, then a rate limiter, a notification fan-out, and an inventory reservation. Add a pattern only when the simpler design would hide a real change in behavior, a vendor boundary, or an invariant.
