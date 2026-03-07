#!/bin/bash
# Populate documentation following DDD principles

set -e

BASE_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

echo "📚 Populating documentation..."
echo ""

# Architecture documentation
cat > "$BASE_DIR/docs/architecture/README.md" << 'EOF'
# Architecture Documentation

System architecture, design patterns, and technical decisions for the Virons Infrastructure MCP Server.

## Contents

- [Model Architecture](model-architecture.md) - Reference architecture for all MCP servers
- [Comprehensive Review](comprehensive-review.md) - Complete server review
- [Diagrams](diagrams/) - Architecture diagrams
- [Decisions](decisions/) - Architecture Decision Records (ADRs)

## Overview

The Virons Infrastructure MCP Server follows a clean 4-layer architecture:

```
API Layer (FastAPI)
    ↓
Application Layer (Services)
    ↓
Domain Layer (Models)
    ↓
Infrastructure Layer (Technical)
```

## Key Patterns

- **Multi-protocol support**: MCP (stdio), HTTP (health), REST API (Swagger)
- **Domain-Driven Design**: Clear separation of concerns
- **Dependency Injection**: Services injected into API layer
- **Repository Pattern**: Upstream registry abstraction

## Documentation

- [Model Architecture](model-architecture.md) - Complete reference
- [Comprehensive Review](comprehensive-review.md) - Implementation review
EOF

# Compliance documentation
cat > "$BASE_DIR/docs/compliance/README.md" << 'EOF'
# Compliance Documentation

Regulatory compliance documentation for BaFin, GDPR, DORA, and EU AI Act.

## Contents

- [Overview](overview.md) - Compliance requirements
- [Logging Implementation](logging-implementation.md) - BaFin audit trails
- [Policies](policies/) - Compliance policies
- [Audits](audits/) - Audit reports
- [Evidence](evidence/) - Compliance evidence

## Regulations

### BaFin MaRisk AT 8.1
- Audit trails with 10-year retention
- Calculation audit before forensic flags
- Write audit on every write operation
- Immutable logs

### GDPR Art 32
- Security measures for data processing
- Encryption at rest and in transit
- Access controls and audit logs

### DORA Art 11
- ICT risk management framework
- Health checks and monitoring
- Incident response procedures

### EU AI Act
- High-risk system documentation
- Model cards and versioning
- Human oversight mechanisms

## Implementation

See [Logging Implementation](logging-implementation.md) for technical details.
EOF

# Operations documentation
cat > "$BASE_DIR/docs/operations/README.md" << 'EOF'
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
EOF

# Development documentation
cat > "$BASE_DIR/docs/development/README.md" << 'EOF'
# Development Documentation

Development guides, implementation notes, and contribution guidelines.

## Contents

- [Implementation](implementation.md) - Implementation details
- [Implementation Progress](implementation-progress.md) - Progress tracking
- [Project Complete](project-complete.md) - Project status
- [Enhancement Summary](enhancement-summary.md) - Recent changes
- [Contributing](contributing/) - Contribution guidelines
- [Testing](testing/) - Testing guides

## Getting Started

```bash
# Clone and setup
git clone <repo>
cd virons-infrastructure-mcp-server
uv sync

# Run tests
uv run pytest

# Start development server
./scripts/development/start-api.sh
```

## Architecture

- **API Layer**: FastAPI with Swagger UI
- **Application Layer**: Service classes (deploy, list, destroy)
- **Domain Layer**: Business models and logic
- **Infrastructure Layer**: Health, metrics, compliance

## Testing

- Unit tests: `tests/`
- Integration tests: `tests/integration/`
- Coverage: 88% (43/49 tests passing)

## Contributing

See [Contributing](contributing/) for guidelines.
EOF

# Getting Started documentation
cat > "$BASE_DIR/docs/getting-started/README.md" << 'EOF'
# Getting Started

Quick start guide for the Virons Infrastructure MCP Server.

## Prerequisites

- Python 3.10+
- uv package manager
- Docker (optional)
- Kubernetes (optional)

## Installation

```bash
# Install dependencies
uv sync

# Verify installation
uv run python -c "from virons.infrastructure_mcp_server import __version__; print(__version__)"
```

## Quick Start

### API Mode (Recommended)
```bash
./scripts/development/start-api.sh
# Open http://localhost:8080/api/docs
```

### MCP Mode
```bash
uv run virons-infrastructure-mcp-server --transport stdio
```

### Health Check Mode
```bash
uv run virons-infrastructure-mcp-server --transport http --port 8080
```

## First Steps

1. **Explore Swagger UI**: http://localhost:8080/api/docs
2. **Check health**: `curl http://localhost:8080/health/ready`
3. **View metrics**: `curl http://localhost:8080/metrics`
4. **Deploy infrastructure**: Use Swagger UI or curl

## Next Steps

- Read [Architecture Documentation](../architecture/)
- Review [Compliance Documentation](../compliance/)
- Check [Operations Guide](../operations/)
- Explore [Development Guide](../development/)
EOF

# Reference documentation
cat > "$BASE_DIR/docs/reference/README.md" << 'EOF'
# Reference Documentation

API reference, changelog, and templates.

## Contents

- [Changelog](changelog.md) - Version history
- [Virons README Template](virons-readme-template.md) - Documentation template

## API Reference

### REST API
- Swagger UI: http://localhost:8080/api/docs
- ReDoc: http://localhost:8080/api/redoc
- OpenAPI: http://localhost:8080/api/openapi.json

### Endpoints

#### Infrastructure
- `POST /api/v1/deploy` - Deploy infrastructure
- `POST /api/v1/destroy` - Destroy infrastructure
- `GET /api/v1/stacks` - List stacks
- `GET /api/v1/info` - Server information

#### Health & Monitoring
- `GET /health/live` - Liveness probe
- `GET /health/ready` - Readiness probe
- `GET /metrics` - Prometheus metrics

## MCP Tools

- `deploy_infrastructure` - Deploy using CDK/CFN/Terraform/IaC
- `destroy_infrastructure` - Destroy infrastructure stack
- `list_stacks` - List deployed stacks

## Version History

See [Changelog](changelog.md) for version history.
EOF

echo "✅ Core documentation populated"
echo ""
echo "📋 Documentation checklist:"
echo "  ✅ docs/architecture/README.md"
echo "  ✅ docs/compliance/README.md"
echo "  ✅ docs/operations/README.md"
echo "  ✅ docs/development/README.md"
echo "  ✅ docs/getting-started/README.md"
echo "  ✅ docs/reference/README.md"
echo ""
echo "✅ Documentation population complete!"
