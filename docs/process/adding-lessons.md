---
title: Adding and Updating Lessons
description: Repeatable process for extending the interview handbook after each study session.
status: stable
audience: all
tags: [process, contributing]
created: 2026-10-15
updated: 2026-10-18
---

# Adding and Updating Lessons

Core Java Modules **4–9** use the **three-book** layout (Spark-aligned). Legacy `docs/java/module-*`
paths are stubs that point to the books.

## Paths

| Book | Path pattern |
| --- | --- |
| Engineering Mastery | `docs/books/01-engineering-mastery/core-java/module-NN-slug/NN-lesson-slug.md` |
| Interview Companion | `docs/books/02-interview-companion/core-java/module-NN-slug/` (mirror filenames) |
| Production Playbook | `docs/books/03-production-playbook/core-java/module-NN-*-production-playbook.md` |

Templates (repo root): `templates/chapter-engineering-mastery.md`,
`templates/chapter-interview-companion.md`,
`templates/chapter-interview-companion-core-java.md` (diagrams + scenario + decision table),
`templates/chapter-interview-companion-concurrency.md`,
`templates/chapter-production-playbook.md`.

## Interview Companion visuals (Book 2)

Book 2 is the **interview cram surface**. Each companion lesson should include:

- A Mermaid `flowchart`, `sequenceDiagram`, or `stateDiagram-v2` (or a tight ASCII timeline).
- A **scenario bite** and a **decision table**.
- A link to that module’s `module-visual-quick-reference.md`.

**Mermaid in MkDocs:** fences must be ` ```mermaid ` (Material + `pymdownx.superfences`). Prefer `flowchart` / `sequenceDiagram` / `stateDiagram-v2`. Avoid `mindmap` unless you have confirmed it renders in the browser — Cursor chat may render diagrams that MkDocs does not. Diagrams appear on the served site (`mkdocs serve`), not in every raw Markdown preview.

## After each interactive session

1. **Preserve structure** — one H1, YAML front matter, shared `Employee` / `Order` / `Payment` examples where relevant.
2. **Edit Book 1 (Mastery)** — canonical concepts, runnable Java, complexity, JDK diagnostics, production notes.
3. **Regenerate Book 2 (Companion)** — fixed section order; **no copied paragraphs**; link canonical Mastery; use **JDK and debug clues** (not Spark UI).
4. **Update Book 3 (Playbook)** when operational procedures change.
5. **Cross-link** — mastery ↔ companion ↔ playbook; do not duplicate full sections in stubs.
6. **Update navigation** — `mkdocs.yml` under **Books** for new lessons.
7. **Update progress** — `PROGRESS.md` at repo root for material actually studied.
8. **Log corrections** — [mistakes-and-misconceptions](../mistakes-and-misconceptions/index.md).
9. **Do not modify** the Spark or DSA handbooks from this repo unless explicitly requested.

Statuses: Covered, In progress, Introduced, Planned, Deferred, Needs revision.
