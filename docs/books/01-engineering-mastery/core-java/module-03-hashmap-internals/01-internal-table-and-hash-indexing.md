---
title: "Lesson 1 — Bucket Table, Hash Spreading, and Indexing"
description: OpenJDK HashMap table, hash spread, power-of-two indexing.
status: covered
audience: practitioner
tags: [java, hashmap, module-3, lesson-1]
created: 2026-10-20
updated: 2026-10-20
---

# Lesson 1 — Bucket Table, Hash Spreading, and Indexing

## Overview

`HashMap` (OpenJDK) stores entries in an array of **buckets**. Each bucket holds zero or more entries (list or tree). This lesson covers how a key’s `hashCode()` becomes a bucket index. API guarantees: unique keys, `get`/`put` behavior — **not** internal bucket layout (implementation detail).

**Prerequisite:** [Module 2 — equals/hashCode](../module-02-equals-and-hashcode/01-equals-and-hashcode-contracts.md). **Shallow usage:** [Collections M4 L4](../module-04-collections/04-map-fundamentals-and-hashmap.md).

## 1. Internal bucket array and capacity

- **`table`**: array of bucket heads (`Node<K,V>[]` or null slots).
- **`capacity`**: length of `table` (always a **power of two** in OpenJDK `HashMap`).
- **`size`**: number of **key-value mappings** (not number of non-empty buckets).

**Lazy allocation:** a new `HashMap()` does not allocate the bucket array until the first `put` that needs it (implementation detail; do not rely on for memory accounting in all JDK versions without checking source).

## 2. Role of `key.hashCode()`

`hashCode()` returns a 32-bit `int`. Keys with broken contracts (`equals` overridden without `hashCode`) break lookup — see Module 2.

## 3. Hash spreading (OpenJDK)

High bits of hash codes are mixed into low bits so keys that differ only in high bits still distribute:

```text
spread = h ^ (h >>> 16)
```

(`h` is `key.hashCode()` after a null check for keys; `HashMap` allows one null key.)

**Purpose:** when capacity is small, indexing uses only low bits; spreading reduces clustering from similar `hashCode()` patterns.

## 4. Bucket index

```text
index = (capacity - 1) & spread
```

Because `capacity` is `2^n`, `(capacity - 1)` is a bitmask selecting `n` low bits — fast modulo.

Example: capacity 16 → mask `0b1111` → indices 0–15.

## 5. Why power-of-two capacity

- Bitmask indexing is fast.
- Resize **doubles** capacity; redistribution can use bit tricks (see Lesson 3).

Trade-off: power-of-two tables can interact badly with some hash patterns; spreading mitigates but does not eliminate clustering.

## Diagram

```text
key.hashCode() --> spread (h ^ (h>>>16)) --> index = (n-1) & spread --> table[index]
```

## Hands-on — observe index (educational)

```java
import java.util.HashMap;

public class IndexDemo {
    public static void main(String[] args) {
        int capacity = 16;
        String key = "tenant:42";
        int h = key.hashCode();
        int spread = h ^ (h >>> 16);
        int index = (capacity - 1) & spread;
        System.out.println("hashCode=" + h + " spread=" + spread + " index=" + index);
        new HashMap<String, String>().put(key, "v"); // actual map uses internal capacity
    }
}
```

## Key takeaways

- **Capacity** = bucket array length (power of two).
- **Spread** mixes high/low hash bits before indexing.
- **Index** = `(capacity - 1) & spread`.
- Distinct from **size** (mapping count).

## See also

- [Lesson 2 — put/get and treeify](02-put-get-flow-and-treeify.md)
