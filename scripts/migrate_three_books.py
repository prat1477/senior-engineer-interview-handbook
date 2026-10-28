#!/usr/bin/env python3
"""Generate three-book Core Java content from legacy docs/java lessons."""
from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LEGACY_JAVA = DOCS / "java"
BOOKS = DOCS / "books"
MASTERY = BOOKS / "01-engineering-mastery" / "core-java"
COMPANION = BOOKS / "02-interview-companion" / "core-java"
PLAYBOOK = BOOKS / "03-production-playbook" / "core-java"

SHARED_DOMAIN = textwrap.dedent(
    """
## Shared domain models

Examples across Modules 4–9 reuse the same records so mental models transfer:

```java
public record Employee(long id, String name, String department, double salary) {}
public record Order(long id, long employeeId, String sku, int quantity, double unitPrice) {}
public record Payment(long orderId, String method, double amount, java.time.Instant paidAt) {}
```

Use them for grouping (`Collectors.groupingBy`), maps (`Map<Long, Employee>`), optional chains
(`Optional<Employee>`), and exception boundaries around payment APIs.
"""
).strip()

MODULES: dict[int, dict] = {
    4: {
        "slug": "module-04-collections",
        "title": "Collections",
        "dir": "module-04-collections",
        "playbook": "module-04-collections-production-playbook.md",
        "practice_src": ("14-interview-practice.md", "15-interview-assessment-answers.md"),
    },
    5: {
        "slug": "module-05-generics",
        "title": "Generics",
        "dir": "module-05-generics",
        "playbook": "module-05-generics-production-playbook.md",
        "practice_src": ("05-interview-practice.md", "06-interview-assessment-answers.md"),
    },
    6: {
        "slug": "module-06-java-8-streams",
        "title": "Java 8 Streams",
        "dir": "module-06-java-8-streams",
        "playbook": "module-06-java-8-streams-production-playbook.md",
        "practice_src": ("05-interview-practice.md", "06-interview-assessment-answers.md"),
    },
    7: {
        "slug": "module-07-optional",
        "title": "Optional",
        "dir": "module-07-optional",
        "playbook": "module-07-optional-production-playbook.md",
        "practice_src": ("03-interview-practice.md", "04-interview-assessment-answers.md"),
    },
    8: {
        "slug": "module-08-exception-handling",
        "title": "Exception handling",
        "dir": "module-08-exception-handling",
        "playbook": "module-08-exception-handling-production-playbook.md",
        "practice_src": ("04-interview-practice.md", "05-interview-assessment-answers.md"),
    },
    9: {
        "slug": "module-09-jvm-basics",
        "title": "JVM basics and GC",
        "dir": "module-09-jvm-basics",
        "playbook": "module-09-jvm-basics-production-playbook.md",
        "practice_src": ("10-interview-practice.md", "11-interview-assessment-answers.md"),
    },
}


@dataclass
class LessonDoc:
    rel_path: str
    title: str
    description: str
    body: str
    tags: list[str]


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, parts[2].lstrip("\n")


def load_lesson(path: Path) -> LessonDoc:
    raw = path.read_text(encoding="utf-8")
    fm, body = parse_front_matter(raw)
    return LessonDoc(
        rel_path=str(path.relative_to(LEGACY_JAVA)).replace("\\", "/"),
        title=fm.get("title", path.stem),
        description=fm.get("description", ""),
        body=body,
        tags=[t.strip() for t in fm.get("tags", "java").split(",")],
    )


def strip_legacy_tail(body: str) -> str:
    """Remove revision / interview-only sections already covered in Companion."""
    cut_markers = [
        "\n## Revision notes",
        "\n## Interview summary",
        "\n## Key takeaways",
        "\n## See also",
    ]
    out = body
    for m in cut_markers:
        idx = out.find(m)
        if idx != -1:
            out = out[:idx]
    return out.rstrip() + "\n"


def m4_l1_pilot_extra() -> str:
    return textwrap.dedent(
        """
## Architecture

The JCF splits **contracts** (`java.util` interfaces) from **implementations**
(`java.util` concrete classes and `java.util.concurrent` concurrent variants).
Application layers (REST controllers, batch jobs, stream processors) should depend
on the narrowest interface that expresses required semantics:

| Layer | Typical types | Why |
| --- | --- | --- |
| Domain service | `Map<Long, Employee>`, `Deque<Order>` | Stable API across refactors |
| Integration | `BlockingQueue<Payment>` | Backpressure at boundaries |
| Analytics path | `Stream<Employee>` (Module 6) | Declarative transforms |

```mermaid
flowchart TB
  API[Service API] --> IF[Collection interfaces]
  IF --> AL[ArrayList / HashMap / ArrayDeque]
  IF --> CONC[ConcurrentHashMap / LinkedBlockingQueue]
  AL --> JVM[Heap objects + GC]
  CONC --> JVM
```

## Internal working

1. **Iteration** — every `Collection` extends `Iterable`; enhanced for-loops compile to
   `iterator()` + `hasNext()` / `next()`.
2. **Views** — `Map` exposes `keySet()`, `values()`, `entrySet()` as **live views**
   (mutations reflect back unless unmodifiable wrappers are used).
3. **Algorithms** — `Collections.sort`, `binarySearch`, and stream collectors reuse
   the same ordering contracts (`Comparable` / `Comparator`).
4. **Fail-fast iterators** — structural modification without iterator `remove()` can
   trigger `ConcurrentModificationException` on many non-concurrent implementations.

## Hands-on

```java
import java.util.*;

public class CollectionsOverviewDemo {
    public static void main(String[] args) {
        Map<Long, Employee> roster = new HashMap<>();
        roster.put(1L, new Employee(1L, "Ada", "Eng", 120_000));
        roster.put(2L, new Employee(2L, "Lin", "Eng", 115_000));

        List<Order> orders = new ArrayList<>();
        orders.add(new Order(100L, 1L, "SKU-1", 2, 9.99));
        orders.add(new Order(101L, 1L, "SKU-2", 1, 19.99));

        Map<Long, List<Order>> byEmployee = new HashMap<>();
        for (Order o : orders) {
            byEmployee.computeIfAbsent(o.employeeId(), k -> new ArrayList<>()).add(o);
        }

        Set<String> departments = new TreeSet<>();
        roster.values().forEach(e -> departments.add(e.department()));

        System.out.println(departments); // sorted encounter order
        System.out.println(byEmployee.get(1L).size());
    }

    record Employee(long id, String name, String department, double salary) {}
    record Order(long id, long employeeId, String sku, int quantity, double unitPrice) {}
}
```

Run with `java CollectionsOverviewDemo.java` (single-file source, JDK 11+).

## Performance

| Choice | Read pattern | Write pattern | Memory |
| --- | --- | --- | --- |
| `ArrayList` | `O(1)` indexed | amortized `O(1)` tail | contiguous array |
| `LinkedList` | `O(n)` index | `O(1)` at known node | extra node overhead |
| `HashMap` | average `O(1)` | average `O(1)` | buckets + nodes/tree bins |
| `TreeMap` | `O(log n)` | `O(log n)` | tree nodes |

> **Performance note**
> Pick implementation by **dominant operation** and **ordering requirement**, not folklore
> ("always `LinkedList` for inserts").

## JDK tools and diagnostic clues

- **`ConcurrentModificationException`** in stack traces → iterator invalidation during mutation;
  look for foreach + `remove`, or map iteration + `put`.
- **Heap dumps** showing single giant `HashMap$Node[]` or `Object[]` → unbounded in-memory caches.
- **JFR events** `jdk.ObjectAllocationInNewTLAB` spikes when resizing `ArrayList`/`HashMap` in hot loops.

## Failure scenarios

| Symptom | Likely cause | Mitigation |
| --- | --- | --- |
| Nondeterministic test failures | Assuming iteration order on `HashSet`/`HashMap` | Use `LinkedHash*` or sort explicitly |
| `NullPointerException` in `TreeMap` | Null keys where comparator not null-tolerant | Guard inputs; use `HashMap` if null keys required |
| Memory growth in long-lived service | Unbounded `Map` cache without eviction | Cap size; `LinkedHashMap` LRU; Caffeine |

## Best practices and anti-patterns

- Program to interfaces (`List`, `Map`, `Queue`) at module boundaries.
- Document **ordering** and **null** policies in public APIs.
- Avoid exposing internal mutable collections without wrapping (`Collections.unmodifiable*`).

> **Production insight**
> Microservices often leak ordering assumptions across API versions — document whether JSON arrays
> are semantically ordered or incidental.

## Staff engineer notes

- The JCF is not a performance toolkit; it is a **semantic** toolkit. Performance comes from
  matching implementation to access pattern and from avoiding accidental `O(n²)` patterns
  (e.g., `List.contains` inside nested loops).
- `Map` not extending `Collection` is a modeling choice: keys are a **set-like** domain with
  associated values, not a bag of entries.
"""
    ).strip()


def generic_supplement(module_num: int, lesson_file: str, title: str) -> str:
    slug = lesson_file.replace(".md", "")
    return textwrap.dedent(
        f"""
## Architecture

This lesson sits in **Module {module_num}** of the Core Java track. Service code should treat
collection/generics/stream/JVM choices as **capacity and correctness** decisions, not style preferences.

## Internal working

Review the numbered sections in **Core concepts (canonical)** below. For interviews, pair each
fact with **complexity**, **ordering**, and **concurrency** implications.

## Hands-on

```java
// Extend the snippet in the canonical section with Employee / Order / Payment records.
// JDK 17+: compile with your module's test source set or `java Main.java`.
```

## Performance

State average vs worst-case costs for the structures or APIs introduced in this lesson.
Call out allocation hot spots (boxing, autoboxing in streams, defensive copies).

## JDK tools and diagnostic clues

- Watch for lesson-specific exceptions in logs (`ConcurrentModificationException`, `ClassCastException`
  at erasure boundaries, `OutOfMemoryError` subtypes for JVM modules).
- Use **async profiler**, **JFR**, or **heap histogram** (`jcmd <pid> GC.class_histogram`) when
  production symptoms match this topic.

## Failure scenarios

Document one production failure mode tied to misuse of this lesson's API, and the guardrail
(service validation, bounded queues, explicit comparators, try-with-resources).

## Best practices and anti-patterns

- Prefer clear types over clever one-liners.
- Make null and empty collection policies explicit at API edges.

> **Production insight**
> Align collection mutability with transaction boundaries — shared mutable structures between
> threads remain the top source of subtle bugs.

## Staff engineer notes

- Teach the **contract** first (what callers may assume), then the **implementation** (how it is enforced).
- Link forward to Module 12 concurrent collections when discussing multi-threaded mutation.
"""
    ).strip()


def build_mastery(lesson: LessonDoc, module_num: int, lesson_file: str, pilot_l1: bool) -> str:
    canonical = strip_legacy_tail(lesson.body)
    mod = MODULES[module_num]
    rel_mastery = f"core-java/{mod['dir']}/{lesson_file}"
    rel_companion = rel_mastery.replace("01-engineering-mastery", "02-interview-companion")
    companion_path = f"../../../02-interview-companion/core-java/{mod['dir']}/{lesson_file}"
    playbook_path = f"../../../03-production-playbook/core-java/{mod['playbook']}"

    extra = m4_l1_pilot_extra() if pilot_l1 else generic_supplement(module_num, lesson_file, lesson.title)

    h1 = re.search(r"^#\s+(.+)$", canonical, re.M)
    heading = h1.group(1) if h1 else lesson.title

    tags = lesson.tags + [f"module-{module_num}", "mastery"]
    tags_s = ", ".join(dict.fromkeys(tags))

    body = f"""---
title: "{lesson.title}"
description: "{lesson.description}"
status: covered
audience: practitioner
tags: [{tags_s}]
created: 2026-10-15
updated: 2026-10-18
---

# {heading}

{lesson.description}

{SHARED_DOMAIN}

## Big picture

Core Java Module {module_num} — **{mod['title']}**. This is the canonical Engineering Mastery
lesson; the [Interview Companion]({companion_path}) compresses interview signal without
introducing new concepts.

## Prerequisites

- Prior modules in the [Core Java track](../../../../java/index.md).
- JDK **17+** for examples unless the lesson notes otherwise.

{extra}

## Core concepts (canonical)

{canonical}

## Key takeaways

- Re-read the comparison tables and misconceptions in the canonical section.
- Pair this lesson with the Companion's **30-second revision** before mocks.

## See also

- [Companion chapter]({companion_path})
- [{mod['title']} production playbook]({playbook_path})
- [Module index](index.md)
"""
    return body


def extract_bullets(section: str, body: str) -> list[str]:
    m = re.search(rf"{section}.*?\n(.*?)(?=\n## |\Z)", body, re.S | re.I)
    if not m:
        return []
    items = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.startswith(("-", "|")) and "Myth" not in line and "---" not in line:
            items.append(line.lstrip("- ").strip())
        if line.startswith("|") and "Myth" in line:
            continue
    return items[:8]


def build_companion(lesson: LessonDoc, module_num: int, lesson_file: str) -> str:
    mod = MODULES[module_num]
    mastery_link = f"../../../01-engineering-mastery/core-java/{mod['dir']}/{lesson_file}"
    body = lesson.body
    traps = extract_bullets("misconception", body) or extract_bullets("Interview trap", body)
    if not traps:
        traps = ["Assuming interface Big-O equals every implementation — read the implementation javadoc."]

    h1 = re.search(r"^#\s+(.+)$", body, re.M)
    heading = h1.group(1) if h1 else lesson.title
    companion_title = lesson.title.replace("Lesson", "Companion").replace("—", "—")

    jdk_clues = [
        "Stack traces mentioning this lesson's types (`java.util.*`, `java.lang.*`) — map frame to contract violation.",
        "Enable `-XX:+HeapDumpOnOutOfMemoryError` when symptoms involve unbounded structures from this module.",
    ]
    if module_num == 9:
        jdk_clues = [
            "GC logs (`-Xlog:gc*`) and `jcmd GC.heap_info` for heap pressure.",
            "Heap dump dominators for `char[]`, `byte[]`, or collection backings tied to retention.",
        ]

    faq = [
        ("What JDK version do examples target?", "JDK 17+ OpenJDK unless the mastery lesson states otherwise."),
        ("Where is the full depth?", f"The [Mastery lesson]({mastery_link}) is canonical."),
    ]

    faq_block = "\n".join(f"- **Q:** {q}\n  **A:** {a}" for q, a in faq)

    return f"""---
title: "{companion_title}"
description: "Interview companion for {lesson.description}"
status: covered
audience: advanced
tags: [interview, companion, module-{module_num}, java]
created: 2026-10-18
updated: 2026-10-18
---

# {heading.replace("Lesson", "Companion")}

**Canonical source:** [{lesson.title}]({mastery_link}).

## Definition

{lesson.description}

## Why it exists

Backend services need predictable in-memory data semantics; this topic encodes the contract
and the trade-offs senior engineers defend in design reviews.

## Must remember

- Program to interfaces; justify implementations with complexity, ordering, and thread-safety.
- `Employee` / `Order` / `Payment` examples tie this lesson to payroll and commerce flows.

## Interview traps

{chr(10).join('- ' + t for t in traps[:6])}

## Frequently asked questions

{faq_block}

## JDK and debug clues

{chr(10).join('- ' + c for c in jdk_clues)}

## Performance notes

- Name the dominant operation before naming a concrete class.
- Watch hidden `O(n)` scans (`contains`, `indexOf`) inside loops.

## Production notes

- Bound in-memory maps and caches; log size metrics where feasible.
- Document nullability and ordering guarantees on public APIs.

## Staff engineer notes

- Separate **semantic requirements** (unique keys, sorted traversal) from **favorite classes**.

## 30-second revision

- Read the mastery tables once, then rehearse answering "why this implementation?" aloud.

## Memory hooks

- **LOMS** — **L**ist order, **O**rdering mode, **M**ap vs Collection, **S**election by access pattern.
"""


def build_playbook(module_num: int) -> str:
    mod = MODULES[module_num]
    return f"""---
title: "Module {module_num} — {mod['title']} production playbook"
description: Operational runbook for {mod['title'].lower()} in JVM services.
status: covered
audience: operator
tags: [playbook, java, module-{module_num}]
created: 2026-10-18
updated: 2026-10-18
---

# Module {module_num} — {mod['title']} production playbook

Runbook for teams operating Spring Boot / JVM services where **{mod['title'].lower()}** choices
affect latency, memory, and incident response.

## Overview

Covers detection, mitigation, and verification for production issues tied to Module {module_num}
lessons. Concepts live in [Engineering Mastery](../../01-engineering-mastery/core-java/{mod['dir']}/index.md).

## When to use this

- Elevated latency or CPU after a release touching domain collections or APIs
- `OutOfMemoryError`, GC churn, or thread pool exhaustion linked to in-memory structures
- Interview prep for "debug this production service" scenarios

## Prerequisites

- JDK 17+ tooling: `jcmd`, `jmap`, `jfr`, async-profiler
- Read access to logs and metrics; approval for heap dumps in prod

## Architecture in production

```mermaid
flowchart LR
  REQ[HTTP / messaging] --> SVC[Service layer]
  SVC --> MEM[In-memory JCF structures]
  MEM --> GC[JVM heap / GC]
  SVC --> OBS[Metrics + logs]
```

## Procedure

1. **Triage** — classify as correctness (exceptions), capacity (GC/OOM), or contention.
2. **Correlate** — deploy time, traffic shape, and dependency latency.
3. **Capture** — thread dump; if memory, histogram or heap dump per policy.
4. **Mitigate** — feature flag, rate limit, bounded queue, or cache cap.
5. **Verify** — p95 latency, error rate, heap stable after full GC cycle.

## Configuration

- Set explicit pool and queue capacities; avoid `Integer.MAX_VALUE` defaults.
- JVM: document heap (`-Xmx`), metaspace, and GC algorithm flags per environment.

## Monitoring and JDK diagnostics

- Metrics: heap used, GC pause, pool depth, cache entry count.
- Logs: structured fields for collection sizes where expensive to compute (sampled).

## Failure scenarios and recovery

| Signal | Action |
| --- | --- |
| `ConcurrentModificationException` | Find concurrent mutation; switch to concurrent collections or copy-on-write |
| Rising old-gen after deploy | Diff collection caches; analyze dominators |
| Timeouts at integration | Check blocking queue depth and rejection policy |

## Performance and cost

- Right-size structures; avoid accidental boxing and mega-collections in hot paths.

## Security and governance

- Do not log full `Employee` / `Payment` payloads; redact PII.

## Rollback

- Revert release if mitigation fails; preserve heap dump artifact before rollback if safe.

## Incident checklist

- [ ] Exception class and stack captured
- [ ] Deploy correlation identified
- [ ] Mitigation validated on metrics
- [ ] Follow-up mastery lesson linked in postmortem

## Key takeaways

- Operate **bounds**, **ordering**, and **concurrency** explicitly.

## See also

- [Mastery module](../../01-engineering-mastery/core-java/{mod['dir']}/index.md)
- [Interview Companion module](../../02-interview-companion/core-java/{mod['dir']}/index.md)
"""


def build_stub(lesson_file: str, module_num: int, is_index: bool = False) -> str:
    mod = MODULES.get(module_num)
    if not mod:
        return build_stub_planned(module_num)
    mastery = f"../../books/01-engineering-mastery/core-java/{mod['dir']}/"
    comp = f"../../books/02-interview-companion/core-java/{mod['dir']}/"
    play = f"../../books/03-production-playbook/core-java/{mod['playbook']}"
    if is_index:
        return f"""---
title: "{mod['title']} (legacy path)"
description: Stub — content moved to the three-book Core Java track.
status: stable
audience: all
tags: [stub, java]
updated: 2026-10-18
---

# Module {module_num} — {mod['title']}

Content moved to the **three-book** layout:

| Book | Location |
| --- | --- |
| Engineering Mastery | [Module index]({mastery}index.md) |
| Interview Companion | [Module index]({comp}index.md) |
| Production playbook | [{mod['title']} playbook]({play}) |

Legacy URLs under `docs/java/` remain for bookmarks only.
"""
    target = f"{mastery}{lesson_file}"
    ctarget = f"{comp}{lesson_file}"
    return f"""---
title: "Moved — {lesson_file}"
description: Stub pointer to Engineering Mastery and Interview Companion.
status: stable
audience: all
tags: [stub]
updated: 2026-10-18
---

# Content moved

| Book | Link |
| --- | --- |
| **Engineering Mastery** | [{lesson_file}]({target}) |
| **Interview Companion** | [{lesson_file}]({ctarget}) |
| **Production playbook** | [Module playbook]({play}) |
"""


def build_stub_planned(module_num: int) -> str:
    return f"""---
title: Module {module_num} (planned)
description: Planned module — lessons not yet authored in Books.
status: planned
audience: all
tags: [stub, java]
updated: 2026-10-18
---

# Module {module_num} — planned

Lessons for this module are **planned**. Follow [Core Java books](../../books/index.md) for Modules 4–9.
"""


def module_index_mastery(module_num: int, lessons: list[str]) -> str:
    mod = MODULES[module_num]
    rows = "\n".join(f"| {i+1} | [{f}]({f}) |" for i, f in enumerate(lessons))
    return f"""---
title: "Module {module_num} — {mod['title']}"
description: Engineering Mastery lessons for {mod['title']}.
status: covered
audience: practitioner
tags: [mastery, module-{module_num}]
updated: 2026-10-18
---

# Module {module_num} — {mod['title']}

Canonical lessons (Book 1). Shared examples: `Employee`, `Order`, `Payment`.

| # | Lesson |
| --- | --- |
{rows}

## Interview material

Practice lives in [Interview Companion](../../../02-interview-companion/core-java/{mod['dir']}/module-interview-practice.md).

## Operations

[{mod['title']} production playbook](../../../03-production-playbook/core-java/{mod['playbook']})
"""


def module_index_companion(module_num: int, lessons: list[str]) -> str:
    mod = MODULES[module_num]
    rows = "\n".join(
        f"| {i+1} | [{f}]({f}) | [Mastery](../../../01-engineering-mastery/core-java/{mod['dir']}/{f}) |"
        for i, f in enumerate(lessons)
    )
    return f"""---
title: "Module {module_num} — {mod['title']} (Companion)"
description: Derived interview companion for Module {module_num}.
status: covered
audience: advanced
tags: [companion, module-{module_num}]
updated: 2026-10-18
---

# Module {module_num} — {mod['title']} — Interview Companion

Derived from [Engineering Mastery](../../../01-engineering-mastery/core-java/{mod['dir']}/index.md).

| # | Companion | Canonical |
| --- | --- | --- |
{rows}

- [Interview practice](module-interview-practice.md)
- [Assessment answers](module-interview-assessment-answers.md)
"""


def list_lesson_files(module_dir: Path) -> list[str]:
    skip = {"index.md"}
    files = sorted(
        p.name
        for p in module_dir.glob("*.md")
        if p.name not in skip and "interview" not in p.name
    )
    return files


def migrate_module(module_num: int, stats: dict) -> list[str]:
    mod = MODULES[module_num]
    legacy_dir = LEGACY_JAVA / mod["dir"]
    lessons = list_lesson_files(legacy_dir)
    m_dir = MASTERY / mod["dir"]
    c_dir = COMPANION / mod["dir"]
    m_dir.mkdir(parents=True, exist_ok=True)
    c_dir.mkdir(parents=True, exist_ok=True)
    PLAYBOOK.mkdir(parents=True, exist_ok=True)

    nav_lessons: list[tuple[str, str]] = []

    for lf in lessons:
        src = legacy_dir / lf
        if not src.exists():
            continue
        doc = load_lesson(src)
        pilot = module_num == 4 and lf == "01-collections-framework-overview.md"
        mastery_text = build_mastery(doc, module_num, lf, pilot)
        companion_text = build_companion(doc, module_num, lf)
        (m_dir / lf).write_text(mastery_text, encoding="utf-8")
        (c_dir / lf).write_text(companion_text, encoding="utf-8")
        stats["created"] += 2

        label = doc.title.split("—")[-1].strip() if "—" in doc.title else lf
        nav_lessons.append((label[:50], f"books/01-engineering-mastery/core-java/{mod['dir']}/{lf}"))

        stub = build_stub(lf, module_num)
        src.write_text(stub, encoding="utf-8")
        stats["stubbed"] += 1

    prac_src, ans_src = mod["practice_src"]
    for name, target in [
        (prac_src, "module-interview-practice.md"),
        (ans_src, "module-interview-assessment-answers.md"),
    ]:
        sp = legacy_dir / name
        if sp.exists():
            (c_dir / target).write_text(sp.read_text(encoding="utf-8"), encoding="utf-8")
            stats["created"] += 1
            sp.write_text(build_stub(name, module_num), encoding="utf-8")
            stats["stubbed"] += 1

    pb = PLAYBOOK / mod["playbook"]
    pb.write_text(build_playbook(module_num), encoding="utf-8")
    stats["created"] += 1

    (m_dir / "index.md").write_text(module_index_mastery(module_num, lessons), encoding="utf-8")
    (c_dir / "index.md").write_text(module_index_companion(module_num, lessons), encoding="utf-8")
    stats["created"] += 2

    (legacy_dir / "index.md").write_text(build_stub("", module_num, is_index=True), encoding="utf-8")
    stats["stubbed"] += 1

    return [n[1] for n in nav_lessons]


def stub_planned_modules(stats: dict) -> None:
    for n in (1, 2, 3):
        d = LEGACY_JAVA / f"module-0{n}-"
        for path in LEGACY_JAVA.glob(f"module-0{n}-*/index.md"):
            path.write_text(build_stub_planned(n), encoding="utf-8")
            stats["stubbed"] += 1


def generate_mkdocs_nav() -> str:
    lines = [
        "  - Books:",
        "      - Overview: books/index.md",
        "      - Book 1 — Engineering Mastery: books/01-engineering-mastery/index.md",
        "      - Book 2 — Interview Companion: books/02-interview-companion/index.md",
        "      - Book 3 — Production Playbook: books/03-production-playbook/index.md",
    ]
    for num in sorted(MODULES):
        mod = MODULES[num]
        lines.append(f'      - "M{num} {mod["title"]} (Mastery)":')
        lines.append(f"          - books/01-engineering-mastery/core-java/{mod['dir']}/index.md")
        legacy = LEGACY_JAVA / mod["dir"]
        for p in sorted(legacy.glob("*.md")):
            if p.name == "index.md" or "interview" in p.name:
                continue
            doc = load_lesson(p) if p.stat().st_size > 200 else None
            title = doc.title if doc else p.stem
            short = title.split("—")[-1].strip()[:40]
            lines.append(f'          - "{short}": books/01-engineering-mastery/core-java/{mod["dir"]}/{p.name}')
        lines.append(f'      - "M{num} {mod["title"]} (Companion)":')
        lines.append(f"          - books/02-interview-companion/core-java/{mod['dir']}/index.md")
        cdir = COMPANION / mod["dir"]
        for cp in sorted(cdir.glob("*.md")):
            if cp.name in ("index.md", "module-interview-practice.md", "module-interview-assessment-answers.md"):
                continue
            short = cp.stem.replace("-", " ")[:40]
            lines.append(
                f'          - "{short}": books/02-interview-companion/core-java/{mod["dir"]}/{cp.name}'
            )
        lines.append(
            f"          - Practice: books/02-interview-companion/core-java/{mod['dir']}/module-interview-practice.md"
        )
        lines.append(
            f"          - Answers: books/02-interview-companion/core-java/{mod['dir']}/module-interview-assessment-answers.md"
        )
        lines.append(
            f'      - "M{num} Playbook": books/03-production-playbook/core-java/{mod["playbook"]}'
        )
    return "\n".join(lines) + "\n"


def patch_mkdocs(nav_block: str) -> None:
    mk = ROOT / "mkdocs.yml"
    text = mk.read_text(encoding="utf-8")
    if "  - Books:" in text:
        text = re.sub(r"  - Books:.*?(?=  - Concurrency:|  - Spring)", nav_block, text, flags=re.S)
    else:
        text = text.replace("  - Concurrency:", nav_block + "  - Concurrency:")
    mk.write_text(text, encoding="utf-8")


def main() -> None:
    stats = {"created": 0, "stubbed": 0}
    for num in sorted(MODULES):
        migrate_module(num, stats)
    stub_planned_modules(stats)
    nav = generate_mkdocs_nav()
    patch_mkdocs(nav)
    print(f"Migration complete: created~{stats['created']} files, stubbed {stats['stubbed']} legacy paths")


if __name__ == "__main__":
    main()
