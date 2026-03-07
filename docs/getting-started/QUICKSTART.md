<link rel="stylesheet" href="../../../platform-resources/styles/virons-markdown.css">

# Platform MCP Quickstart

## Prerequisites

***

- Python 3.11+
- Docker Desktop (for Kind cluster)
- kubectl 1.28+
- helm 3.12+
- AWS CLI (for EKS deployment)

## Local Setup (Kind)

***

```bash
# Clone repository
cd platform-mcp

# Install dependencies
pip install -e ".[dev]"

# Start Kind cluster
kind create cluster --config infrastructure/kind-config.yaml

# Verify cluster
kubectl cluster-info --context kind-virons-mcp

# Deploy MCP servers
helm install virons-mcp charts/virons-mcp \
  --set environment=local \
  --set audit.enabled=true

# Verify deployment
kubectl get pods -n virons-mcp
```

## Production Setup (EKS)

***

```bash
# Configure AWS credentials
aws configure --profile virons-prod

# Connect to EKS cluster
aws eks update-kubeconfig \
  --region eu-central-1 \
  --name virons-prod-cluster \
  --profile virons-prod

# Deploy with production values
helm upgrade --install virons-mcp charts/virons-mcp \
  -f values-prod.yaml \
  --namespace virons-mcp \
  --create-namespace

# Verify
kubectl get pods -n virons-mcp
kubectl logs -n virons-mcp -l app=gitleaks
```

## Available MCP Servers

***

### Security Context (9100-9109)

| Server | Port | Purpose | Compliance |
|--------|------|---------|------------|
| **gitleaks** | 9100 | Pre-commit secret scanning | BaFin AT 8.1 |
| **compliance-gate** | 9101 | Pre-commit compliance checks | GDPR Art 25 |

```bash
# Test gitleaks
curl http://localhost:9100/health
curl -X POST http://localhost:9100/scan -d '{"repo": "."}'
```

### Governance Context (9110-9119)

| Server | Port | Purpose | Compliance |
|--------|------|---------|------------|
| **org-governance** | 9102 | Organization policy enforcement | BaFin AT 8.1 |
| **workflow-governance** | 9103 | Workflow validation | DORA Art 11 |

```bash
# Test org-governance
curl http://localhost:9102/validate-policy \
  -d '{"policy": "branch-protection"}'
```

### Operations Context (9120-9129)

| Server | Port | Purpose | Compliance |
|--------|------|---------|------------|
| **secrets-rotation** | 9104 | Automated secret rotation | DORA Art 11 |

```bash
# Trigger rotation
curl -X POST http://localhost:9104/rotate \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"secret_id": "virons/api-key"}'
```

### Compliance Context (9130-9139)

| Server | Port | Purpose | Compliance |
|--------|------|---------|------------|
| **compliance-checklist** | 9105 | Multi-regulation validation | BaFin/GDPR/DORA |

```bash
# Run compliance check
curl http://localhost:9105/check \
  -d '{"regulations": ["bafin", "gdpr", "dora"]}'
```

## Testing

***

```bash
# Unit tests
pytest tests/servers/ -v

# Integration tests (requires Kind cluster)
pytest tests/integration/ --kind-cluster

# Compliance validation
python scripts/validate_compliance.py --all

# Load testing
locust -f tests/load/locustfile.py --host http://localhost:9100
```

## Configuration

***

### Environment Variables

```bash
# Required
export VIRONS_ENV=local|staging|production
export AUDIT_DB_URL=postgresql://user:pass@localhost:5432/audit
export AWS_REGION=eu-central-1

# Optional
export LOG_LEVEL=INFO
export ROTATION_INTERVAL_DAYS=90
```

### Helm Values

```yaml
# values-local.yaml
environment: local
audit:
  enabled: true
  retention: 7y
secrets:
  rotation:
    enabled: true
    interval: 90d
```

## Troubleshooting

***

### MCP Server Not Starting

```bash
# Check logs
kubectl logs -n virons-mcp -l app=gitleaks --tail=100

# Check events
kubectl get events -n virons-mcp --sort-by='.lastTimestamp'

# Restart pod
kubectl rollout restart deployment/gitleaks -n virons-mcp
```

### Audit Logs Not Writing

```bash
# Verify database connection
kubectl exec -it -n virons-mcp deploy/gitleaks -- \
  psql $AUDIT_DB_URL -c "SELECT 1"

# Check audit table
kubectl exec -it -n virons-mcp deploy/gitleaks -- \
  psql $AUDIT_DB_URL -c "SELECT COUNT(*) FROM audit_log"
```

## Next Steps

***

- [Architecture Overview](../architecture/README.md)
- [DDD Context Map](../architecture/ddd/CONTEXT-MAP.md)
- [Contributing Guide](../development/contributing/README.md)
- [Runbooks](../operations/runbooks/README.md)
- [Compliance Matrix](../compliance/COMPLIANCE_MATRIX.md)

## Navigation
← [Docs Home](../README.md)

***

**Last Updated**: 2026-03-05
**Maintained By**: platform@virons.ai
