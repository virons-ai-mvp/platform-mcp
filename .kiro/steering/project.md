# platform-mcp — Project Reference

**Repo**: platform-mcp | **Type**: MCP Server Platform | **Cluster**: virons-mvp (EKS 1.31)
**Region**: eu-central-1 | **Compliance**: BaFin MaRisk AT 8.1, GDPR Art 32, DORA Art 11, EU AI Act

## Critical Rules (Non-Negotiable)

| Rule | Requirement |
|---|---|
| **TDD** | **Write tests FIRST, then code to pass tests. 95% minimum coverage** |
| **DDD** | **Follow Domain-Driven Design — application/domain/infrastructure layers** |
| **Tool Docs** | **Every tool MUST have comprehensive Args documentation for AI agents** |
| **Pre-commit** | **Never skip hooks — always fix issues before committing** |
| GDPR | All data in eu-central-1, 100% request audit logging |
| Security | Scan on commit, block secrets, Trivy on push, image signing |
| Monitoring | Prometheus metrics, health checks, distributed tracing with correlation IDs |
| Gateway Pattern | All MCP servers expose /tools, /health, /ready, /metrics |

## MCP Server Catalog

| Service | Port | Tools | Status | Documentation |
|---------|------|-------|--------|---------------|
| Gateway | 9000 | 90 (aggregated) | ✅ | [📖 Docs](src/virons-mcp-gateway/README.md) |
| Infrastructure | 9100 | 78 | ✅ | [📖 Docs](src/virons-infrastructure-mcp-server/README.md) |
| Security | 9500 | 4 | ✅ | [📖 Docs](src/virons-security-mcp-server/README.md) |
| Operations | 9510 | 4 | ✅ | [📖 Docs](src/virons-operations-mcp-server/README.md) |
| Monitoring | 9520 | 4 | ✅ | [📖 Docs](src/virons-monitoring-mcp-server/README.md) |

### Infrastructure MCP Server (78 tools)
**Categories**: EC2, Lambda, S3, RDS, DynamoDB, CloudFormation, IAM, VPC, ECS, EKS, CloudWatch, Cost Management, Backup, Resource Management

**Key Tools**:
- `list_ec2_instances`, `start_instance`, `stop_instance`, `create_instance`
- `list_lambda_functions`, `invoke_lambda`, `update_lambda_code`
- `list_s3_buckets`, `upload_to_s3`, `download_from_s3`
- `list_rds_instances`, `create_db_snapshot`, `restore_db_snapshot`
- `list_cloudformation_stacks`, `create_stack`, `update_stack`, `delete_stack`
- `get_logs`, `query_logs`, `create_alarm`, `set_budget`
- `search_resources`, `tag_resources`, `get_resource_compliance`

### Security MCP Server (4 tools)
- `scan_secrets` — Scan code for exposed secrets
- `check_compliance` — Validate compliance requirements
- `audit_iam` — Audit IAM policies and permissions
- `scan_vulnerabilities` — Scan for security vulnerabilities

### Operations MCP Server (4 tools)
- `deploy_service` — Deploy service to Kubernetes
- `rollback_deployment` — Rollback to previous version
- `scale_service` — Scale service replicas
- `restart_service` — Restart service pods

### Monitoring MCP Server (4 tools)
- `get_metrics` — Retrieve Prometheus metrics
- `query_logs` — Query application logs
- `check_health` — Check service health status
- `get_alerts` — Retrieve active alerts

## AWS Coordinates

- **Account**: virons-management (412179655775)
- **Profile**: `virons-management`
- **Region**: eu-central-1
- **ECR**: 412179655775.dkr.ecr.eu-central-1.amazonaws.com
- **EKS Cluster**: virons-mvp
- **Namespace**: mcp-platform

## Quick Commands

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View gateway tools
curl http://localhost:9000/tools | jq

# Run tests
pytest

# Validate documentation
./scripts/validate-tool-docs.sh

# Run pre-push validation
.git/hooks/pre-push
```

## Documentation Structure (DDD)

```
docs/
├── domain/              # Core business concepts
│   ├── tools/          # Tool catalog, standards
│   └── integration/    # Integration patterns
├── application/        # Use cases and workflows
│   └── workflows/
└── infrastructure/     # Technical implementation
    └── deployment/
```

## Testing Requirements

- **TDD Mode**: Enabled
- **Min Coverage**: 95%
- **Frameworks**: pytest (Python)
- **Test Types**: Unit, Integration, E2E, Test Containers
- **Run on Save**: Disabled (manual trigger)

## Compliance Frameworks

- **BaFin MaRisk AT 8.1**: Audit logging, calculation ordering
- **GDPR Art 32**: Data residency (eu-central-1), PII encryption
- **DORA Art 11**: RTO 4h, RPO 1h, resilience requirements
- **EU AI Act**: High-risk AI systems, model cards, human oversight

## Security Policies

- Scan on commit (TruffleHog)
- Block secrets in commits
- Trivy scan on push
- Image signing with Cosign
- Run as non-root
- Read-only root filesystem
- Network policies enabled
- OPA admission control

## Monitoring & Observability

- **Prometheus**: Metrics collection on port 9090
- **Health Checks**: `/health` (liveness), `/ready` (readiness)
- **Metrics**: `/metrics` endpoint on all services
- **Distributed Tracing**: Correlation ID middleware
- **Logging**: Structured JSON logs with correlation IDs

## Deployment

- **Strategy**: Rolling updates
- **Max Unavailable**: 1
- **Max Surge**: 1
- **Min Ready Seconds**: 10
- **Progress Deadline**: 600s
- **Autoscaling**: 2-10 replicas, 70% CPU target
- **PDB**: Min available 1
- **Graceful Shutdown**: 30s

## Resources

- **Requests**: 100m CPU, 128Mi memory
- **Limits**: 500m CPU, 512Mi memory

## Git Hooks

- **Pre-commit**: trufflehog, ruff, pytest-fast
- **Pre-push**: trivy, verify-docs, ddd-validation, tdd-validation
- **Commit-msg**: conventional-commits

Install: `./scripts/install-hooks.sh`
