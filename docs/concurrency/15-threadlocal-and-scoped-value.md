---
title: "Lesson 15 — ThreadLocal and ScopedValue"
description: Request context, cleanup, virtual-thread memory, ScopedValue (JDK 21+).
status: covered
audience: advanced
tags: [concurrency, lesson-15, threadlocal]
created: 2026-10-25
updated: 2026-10-25
---

# Lesson 15 — `ThreadLocal` and `ScopedValue`

## ThreadLocal — thread confinement

```java
private static final ThreadLocal<String> REQUEST_ID = new ThreadLocal<>();

void handle() {
    REQUEST_ID.set(UUID.randomUUID().toString());
    try {
        service.process();
    } finally {
        REQUEST_ID.remove(); // mandatory in pooled threads
    }
}
```

**Pool reuse:** without `remove()`, next task on same platform thread sees **stale** request ID (security + logic bugs).

## Propagation limits

`ThreadLocal` does **not** flow to:

- `ExecutorService.submit` workers (unless you copy explicitly)
- `CompletableFuture` chains
- Virtual threads you did not set it on

For async pipelines use explicit context propagation (MDC adapters, `ScopedValue`, tracing APIs).

## Virtual threads + ThreadLocal

Many virtual threads each holding large `ThreadLocal` maps → **heap** pressure. Prefer immutable context objects; avoid unbounded ThreadLocal caches per VT.

## ScopedValue (JDK 21+ preview, finalized JDK 23+)

Dynamically scoped binding — readable only while scope is active:

```java
private static final ScopedValue<String> REQ = ScopedValue.newInstance();

ScopedValue.where(REQ, requestId).run(() -> {
    service.process(); // REQ.get() valid here
});
```

| | ThreadLocal | ScopedValue |
| --- | --- | --- |
| Lifetime | Until removed | Lexical/dynamic scope |
| Immutability | Often mutable holder | Bound value treated immutable in scope |
| Async propagation | Manual | **Not automatic** for arbitrary async — still bound execution boundaries |

**Version:** confirm `ScopedValue` on your JDK (preview vs final). Not a drop-in for all logging frameworks without integration.

## 10+ YOE pitch

“ThreadLocal in pools demands `remove()` in `finally`. For virtual threads I minimize ThreadLocal footprint. ScopedValue models request context with clearer bounds but still does not magically cross every async boundary.”

## Cross-links

- [Lesson 21 — Production debugging](21-production-debugging.md)
- [Lesson 14 — Virtual threads](14-virtual-threads.md)
