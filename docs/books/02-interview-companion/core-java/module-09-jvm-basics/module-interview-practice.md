---
title: "Lesson 10 — JVM Memory Debugging Scenarios and Interview Practice"
description: GC churn, retention, dominators, Spring singleton, container OOM, shallow vs retained.
status: draft
audience: advanced
tags: [jvm, interview, module-9, lesson-10]
created: 2026-10-18
updated: 2026-10-18
---

# Lesson 10 — JVM Memory Debugging Scenarios and Interview Practice

Answers: [module-interview-assessment-answers.md](module-interview-assessment-answers.md).

## Scenarios

1. **Frequent GC, but post-GC heap occupancy remains stable.**  
   What does this suggest? Is it always a memory leak?

2. **Post-GC heap occupancy rises over time.**  
   What is your next step?

3. **A large `HashMap` retains millions of `byte[]` entries.**  
   Which heap-dump views do you use first?

4. **A Spring `@Singleton` bean holds a growing `List` of events.**  
   Why does GC not reclaim those events?

5. **Container memory exceeds its limit while Java heap usage stays below `-Xmx`.**  
   What areas do you investigate?

6. **`OutOfMemoryError` vs `StackOverflowError`.**  
   Which memory areas are involved?

7. **Heap usage looks stable but the process still has memory pressure.**  
   Why are heap metrics alone insufficient?

8. **Why is increasing `-Xmx` not always the right fix?**  
   Include container budget risk.

9. **When would you use GC logs versus a heap dump?**

10. **What is the difference between shallow size and retained heap?**  
    Sketch a tiny object graph in your answer.

## Conceptual (short)

11. Name three GC roots you would mention in a senior interview.

12. What does `-XX:MaxGCPauseMillis` **not** guarantee for G1?

13. Why can `WeakHashMap` fail to remove entries even when keys are no longer used in application logic?

14. Summarize the Spark SQL optimizer OOM case in three sentences — **only documented facts**.

## Mini-assessment

| # | Task |
| --- | --- |
| A | Write `jcmd` to capture a heap dump for PID `12345` to `/tmp/app.hprof`. |
| B | One flag to enable GC logging on JDK 17+. |
| C | One sentence: Java memory leak definition. |
