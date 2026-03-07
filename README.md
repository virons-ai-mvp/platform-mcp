# Virons MCP Platform

Multi-service MCP platform with 90 tools across infrastructure, security, operations, and monitoring.

## Quick Start

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View gateway tools
curl http://localhost:9000/tools | jq
```

## Documentation

📖 **[Complete Documentation Index](docs/INDEX.md)**

### Key Documents
- **[Architecture](docs/architecture/)** - Design guidelines, DDD patterns, MCP server standard
- **[Operations](docs/operations/)** - Deployment, Docker optimization, runbooks
- **[Development](docs/development/)** - Developer guide, coding tips, contributing
- **[Compliance](docs/compliance/)** - BaFin, DORA, GDPR requirements

## Services

| Service | Port | Tools | Documentation | Status |
|---------|------|-------|---------------|--------|
| [Gateway](src/virons-mcp-gateway/) | 9000 | 90 (aggregated) | [📖 Docs](src/virons-mcp-gateway/README.md) | ✅ |
| [Infrastructure](src/virons-infrastructure-mcp-server/) | 9100 | 78 | [📖 Docs](src/virons-infrastructure-mcp-server/README.md) | ✅ |
| [Security](src/virons-security-mcp-server/) | 9500 | 4 | [📖 Docs](src/virons-security-mcp-server/README.md) | ✅ |
| [Operations](src/virons-operations-mcp-server/) | 9510 | 4 | [📖 Docs](src/virons-operations-mcp-server/README.md) | ✅ |
| [Monitoring](src/virons-monitoring-mcp-server/) | 9520 | 4 | [📖 Docs](src/virons-monitoring-mcp-server/README.md) | ✅ |

### Service Features

Each service follows DDD architecture with complete documentation:
- **Application Layer** - Use cases and orchestration
- **Domain Layer** - Business logic and entities  
- **Infrastructure Layer** - External integrations
- **Tests** - Comprehensive test suites
- **Scripts** - Development and operations tools

## Architecture

All MCP servers follow the [gateway pattern](docs/architecture/mcp-server-standard.md):
- Correlation ID middleware for distributed tracing
- Prometheus metrics on `/metrics`
- Health checks on `/health` and `/ready`
- Tool discovery on `/tools`

### Development Tools

- **[Git Hooks](scripts/hooks/)** - Pre-push validation (DDD, TDD, docs, compliance)
- **[Verification Scripts](scripts/)** - Documentation and code quality checks
- **[Testing Tools](scripts/test-examples.sh)** - Automated example testing

Install hooks: `./scripts/install-hooks.sh`

## Testing

```bash
# Run all tests
pytest

# Test documentation examples
./scripts/test-examples.sh

# Verify documentation quality
./scripts/verify-docs.sh

# Run pre-push validation
.git/hooks/pre-push
```

## License

Apache-2.0
