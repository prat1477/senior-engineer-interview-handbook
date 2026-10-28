---
title: Module 3 — Interview Practice
description: HashMap internals drills.
status: covered
audience: advanced
tags: [interview, module-3]
created: 2026-10-20
updated: 2026-10-20
---

# Module 3 — Interview Practice

Answers: [module-interview-assessment-answers.md](module-interview-assessment-answers.md).

## Checklist

- [ ] spread `h ^ (h >>> 16)` (OpenJDK)
- [ ] index `(capacity-1) & hash`
- [ ] threshold = capacity × load factor; default 12 @ 16
- [ ] 13th **distinct** key resize
- [ ] treeify: 8 / 6 / 64 constants (implementation)
- [ ] CHM `merge` vs get+put

## Questions

1. How does `HashMap` calculate a bucket index?
2. Why spread hash bits?
3. Outline `put()` for new vs existing key.
4. Outline `get()` when collisions exist.
5. When can a bucket become a tree (OpenJDK)?
6. Capacity vs size vs threshold?
7. Why can the 13th distinct mapping resize a default map?
8. Why doesn’t occupied bucket count set the threshold?
9. What happens during resize?
10. Risks of mutable keys and poor `hashCode`?
11. Why is `HashMap` not thread-safe?
12. Fix lost increment on concurrent map?

## Output prediction

13. After 12 distinct `put`s on new `HashMap()`, does `size()` return 12 before any resize? (default path)

14. Two threads both `put(k, getOrDefault(k,0)+1)` — possible final value?
