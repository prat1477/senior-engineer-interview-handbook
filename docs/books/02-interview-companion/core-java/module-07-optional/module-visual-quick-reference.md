---
title: Optional — Visual Quick Reference
description: Presence, map, and flatMap cheat sheet.
status: covered
audience: advanced
tags: [companion, optional, cheat-sheet]
updated: 2026-10-28
---

# Optional — Visual Quick Reference

```mermaid
flowchart TD
  find[Repository Optional] --> present{present?}
  present -->|value| map[map]
  present -->|nested Optional| flat[flatMap]
  present -->|required| thr[orElseThrow]
```

| API | Use |
| --- | --- |
| `orElse` | Cheap default |
| `orElseGet` | Expensive default |
| `map` | `T → U` |
| `flatMap` | `T → Optional<U>` |

- [01 fundamentals](01-optional-fundamentals.md)
- [02 composition](02-optional-composition-and-antipatterns.md)
