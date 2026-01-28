# Technical Constraints

This document defines the technical constraints, assumptions, and dependencies for the Waterlily project.

## Technology Stack

### Application

| Component | Technology | Version | Notes |
|-----------|------------|---------|-------|
| Language | Kotlin | 1.9+ | JVM-based |
| Framework | Ktor | 2.x | Lightweight, async-friendly |
| Build Tool | Gradle | 8.x | Kotlin DSL |
| JVM | OpenJDK/Corretto | 17+ | LTS version |

### Database

| Component | Technology | Version | Notes |
|-----------|------------|---------|-------|
| Database | MySQL | 8.x | Single instance |
| Driver | MySQL Connector/J | 8.x | JDBC driver |
| Connection Pool | HikariCP | 5.x | High-performance pool |

### Benchmark Tools

| Component | Technology | Notes |
|-----------|------------|-------|
| Load Generator | wrk | HTTP benchmarking tool |
| Scripting | Lua | wrk scripting language |

---

## Deployment Constraints

### Environment

The database is already available. We should scan the database to see if the actual 
database schema matches with this specification.

Database connection is provided in [mysql-config.json](/experiment/mysql-config.json)

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Platform | localhost | Single machine benchmark eliminates network variables |
| Database instances | 1 | Baseline performance measurement |
| Application instances | 1 | Isolate database performance from app scaling |

### Hardware Requirements (Recommended)

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 16 GB | 32+ GB |
| Storage | SSD, 200 GB | NVMe SSD, 500 GB |

**Notes:**
- MySQL InnoDB buffer pool should be sized to fit hot data (~32 GB recommended)
- Application heap should be at least 2 GB

---

## Assumptions

### Data Assumptions

| Assumption | Description |
|------------|-------------|
| ASM-001 | Products are pre-loaded in the database before benchmarks run |
| ASM-002 | Product IDs for benchmark are extracted to a text file |
| ASM-003 | Data distribution is realistic (varied categories, variants, media) |
| ASM-004 | No concurrent writes during read benchmark |

### Operational Assumptions

| Assumption | Description |
|------------|-------------|
| ASM-005 | No authentication required (trusted internal network) |
| ASM-006 | No caching layers (pure database performance test) |
| ASM-007 | Single user running benchmarks (no resource contention) |
| ASM-008 | Stable network (localhost eliminates network variance) |

### Performance Assumptions

| Assumption | Description |
|------------|-------------|
| ASM-009 | Database has warmed up (buffer pool populated) before benchmarks |
| ASM-010 | System has sufficient resources to avoid swapping |
| ASM-011 | No background processes competing for resources |

---

## Dependencies

### Runtime Dependencies

| Dependency | Purpose | Required |
|------------|---------|----------|
| JVM 17+ | Application runtime | Yes |
| MySQL 8.x server | Data storage | Yes |
| wrk | Benchmark execution | Yes |

### Development Dependencies

| Dependency | Purpose |
|------------|---------|
| Gradle 8.x | Build automation |
| Docker (optional) | MySQL container |
| Git | Version control |

### External Dependencies

None. The system operates entirely on localhost with no external service calls.

---

## Design Constraints

### API Design

| Constraint | Description |
|------------|-------------|
| CON-001 | REST API style with JSON payloads |
| CON-002 | Batch endpoint limited to 50 IDs per request |
| CON-003 | No pagination (benchmark focuses on direct ID lookups) |
| CON-004 | Synchronous request handling (no async streaming) |

### Database Access

| Constraint | Description |
|------------|-------------|
| CON-005 | Raw JDBC for maximum control and performance transparency |
| CON-006 | No ORM (JPA/Hibernate) overhead |
| CON-007 | Prepared statements for all queries |
| CON-008 | Connection pool managed by HikariCP |

### Benchmark Design

| Constraint | Description |
|------------|-------------|
| CON-009 | wrk Lua scripts handle request generation |
| CON-010 | Product IDs loaded from file at script startup |
| CON-011 | Results exported to JSON for analysis |
| CON-012 | Each benchmark run tests one API at one CCU level |

---

## Out of Scope

The following are explicitly excluded from this project scope:

| Item | Reason |
|------|--------|
| Create/Update/Delete operations | Read benchmark focus |
| Authentication/Authorization | Adds overhead, complicates benchmark |
| Caching (Redis, in-memory) | Pure database performance measurement |
| Distributed deployment | Single-instance baseline first |
| Multiple database types | Future benchmark contexts |
| Production deployment | Local development/benchmark only |
| Monitoring/Observability | Benchmark tool provides metrics |

---

## Configuration Parameters

### Application Configuration

```yaml
server:
  host: 0.0.0.0
  port: 8080

database:
  url: jdbc:mysql://localhost:3306/waterlily
  username: waterlily
  password: ${DB_PASSWORD}
  pool:
    minimumIdle: 50
    maximumPoolSize: 100
    connectionTimeout: 30000
    idleTimeout: 600000
```

### Benchmark Configuration

```lua
-- wrk script configuration
PRODUCT_IDS_FILE = "product_ids.txt"
BASE_URL = "http://localhost:8080"
```
