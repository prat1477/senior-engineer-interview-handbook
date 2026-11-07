---
title: Exceptions — Visual Quick Reference
description: Hierarchy, retries, and idempotency cheat sheet.
status: covered
audience: advanced
tags: [companion, exceptions, cheat-sheet]
updated: 2026-10-28
---

# Exceptions — Visual Quick Reference

## Hierarchy

```mermaid
flowchart TD
  t[Throwable]
  t --> err[Error]
  t --> ex[Exception]
  ex --> chk[Checked]
  ex --> rt[RuntimeException unchecked]
```

## Retry

| Failure | Action |
| --- | --- |
| 503, timeout | Bounded retry, same idempotency key |
| 400 validation | Do not retry |
| Timeout after charge | Query provider, do not new charge |

See also [Concurrency L22 companion](../../concurrency/22-backend-concurrency-scenarios.md).

## Lessons

- [01 hierarchy](01-throwable-hierarchy-and-propagation.md)
- [02 try-with-resources](02-try-with-resources-and-wrapping.md)
- [03 retries and idempotency](03-production-spring-retries-idempotency.md)
