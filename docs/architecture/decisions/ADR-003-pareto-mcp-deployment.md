# ADR-003: Pareto (20/80) MCP Server Deployment

**Status**: ✅ Accepted
**Date**: 2026-03-08
**Principle**: Deploy 20% of servers that deliver 80% of value
**Timeline**: 2-4 weeks for core 8 servers

## Context

We have 40 Tier 1 AWS MCP servers planned (ADR-002), but need immediate deployment to unblock service development. Apply Pareto principle: identify the 8 critical servers (20%) that enable 80% of platform capabilities.

## Decision

### Deploy 8 Core Servers Immediately (Week 1-4)

#### Critical Path Servers (8 servers)

**Infrastructure Foundation (3 servers)**
1. **aws-iac-mcp-server** (9143) - Score: 46
   - Unified IaC deployment (replaces cdk/cfn/terraform)
   - Enables: All infrastructure deployment
   - Effort: 3 days
   - Priority: P0 - Blocks everything

2. **eks-mcp-server** (9121) - Score: 54
   - Kubernetes cluster management
   - Enables: Service deployment, scaling
   - Effort: 2 days
   - Priority: P0 - Blocks service deployment

3. **aws-network-mcp-server** (9144) - Score: 49
   - VPC, subnets, security groups
   - Enables: Network infrastructure
   - Effort: 2 days
   - Priority: P0 - Blocks connectivity

**Data Layer (3 servers)**
4. **postgres-mcp-server** (9150) - Score: 59
   - Primary transactional database
   - Enables: Forensic audit logs, user data
   - Effort: 2 days
   - Priority: P0 - Blocks all services

5. **dynamodb-mcp-server** (9180) - Score: 57
   - NoSQL for blockchain, transactions
   - Enables: Transaction ledger, high-throughput data
   - Effort: 2 days
   - Priority: P0 - Blocks blockchain services

6. **s3-tables-mcp-server** (9185) - Score: 42
   - Data lake for ML training
   - Enables: Forensic data lake, ML pipelines
   - Effort: 1 day
   - Priority: P1 - Blocks ML services

**Observability (2 servers)**
7. **cloudwatch-mcp-server** (9190) - Score: 62
   - Metrics, logs, alarms
   - Enables: Production monitoring
   - Effort: 2 days
   - Priority: P0 - Blocks production readiness

8. **cloudtrail-mcp-server** (9102) - Score: 71
   - Audit trail (BaFin AT 8.1)
   - Enables: Compliance, security investigations
   - Effort: 2 days
   - Priority: P0 - Blocks compliance

### Deferred to Phase 2 (32 servers)

**Can be added incrementally without blocking development:**
- IAM management (use AWS console temporarily)
- Cost optimization (manual monitoring initially)
- Additional databases (add as needed)
- ML services (after core services deployed)
- Advanced monitoring (Prometheus, Grafana)

## Implementation Plan

### Week 1: Infrastructure Foundation (Days 1-5)
```bash
# Day 1-3: aws-iac-mcp-server (9143)
- Deploy server container
- Configure IAM: CloudFormation, CDK, Terraform permissions
- Test: Deploy sample stack
- Document: Basic IaC operations

# Day 4-5: eks-mcp-server (9121)
- Deploy server container
- Configure IAM: EKS read/write permissions
- Test: List clusters, scale deployment
- Document: Kubernetes operations

# Day 5: aws-network-mcp-server (9144)
- Deploy server container
- Configure IAM: VPC, subnet, security group permissions
- Test: List VPCs, create security group
- Document: Network operations
```

### Week 2: Data Layer (Days 6-10)
```bash
# Day 6-7: postgres-mcp-server (9150)
- Deploy server container
- Configure IAM: RDS permissions
- Test: Create database, run queries
- Document: Database operations

# Day 8-9: dynamodb-mcp-server (9180)
- Deploy server container
- Configure IAM: DynamoDB permissions
- Test: Create table, put/get items
- Document: NoSQL operations

# Day 10: s3-tables-mcp-server (9185)
- Deploy server container
- Configure IAM: S3 permissions
- Test: Create bucket, upload data
- Document: Data lake operations
```

### Week 3: Observability (Days 11-14)
```bash
# Day 11-12: cloudwatch-mcp-server (9190)
- Deploy server container
- Configure IAM: CloudWatch permissions
- Test: Query metrics, create alarm
- Document: Monitoring operations

# Day 13-14: cloudtrail-mcp-server (9102)
- Deploy server container
- Configure IAM: CloudTrail permissions
- Test: Lookup events, query Lake
- Document: Audit operations
```

### Week 4: Integration & Testing (Days 15-20)
```bash
# Day 15-17: End-to-end testing
- Deploy sample service using all 8 servers
- Test infrastructure → data → observability flow
- Validate compliance requirements

# Day 18-19: Documentation
- Update gateway to expose all tools
- Create quickstart guide
- Document common workflows

# Day 20: Production readiness
- Security review
- Performance testing
- Deployment runbook
```

## Deployment Template (Minimal)

### docker-compose.yml Addition
```yaml
  virons-aws-iac-mcp:
    build:
      context: .
      dockerfile: src/awslabs/aws-iac-mcp-server/Dockerfile
    container_name: virons-aws-iac-mcp
    ports:
      - "9143:9143"
    environment:
      PORT: 9143
      AWS_REGION: eu-central-1
    volumes:
      - ~/.aws:/root/.aws:ro
    networks:
      - virons-mcp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9143/health"]
```

### Gateway Integration
```python
# src/virons-mcp-gateway/virons/mcp_gateway/server.py
UPSTREAM_CONFIG = {
    "iac": {
        "command": "/app/.venv/bin/python",
        "args": ["-m", "awslabs.aws_iac_mcp_server.server"],
        "description": "AWS IaC MCP Server"
    },
    "eks": {
        "command": "/app/.venv/bin/python",
        "args": ["-m", "awslabs.eks_mcp_server.server"],
        "description": "AWS EKS MCP Server"
    },
    # ... repeat for all 8 servers
}
```

## Success Criteria

**Week 1**: Can deploy infrastructure via IaC
**Week 2**: Can create databases and store data
**Week 3**: Can monitor services and audit events
**Week 4**: Can deploy first Virons service end-to-end

## Value Delivered (80%)

With these 8 servers, we enable:
- ✅ Infrastructure deployment (IaC, EKS, networking)
- ✅ Data persistence (Postgres, DynamoDB, S3)
- ✅ Production monitoring (CloudWatch)
- ✅ Compliance (CloudTrail audit trail)
- ✅ Service development (all core dependencies met)

**Blocked without these 8**: Everything
**Blocked without remaining 32**: Nice-to-have features

## Rationale

### Why These 8?

1. **aws-iac-mcp-server**: Single server replaces 3 (cdk, cfn, terraform)
2. **eks-mcp-server**: Required for container orchestration
3. **aws-network-mcp-server**: Required for connectivity
4. **postgres-mcp-server**: Primary database for most services
5. **dynamodb-mcp-server**: Required for blockchain/high-throughput
6. **s3-tables-mcp-server**: Required for ML data pipelines
7. **cloudwatch-mcp-server**: Required for production operations
8. **cloudtrail-mcp-server**: Required for BaFin compliance

### Why Not Others?

- **IAM**: Can manage via AWS console initially
- **Cost Explorer**: Can monitor via AWS console initially
- **Lambda/ECS**: EKS covers container orchestration
- **Step Functions**: Can add later for complex workflows
- **Additional DBs**: Add as services require them
- **ML servers**: Add when ML services are ready
- **Prometheus/Grafana**: CloudWatch sufficient initially

## Next Steps

1. Create deployment scripts for 8 servers
2. Configure IAM policies (least privilege)
3. Update gateway to integrate all 8
4. Test end-to-end deployment
5. Document quickstart guide
6. Deploy to staging environment
7. Production deployment

## Compliance Impact

**BaFin AT 8.1**: ✅ Covered (CloudTrail)
**GDPR Art 25/32**: ✅ Covered (Postgres encryption, CloudTrail monitoring)
**DORA Art 11**: ✅ Covered (CloudWatch monitoring, infrastructure resilience)

All critical compliance requirements met with these 8 servers.
