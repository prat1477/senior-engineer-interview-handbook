---
title: "Companion 4 — synchronized"
description: Monitors, reentrancy, and virtual-thread pinning notes.
status: covered
audience: advanced
tags: [interview, companion, concurrency, lesson-4]
updated: 2026-10-25
---

# Companion 4 — `synchronized`

**Canonical source:** [Lesson 4 — synchronized](../../../concurrency/04-synchronized.md).

## Definition

`synchronized` acquires an object’s **monitor** — mutual exclusion plus unlock→lock happens-before for the next acquirer.

## Why it exists

Simple in-JVM critical sections without explicit `Lock` API; establishes HB for guarded fields.

## Must remember

- **Reentrant** — same thread can re-enter the same monitor.
- One monitor per object; static methods lock on `Class` object.
- Coarse locking → contention and throughput loss.
- No `tryLock` / timeout — use `ReentrantLock` ([Companion 6](06-locks.md)).
- Virtual threads: blocking in `synchronized` may **pin** carrier (JDK-dependent) — [Companion 14](14-virtual-threads.md).

## Interview traps

- `synchronized` on a **new** object per call — no mutual exclusion.
- Assuming instance method sync helps **two JVMs** on the same DB row.

## Frequently asked questions

- **Q:** What HB edge does `synchronized` create?
  **A:** Unlock on monitor M happens-before subsequent lock on M.
- **Q:** `synchronized` vs `volatile`?
  **A:** Sync = mutual exclusion + HB; volatile = visibility for one field, no compound atomicity.

## Interview flow

```mermaid
flowchart LR
  enter[enter synchronized]
  cs[critical section]
  exit[exit releases monitor]
  enter --> cs --> exit
  exit -->|HB| next[next thread lock]
```

## ASCII / table recall

```text
Thread A: [ lock obj ] work [ unlock ] --HB--> Thread B: [ lock obj ]
```

## Explain aloud (whiteboard)

1. “Monitor = built-in lock on an object; only one thread in the block.”
2. “Unlock happens-before the next lock — visibility for guarded state.”
3. “For try/timeout or fairness I use `ReentrantLock`; on VT I watch pinning.”

## JDK and debug clues

- Many threads `BLOCKED` on same monitor → lock contention hotspot.
- JFR / pinning events on virtual threads inside synchronized blocks.

## 30-second revision

- Monitor, reentrant, HB on unlock; not distributed; pinning risk on VT; use Lock for timeouts.

## Memory hooks

- **MHB** — **M**onitor unlock **H**appens-before next **B**lock.

## Cross-links

- [Companion 6 — Locks](06-locks.md)
- [Companion 14 — Virtual threads](14-virtual-threads.md)
