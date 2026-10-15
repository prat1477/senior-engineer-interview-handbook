# Senior Engineer Interview Preparation Handbook

A versioned, interview-focused handbook for **senior backend and data-platform engineering**
roles. It preserves interactive study sessions, tracks progress honestly, and follows a
fixed 14-day preparation sequence without duplicating your existing Spark curriculum.

> **Current focus:** Core Java — **Collections** (in progress). Next: **Generics**, then
> **Java 8 Streams**, then the concurrency track per the roadmap.

## Who this is for

- ~9 years of professional engineering experience; target roles include Senior Backend
  Engineer, Distributed Systems Engineer, Data Platform Engineer, and Platform Engineer.
- Preparation emphasizes **judgment, trade-offs, and production behavior**, not syntax drills.
- **70/30 rule:** most time on high-value interview topics; breadth for credibility without
  trivia rabbit holes.

## Relationship to other handbooks

| Handbook | Location | How this book uses it |
| --- | --- | --- |
| Spark Engineering Handbook | [`../spark-engineering-handbook/docs/`](../spark-engineering-handbook/docs/index.md) (sibling repo) | Modules 1–10 (+ most of 11) **completed** — cross-reference only; do not duplicate. |
| DSA Handbook | _Not found in `D:\Github` during setup_ | Link when you add the path in [`docs/dsa/index.md`](docs/dsa/index.md). |

**Safeguard:** This handbook does not modify Spark or DSA source repositories.

## What's inside

| Path | Purpose |
| --- | --- |
| [`docs/index.md`](docs/index.md) | Home and reading map |
| [`docs/14-day-roadmap.md`](docs/14-day-roadmap.md) | Fixed 14-day sequence (do not reorder days) |
| [`docs/curriculum/`](docs/curriculum/index.md) | Master curriculum and Core Java track order |
| [`docs/java/`](docs/java/index.md) | Core Java (Collections documented; Generics/Streams planned) |
| [`docs/concurrency/`](docs/concurrency/index.md) | Java concurrency curriculum (24-lesson sequence) |
| [`docs/spring-microservices/`](docs/spring-microservices/index.md) | Spring Boot and microservice reliability |
| [`docs/distributed-systems/`](docs/distributed-systems/index.md) | System design and distributed patterns |
| [`docs/kafka/`](docs/kafka/index.md) | Kafka for interviews |
| [`docs/data-engineering/`](docs/data-engineering/index.md) | Lakehouse, Delta, Iceberg, Databricks, pipelines |
| [`docs/aws/`](docs/aws/index.md) | AWS data platform and ops |
| [`docs/dsa/`](docs/dsa/index.md) | Coding interview tracker + links |
| [`docs/behavioral/`](docs/behavioral/index.md) | Behavioral preparation |
| [`docs/mock-interviews/`](docs/mock-interviews/index.md) | Mock interview framework |
| [`docs/rapid-revision/`](docs/rapid-revision/day-14-plan.md) | Day 14 rapid revision plan |
| [`docs/mistakes-and-misconceptions/`](docs/mistakes-and-misconceptions/index.md) | Corrections and weak spots |
| [`PROGRESS.md`](PROGRESS.md) | Honest status: Covered / In progress / Planned / Deferred |
| [`docs/process/adding-lessons.md`](docs/process/adding-lessons.md) | How to extend the handbook after each session |

## Conventions (from Spark Handbook)

- **Modules and lessons:** `module-NN-slug/` with numbered lesson files `NN-lesson-slug.md`.
- **Front matter** on lessons: `title`, `description`, `status`, `audience`, `tags`, dates.
- **Markdown:** admonitions, Mermaid diagrams (MkDocs Material), comparison tables.
- **Lesson shape:** Overview → numbered concepts → misconceptions → revision notes →
  interview summary (adapted from the Spark [`STYLE_GUIDE.md`](../spark-engineering-handbook/STYLE_GUIDE.md)).

## Local preview

```bash
cd D:\Github\senior-engineer-interview-handbook
pip install -r requirements.txt
mkdocs serve
```

Or: `make serve` (see [`Makefile`](Makefile)).

## Interactive study contract

When learning with an assistant:

1. Explain → example → trade-offs → **one question at a time** → evaluate → correct →
   interview-ready summary → next concept.
2. Do not quiz on topics not yet taught.
3. Finish **Collections**, then **Generics**, then **Streams** before jumping to
   concurrency or system design tangents.

## Privacy

No employer names or confidential recruitment details appear in this repository. Technical
content is tailored to senior backend + data-platform interviews in general.
