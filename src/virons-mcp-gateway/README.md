# Virons MCP Gateway

Production-ready HTTP gateway for all Virons MCP servers with enterprise features.

**Port**: 9000 | **Status**: 🟢 Production Ready | **Compliance**: ✅ Born Compliant

## Features

- ✅ **Circuit Breaker** - 5 failures → 60s timeout per service
- ✅ **Rate Limiting** - 100 requests/60s per IP
- ✅ **Prometheus Metrics** - Request count, duration, status codes
- ✅ **Correlation IDs** - X-Correlation-ID header propagation
- ✅ **Authorization** - Bearer token validation
- ✅ **Service Registry** - Dynamic JSON-based configuration
- ✅ **Health Checks** - Aggregated backend health status
- ✅ **Swagger UI** - Interactive API documentation at `/docs`

## Quick Start

```bash
# HTTP mode (production)
uv run virons-mcp-gateway --transport http --port 9000

# MCP stdio mode (development)
uv run virons-mcp-gateway --transport stdio
```

## API Endpoints

### Tool Execution
```bash
POST /tools/{tool_name}
Authorization: Bearer <token>
Content-Type: application/json

{
  "param1": "value1",
  "param2": "value2"
}
```

### List Tools
```bash
GET /tools

Response:
{
  "tools": [
    {"name": "terraform_validate", "service": "infrastructure-mcp"},
    {"name": "scan_security", "service": "security-mcp"}
  ]
}
```

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "gateway": "virons-mcp-gateway",
  "services": [
    {"name": "infrastructure-mcp", "status": "healthy", "url": "http://localhost:9100"},
    {"name": "security-mcp", "status": "healthy", "url": "http://localhost:9500"}
  ],
  "version": "1.0.0"
}
```

### Readiness Check
```bash
GET /ready

Response (200 if ready, 503 if not):
{
  "ready": true,
  "services": [...]
}
```

### Prometheus Metrics
```bash
GET /metrics

Response (text/plain):
http_requests_total{method="GET",endpoint="/health",status="200"} 42.0
http_request_duration_seconds_bucket{method="GET",endpoint="/health",le="0.005"} 40.0
```

### Documentation
- **Swagger UI**: http://localhost:9000/docs
- **ReDoc**: http://localhost:9000/redoc
- **OpenAPI Schema**: http://localhost:9000/openapi.json

## Configuration

Service registry is configured via `virons/mcp_gateway/config/services.json`:

```json
{
  "services": [
    {
      "name": "infrastructure-mcp",
      "url": "${INFRASTRUCTURE_MCP_URL:http://localhost:9100}",
      "tools": ["terraform_validate", "kubectl_apply"]
    }
  ]
}
```

Environment variables override defaults:
```bash
export INFRASTRUCTURE_MCP_URL=http://production:9100
export SECURITY_MCP_URL=http://production:9500
```

## Docker Deployment

```bash
# Build and run all services
docker-compose up -d

# Check health
curl http://localhost:9000/health

# View logs
docker logs virons-mcp-gateway

# Stop
docker-compose down
```

## Architecture

```
virons-mcp-gateway/
├── virons/mcp_gateway/
│   ├── server.py              # FastAPI app + MCP server
│   ├── domain/
│   │   ├── gateway.py         # GatewayRouter with circuit breaker
│   │   └── registry.py        # ServiceRegistry
│   ├── infrastructure/
│   │   ├── config.py          # JSON config loader
│   │   └── metrics.py         # Prometheus metrics
│   └── config/
│       └── services.json      # Service registry
└── tests/                     # 48 comprehensive tests
```

## Middleware

### Rate Limiting
- **Limit**: 100 requests per 60 seconds per IP
- **Response**: 429 Too Many Requests
- **Headers**: None (transparent)

### Correlation IDs
- **Header**: X-Correlation-ID
- **Behavior**: Generated if not provided, propagated in response
- **Format**: UUID v4

### Metrics
- **Counter**: `http_requests_total{method, endpoint, status}`
- **Histogram**: `http_request_duration_seconds{method, endpoint}`
- **Export**: `/metrics` endpoint (Prometheus format)

## Circuit Breaker

Per-service circuit breaker prevents cascading failures:

- **Threshold**: 5 consecutive failures
- **Timeout**: 60 seconds
- **Behavior**: Returns 503 when open, auto-recovers after timeout

## Compliance

| Regulation | Implementation |
|---|---|
| **BaFin MaRisk AT 8.1** | Audit trail via virons.common |
| **GDPR Art 25, 32** | Data residency (eu-central-1), correlation IDs |
| **DORA Art 11** | Health checks, circuit breaker |

## Development

### Running Tests
```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=virons.mcp_gateway --cov-report=term-missing

# Specific test
uv run pytest tests/test_server.py -v
```

### Code Quality
```bash
# Linting
uv run ruff check .

# Type checking
uv run pyright

# Format
uv run ruff format .
```

## Monitoring

### Health Monitoring
```bash
# Liveness (gateway itself)
curl http://localhost:9000/health

# Readiness (gateway + all backends)
curl http://localhost:9000/ready
```

### Metrics Collection
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'virons-mcp-gateway'
    static_configs:
      - targets: ['localhost:9000']
    metrics_path: '/metrics'
```

## Troubleshooting

### Circuit Breaker Open
```bash
# Check which service is failing
curl http://localhost:9000/health | jq '.services[] | select(.status=="unhealthy")'

# Wait 60s for auto-recovery or fix backend
```

### Rate Limited
```bash
# Response: {"error": "Too many requests"}
# Solution: Wait 60s or increase rate_limit in create_app()
```

### Backend Unreachable
```bash
# Check backend health directly
curl http://localhost:9100/health

# Check docker network
docker network inspect platform-mcp_virons-mcp
```

## License

Apache-2.0 — See [LICENSE](../../LICENSE)

Copyright 2026 Virons Fintech. All Rights Reserved.
