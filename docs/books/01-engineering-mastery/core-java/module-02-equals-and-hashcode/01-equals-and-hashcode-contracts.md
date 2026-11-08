---
title: "Lesson 1 — equals() and hashCode() Contracts"
description: Logical equality, Object defaults, the equals contract, hashCode coupling, and HashMap/HashSet usage.
status: covered
audience: practitioner
tags: [java, equals, hashcode, module-2, lesson-1]
created: 2026-10-20
updated: 2026-11-07
---

# Lesson 1 — `equals()` and `hashCode()` Contracts

## Overview

Java distinguishes **reference identity** (`==`) from **logical equality** (`equals`). Hash-based collections (`HashMap`, `HashSet`, `Hashtable`, `ConcurrentHashMap` for key lookup) depend on a consistent pair: `hashCode()` for bucketing and `equals()` for exact key match within a bucket.

**JDK:** 17+ examples. Behavior of `Object.equals` / `Object.hashCode` follows the Java SE API; OpenJDK `HashMap` internals are cited as **implementation detail** where noted.

## Big picture

| Concern | Mechanism |
| --- | --- |
| Same JVM object twice | `==` true; `equals` true if not overridden |
| Same business identity, different instances | Override `equals` (and usually `hashCode`) |
| Fast lookup in hash table | `hashCode` → bucket; `equals` → disambiguate collisions |

Foundation for [Module 3 — HashMap internals](../module-03-hashmap-internals/index.md). Map **usage** contracts also appear in [Collections L4](../module-04-collections/04-map-fundamentals-and-hashmap.md) — this module explains **why** those contracts exist.

## Prerequisites

- Basic `Object` and references.
- Optional preview: [Map fundamentals (M4 L4)](../module-04-collections/04-map-fundamentals-and-hashmap.md).

## 1. Identity versus logical equality

```java
String a = new String("order-42");
String b = new String("order-42");

System.out.println(a == b);       // false — different references
System.out.println(a.equals(b));  // true — same character sequence
```

`==` compares references. `equals` compares state according to the class definition (or `Object` default).

## 2. `Object` defaults

```java
// Conceptual — every class inherits from Object
public boolean equals(Object obj) {
    return this == obj;
}

public int hashCode() {
    // identity-based; implementation uses internal object address / identity hash
}
```

Until overridden, **only the same reference** is equal. `hashCode` is stable for an object’s lifetime (for identity hash) but not useful for value-based keys.

## 3. The five `equals()` contract requirements

For any non-null reference `x`, `y`, `z` of types where equality is defined:

| Property | Meaning |
| --- | --- |
| **Reflexive** | `x.equals(x)` is `true` |
| **Symmetric** | `x.equals(y)` ⇔ `y.equals(x)` |
| **Transitive** | If `x.equals(y)` and `y.equals(z)`, then `x.equals(z)` |
| **Consistent** | Repeated calls return the same result if state used in `equals` is unchanged |
| **Non-null** | `x.equals(null)` is `false` |

**Memory aid — RSTCN:** Reflexive, Symmetric, Transitive, Consistent, Non-null.

Violations break collections, caches, and distributed idempotency keys that rely on stable equality.

## 4. Correct `equals(Object)` pattern

```java
public final class OrderKey {
    private final long tenantId;
    private final String orderId;

    public OrderKey(long tenantId, String orderId) {
        this.tenantId = tenantId;
        this.orderId = orderId;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this) {
            return true;
        }
        if (!(obj instanceof OrderKey other)) {
            return false;
        }
        return tenantId == other.tenantId
            && java.util.Objects.equals(orderId, other.orderId);
    }

    @Override
    public int hashCode() {
        return java.util.Objects.hash(tenantId, orderId);
    }
}
```

**Design choice:** which fields define equality is **domain-specific** (id only vs id + version). Document the invariant on the type.

Steps interviewers expect:

1. `==` short-circuit.
2. `instanceof` / type check (or `getClass()` if rejecting subclasses — see Lesson 2).
3. Compare significant fields with `Objects.equals` for references.

## 5. Null-safe field comparison — `Objects.equals()`

```java
Objects.equals(a, b); // true if both null; false if one null; else a.equals(b)
```

Avoids NPE when comparing optional reference fields.

## 6. Relationship between `equals()` and `hashCode()`

**API rule (must hold for hash-based collections):**

> If `a.equals(b)` is `true`, then `a.hashCode() == b.hashCode()`.

**Not reversible:** equal hash codes do **not** imply `equals`.

```java
System.out.println("Aa".hashCode()); // 2112
System.out.println("BB".hashCode()); // 2112 — collision, not equal strings
```

## 7. Overriding `equals()` without `hashCode()`

```java
class BadKey {
    private final int id;
    BadKey(int id) { this.id = id; }
    @Override
    public boolean equals(Object o) {
        return o instanceof BadKey b && b.id == id;
    }
    // hashCode() not overridden — still Object identity hash
}

var map = new java.util.HashMap<BadKey, String>();
var k1 = new BadKey(1);
var k2 = new BadKey(1);
map.put(k1, "paid");
System.out.println(map.get(k2)); // null — equal by equals(), different buckets
```

`HashSet` may contain **duplicates** that `equals` considers the same. This is a common interview trap.

## 8. How `HashMap` and `HashSet` use hashing

Simplified lookup path (details in Module 3):

1. Compute spread hash from `key.hashCode()`.
2. Index into bucket array.
3. Walk bucket entries; match `hash` then `key.equals(k)`.

`HashSet` stores keys in a `HashMap` internally (implementation detail); membership is `contains` → same equals/hash contract.

## 9. Mutable keys

If fields participating in `equals` / `hashCode` change after insertion, the entry may sit in the **wrong bucket**:

```java
class MutableId {
    int id;
    MutableId(int id) { this.id = id; }
    @Override public boolean equals(Object o) {
        return o instanceof MutableId m && m.id == id;
    }
    @Override public int hashCode() { return Integer.hashCode(id); }
}

var map = new HashMap<MutableId, String>();
var key = new MutableId(1);
map.put(key, "v");
key.id = 2;
System.out.println(map.get(key)); // may miss; not guaranteed null
```

**Production rule:** use **immutable** keys (`Long`, `String`, records with final components, UUID strings).

The lookup outcome is **not** “always null.” `HashMap` chooses a bucket from the current hash, then uses equality inside candidate entries. After `key.id = 2`:

- A later `get` with the **same mutated instance** recomputes the hash from the new id. If that hash indexes a different bucket from the one chosen at `put`, the search misses the entry, which still sits in the old bucket.
- If the new hash happens to index the **same** bucket, the walk can still find the entry, because the stored key and the lookup key are the same object and `equals` sees the new id.
- A **different** instance that equals the mutated key is found only when its hash selects the bucket where the entry was stored.

Say “lookup may fail, depending on bucket placement and hash comparison,” not “`get` always returns null.”

## 10. Hash collisions

Collisions are normal. Correctness relies on `equals` after `hashCode` narrows the bucket. Poor hash functions increase chain/tree depth and hurt performance — not the same as breaking the equals/hashCode contract.

## 11. Session implementation — `PaymentRequest`

Equality for this type is the transaction id, not the whole payment payload.

```java
@Override
public boolean equals(Object obj) {
    if (this == obj) {
        return true;
    }
    if (obj == null || getClass() != obj.getClass()) {
        return false;
    }
    PaymentRequest other = (PaymentRequest) obj;
    return Objects.equals(transactionId, other.transactionId);
}

@Override
public int hashCode() {
    return Objects.hash(transactionId);
}
```

`getClass() != obj.getClass()` requires the same runtime class. A subclass instance is not equal. That keeps symmetry when a subclass would otherwise add fields. `instanceof` accepts subclasses and needs a careful design so both directions agree. The symmetry problem is worked in [Lesson 2](02-inheritance-records-and-equality.md).

For a single field, `return Objects.hashCode(transactionId);` is a suitable simpler implementation. It is null-safe and returns that object's hash code (or `0` when the id is null). `Objects.hash(transactionId)` also preserves the contract, but it mixes the value through the varargs formula (`31 * 1 + hash`), so the two calls are not the same integer. Either is fine. Do not mix them across equal instances of the same class. Use `Objects.hash` when several fields participate.

## 12. Inconsistent `hashCode` — equal objects, different codes

Interview setup: `equals` uses only the employee id. `hashCode` uses the employee id **and** the name.

```java
public final class EmployeeKey {
    private final String id;
    private final String name;

    public EmployeeKey(String id, String name) {
        this.id = id;
        this.name = name;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null || getClass() != obj.getClass()) {
            return false;
        }
        EmployeeKey other = (EmployeeKey) obj;
        return Objects.equals(id, other.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name); // name is not part of equals
    }
}
```

`new EmployeeKey("E1", "Asha")` and `new EmployeeKey("E1", "Asha K")` compare equal and can hash differently. `HashSet` is backed by a `HashMap`. It only treats two keys as the same when they land in the same candidate chain **and** `equals` returns true. Different hash codes send them to different buckets, so the set can contain both. The contract failure is the mismatch, not a mysterious `HashSet` bug.

Fields that participate in equality must be enough to force equal hash codes. The practical rule is to hash the same state `equals` uses. Extra fields in `hashCode` are only safe when equal objects cannot differ on those fields.

## Hands-on — contract check

```java
public static void assertEqualsContract(Object x, Object y) {
    if (!x.equals(x)) throw new AssertionError("reflexive");
    if (x.equals(y) != y.equals(x)) throw new AssertionError("symmetric");
    if (x.equals(null)) throw new AssertionError("non-null");
}
```

## Performance notes

- `hashCode` should be **cheap** and use fields already in `equals`.
- Avoid deep graph walks in `hashCode` unless equality requires them.
- `String` caches its hash code — repeated map lookups are efficient.

## Failure scenarios

| Symptom | Likely cause |
| --- | --- |
| `get` misses a key that `equals` would accept | Mutable key field changed after `put`, or `hashCode` was not overridden. Misses depend on the bucket; they are not guaranteed |
| Duplicate “equal” entries in a `Set` | Broken `hashCode` contract |
| Flaky cache hits | Equality includes non-stable fields (timestamp) |

## Best practices

- Override **both** `equals` and `hashCode` together (IDE generators, records).
- Prefer immutable key types at map boundaries.
- Document which fields define equality on value objects.

## Staff engineer notes

- **Liskov:** subclasses that widen equality can break symmetry/transitivity — Lesson 2.
- Distinguish **value equality** from **database identity** (surrogate keys vs natural keys).

## Key takeaways

- `==` is identity; `equals` is logical sameness per class definition.
- **RSTCN:** reflexive, symmetric, transitive, consistent, non-null.
- `equals` ⇒ equal `hashCode`; collisions do not imply equality. Inconsistent hashes let a `HashSet` hold logically equal objects.
- `HashMap` buckets by hash and confirms with `equals`. Mutating a key field may make lookup fail; it does not always return null.

## See also

- [Lesson 2 — Inheritance, records, composition](02-inheritance-records-and-equality.md)
- [Module 3 — HashMap internals](../module-03-hashmap-internals/index.md)
- [Interview Companion](../../../02-interview-companion/core-java/module-02-equals-and-hashcode/01-equals-and-hashcode-contracts.md)
