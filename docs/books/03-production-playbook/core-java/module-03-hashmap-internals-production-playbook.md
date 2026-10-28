---
title: Module 3 — HashMap Production Playbook
description: Lookup failures, performance, lost updates, sizing.
status: covered
audience: operator
tags: [playbook, module-3, hashmap]
created: 2026-10-20
updated: 2026-10-20
---

# Module 3 — HashMap Production Playbook

Operational scenarios derived from [Engineering Mastery Module 3](../../01-engineering-mastery/core-java/module-03-hashmap-internals/index.md). Illustrative examples only — not reported production incidents.

## Case 1 — HashMap lookup unexpectedly fails

### Symptoms

- `map.get(key)` returns `null` though key “looks” present
- Cache appears to miss after in-place object update

### Likely causes

- **Mutable key** mutated after `put` (equality/hash fields changed)
- **`equals` without matching `hashCode`**
- Wrong key instance (equal logically but not found — see Module 2)

### Inspect

- Review `equals`/`hashCode` fields; confirm immutability.
- Reproduce with minimal main:

```java
class MutableKey {
    String id;
    MutableKey(String id) { this.id = id; }
    @Override public boolean equals(Object o) {
        return o instanceof MutableKey m && Objects.equals(id, m.id);
    }
    @Override public int hashCode() { return Objects.hashCode(id); }
}

var map = new HashMap<MutableKey, String>();
var k = new MutableKey("a");
map.put(k, "v");
k.id = "b";
System.out.println(map.get(k)); // null
```

### Corrective actions

- Replace key type with immutable value (`String`, record with final fields).
- See [Module 2 playbook](module-02-equals-and-hashcode-production-playbook.md).

---

## Case 2 — Poor HashMap performance

### Symptoms

- Elevated CPU on map-heavy path; latency grows with modest entry count

### Possible causes

- **Degenerate hashing** (constant or clustered `hashCode`)
- **O(n) bucket chains** before/without treeify
- Oversized map causing memory pressure (GC) — correlate with heap metrics
- Wrong structure (frequent ordered traversal — consider `TreeMap` if sorted order required)

### Evidence to gather

- Allocation rate, GC pause, flame graph on `HashMap.get/put`
- Map `size` and key type; sample hash distribution in tests
- Confirm problem is map path vs DB/network

### Remediation

- Fix key `hashCode` quality; use stable immutable keys
- `new HashMap<>(expectedSize)` when size known
- If ordering required, choose appropriate `Map` implementation ([M4 L5](../../01-engineering-mastery/core-java/module-04-collections/05-hashmap-linkedhashmap-treemap.md))

---

## Case 3 — Lost updates during concurrent map access

### Symptoms

- Under-counted metrics; intermittent wrong aggregates

### Cause

Non-atomic read-modify-write on plain `HashMap`:

```java
map.put(key, map.getOrDefault(key, 0L) + 1); // race
```

### Fix patterns

```java
ConcurrentHashMap<String, Long> m = new ConcurrentHashMap<>();
m.merge("hits", 1L, Long::sum);

ConcurrentHashMap<String, LongAdder> metrics = new ConcurrentHashMap<>();
metrics.computeIfAbsent("hits", k -> new LongAdder()).increment();
```

**Limits:** single-key atomicity only; multi-key invariants need transactions or locks. See [Mastery L4](../../01-engineering-mastery/core-java/module-03-hashmap-internals/04-thread-safety-and-concurrent-patterns.md).

---

## Case 4 — Memory and resize considerations

### Symptoms

- Heap growth from large maps; allocation spikes during warm-up

### Notes

- Default map grows by resize when **size > threshold** (not per collision).
- Pre-size: `HashMap` constructor with expected mappings reduces resize copies.

### Procedure

1. Estimate peak distinct keys; set initial capacity via constructor.
2. Monitor heap after deploy; compare before/after pre-sizing.
3. If growth unbounded, add eviction (cache policy) — [LinkedHashMap LRU](../../01-engineering-mastery/core-java/module-04-collections/11-linkedhashmap-lru-cache.md).

## See also

- [Module 4 Collections playbook](module-04-collections-production-playbook.md)
- [Concurrency curriculum](../../../concurrency/index.md)
