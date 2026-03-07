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
