---
title: "Lesson 7 — Iterators and Modifying Collections During Iteration"
description: Fail-fast behavior, safe removal, and ConcurrentModificationException.
status: draft
audience: advanced
tags: [collections, iterator, module-4, lesson-7]
created: 2026-10-15
updated: 2026-10-15
---

# Lesson 7 — Iterators and Modifying Collections During Iteration

Iteration is how you process collections in business logic. Structural changes during iteration require discipline — **fail-fast** iterators detect many illegal patterns but are **not** a correctness or concurrency guarantee.

## 1. Iterator API

```java
Iterator<String> it = names.iterator();
while (it.hasNext()) {
    String name = it.next();
    if (name.isEmpty()) {
        it.remove(); // safe: updates iterator state
    }
}
```

- **`hasNext()`** / **`next()`** — walk elements.
- **`remove()`** — removes last returned element via iterator.

## 2. Enhanced for-loop

```java
for (String name : names) { ... }
```

Uses an iterator under the hood — same structural modification rules apply.

## 3. Unsafe: modify collection directly

```java
for (String name : names) {
    if (name.isEmpty()) {
        names.remove(name); // often ConcurrentModificationException
    }
}
```

Direct `Collection.remove` while iterating can leave iterator state inconsistent → **`ConcurrentModificationException`** (best-effort).

## 4. Safe alternatives

- **`iterator.remove()`** during explicit iteration.
- **`removeIf(Predicate)`** — bulk remove with defined behavior.
- **Copy-on-write** or **concurrent** collections for concurrent access (different rules — see [Lesson 12](12-concurrent-collections-overview.md)).

## 5. Fail-fast limitations

| Fact | Implication |
| --- | --- |
| Not guaranteed in all cases | Do not rely on CME for program logic |
| Single-threaded structural change | Typical trigger |
| Not thread safety | Use concurrent collections or synchronization for threads |

Multiple threads modifying a non-concurrent collection can corrupt state **without** CME.

## Incorrect vs correct pattern

```java
// Incorrect for ArrayList during foreach
list.forEach(x -> { if (bad(x)) list.remove(x); });

// Correct
list.removeIf(bad);
```

## Revision notes

- Foreach = iterator.
- Structural change during iteration → use iterator.remove or removeIf.
- Fail-fast ≠ thread-safe.

## See also

- [Concurrent collections overview](12-concurrent-collections-overview.md)
