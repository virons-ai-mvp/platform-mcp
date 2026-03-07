# Virons Infrastructure MCP Server - Deployment Guide

## Overview

Production-ready MCP server that orchestrates AWS infrastructure tools (CDK, CloudFormation, Terraform, IaC) with full compliance (BaFin, GDPR, DORA).

## Quick Start

### Local Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest -v

# Run server
uv run python -m virons.infrastructure_mcp_server.server --allow-write
```

### Docker Build

```bash
# Build image
docker build -t virons-infrastructure-mcp-server:0.1.0 .

# Run container
docker run -p 8080:8080 virons-infrastructure-mcp-server:0.1.0
```

### Kubernetes Deployment

```bash
# Install with Helm
helm install virons-infrastructure ./helm/virons-infrastructure \
  --set upstream.cdk.host=virons-cdk-mcp-server \
  --set upstream.cfn.host=virons-cfn-mcp-server \
  --set compliance.region=eu-central-1

# Check health
kubectl get pods -l app=virons-infrastructure
kubectl logs -l app=virons-infrastructure

# Port forward for testing
kubectl port-forward svc/virons-infrastructure 8080:8080
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `UPSTREAM_CDK_HOST` | CDK MCP server host | `localhost` |
| `UPSTREAM_CDK_PORT` | CDK MCP server port | `9140` |
| `UPSTREAM_CFN_HOST` | CloudFormation server host | `localhost` |
| `UPSTREAM_CFN_PORT` | CloudFormation server port | `9141` |
| `UPSTREAM_TERRAFORM_HOST` | Terraform server host | `localhost` |
| `UPSTREAM_TERRAFORM_PORT` | Terraform server port | `9142` |
| `UPSTREAM_IAC_HOST` | IaC server host | `localhost` |
| `UPSTREAM_IAC_PORT` | IaC server port | `9143` |
| `COMPLIANCE_REGION` | GDPR data residency region | `eu-central-1` |
| `FASTMCP_LOG_LEVEL` | Log level | `WARNING` |

### Helm Values

```yaml
replicaCount: 1

image:
  repository: virons-infrastructure-mcp-server
  tag: "0.1.0"

upstream:
  cdk:
    host: virons-cdk-mcp-server
    port: 9140
  cfn:
    host: virons-cfn-mcp-server
    port: 9141

compliance:
  region: eu-central-1
  auditEnabled: true
```

## Health Checks

### Liveness Probe
```bash
curl http://localhost:8080/health/live
# {"status": "ok", "timestamp": "2026-03-06T19:50:00Z"}
```

### Readiness Probe
```bash
curl http://localhost:8080/health/ready
# {"status": "ok", "upstreams": {...}, "timestamp": "2026-03-06T19:50:00Z"}
```

## Metrics

Prometheus metrics exposed at `/metrics`:

- `mcp_tool_calls_total{tool, status}` - Total tool calls
- `mcp_tool_duration_seconds{tool}` - Tool execution duration
- `mcp_upstream_healthy{server}` - Upstream health status (0/1)
- `mcp_errors_total{error_type}` - Total errors by type

## Compliance

### BaFin MaRisk AT 8.1 - Audit Trail
All write operations (deploy, destroy) create audit records:
```json
{
  "audit_id": "550e8400-e29b-41d4-a716-446655440000",
  "operation": "deploy_infrastructure",
  "entity_id": "my-stack",
  "timestamp": "2026-03-06T19:50:00Z"
}
```

### GDPR Art 25 - Data Residency
Region enforcement on all deployments:
```python
# Only EU regions allowed
enforce_region(region="eu-central-1")  # ✅ OK
enforce_region(region="us-east-1")     # ❌ Error
```

### GDPR Art 32 - Correlation IDs
All requests tagged with correlation IDs for traceability.

### DORA Art 11 - Operational Resilience
Health checks monitor upstream service availability.

## Tools

### deploy_infrastructure
```json
{
  "tool": "cdk",
  "stack_name": "my-stack",
  "template_path": "/path/to/template",
  "parameters": {"key": "value"}
}
```

### list_stacks
```json
{
  "tool": "cdk"
}
```

### destroy_infrastructure
```json
{
  "tool": "cdk",
  "stack_name": "my-stack",
  "confirm": true
}
```

## Architecture

```
┌─────────────────────────────────────┐
│  virons-infrastructure-mcp-server   │
│  ┌───────────────────────────────┐  │
│  │   FastMCP Server (stdio)      │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │   Application Services        │  │
│  │   - DeployService             │  │
│  │   - ListService               │  │
│  │   - DestroyService            │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │   Domain Layer                │  │
│  │   - UpstreamRegistry          │  │
│  │   - MCPClient                 │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
           │  │  │  │
           ▼  ▼  ▼  ▼
    ┌─────┬─────┬─────┬─────┐
    │ CDK │ CFN │ TF  │ IaC │
    └─────┴─────┴─────┴─────┘
```

## Testing

```bash
# Unit tests
uv run pytest tests/domain tests/application -v

# Infrastructure tests
uv run pytest tests/infrastructure -v

# Integration tests
uv run pytest tests/integration -v

# All tests
uv run pytest -v

# Coverage
uv run pytest --cov --cov-report=html
```

## Security

- Runs as non-root user (UID 1000)
- Multi-stage Docker build
- No secrets in environment variables
- Audit trail for all write operations
- GDPR-compliant data residency

## Troubleshooting

### Upstream Connection Errors
```bash
# Check upstream services are running
kubectl get pods -l app=virons-cdk-mcp-server

# Check network connectivity
kubectl exec -it virons-infrastructure-xxx -- ping virons-cdk-mcp-server
```

### Health Check Failures
```bash
# Check readiness probe
kubectl describe pod virons-infrastructure-xxx

# View logs
kubectl logs virons-infrastructure-xxx
```

## Support

- **Documentation**: `/docs`
- **Issues**: GitHub Issues
- **Team**: Virons Fintech Engineering

---

**Version**: 0.1.0
**Last Updated**: 2026-03-06
**License**: Apache-2.0
