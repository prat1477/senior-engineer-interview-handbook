---
title: Spring Boot and Microservices
description: Spring Core, Spring Boot, and microservice reliability roadmap for senior backend interviews.
status: in-progress
audience: advanced
tags: [spring, microservices]
created: 2026-10-15
updated: 2026-11-08
---

# Spring Boot and Microservices

**Status: In progress** (Days 5–6). Spring Core Lesson 1 is covered conceptually; implementation assessment remains separate. Focus on production behavior, not beginner tutorials.

## Spring Core sequence

| # | Topic | Status |
| --- | --- | --- |
| 1 | [Inversion of Control (IoC) and Dependency Injection (DI)](01-ioc-and-dependency-injection.md) | **Covered** (conceptual) |
| 2 | Spring Bean Lifecycle | **Planned** |
| 3 | Spring Bean Scopes | **Planned** |
| 4 | BeanFactory vs ApplicationContext | **Planned** |

## Spring Boot and microservices roadmap

| # | Topic |
| --- | --- |
| 1 | Spring Boot architecture and request lifecycle |
| 2 | REST APIs — design, status codes, pagination |
| 3 | Validation and exception handling |
| 4 | Dependency injection and bean scopes |
| 5 | Transactions and transaction boundaries |
| 6 | Connection pools and DB interaction |
| 7 | ORM pitfalls (N+1, lazy loading, flush timing) |
| 8 | Service-to-service communication |
| 9 | Timeouts, retries, and idempotency keys |
| 10 | Circuit breakers and bulkheads |
| 11 | Transactional Outbox Pattern |
| 12 | Saga patterns (orchestration vs choreography) |
| 13 | Cascading failures and graceful degradation |
| 14 | API versioning |
| 15 | Observability — logs, metrics, traces |
| 16 | Production debugging scenarios |

Cross-links: [Kafka](../kafka/index.md), [Distributed systems](../distributed-systems/index.md).
