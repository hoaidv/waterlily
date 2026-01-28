# Waterlily Software Specification

## Project Information

| Field | Value |
|-------|-------|
| Project Name | Waterlily |
| Version | 1.0.0 |
| Last Updated | January 2026 |

## Problem Statement

Benchmark MySQL database performance for read-heavy e-commerce product queries at scale. The goal is to discover throughput and latency characteristics when serving product data from a 35 million product database under varying concurrent load conditions.

## Scope

### In Scope

- Read-only REST APIs for product retrieval
- Single product lookup by ID
- Batch product lookup by multiple IDs (max 50)
- Benchmark execution with wrk/Lua scripts
- Performance measurement up to 100,000 RPS
- MySQL single-instance deployment on localhost

### Out of Scope

- Create, Update, Delete operations
- Authentication and authorization
- Caching layers (Redis, in-memory)
- Distributed database deployments
- Multi-database comparisons (deferred to future benchmark contexts)
- Frontend/UI components

## Objectives

1. Build a minimal Kotlin/Ktor application to serve product data via REST APIs
2. Measure throughput (RPS) and latency (p50, p95, p99) under different CCU levels
3. Identify MySQL performance characteristics for the given data volume and access pattern
4. Produce benchmark results in JSON format for analysis and visualization

## Key Stakeholders

| Role | Responsibility |
|------|----------------|
| Developer | Implement application, run benchmarks, analyze results |
| Architect | Define benchmark contexts, interpret performance data |

## Related Documents

- [Functional Requirements](functional-req.md)
- [API Specification](api-spec.md)
- [Data Model](data-model.md)
- [Non-Functional Requirements](nfr.md)
- [Technical Constraints](constraints.md)
- [Glossary](glossary.md)
- [Benchmark Script](benchmark-script.md)

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | January 2026 | - | Initial specification |
