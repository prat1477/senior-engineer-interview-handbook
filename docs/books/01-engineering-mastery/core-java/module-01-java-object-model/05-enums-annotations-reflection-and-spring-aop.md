---
title: "Lesson 5 - Enums, Annotations, Reflection, and Spring AOP"
description: Type-safe enum design, metadata, reflection, annotation processing, and transactional proxies.
status: covered
audience: practitioner
tags: [java, enums, annotations, reflection, spring, transactions, module-1, lesson-5]
created: 2026-11-08
updated: 2026-11-08
---

# Lesson 5 - Enums, Annotations, Reflection, and Spring AOP

## Overview

Enums model a closed set of values. Annotations carry metadata. Reflection lets code inspect that metadata at runtime. Spring uses these mechanisms as inputs to its container and proxy infrastructure; neither annotations nor reflection magically performs business behavior by themselves.

## A. Java enums

An enum represents a **fixed, predefined, type-safe** set of constants. Prefer it to a `String` when the valid values are owned by the application and change only through a code release. The compiler prevents arbitrary values and makes switches exhaustive-aware.

```java
public enum PaymentStatus {
    PENDING, ACCEPTED, REJECTED
}
```

`"ACCEPTED"` is merely text: it can be misspelled, be null, or come from an uncontrolled source. `PaymentStatus.ACCEPTED` is a value of a constrained type. Each enum constant is one singleton instance for that enum **per class loader**. Class initialization creates the constants; application code cannot call `new PaymentStatus(...)`.

Enums can have fields, methods, and constructors. Constructors are implicitly private. They can implement interfaces but cannot extend arbitrary classes because they already extend `java.lang.Enum`.

```java
public enum PaymentProvider {
    STRIPE("stripe", "Card payments"),
    RAZORPAY("razorpay", "India payment gateway");

    private final String code;
    private final String description;

    PaymentProvider(String code, String description) {
        this.code = code;
        this.description = description;
    }

    public String getCode() { return code; }
    public String getDescription() { return description; }
}
```

The explicit, stable `code` is appropriate for a database column or external business identifier. Do not persist `ordinal()`: inserting or reordering constants changes its integer meaning. A stable code also makes a rename of the Java constant possible without silently rewriting data.

### Built-in APIs

| API | Meaning | Caution |
| --- | --- | --- |
| `values()` | Array of constants in declaration order | Returns an array; do not use order as a business contract |
| `valueOf("ACCEPTED")` | Constant with that exact `name()` | Case-sensitive; invalid text throws `IllegalArgumentException` |
| `name()` | Source-level constant name | Stable only if the constant name is deliberately part of the external contract |
| `toString()` | Display representation | May be overridden; do not parse it for persistence |
| `ordinal()` | Zero-based declaration position | Unsafe as a persisted identifier |

`name()` is the declared identifier and cannot be overridden. `toString()` defaults to `name()` but may be overridden, including in a constant-specific body. Usually expose a `description` field instead of overloading `toString()` with UI or business meaning.

```java
enum DeliverySpeed {
    STANDARD,
    EXPRESS {
        @Override public String toString() { return "express delivery"; }
    }
}
```

Constant-specific class bodies are useful for small fixed behavior. For larger behavior, use a strategy class or Spring-managed adapter rather than placing mutable service state in an enum.

### Enums and concurrency

Singleton does **not** mean thread-safe. Fields in an enum constant are shared by all callers of that class loader. `count++` is read, add, write; it is not one atomic operation, so concurrent calls can lose updates.

```java
enum MetricsBucket {
    PAYMENTS;
    private final AtomicInteger count = new AtomicInteger();
    void increment() { count.incrementAndGet(); }
    int count() { return count.get(); }
}
```

`synchronized` can protect a compound invariant, while `AtomicInteger` uses compare-and-set (CAS): compare the observed value, write only if unchanged, otherwise retry with a fresh read. `AtomicInteger` is suitable when an exact atomic counter or conditional update matters. `LongAdder` spreads writes across cells and usually has higher throughput under **high contention**; `sum()` aggregates cells and is not a linearizable snapshot for decision-making. High concurrency only means many tasks exist; high contention means many threads fight over the same shared location.

Avoid mutable application business state in enum constants. It couples global state to a type singleton, complicates tests and class-loader lifecycles, and rarely represents the authoritative database or distributed state.

### Jackson, Spring Boot, and evolving values

Jackson normally deserializes enum names case-sensitively. Unknown values fail deserialization. Spring Boot can enable case-insensitive matching:

```properties
spring.jackson.mapper.accept-case-insensitive-enums=true
```

For an explicit code, use a `@JsonCreator` factory; reject unknown input deliberately.

```java
@JsonCreator
public static PaymentProvider fromCode(String code) {
    return Arrays.stream(values())
        .filter(provider -> provider.code.equalsIgnoreCase(code))
        .findFirst()
        .orElseThrow(() -> new IllegalArgumentException("Unknown provider: " + code));
}
```

`@JsonEnumDefaultValue` can mark a fallback constant when Jackson is configured with `READ_UNKNOWN_ENUM_VALUES_USING_DEFAULT_VALUE` (in Boot, `spring.jackson.deserialization.read-unknown-enum-values-using-default-value=true`). That can be useful for tolerant consumers, but silently turning a new partner value into `UNKNOWN` can hide a contract break; log, meter, or reject according to the endpoint's risk.

### Enum versus a dynamic domain model

Use an enum for fixed statuses such as `PENDING`, `ACCEPTED`, and `REJECTED`, where changing the set means changing code and deploying. Use a runtime-configurable model when administrators can add a payment provider without redeployment: provider code, display name, credentials reference, enabled flag, and routing rules belong in configuration or a database.

Dynamic metadata does not create integration behavior. A newly configured provider still needs a tested adapter/strategy implementation capable of signing, calling, and interpreting that provider's API. Configuration selects known behavior; it does not compile a new integration.

## B. Java annotations

Annotations are **metadata** attached to program elements. Adding an annotation does not execute business logic. A framework, annotation processor, interceptor, or custom code must inspect and interpret it. Spring Boot uses annotations for component discovery (`@Component`), web endpoints (`@RestController`, `@GetMapping`), validation, injection metadata, transactions, configuration, and tests.

### Custom annotations

Declare an annotation with `@interface`. Its elements are methods with no parameters; they may have defaults. Legal element types are primitives, `String`, `Class`, enum types, annotation types, and arrays of those. `List` and `Map` are not legal because annotation metadata must be represented in the class file with a restricted, compile-time-safe value model.

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Auditable {
    String value();                 // value() permits @Auditable("PAYMENT_CREATE")
    String action() default "READ";
    boolean includeArguments() default false;
    Class<?> resourceType() default Void.class;
}
```

`@Auditable` records intent only. An aspect or interceptor must inspect it and emit an audit event. `@Auditable(value = "PAYMENT_CREATE")` and `@Auditable("PAYMENT_CREATE")` are equivalent because the element is named `value`.

### Meta-annotations

`@Target` limits where an annotation may appear. Common targets are `TYPE` (class, interface, enum, annotation), `METHOD`, `FIELD`, `PARAMETER`, and `CONSTRUCTOR`; others include `ANNOTATION_TYPE`, `PACKAGE`, `TYPE_PARAMETER`, `TYPE_USE`, `MODULE`, and `RECORD_COMPONENT`.

```java
@Target({ElementType.TYPE, ElementType.METHOD})
@interface Monitored {}
```

`@Retention` controls how long metadata remains:

| Retention | Availability | Example use |
| --- | --- | --- |
| `SOURCE` | Compiler source only | `@Override`, static-analysis markers |
| `CLASS` | Class file, not normally reflection-visible | Bytecode tooling |
| `RUNTIME` | Class file and runtime reflection | Spring/AOP annotations |

```java
@Retention(RetentionPolicy.RUNTIME)
@interface FeatureGate { String value(); }
```

`@Documented` asks Javadoc to include uses of the annotation. It has no runtime effect. `@Inherited` lets a **class-level** annotation be observed on a subclass through its superclass when queried by reflection. It does not apply to method annotations, fields, or interface inheritance.

```java
@Inherited
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@interface TenantScoped {}

@TenantScoped class BaseJob {}
class BillingJob extends BaseJob {} // BillingJob sees TenantScoped via getAnnotation
```

## C. Reflection and annotation processing

Reflection is runtime inspection and use of classes, methods, fields, constructors, and annotations. `Class.forName("com.example.PaymentService")` loads a named class (and normally initializes it). `getDeclaredMethods()`, `getDeclaredFields()`, and `getDeclaredConstructor()` inspect members declared directly on that class, including non-public members. `getMethods()` returns public methods, including inherited ones. `getDeclaredMethod("capture", Payment.class)` selects a declared method by name and parameter types.

```java
Class<?> type = Class.forName("com.example.PaymentService");
Method method = type.getDeclaredMethod("capture", Payment.class);
Constructor<?> constructor = type.getDeclaredConstructor();
Field[] fields = type.getDeclaredFields();
Method[] declared = type.getDeclaredMethods();
Method[] publicAndInherited = type.getMethods();

if (method.isAnnotationPresent(Auditable.class)) {
    Auditable audit = method.getAnnotation(Auditable.class);
    Object result = method.invoke(service, payment);
}
```

Frameworks use reflection to discover metadata. Spring scans candidate classes, reads stereotype annotations, finds injection points such as `@Autowired`, and reads transaction attributes such as `@Transactional`. Reflection finds the facts; Spring's container creates and wires beans, and its AOP infrastructure supplies transactional interception. Reflection itself does not inject a dependency or roll back a transaction.

Trade-offs are runtime overhead, reduced compile-time type safety, refactor fragility, harder debugging, and access restrictions. Java modules may deny deep reflection; `setAccessible`/`trySetAccessible` is constrained by module openness. Cache reflective lookups, prefer explicit APIs where practical, and do not use private-field reflection as ordinary application design.

Annotation processing happens at **compile time**, not through runtime reflection. The Java Annotation Processing API lets processors inspect source/compiler models and generate source or resources. Lombok integrates with compilation to reduce handwritten boilerplate such as getters and builders; it transforms compiler processing rather than producing a conventional hand-written runtime mapper. MapStruct generates explicit mapper implementations at compile time from mapping declarations. Generated code reduces runtime reflection requirements and makes missing mappings visible at build time. Neither requires a custom processor for this lesson.

## D. Spring AOP and `@Transactional`

Aspect-Oriented Programming (AOP) modularizes **cross-cutting concerns** such as transactions, auditing, authorization, tracing, and retries. An **aspect** groups that concern; **advice** is work performed before, after, or around an invocation; a **join point** is a candidate execution point; a **pointcut** selects join points; and a **proxy** intercepts calls. Spring AOP is proxy-based: calls crossing a Spring proxy can be advised (with JDK interface proxies or CGLIB subclass proxies), not arbitrary internal bytecode calls.

`@Transactional` is transaction metadata. On an external call through a Spring proxy, the transaction interceptor reads that metadata, asks the configured `PlatformTransactionManager` to begin or join a transaction, invokes the business method, then commits or rolls back. JDBC/JPA resources do the underlying connection/entity-manager transaction work; reflection is not the component that rolls back.

1. An external caller invokes a Spring proxy.
2. The transaction interceptor reads transaction attributes.
3. It begins a transaction or joins an existing one through the transaction manager.
4. The business method runs with JDBC/JPA resources bound to that transaction.
5. The interceptor commits, or rolls back according to outcome and rollback rules.

### Self-invocation

```java
@Service
class PaymentService {
    @Transactional
    public void place(Payment payment) {
        this.recordLedger(payment); // direct call: bypasses this bean's proxy
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void recordLedger(Payment payment) { /* ... */ }
}
```

The inner annotation is not independently applied because `this.recordLedger` never crosses the proxy. If `place` started a transaction, `recordLedger` still executes inside that outer transaction, but `REQUIRES_NEW` is not honored. If the outer method is not transactional, no transaction starts from the inner annotation. Move `recordLedger` to another Spring-managed service and call that bean when separate interception/propagation is required.

### Rollback traces

| Scenario | Default result |
| --- | --- |
| Uncaught `RuntimeException` escapes a transactional method | Interceptor rolls back |
| Uncaught checked exception escapes | Commits by default unless configured |
| `RuntimeException` is caught and swallowed in the same method | Interceptor sees normal return and may commit |
| Participating inner proxied method throws runtime exception; outer catches it | Transaction can be marked rollback-only; outer completion can throw `UnexpectedRollbackException` |

Use `@Transactional(rollbackFor = PaymentCheckedException.class)` for a checked exception that must roll back. Code may explicitly mark rollback-only through `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()`, but use that sparingly because it makes a later apparent success fail at completion. Propagation settings determine whether a method joins, suspends, or creates transaction boundaries; they do not make self-invocation pass through the proxy.

**Trace: uncaught runtime failure.** Proxy starts transaction T1, `capture()` writes a payment row, `RuntimeException` escapes, the interceptor asks the transaction manager to roll back T1, and JDBC/JPA rolls back the resource work.

**Trace: caught failure without rollback-only.** Proxy starts T1, `capture()` catches its own `RuntimeException` and returns normally, so the interceptor sees success and commits T1. Catching is a business decision; if the partial work is invalid, rethrow or mark T1 rollback-only.

**Trace: rollback-only surprise.** An outer proxied `@Transactional` call starts T1. It invokes a separate bean whose participating transactional method throws a runtime exception; its interceptor marks T1 rollback-only. The outer method catches the exception and returns normally. At T1 completion Spring cannot commit and throws `UnexpectedRollbackException` to avoid reporting a commit that never occurred.

## E. Senior interview checklist

- An enum is a fixed code-owned set; a database/configuration model is runtime-extensible metadata.
- Singleton enum constants can still expose racy mutable shared fields.
- `ordinal()` is position, not a durable business identifier.
- Annotation metadata needs a processor; `RUNTIME` retention is necessary for ordinary reflection.
- Reflection discovers metadata. Spring container and proxies perform DI and transaction behavior.
- `@Transactional` works only when an invocation crosses the relevant Spring proxy.

## See also

- [Concurrency - atomics and CAS](../../../../concurrency/07-atomics-and-cas.md)
- [Concurrency - thread-safety patterns](../../../../concurrency/19-thread-safety-patterns.md)
- [Spring and microservices curriculum](../../../../spring-microservices/index.md)
