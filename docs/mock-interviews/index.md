---
title: Mock Interview Framework
description: Day 13 full mock and reusable session templates.
status: planned
audience: advanced
tags: [mock-interview]
created: 2026-10-15
updated: 2026-11-14
---

# Mock Interview Framework

**Status: Planned** — use on Day 13 of the [14-day roadmap](../14-day-roadmap.md).

## Day 13 sequence (fixed order)

1. Java and Collections
2. Coding and complexity analysis
3. Concurrency
4. Spring Boot and microservices
5. Kafka
6. Distributed-system design
7. Data engineering and lakehouse
8. AWS / production scenarios (as needed)
9. Behavioral (short segment)

## Session template

See [framework.md](framework.md) for timing, scoring rubric placeholders, and self-assessment columns (leave blank until you run a mock).

## Self-assessment

| Area | Confident | Needs practice | Not yet covered |
| --- | --- | --- | --- |
| Java / Collections | _fill after mock_ | | |
| Coding | | | |
| Concurrency | | | |
| Microservices | | | |
| Kafka | | | |
| System design | | | |
| Data / lakehouse | | | |
| Behavioral | | | |

Do not pre-fill scores.

## Candidate-reported JPMorgan Chase SDE-3 patterns (research, not hiring criteria)

The following is a concise preparation signal from three public, firsthand candidate reports. It
is **not** official JPMorgan Chase guidance and does not predict an exact interview format or
question. Treat it as a reason to practise transferable senior-engineering skills, not a question
bank to memorize.

| Reported pattern | Preparation implication |
| --- | --- |
| Coding / medium DSA, including arrays, stacks, graphs, linked lists, and reasoning about optimal solutions | Continue independent Java coding with edge cases, complexity, and clear explanation. |
| Pull-request review, code cleanup, Java/Spring questions, concurrency, and project-technology follow-ups | Practise a realistic Spring Boot review: correctness, shared state, errors, SQL/cache behaviour, and trade-offs. Be ready to defend choices on the résumé. |
| Streams/Collections follow-up | Explain idiomatic Java after solving a problem; do not trade correctness for cosmetic stream usage. |
| HLD/LLD such as payment systems, document validation, delivery-style domain modelling, and scalability/caching/SQL | Practise requirements, APIs, data model, async workflow, idempotency, failure paths, and end-to-end diagrams. |
| Behavioural / hiring-manager depth | Prepare concise, truthful contribution stories, cross-team collaboration, learning, and mentorship examples. |

One report also mentioned Java 21, distributed concurrency, detailed review/fix exercises, and a
document-validation design; another reported payment-system HLD plus a pull-request/DSA/Streams
round. These reports support the current priorities, but neither establishes a company-wide
standard nor verifies React, Spring Security, JavaScript, Java 25, rate limiter, or Agentic-AI
coverage for this specific process.

Sources: [Bangalore SDE-3 candidate report](https://leetcode.com/discuss/post/7359766/jpmorgan-chase-sde-3-java-full-stack-dev-rxak/), [SDE-3 candidate report](https://leetcode.com/discuss/post/7128358/jpmc-sde-3-interview-exp-by-anonymous_us-5ya6/), and [Mumbai SDE-3 candidate report](https://leetcode.com/discuss/post/6766946/jpmorgan-interview-experice-sde-3-mumbai-o9su/).

### Project-story guardrail

Reserve preparation time for current-organization AI work: explain the verified architecture,
data flow, tool invocation, security, failure handling, observability, and your actual
contribution. Do not claim personal ownership of the complete architecture unless independently
established, and do not invent technologies for organizational initiatives or the separate
TwinOps AI portfolio project.
