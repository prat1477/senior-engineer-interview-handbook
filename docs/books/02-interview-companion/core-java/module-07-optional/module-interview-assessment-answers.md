---
title: "Optional — Assessment Answers"
description: Answers for Module 7 interview practice.
status: draft
audience: advanced
tags: [optional, interview, answers, module-7]
created: 2026-10-17
updated: 2026-10-17
---

# Optional — Assessment Answers

## 1. `of` vs `ofNullable` with null

`of(null)` throws **NPE**. `ofNullable(null)` returns `Optional.empty()`.

## 2. `orElse` eager evaluation

`loadUserFromDb()` is evaluated **before** `orElse` runs — always hits DB. Use `orElseGet(() -> loadUserFromDb())`.

## 3. Optional vs exception

**Optional:** absence is a normal outcome (lookup by optional key). **Exception:** violated invariant or client error requiring error response. `require*` methods throw for HTTP 404-style cases.

## 4. `map` and null result

`map` treats null result as **empty** Optional (no nested `Optional`).

## 5. Idiomatic rewrite

```java
return opt.map(Account::getBalance).orElse(BigDecimal.ZERO);
```

## 6. `List<Optional<Payment>>`

Poor — forces callers to unwrap. Prefer `List<Payment>` (only successes) or a sealed result type / stream of present values.

## 7. `Optional` request parameter

Generally **no** — use `@RequestParam(required = false) String` or `Optional` only if team style guide allows; Spring supports it but many teams ban Optional parameters for clarity.

## Mini-assessment

**A.**

```java
findUser(id)
    .flatMap(User::getShippingAddress)
    .map(Address::getZipCode);
```

**B.**

```java
cache.get(key).or(() -> db.find(key));
```

**C.** `isEmpty()` — Java 11+; `or()` — Java 9+.
