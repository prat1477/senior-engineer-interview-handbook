---
title: "Lesson 4 — Exception Handling Interview Practice"
description: finally traps, suppressed exceptions, Spring and payment scenarios.
status: draft
audience: advanced
tags: [exceptions, interview, module-8, lesson-4]
created: 2026-10-17
updated: 2026-10-17
---

# Lesson 4 — Exception Handling Interview Practice

Answers: [05-interview-assessment-answers.md](module-interview-assessment-answers.md).

## Conceptual

1. Checked vs unchecked — when would you add a **checked** exception to a public library API?

2. What happens if both `try` block and `close()` throw?

3. Why is `catch (Exception e) { throw new RuntimeException(e); }` at every layer harmful?

## Code / debugging

4. What does `bad()` return?

```java
int bad() {
    try {
        return 1;
    } finally {
        return 2;
    }
}
```

5. Write try-with-resources for a `Connection` that must close.

6. Show wrapping that preserves the original stack:

```java
throw new OrderProcessingException("Unable to process order", e);
```

## Scenario (senior)

7. Payment succeeds; DB update fails; client retries. Explain role of **idempotency key** persisted before charge.

8. Why does idempotency **not** alone give atomic consistency between PSP and your database?

9. Name two failure types where retry with backoff is reasonable vs two where it is not.

10. How does exception handling differ from saga/outbox recovery?

## Mini-assessment

| # | Task |
| --- | --- |
| A | Order catch blocks for `SQLException` then `Exception`. |
| B | Access suppressed exception from caught `IOException`. |
| C | One sentence: retry policy should depend on what? |
## Whiteboard (use the cheat sheet)

1. Draw the module flowchart from the visual quick reference without notes.
2. Give one production scenario and the decision-table row you would choose.
3. Name one interview trap and the correction.
