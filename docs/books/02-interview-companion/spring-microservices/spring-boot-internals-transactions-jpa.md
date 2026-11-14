---
title: Spring Boot, Transactions, JPA, and JDBC — Interview Companion
description: Fast senior-level recall for bean internals, AOP, JPA/Hibernate, JDBC batches, and cache consistency.
status: in-progress
audience: advanced
tags: [companion, spring-boot, transactions, jpa, jdbc, caching]
created: 2026-11-14
updated: 2026-11-14
---

# Spring Boot, Transactions, JPA, and JDBC — Interview Companion

**Canonical depth:** [Spring Boot internals, transactions, JPA, and batch processing](../../../spring-microservices/03-spring-boot-internals-transactions-jpa.md), plus the [production cache review](../../../spring-microservices/02-production-pr-review-caching-and-resilience.md). This page is for fast recall; it is not evidence of independent implementation.

## 1. One-minute visual map

```mermaid
flowchart LR
  container[ApplicationContext] --> proxy[Spring proxy]
  proxy --> tx[transaction boundary]
  tx --> jpa[Persistence context / managed entities]
  tx --> jdbc[JdbcTemplate / bound connection]
  jpa --> version[@Version SQL]
  jdbc --> batch[batch counts / chunks]
  cache[L1 Caffeine + L2 Redis] --> db[(PostgreSQL truth)]
```

## 2. Core answers, traps, and follow-ups

Each answer is sized for a 30--60 second response. “Limit” is the important qualification to add
before an interviewer has to ask for it.

| Topic | Interview answer | Common trap / memory trick | Limit and follow-up |
| --- | --- | --- | --- |
| 1. Bean storage / context | A bean is a heap object managed by `ApplicationContext`; the context owns definitions, wiring, lifecycle and references. A singleton is one instance per bean definition per container. | **Bean = Java object managed by Spring; singleton is scoped to the container.** | Not cluster-global: each pod/JVM has its own context. *Where does the object actually live?* |
| 2. Constructor vs field injection | Constructor injection exposes required collaborators, permits final references, fails invalid construction early and makes unit tests ordinary Java. | Field injection hides requirements. **Constructor injection makes required dependencies explicit.** | `final` reference does not make collaborator immutable/thread-safe. *When is setter injection reasonable?* |
| 3. Boot startup | JVM starts `main`, `SpringApplication.run` prepares environment/context, registers definitions, scans/auto-configures, creates/injects beans, post-processes/proxies, then web/readiness infrastructure. | Do not claim exact internal event order. | Lazy beans and early proxies are special cases. *What does `@SpringBootApplication` combine?* |
| 4. Bean lifecycle / BPP | Definition -> instantiate -> inject -> BPP before -> init / `@PostConstruct` -> BPP after -> possible proxy. | `@PostConstruct` is not a safe self-invocation transaction hook. | Lazy creation can defer it. *Where are transaction proxies added?* |
| 5. JDK proxy vs CGLIB | JDK proxies implement interfaces; CGLIB subclasses the target class. Both are Spring proxy infrastructure for eligible calls. | “A special classloader creates the proxy” misses the point. | Final classes/methods cannot be overridden by CGLIB. *Which proxy works when there is no interface?* |
| 6. AOP self-invocation | `this.method()` stays inside the target and bypasses its proxy, so the inner `@Transactional` advice does not run. | **Calling `this.method()` bypasses default Spring proxy advice.** | Move the separately advised work to another bean. *What happens to `REQUIRES_NEW` in the same class?* |
| 7. `REQUIRED` vs `REQUIRES_NEW` | `REQUIRED` joins an existing physical transaction or starts one; `REQUIRES_NEW` suspends the outer one and starts an independent physical transaction. | **REQUIRED: existing transaction joined. REQUIRES_NEW: outer suspended.** | `REQUIRES_NEW` needs another connection. *How does this affect pool sizing?* |
| 8. Logical vs physical transaction | Multiple `REQUIRED` method scopes are logical scopes that commonly share one physical transaction. | Do not call an internal method a “child transaction.” | Each logical scope can affect rollback-only state. *Why can a shared T1 fail after the outer returns?* |
| 9. Caught exception / rollback-only | A proxied inner `REQUIRED` runtime exception can mark shared T1 rollback-only even when outer code catches it. | Catching Java exception does not unmark T1. | Same-class invocation lacks that inner advice. *What result does caller receive?* |
| 10. `UnexpectedRollbackException` | Outer method can return normally, but the outer interceptor cannot commit rollback-only T1 and reports `UnexpectedRollbackException`. | **Caught error != committable transaction.** | It protects caller from being told a commit occurred. *How does `REQUIRES_NEW` change it?* |
| 11. Checked vs unchecked rollback | Spring rolls back `RuntimeException`/`Error` by default, but checked exceptions commit unless configured. | **Unchecked rolls back; checked doesn't; `rollbackFor` changes the rule.** | Database-aborted state cannot always be overridden. *Show checked-exception rollback configuration.* |
| 12. Transactional outbox | Write business state and outbox record atomically; a relay publishes after commit and consumers are idempotent. | `REQUIRES_NEW` alone is not reliable async delivery. | Usually at-least-once, so duplicates occur. *Why is an after-commit callback insufficient?* |
| 13. Lazy initialization | A lazy association accessed after its persistence context closes can cause `LazyInitializationException`. | Returning entities couples API serialization to persistence. | One parent/collection is often one extra query; N+1 is many parents. *What does OSIV change?* |
| 14. OSIV | Enabled OSIV can let serialization load lazy data late; disabled OSIV exposes missing fetch plans sooner. | “OSIV fixes lazy loading” hides query/connection scope risk. | Neither is a substitute for DTO/fetch design. *Why can it create N+1?* |
| 15. EntityGraph / fetch join / DTO | Graph is declarative entity fetching; fetch join is query-local entity fetching; DTO projection selects endpoint data directly. | EntityGraph does not universally promise exactly one query. | Avoid collection fetch joins with pagination. *Which one for a summary endpoint?* |
| 16. Persistence context | Hibernate workspace/first-level cache holding managed entities and state snapshots. | **Persistence context = managed-entity workspace and L1 cache.** | It can conceptually exist outside an active DB transaction. *What makes an entity detached?* |
| 17. Managed vs detached | A managed entity is tracked and synchronized on flush; a detached one is an ordinary object no longer tracked. | Repository `findById()` without outer transaction may return detached state after its method ends. | `merge`/`save` has different meaning for detached state. *Will a detached setter write SQL?* |
| 18. Dirty checking / `save` | Change a managed entity in a transaction and Hibernate detects it at flush; explicit `save()` is normally unnecessary. | **Managed object changed -> Hibernate synchronizes at flush.** | Flush sends SQL; commit decides durability. *When might `save` still matter?* |
| 19. `@Version` SQL | Hibernate updates with `WHERE id=? AND version=?` and increments version; zero affected rows signals stale state. | **Version in WHERE; zero rows means mismatch or missing row.** | This is Hibernate SQL generation, not Spring AOP. *When is conflict detected?* |
| 20. JPQL bulk update | JPQL `UPDATE` bypasses normal per-entity dirty checking and automatic version checking, even for one row. | Bulk DML is not “managed entity update.” | It can stale the context/callbacks; add predicate/increment deliberately. *Why clear afterward?* |
| 21. Bulk vs Hibernate batch vs JDBC batch | Bulk is set SQL; Hibernate batch batches entity-driven SQL; JDBC batch submits parameterized SQL directly. | **Batching reduces overhead; it does not define isolation/conflict resolution.** | `saveAll()` does not guarantee a batch. *Which for 100k independent updates?* |
| 22. JPA vs JDBC | JPA helps with object graphs, cascades and lifecycle; JDBC gives exact SQL, low-level batching and explicit counts. | “JDBC is always faster” is a claim to measure, not assume. | They can coexist only with deliberate resource/transaction configuration. *When is ORM behaviour valuable?* |
| 23. JDBC batch counts | `1` is a row update, `0` is conflict/missing, `SUCCESS_NO_INFO` lacks individual count, and `EXECUTE_FAILED` is driver-reported failure where supported. | Treat only 0/1 as a portability bug. | Driver continuation/alignment varies; execution success is not commit. *How do you handle `BatchUpdateException`?* |
| 24. PostgreSQL statement error | Constraint/deadlock/SQL errors differ from zero-row CAS; PostgreSQL normally marks current transaction aborted after a statement error. | **Java catch does not repair DB transaction state.** | Savepoints must be designed before recovery. *What happens to prior uncommitted updates?* |
| 25. Chunked transactions | Coordinate chunks outside transactions; a separate transactional writer commits each bounded chunk and aggregates results. | Internal transactional writer call may bypass proxy. | Chunk size is benchmarked; idempotency and retries matter. *Why not one transaction for 100k rows?* |
| 26. `@Transactional` + JDBC | Proxy starts/joins transaction; manager binds JDBC connection; all `JdbcTemplate` statements use that connection and rollback together by default rules. | **Spring transactions work with JDBC, not only Hibernate.** | Auto-commit can commit individual statements without surrounding tx. *Name the JDBC transaction managers.* |
| 27. Redis stale cache fill | A reader can miss/read old DB value, writer commits/invalidate, then reader writes old value to Redis. | **Redis DEL cannot stop a late stale SET.** | TTL starts at late fill; retain version metadata/fences or use primary reads for strict freshness. *Why is version deletion itself tricky?* |
| 28. Caffeine + Redis | L1 Caffeine is per JVM; L2 Redis is shared; an orchestration layer must decide reads/fills/invalidations. | **L1 local; L2 shared; coherence is extra design.** | Redis invalidation does not fan out to all L1s; one Kafka consumer group load-balances rather than broadcasts. *When is two-level cache justified?* |

## 3. Snippets worth remembering

### Memory bank

- **Spring AOP:** Proxy interception determines whether transactional advice actually executes.
- **Flush:** SQL execution is not the same as transaction commit.
- **Bulk update:** Bulk JPQL DML bypasses normal managed-entity dirty checking and automatic `@Version` enforcement.
- **Batching:** Batching reduces execution overhead; it does not automatically define transaction isolation or conflict resolution.
- **Database error:** A PostgreSQL statement error can abort the transaction; a Java catch does not undo that database state.
- **JDBC transactions:** Spring `@Transactional` works with JDBC, not only Hibernate.
- **Cache consistency:** Redis `DEL` does not prevent an older in-flight reader from writing stale data afterward.
- **Multi-level caching:** L1 Caffeine is local; L2 Redis is shared; both need a coherent invalidation strategy.

```java
// Explicit public API absence contract
OrderResponse response = repository.findResponseById(id)
    .orElseThrow(() -> new OrderNotFoundException(id));

// Checked failure should roll back
@Transactional(rollbackFor = IOException.class)
void importFile() throws IOException { /* ... */ }

// Explicit optimistic compare-and-update in JPQL bulk DML
@Modifying
@Query("""
  UPDATE Order o SET o.status = :status, o.version = o.version + 1
  WHERE o.id = :id AND o.version = :expectedVersion
  """)
int updateIfVersionMatches(
    @Param("id") Long id,
    @Param("status") String status,
    @Param("expectedVersion") Long expectedVersion
);
```

```java
// Correctly separate propagation boundary
@Service
class PaymentWriter {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    void write(Payment payment) { repository.save(payment); }
}
```

## 4. Final production PR checklist

For an order GET service, say you checked:

- singleton shared state and thread-unsafe `HashMap`;
- non-atomic miss/load, duplicate loads, bounds, expiry, metrics and stampede policy;
- immutable DTO projection rather than a mutable JPA entity in cache/API;
- custom missing-order exception with `ProblemDetail` 404 mapping;
- lazy serialization, N+1, validation and API error contract;
- stale data, cross-pod cache scope, invalidation race, L1 fan-out and data freshness contract;
- database fallback timeouts, connection budgets, rate limits/bulkheads/circuit breaker;
- observability: cache hit/load/eviction, Redis errors, DB saturation, latency and rejection metrics.

**30-second close:** “I do not stop at making the map concurrent. I make values immutable,
bound/observe the cache, specify freshness and cross-pod invalidation, give absence a 404 contract,
and protect PostgreSQL if the cache is unavailable.”

## 5. Recall drills

1. A separate `REQUIRED` writer throws, caller catches, outer returns. What exception reaches the caller and why?
2. Why is `REQUIRES_NEW` not a reliable notification-delivery mechanism by itself?
3. Contrast a zero-row conditional update with a PostgreSQL constraint violation.
4. Pick a fetch strategy for paginated orders with line-item summaries, and explain why.
5. Draw the three-event stale Redis fill race without looking at the canonical page.

## 6. Status and next checkpoint

These topics are **discussed / conceptually understood**. Independent validation remains for a
larger Spring PR review, Java coding, mixed propagation mock, JPA/Hibernate implementation, and
a production-grade batch writer.

Next topic: **Spring Security / OAuth2 Resource Server / JWT verification and authorization**.
