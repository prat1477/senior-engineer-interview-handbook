---
title: "Lesson 5 — Streams Interview Practice"
description: Pipeline, collectors, parallel traps, and scenario questions.
status: draft
audience: advanced
tags: [streams, interview, module-6, lesson-5]
created: 2026-10-17
updated: 2026-10-17
---

# Lesson 5 — Streams Interview Practice

Use a shared model:

```java
record Employee(String name, String dept, String title, double salary) {}
```

Answers: [06-interview-assessment-answers.md](module-interview-assessment-answers.md).

## Conceptual

1. When does a stream pipeline actually execute?
2. Why is `allMatch` on an empty stream `true`?
3. What is the difference between `unordered()` and `sorted()`?

## Code / debugging

4. What is wrong with collecting into a shared `ArrayList` inside `forEach` on a `parallelStream`?

5. Write a pipeline: total salary for Engineering employees using primitive aggregation.

6. Group employees by department and job title into `Map<String, Map<String, List<Employee>>>`.

7. Build a `Map<String, Employee>` by name; two employees share a name — how do you avoid `IllegalStateException`?

8. Compare one `flatMap` vs nested `map` when parsing lines into tokens.

## Scenario

9. A service logs PII inside `peek` before `filter`. Why might audits miss rejected records?

10. You need top 3 salaries from 10 million rows in memory. Sort + limit or heap? What do you say in the interview?

## Mini-assessment

| # | Task |
| --- | --- |
| A | Short-circuit: first Engineering employee with salary > 200k. |
| B | `partitioningBy` for salary > 100k and count each partition. |
| C | Why must you not use `Stream` twice on the same instance? |
## Whiteboard (use the cheat sheet)

1. Draw the module flowchart from the visual quick reference without notes.
2. Give one production scenario and the decision-table row you would choose.
3. Name one interview trap and the correction.
