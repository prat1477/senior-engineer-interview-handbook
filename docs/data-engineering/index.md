---
title: Data Engineering and Lakehouse
description: Delta, Iceberg, streaming, Databricks — interview prep beyond completed Spark modules.
status: planned
audience: advanced
tags: [data-engineering, spark, lakehouse]
created: 2026-10-15
updated: 2026-10-15
---

# Data Engineering and Lakehouse

## Spark Handbook cross-reference

**Do not duplicate** Modules 1–10 (and most of Module 11) — they are **Covered** in the
[Spark Engineering Handbook](../../../spark-engineering-handbook/docs/books/01-engineering-mastery/index.md).

| Spark module | Your status | Action here |
| --- | --- | --- |
| 1–10 | Completed | Link only — [spark-cross-reference.md](spark-cross-reference.md) |
| 11 File formats | Mostly completed | Brief recap when needed |
| 12 Delta Lake | Planned | Author lessons here |
| 13 Structured Streaming | Planned | Author lessons here |
| 14 Databricks | Planned | Author lessons here |

## Interview topics (roadmap)

- Delta Lake transaction log, ACID, time travel
- Delta vs Parquet
- Apache Iceberg — manifests, snapshots
- Unity Catalog (governance)
- Structured Streaming — watermarks, late data, guarantees
- AWS EMR + S3 patterns
- Airflow orchestration
- SQL and query optimization for pipelines
- Pipeline reliability and recovery
- Lakehouse architecture
- **Production debugging:** driver OOM, Catalyst plans, concurrent job contention, shuffle/spill, executor loss, dynamic allocation

## Practice context (for scenarios)

- PySpark transformations in production pipelines
- Databricks on Azure with Delta and Unity Catalog
- AWS EMR/S3 with Iceberg

See [spark-cross-reference.md](spark-cross-reference.md) for lesson links.
