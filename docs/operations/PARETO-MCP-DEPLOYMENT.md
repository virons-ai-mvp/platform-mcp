# Pareto (20/80) MCP Server Deployment Plan

**Status**: Ready for Execution
**Timeline**: 1-2 weeks (revised from 2-4 weeks)
**Strategy**: 5 pre-built images + 5 custom builds = 10 servers

## Quick Start

```bash
# 1. Deploy 10 core servers (5 pre-built + 5 custom)
docker-compose -f docker-compose.core.yml up -d

# 2. Check status
docker-compose -f docker-compose.core.yml ps

# 3. Test gateway
curl http://localhost:9000/tools | jq '.tools | length'

# 4. Verify all 10 servers
./scripts/verify-core-servers.sh
```

## The 10 Core Servers

### Pre-Built Images (5 servers - Deploy Day 1)
1. **mcp/kubernetes** (9121) - Container orchestration
2. **mcp/aws-terraform** (9142) - Terraform IaC
3. **ghcr.io/pab1it0/prometheus-mcp-server** (9191) - Metrics
4. **mcp/redis** (9184) - Cache layer
5. **ghcr.io/github/github-mcp-server** (9111) - GitHub ops

### Custom Builds (5 servers - Week 1-2)
6. **aws-network-mcp-server** (9144) - VPC/networking
7. **postgres-mcp-server** (9150) - Primary database
8. **dynamodb-mcp-server** (9180) - NoSQL/blockchain
9. **cloudwatch-mcp-server** (9190) - AWS monitoring
10. **cloudtrail-mcp-server** (9102) - Audit trail (BaFin)

## Why These 10?

**Enables 80% of capabilities:**
- ✅ Container orchestration (Kubernetes)
- ✅ Infrastructure as Code (Terraform)
- ✅ Networking (AWS Network)
- ✅ Data persistence (Postgres, DynamoDB)
- ✅ Caching (Redis)
- ✅ Monitoring (Prometheus, CloudWatch)
- ✅ Compliance (CloudTrail audit trail)
- ✅ Git operations (GitHub)

**Pre-built images save 50% build time**
**10 servers vs 8 originally planned**

## Implementation Timeline

### Day 1: Pre-Built Images (1 hour)
```bash
# Pull and start 5 pre-built images
docker-compose -f docker-compose.core.yml pull
docker-compose -f docker-compose.core.yml up -d \
  virons-kubernetes-mcp \
  virons-terraform-mcp \
  virons-prometheus-mcp \
  virons-redis-mcp \
  virons-github-mcp

# Verify
curl http://localhost:9121/health  # Kubernetes
curl http://localhost:9142/health  # Terraform
curl http://localhost:9191/health  # Prometheus
curl http://localhost:9184/health  # Redis
curl http://localhost:9111/health  # GitHub
```

### Week 1: Critical Builds (Days 2-7)
- Day 2-3: aws-network-mcp-server (9144)
- Day 4-5: postgres-mcp-server (9150)
- Day 6-7: dynamodb-mcp-server (9180)

### Week 2: Observability (Days 8-14)
- Day 8-10: cloudwatch-mcp-server (9190)
- Day 11-13: cloudtrail-mcp-server (9102)
- Day 14: Integration testing

## Per-Server Deployment (Minimal)

Each server requires:

1. **Dockerfile** (if not exists)
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY src/awslabs/<server-name> .
RUN pip install -e .
CMD ["python", "-m", "awslabs.<module>.server"]
```

2. **IAM Policy** (least privilege)
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["<service>:*"],
    "Resource": "*",
    "Condition": {
      "StringEquals": {"aws:RequestedRegion": "eu-central-1"}
    }
  }]
}
```

3. **Health Check**
```bash
curl -f http://localhost:<port>/health
```

4. **Gateway Integration**
```python
# Add to virons-infrastructure-mcp-server
UPSTREAM_CONFIG["<server>"] = {
    "command": "/app/.venv/bin/python",
    "args": ["-m", "awslabs.<module>.server"],
    "description": "<description>"
}
```

## Deployment Checklist

### Pre-Deployment
- [ ] AWS credentials configured (~/.aws/credentials)
- [ ] Docker installed and running
- [ ] Port 9000-9199 available
- [ ] eu-central-1 region accessible

### Per Server (8x)
- [ ] Dockerfile exists or created
- [ ] IAM policy defined
- [ ] Added to docker-compose.core.yml
- [ ] Health check configured
- [ ] Gateway integration added
- [ ] Basic test passed

### Post-Deployment
- [ ] All 8 servers healthy
- [ ] Gateway aggregates all tools
- [ ] End-to-end test passed
- [ ] Documentation updated
- [ ] Runbook created

## Testing

### Individual Server Test
```bash
# Test server is running
curl http://localhost:<port>/health

# List tools
curl http://localhost:<port>/tools | jq '.tools[].name'

# Test tool execution
curl -X POST http://localhost:<port>/call_tool \
  -H "Content-Type: application/json" \
  -d '{"name": "<tool>", "arguments": {}}'
```

### End-to-End Test
```bash
# 1. Deploy infrastructure
curl -X POST http://localhost:9143/call_tool \
  -d '{"name": "deploy_stack", "arguments": {...}}'

# 2. Create database
curl -X POST http://localhost:9150/call_tool \
  -d '{"name": "create_database", "arguments": {...}}'

# 3. Query metrics
curl -X POST http://localhost:9190/call_tool \
  -d '{"name": "get_metrics", "arguments": {...}}'

# 4. Check audit trail
curl -X POST http://localhost:9102/call_tool \
  -d '{"name": "lookup_events", "arguments": {...}}'
```

## Success Criteria

**Day 1**: ✅ 5 pre-built servers deployed and healthy
**Week 1**: ✅ 8 total servers (5 pre-built + 3 builds)
**Week 2**: ✅ 10 total servers (all operational)

## Deferred to Phase 2 (33 remaining servers)

**Available as pre-built images:**
- Kafka + Schema Registry (messaging)
- Neo4j (graph database for fraud detection)
- Elasticsearch (search)
- Additional development tools

**Requires custom builds:**
- IAM management
- Cost optimization
- Additional AWS services
- ML services (SageMaker, Bedrock)

## Compliance

**BaFin AT 8.1**: ✅ CloudTrail (audit trail)
**GDPR Art 25/32**: ✅ Postgres (encryption), CloudTrail (monitoring)
**DORA Art 11**: ✅ CloudWatch (resilience monitoring)

All critical compliance requirements met.

## Next Steps

1. Review ADR-003 for detailed rationale
2. Run `./scripts/deploy-core-mcp-servers.sh`
3. Test each server individually
4. Run end-to-end integration test
5. Deploy first Virons service
6. Plan Phase 2 (remaining 32 servers)

## Support

- **Documentation**: `docs/architecture/decisions/ADR-003-pareto-mcp-deployment.md`
- **Deployment Script**: `scripts/deploy-core-mcp-servers.sh`
- **Docker Compose**: `docker-compose.core.yml`
- **Issues**: Create GitHub issue with `mcp-deployment` label
