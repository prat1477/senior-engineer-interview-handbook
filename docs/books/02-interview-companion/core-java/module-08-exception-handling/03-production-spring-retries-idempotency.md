---
title: "Companion 3 — Retries and idempotency"
description: Interview recall for Retries and idempotency.
status: covered
audience: advanced
tags: [interview, companion, java]
updated: 2026-10-28
---

# Companion 3 — Retries and idempotency

**Canonical source:** [Mastery lesson](../../../01-engineering-mastery/core-java/module-08-exception-handling/03-production-spring-retries-idempotency.md).

**Cheat sheet:** [Module visual quick reference](module-visual-quick-reference.md).

## Definition

Retries are safe only when the operation is idempotent or the failure happened before any side effect; payments need a stable idempotency key.

## Must remember

- Separate retryable (timeout, 503) from fatal (400 validation).
- Bounded attempts and backoff with jitter.
- Idempotency key reused across retries — not a new UUID each click.
- DB transaction cannot roll back an external charge.

## Interview traps

- Retrying a non-idempotent POST doubles the charge.
- Infinite retry on a bug.

## Interview flow

```mermaid
flowchart TD
  call[Call provider] --> ok{Outcome}
  ok -->|success| store[Store SUCCEEDED]
  ok -->|timeout| same[Retry SAME idempotency key]
  same --> call

```

## Scenario bite

Client double-submits Pay with a new UUID each time — unique constraint does not dedupe. Reuse Idempotency-Key or a payment intent id.

## Decision table

| Situation | Prefer |
| --- | --- |
| Transient 503 | Retry with same key |
| Validation 400 | Do not retry |
| Unknown after timeout | Query provider, do not new charge |

## Explain aloud (whiteboard)

1. Classify the failure.
2. Same business key on retry.
3. Effectively-once, not magic exactly-once.

## 30-second revision

- Retry only idempotent or keyed operations; persist outcome before assuming success.

## Memory hook

- **KEY** — Keep the same idempotency key.

## Cross-links

- [Module visual quick reference](module-visual-quick-reference.md)
