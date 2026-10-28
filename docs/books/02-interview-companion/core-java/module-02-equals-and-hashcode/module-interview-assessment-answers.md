---
title: Module 2 — Assessment Answers
description: Answers for Module 2 interview practice.
status: covered
audience: advanced
tags: [interview, module-2, answers]
created: 2026-10-20
updated: 2026-10-20
---

# Module 2 — Assessment Answers

1. **Reflexive, symmetric, transitive, consistent, non-null** (`false` for `null`).
2. Hash structures bucket by `hashCode` then confirm with `equals`; unequal hashes would split equal keys.
3. **Yes** — collisions are normal; `equals` disambiguates.
4. Equal logical keys may sit in different buckets; `get`/`Set` break.
5. Changing fields used in `hashCode`/`equals` moves or orphans entries; `get` returns null.
6. Subclass/parent `equals` accept different types (e.g. `Point` vs `ColorPoint`) → `p.equals(cp) != cp.equals(p)`.
7. Component-wise equality on **all** record components; generated `hashCode` matches.

8. **`null`** (or absent behavior) — keys equal by `equals` but different identity hash buckets.

9. Set may contain duplicates logically, or `contains` fails after mutation — unstable `hashCode`.

10. Intermittent cache/map misses after status updates; “same” order id not found until restart.
