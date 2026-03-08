# Database Manager Agent
**Version**: 2.0.0
**Role**: PostgreSQL Database Architecture & Optimization
**Stack**: RDS PostgreSQL 15, pgvector, TimescaleDB
**Risk Level**: CRITICAL (0.95)

## Purpose
Design, optimize, and maintain PostgreSQL databases for Virons AI platform with focus on performance, security, and compliance.

## Virons Database Architecture

### Primary Database (RDS PostgreSQL 15)
- **Instance**: db.t4g.medium (prod), db.t4g.micro (dev)
- **Storage**: gp3 SSD, 100GB (prod), 20GB (dev)
- **Multi-AZ**: Enabled (prod/staging), disabled (dev)
- **Encryption**: KMS customer-managed key
- **Backups**: 30 days (prod), 7 days (dev)
- **Region**: eu-central-1

### Extensions
- **pgvector**: Vector similarity search for AI embeddings
- **TimescaleDB**: Time-series data for analytics
- **pg_stat_statements**: Query performance monitoring
- **uuid-ossp**: UUID generation

### Schema Design

```sql
-- Users and authentication
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI conversations
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  model VARCHAR(100) NOT NULL, -- claude-3-5-sonnet, etc.
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI messages with vector embeddings
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID REFERENCES conversations(id),
  role VARCHAR(20) NOT NULL, -- user, assistant, system
  content TEXT NOT NULL,
  embedding vector(1536), -- OpenAI ada-002 embeddings
  tokens INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Vector similarity index
CREATE INDEX ON messages USING ivfflat (embedding vector_cosine_ops);

-- Financial data (time-series)
CREATE TABLE market_data (
  time TIMESTAMPTZ NOT NULL,
  symbol VARCHAR(10) NOT NULL,
  price DECIMAL(10,2),
  volume BIGINT
);

SELECT create_hypertable('market_data', 'time');
```

### Performance Optimization

**Connection Pooling (PgBouncer)**:
```ini
[databases]
virons = host=virons-demo-rds.xxx.eu-central-1.rds.amazonaws.com port=5432 dbname=virons

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
reserve_pool_size = 5
```

**Query Optimization**:
- Index on frequently queried columns
- Partial indexes for filtered queries
- EXPLAIN ANALYZE for slow queries
- pg_stat_statements for query monitoring

**Vacuum Strategy**:
- Autovacuum enabled
- Aggressive vacuum for high-churn tables
- VACUUM ANALYZE after bulk operations

### Security

**Encryption**:
- At rest: KMS encryption
- In transit: SSL/TLS required
- Column-level: pgcrypto for sensitive data

**Access Control**:
- IAM database authentication
- Least privilege roles
- No public access (private subnet)

**Compliance**:
- GDPR: Data encryption, audit logging
- BaFin: Encryption, access controls
- DORA: Backup/restore, resilience

### Monitoring

**CloudWatch Metrics**:
- CPU utilization (target < 80%)
- Database connections (target < 80% max)
- Storage space (alert at 80%)
- IOPS utilization

**Query Performance**:
```sql
-- Top 10 slowest queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Table sizes
SELECT schemaname, tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Backup & Recovery

**Automated Backups**:
- Daily snapshots
- 30-day retention (prod)
- Cross-region copy to eu-west-1
- Point-in-time recovery (5-minute granularity)

**Manual Backups**:
```bash
# Create snapshot
aws rds create-db-snapshot --db-instance-identifier virons-demo-rds --db-snapshot-identifier manual-backup-$(date +%Y%m%d)

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier virons-demo-rds-restored --db-snapshot-identifier <snapshot-id>
```

## Quick Reference

```bash
# Connect to RDS
psql -h virons-demo-rds.xxx.eu-central-1.rds.amazonaws.com -U postgres -d virons

# Run migrations
cd infrastructure/terraform/modules/database
terraform apply

# Monitor performance
aws rds describe-db-instances --db-instance-identifier virons-demo-rds
aws cloudwatch get-metric-statistics --namespace AWS/RDS --metric-name CPUUtilization
```

---
**Version**: 2.0.0
**Last Updated**: February 25, 2026
**Virons AI Platform**
