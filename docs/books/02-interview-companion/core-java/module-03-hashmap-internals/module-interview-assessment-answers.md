---
title: Module 3 — Assessment Answers
description: Answers for Module 3 interview practice.
status: covered
audience: advanced
tags: [interview, module-3, answers]
created: 2026-10-20
updated: 2026-10-20
---

# Module 3 — Assessment Answers

1. `spread = hashCode ^ (hashCode >>> 16)`; `index = (table.length - 1) & spread`.
2. Use high bits so similar low-only patterns still distribute when capacity is small.
3. New key: insert, `size++`, maybe resize. Existing equal key: replace value, `size` unchanged.
4. Check head; if no match, walk linked list or search tree bin using hash then `equals`.
5. When chain length reaches treeify threshold (8) **and** table capacity ≥ 64 (OpenJDK), on insertion path — not guaranteed for every bucket at exactly 8.
6. **Capacity** = buckets; **size** = mappings; **threshold** = max size before resize (capacity × load factor).
7. Threshold 12; 13th distinct mapping makes `size > threshold`.
8. Threshold is based on **mapping count**, not how many buckets are non-empty.
9. Double capacity; rehash entries into new table (often same index or + old capacity).
10. Lost lookups / one long bucket / O(n) scans.
11. Concurrent structural changes without sync → corruption or lost updates; not designed for multi-writer.
12. `ConcurrentHashMap.merge(k, 1, Long::sum)` or `LongAdder` per key.

13. **Yes** — `size` is 12; resize typically triggers when adding 13th **distinct** key (after increment crosses threshold).
14. **1** if both read 0 — lost update; not atomic.
