---
title: JVM — Visual Quick Reference
description: Memory areas, GC, and OOM triage cheat sheet.
status: covered
audience: advanced
tags: [companion, jvm, cheat-sheet]
updated: 2026-10-28
---

# JVM — Visual Quick Reference

```mermaid
flowchart TD
  oom[OutOfMemoryError] --> heap[Java heap space dump]
  oom --> meta[Metaspace class loaders]
  oom --> thr[Unable to create thread]
  heap --> dom[Dominator tree]
```

| Area | Holds |
| --- | --- |
| Heap | Objects |
| Stack | Frames per thread |
| Metaspace | Class metadata |

| Signal | First move |
| --- | --- |
| Heap OOM | Dump, find retainer, bound cache |
| Container kill | `-Xmx` vs cgroup |
| High alloc | Reduce garbage before collector folklore |

Lessons 01–09 in this folder.
