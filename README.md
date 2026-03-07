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

| Service | Port | Tools | Status |
|---------|------|-------|--------|
| Gateway | 9000 | 90 (aggregated) | ✅ |
| Infrastructure | 9100 | 78 | ✅ |
| Security | 9500 | 4 | ✅ |
| Operations | 9510 | 4 | ✅ |
| Monitoring | 9520 | 4 | ✅ |

## Architecture

All MCP servers follow the [gateway pattern](docs/architecture/mcp-server-standard.md):
- Correlation ID middleware for distributed tracing
- Prometheus metrics on `/metrics`
- Health checks on `/health` and `/ready`
- Tool discovery on `/tools`

## License

Apache-2.0
