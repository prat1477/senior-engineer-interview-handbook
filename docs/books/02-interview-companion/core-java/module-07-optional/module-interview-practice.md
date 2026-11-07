---
title: "Lesson 3 — Optional Interview Practice"
description: orElse traps, composition, and service-layer scenarios.
status: draft
audience: advanced
tags: [optional, interview, module-7, lesson-3]
created: 2026-10-17
updated: 2026-10-17
---

# Lesson 3 — Optional Interview Practice

Answers: [04-interview-assessment-answers.md](module-interview-assessment-answers.md).

## Questions

1. What is the difference between `Optional.of(null)` and `Optional.ofNullable(null)`?

2. Why is `user.orElse(loadUserFromDb())` dangerous when `loadUserFromDb()` is expensive?

3. When should a repository return `Optional<T>` vs throw `NotFoundException`?

4. What does `optional.map(User::getName)` return if `getName()` returns `null`?

5. Rewrite without `isPresent`/`get`:

```java
if (opt.isPresent()) {
    return opt.get().getBalance();
}
return BigDecimal.ZERO;
```

6. Is `List<Optional<Payment>>` a good API shape? Why?

7. **Scenario:** REST controller receives optional query param. Should the controller method take `Optional<String>`?

## Mini-assessment

| # | Task |
| --- | --- |
| A | Chain: userId → user → shipping address → zip code as `Optional<String>`. |
| B | Primary cache `Optional`, fallback DB — use `or()`. |
| C | Name one JDK version for `isEmpty()` and one for `or()`. |
## Whiteboard (use the cheat sheet)

1. Draw the module flowchart from the visual quick reference without notes.
2. Give one production scenario and the decision-table row you would choose.
3. Name one interview trap and the correction.
