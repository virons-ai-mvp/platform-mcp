# ADR-004: Use Pre-Built MCP Images

**Status**: ✅ Accepted
**Date**: 2026-03-08
**Supersedes**: ADR-003 (partially - reduces build effort)

## Context

We discovered 43 pre-built MCP server images available from Docker Hub, GitHub Container Registry, and other sources. These can replace custom builds and accelerate deployment.

## Decision

### Use Pre-Built Images Where Available

**Replace 5 of 8 planned builds with pre-built images:**

1. ~~eks-mcp-server~~ → `mcp/kubernetes` (9121)
2. ~~terraform-mcp-server~~ → `mcp/aws-terraform` (9142)
3. ~~prometheus-mcp-server~~ → `ghcr.io/pab1it0/prometheus-mcp-server` (9191)
4. ~~elasticache-mcp-server~~ → `mcp/redis` (9184)
5. **BONUS**: `ghcr.io/github/github-mcp-server` (9111)

**Keep Custom Builds (5 servers):**
- aws-network-mcp-server (9144) - No pre-built available
- postgres-mcp-server (9150) - No pre-built available
- dynamodb-mcp-server (9180) - No pre-built available
- cloudwatch-mcp-server (9190) - No pre-built available
- cloudtrail-mcp-server (9102) - No pre-built available

### Revised Core Deployment: 10 Servers

**5 Pre-Built (Deploy Day 1):**
1. Kubernetes (9121) - Container orchestration
2. Terraform (9142) - IaC
3. Prometheus (9191) - Metrics
4. Redis (9184) - Cache
5. GitHub (9111) - Git operations

**5 Custom Builds (Week 1-2):**
6. AWS Network (9144) - VPC/networking
7. Postgres (9150) - Primary database
8. DynamoDB (9180) - NoSQL
9. CloudWatch (9190) - AWS monitoring
10. CloudTrail (9102) - Audit trail

## Rationale

### Benefits

1. **50% Faster Deployment**: 5 servers deploy immediately (no build time)
2. **Reduced Maintenance**: Pre-built images maintained by upstream
3. **Proven Stability**: Images already tested in production
4. **Focus Build Effort**: Only build AWS-specific servers without alternatives

### Trade-offs

- **Less Control**: Can't customize pre-built images
- **Dependency Risk**: Rely on upstream image availability
- **Version Lock**: Using SHA256 pins for stability

## Implementation

### docker-compose.core.yml

```yaml
# Pre-built images (5)
virons-kubernetes-mcp:
  image: mcp/kubernetes@sha256:5565164f78ee41f3de9d957dbd3c7349fb06be8e95799a2a650cdd90d6d6d529

virons-terraform-mcp:
  image: mcp/aws-terraform@sha256:db3126c26fc13947f8d200235a872b35cdf7235f07c8fc63c262fb40196dd18e

virons-prometheus-mcp:
  image: ghcr.io/pab1it0/prometheus-mcp-server@sha256:32d47c88845ee78bc343d4c3a39a24b1bd9bebce4f53becdbbf5704221185925

virons-redis-mcp:
  image: mcp/redis@sha256:ab96ec0a8618804fe4e08414d27e515c85df8a58806e4f8353331e14670c3b10

virons-github-mcp:
  image: ghcr.io/github/github-mcp-server@sha256:7b1384cdd6d025c09256af2fb6cb79bc5e87aedc957c8826b5e50d8cb82f0be3

# Custom builds (5)
virons-aws-network-mcp:
  build:
    context: .
    dockerfile: src/awslabs/aws-network-mcp-server/Dockerfile
# ... (postgres, dynamodb, cloudwatch, cloudtrail)
```

## Timeline Impact

**Original (ADR-003)**: 2-4 weeks for 8 servers
**Revised (ADR-004)**: 1-2 weeks for 10 servers

**Day 1**: Deploy 5 pre-built images (1 hour)
**Week 1**: Build 3 critical (network, postgres, dynamodb)
**Week 2**: Build 2 observability (cloudwatch, cloudtrail)

## Future Considerations

### Phase 2 Pre-Built Images (High Value)

**Messaging:**
- `aywengo/kafka-schema-reg-mcp:stable` (9171)

**Graph Database:**
- `mcp/neo4j` (9183)
- `mcp/neo4j-cypher` (9183)

**Search:**
- `mcp/elasticsearch` (9302)

**Development:**
- `mcp/git` (9112)
- `mcp/playwright` (automation)
- `mcp/puppeteer` (automation)

### Image Update Strategy

1. **Pin by SHA256**: Ensure reproducibility
2. **Monthly Review**: Check for security updates
3. **Test Before Update**: Verify compatibility
4. **Rollback Plan**: Keep previous SHA256 in comments

## Compliance

No impact on compliance requirements:
- **BaFin AT 8.1**: CloudTrail (custom build) ✅
- **GDPR Art 25/32**: Postgres encryption (custom build) ✅
- **DORA Art 11**: CloudWatch monitoring (custom build) ✅

All compliance-critical servers remain custom builds.

## Success Metrics

- ✅ 5 pre-built servers deployed Day 1
- ✅ 50% reduction in build effort
- ✅ 50% faster time to production
- ✅ 10 total servers vs 8 originally planned
