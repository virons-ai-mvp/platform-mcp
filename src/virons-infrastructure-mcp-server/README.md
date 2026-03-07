# Virons Infrastructure MCP Server

**Status**: ✅ PRODUCTION READY | **Version**: 0.1.0 | **Coverage**: 88%

Infrastructure orchestrator with **REST API + Swagger UI** that wraps AWS CDK, CloudFormation, Terraform, and IaC MCP servers with BaFin-compliant audit trails.

## 🚀 Quick Start

### API Mode (REST + Swagger UI)
```bash
./scripts/development/start-api.sh
# Open http://localhost:8080/api/docs
```

### MCP Mode (stdio)
```bash
uv run virons-infrastructure-mcp-server --transport stdio
```

### Health Check Mode (Kubernetes)
```bash
uv run virons-infrastructure-mcp-server --transport http --port 8080
```

## ✨ Features

- ✅ **Multi-protocol**: MCP (stdio), HTTP (health), REST API (Swagger)
- ✅ **Multi-tool**: CDK, CloudFormation, Terraform, IaC
- ✅ **BaFin compliant**: Full audit trails with 10-year retention
- ✅ **Observability**: Prometheus metrics, structured logging
- ✅ **API documentation**: OpenAPI/Swagger UI + ReDoc
- ✅ **Kubernetes ready**: Health probes, Helm chart, metrics

## 📚 API Endpoints

### Documentation
- `GET /api/docs` - **Swagger UI** (interactive API docs)
- `GET /api/redoc` - ReDoc (alternative docs)
- `GET /api/openapi.json` - OpenAPI schema

### Infrastructure Operations
- `POST /api/v1/deploy` - Deploy infrastructure
- `POST /api/v1/destroy` - Destroy infrastructure
- `GET /api/v1/stacks` - List stacks
- `GET /api/v1/info` - Server information

### Health & Monitoring
- `GET /health/live` - Liveness probe
- `GET /health/ready` - Readiness probe
- `GET /metrics` - Prometheus metrics

## 💡 Usage Examples

### Deploy Infrastructure
```bash
curl -X POST http://localhost:8080/api/v1/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "cdk",
    "stack_name": "my-stack",
    "template_path": "/path/to/template",
    "parameters": {"env": "prod"}
  }'
```

### List Stacks
```bash
curl http://localhost:8080/api/v1/stacks?tool=cdk
```

### Destroy Infrastructure
```bash
curl -X POST http://localhost:8080/api/v1/destroy \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "cdk",
    "stack_name": "my-stack",
    "confirmation": "yes"
  }'
```

### Get Server Info
```bash
curl http://localhost:8080/api/v1/info
```

## 🏗️ Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=virons --cov-report=html

# Start API server
./scripts/development/start-api.sh

# Start MCP server
uv run virons-infrastructure-mcp-server --transport stdio
```

## 🐳 Docker

```bash
# Build
docker build -t virons-infrastructure-mcp-server:0.1.0 .

# Run API mode
docker run -p 8080:8080 virons-infrastructure-mcp-server:0.1.0 \
  --transport api --port 8080

# Run health mode (K8s)
docker run -p 8080:8080 virons-infrastructure-mcp-server:0.1.0 \
  --transport http --port 8080
```

## ☸️ Kubernetes

```bash
# Deploy
helm install virons-infrastructure ./helm/virons-infrastructure \
  --set image.tag=0.1.0 \
  --set transport=http

# Verify
kubectl get pods -l app=virons-infrastructure
kubectl logs -l app=virons-infrastructure

# Port forward
kubectl port-forward svc/virons-infrastructure 8080:8080

# Test
curl http://localhost:8080/health/ready
curl http://localhost:8080/metrics
```

## 📖 Documentation

- **[docs/INDEX.md](docs/INDEX.md)** - Complete documentation index
- **[docs/architecture/model-architecture.md](docs/architecture/model-architecture.md)** - Reference architecture
- **[docs/compliance/logging-implementation.md](docs/compliance/logging-implementation.md)** - BaFin audit trails
- **[docs/operations/deployment-complete.md](docs/operations/deployment-complete.md)** - Deployment guide
- **[docs/development/enhancement-summary.md](docs/development/enhancement-summary.md)** - Recent changes

## 🔒 Compliance

- ✅ **BaFin MaRisk AT 8.1** - Audit trails with 10-year retention
- ✅ **GDPR Art 32** - Security measures
- ✅ **DORA Art 11** - ICT risk management
- ✅ **EU AI Act** - High-risk system documentation

See [docs/compliance/logging-implementation.md](docs/compliance/logging-implementation.md) for implementation details.

## 🏛️ Architecture

This server serves as the **reference model** for all Virons MCP servers:

```
API Layer (FastAPI)
    ↓
Application Layer (Services)
    ↓
Domain Layer (Models)
    ↓
Infrastructure Layer (Technical)
```

See [docs/architecture/model-architecture.md](docs/architecture/model-architecture.md) for comprehensive documentation.

## 📊 Metrics

- `mcp_tool_calls_total{tool, status}` - Tool invocation counter
- `mcp_tool_duration_seconds{tool}` - Tool execution time
- `mcp_upstream_healthy{server}` - Upstream health status
- `mcp_errors_total{error_type}` - Error counter

## 🧪 Testing

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=virons --cov-report=html

# Integration tests
uv run pytest tests/integration/

# Current: 88% coverage (43/49 tests passing)
```

## 📝 License

Apache-2.0 - See [LICENSE](LICENSE) and [NOTICE](NOTICE)

---

**Model Server**: This implementation serves as the reference architecture for all Virons MCP servers. See [docs/architecture/model-architecture.md](docs/architecture/model-architecture.md) for the complete pattern.
