# Non-Functional Requirements

This document defines the non-functional requirements (NFRs) for the Waterlily product service, focused on performance benchmarking objectives.

## Performance Requirements

### NFR-001: Throughput Capacity

| Attribute | Value |
|-----------|-------|
| ID | NFR-001 |
| Category | Performance |
| Priority | High |

**Requirement:** The system must be benchmarkable up to 100,000 requests per second (RPS).

**Rationale:** The primary goal is to discover MySQL performance limits under read-heavy workloads. The system must not be the bottleneck before reaching target throughput.

**Verification:** Benchmark using wrk with increasing connection counts until target RPS or system limit is reached.

---

### NFR-002: Latency Measurement

| Attribute | Value |
|-----------|-------|
| ID | NFR-002 |
| Category | Performance |
| Priority | High |

**Requirement:** The system must measure and report latency metrics including minimum, average, maximum, and standard deviation.

**Rationale:** This is a discovery benchmark - no hard latency targets are set. The goal is to measure actual latency characteristics under various loads.

**Metrics to capture:**
- p50 (median)
- p95
- p99
- Average
- Min/Max
- Standard deviation

**Verification:** wrk output includes latency distribution; results exported to JSON.

---

### NFR-003: Concurrency Support

| Attribute | Value |
|-----------|-------|
| ID | NFR-003 |
| Category | Scalability |
| Priority | High |

**Requirement:** The system must support concurrent user (CCU) levels of 100, 1,000, 10,000, and 100,000.

**Rationale:** Different concurrency levels reveal different performance characteristics (connection handling, context switching, resource contention).

**Benchmark Matrix:**

| CCU Level | wrk --connections |
|-----------|-------------------|
| Low | 100 |
| Low | 200 |
| Low | 500 |
| Medium | 1,000 |
| Medium | 2,000 |
| Medium | 5,000 |
| High | 10,000 |
| High | 20,000 |
| High | 50,000 |
| Extreme | 100,000 |

**Verification:** Run benchmarks at each CCU level and record results.

---

### NFR-004: Connection Pool Configuration

| Attribute | Value |
|-----------|-------|
| ID | NFR-004 |
| Category | Configuration |
| Priority | Medium |

**Requirement:** The database connection pool must be configurable between 50 and 200 connections.

**Rationale:** Connection pool size significantly impacts database performance. Medium-sized pools balance connection overhead with parallelism.

**Configuration:**
- Minimum pool size: 50
- Maximum pool size: 200
- Default: 100

**Verification:** Adjust pool size via configuration and observe impact on throughput/latency.

---

### NFR-005: Data Volume Handling

| Attribute | Value |
|-----------|-------|
| ID | NFR-005 |
| Category | Capacity |
| Priority | High |

**Requirement:** The system must handle a database containing 35 million products.

**Rationale:** Large data volumes ensure benchmark results are representative of production-scale scenarios.

**Data Volume:**
- Products: 35,000,000
- Variants: ~70,000,000 (avg 2 per product)
- Media: ~140,000,000 (avg 4 per product)
- Categories: ~10,000

**Verification:** Load test data and verify query performance across full dataset.

---

### NFR-006: Response Size

| Attribute | Value |
|-----------|-------|
| ID | NFR-006 |
| Category | Performance |
| Priority | Medium |

**Requirement:** Response sizes must be reasonable for network transfer and parsing.

**Estimates:**
| Endpoint | Max Response Size |
|----------|-------------------|
| Single product | ~5 KB |
| Batch (50 products) | ~250 KB |

**Rationale:** Large responses impact network bandwidth and serialization time. Monitoring response size helps identify bottlenecks.

**Verification:** Measure actual response sizes during benchmarks; include transfer data volume in results.

---

## Reliability Requirements

### NFR-007: Error Handling

| Attribute | Value |
|-----------|-------|
| ID | NFR-007 |
| Category | Reliability |
| Priority | Medium |

**Requirement:** The system must handle errors gracefully without crashing under load.

**Acceptance Criteria:**
- Database connection failures return appropriate error responses
- Invalid requests return 400 status codes
- Unexpected errors return 500 status codes with safe error messages
- No stack traces exposed in responses

---

### NFR-008: Startup Time

| Attribute | Value |
|-----------|-------|
| ID | NFR-008 |
| Category | Operability |
| Priority | Low |

**Requirement:** Application startup time should be under 10 seconds.

**Rationale:** Fast startup enables quick iteration during benchmark configuration changes.

---

## NFR Traceability

| NFR | Related User Story | Verification Method |
|-----|-------------------|---------------------|
| NFR-001 | US-003 | wrk benchmark at target RPS |
| NFR-002 | US-003 | Latency metrics in benchmark output |
| NFR-003 | US-003 | Benchmark at each CCU level |
| NFR-004 | US-003 | Configuration testing |
| NFR-005 | US-001, US-002 | Query on full dataset |
| NFR-006 | US-001, US-002 | Response size measurement |
| NFR-007 | US-001, US-002 | Error injection testing |
| NFR-008 | US-003 | Startup time measurement |
