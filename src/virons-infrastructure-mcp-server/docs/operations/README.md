# Operations Documentation

Deployment, monitoring, and operational procedures.

## Contents

- [Deployment Guide](deployment-guide.md) - How to deploy
- [Deployment Complete](deployment-complete.md) - Deployment summary
- [Production Deployment](production-deployment.md) - Production setup
- [Deployment Success](deployment-success.md) - Success notes
- [Runbooks](runbooks/) - Operational runbooks

## Quick Start

### Local Development
```bash
uv sync
uv run virons-infrastructure-mcp-server --transport api --port 8080
```

### Docker
```bash
docker build -t virons-infrastructure-mcp-server:0.1.0 .
docker run -p 8080:8080 virons-infrastructure-mcp-server:0.1.0
```

### Kubernetes
```bash
helm install virons-infrastructure ./helm/virons-infrastructure
kubectl get pods -l app=virons-infrastructure
```

## Monitoring

- Health: `/health/live`, `/health/ready`
- Metrics: `/metrics` (Prometheus)
- Logs: `kubectl logs -l app=virons-infrastructure`

## Documentation

See individual guides for detailed procedures.
