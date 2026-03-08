# Enterprise MCP Server Standards

## Dockerfile Requirements

All MCP servers MUST follow these standards for production deployment:

### 1. Multi-Stage Build
```dockerfile
FROM python:3.13-slim AS base
FROM base AS builder
FROM base AS runtime
```
**Why**: Reduces final image size by 60-80%

### 2. Non-Root User
```dockerfile
RUN useradd -m -u 1000 mcp
USER mcp
```
**Why**: Security best practice (BaFin, GDPR compliance)

### 3. Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1
```
**Why**: Kubernetes/Docker orchestration, automatic recovery

### 4. Environment Variables
```dockerfile
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PORT=9000 \
    LOG_LEVEL=INFO \
    AWS_REGION=eu-central-1
```
**Why**: 12-factor app, configuration management

### 5. Minimal Dependencies
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
```
**Why**: Reduces attack surface, faster builds

### 6. Copyright & License
```dockerfile
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
```
**Why**: Legal compliance, open source attribution

## docker-compose.yml Requirements

### 1. Resource Limits
```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 512M
    reservations:
      cpus: '0.25'
      memory: 128M
```
**Why**: Prevent resource exhaustion, cost control

### 2. Health Check
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:9000/health"]
  interval: 30s
  timeout: 3s
  retries: 3
  start_period: 10s
```
**Why**: Automatic recovery, monitoring integration

### 3. Restart Policy
```yaml
restart: unless-stopped
```
**Why**: High availability, automatic recovery

### 4. Networks
```yaml
networks:
  - virons-mcp
```
**Why**: Isolation, security, service discovery

### 5. Volumes (AWS Credentials)
```yaml
volumes:
  - ~/.aws:/root/.aws:ro
```
**Why**: AWS authentication, read-only for security

### 6. Environment Variables
```yaml
environment:
  PORT: 9000
  LOG_LEVEL: INFO
  AWS_REGION: eu-central-1
```
**Why**: Configuration management, 12-factor app

## Logging Standards

### 1. Structured Logging
```python
import structlog
logger = structlog.get_logger()
logger.info("server_started", port=9000, version="1.0.0")
```

### 2. Log Levels
- **ERROR**: System failures, requires immediate action
- **WARN**: Degraded performance, potential issues
- **INFO**: Normal operations, key events
- **DEBUG**: Detailed diagnostics (dev only)

### 3. Correlation IDs
```python
logger.info("request_received", correlation_id=request_id)
```
**Why**: Distributed tracing, audit trail (BaFin)

## Security Standards

### 1. No Hardcoded Secrets
```python
# ❌ BAD
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"

# ✅ GOOD
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
```

### 2. Read-Only Volumes
```yaml
volumes:
  - ~/.aws:/root/.aws:ro  # :ro = read-only
```

### 3. Network Policies
```yaml
networks:
  virons-mcp:
    driver: bridge
    internal: false  # Allow external access via gateway only
```

### 4. Least Privilege IAM
```json
{
  "Effect": "Allow",
  "Action": ["service:SpecificAction"],
  "Resource": "arn:aws:service:eu-central-1:*:resource/*"
}
```

## Monitoring Standards

### 1. Prometheus Metrics
```python
from prometheus_client import Counter, Histogram
requests_total = Counter('mcp_requests_total', 'Total requests')
request_duration = Histogram('mcp_request_duration_seconds', 'Request duration')
```

### 2. Health Endpoint
```python
@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}
```

### 3. Ready Endpoint
```python
@app.get("/ready")
def ready():
    # Check dependencies
    return {"status": "ready", "upstreams": {"db": "ok"}}
```

### 4. Metrics Endpoint
```python
@app.get("/metrics")
def metrics():
    return prometheus_client.generate_latest()
```

## Compliance Standards

### BaFin AT 8.1 (Audit Trail)
- ✅ All requests logged with correlation ID
- ✅ CloudTrail integration for AWS API calls
- ✅ 7-year log retention

### GDPR Art 25/32 (Security)
- ✅ Non-root user
- ✅ Encryption at rest (KMS)
- ✅ Encryption in transit (TLS)
- ✅ No PII in logs

### DORA Art 11 (Resilience)
- ✅ Health checks
- ✅ Automatic restart
- ✅ Resource limits
- ✅ Graceful shutdown

## Testing Standards

### 1. Unit Tests
```python
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### 2. Integration Tests
```python
def test_tool_execution():
    response = client.post("/call_tool", json={
        "name": "list_resources",
        "arguments": {}
    })
    assert response.status_code == 200
```

### 3. Load Tests
```bash
# 100 requests, 10 concurrent
ab -n 100 -c 10 http://localhost:9000/health
```

## Deployment Checklist

- [ ] Dockerfile follows multi-stage build pattern
- [ ] Non-root user configured
- [ ] Health check implemented
- [ ] Resource limits set
- [ ] Environment variables externalized
- [ ] AWS credentials mounted read-only
- [ ] Logging configured (structured, correlation IDs)
- [ ] Metrics endpoint exposed
- [ ] Security scan passed (Trivy, Snyk)
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Documentation updated

## Quick Commands

```bash
# Generate Dockerfiles
./scripts/generate-mcp-dockerfiles.sh

# Build single server
docker build -t virons-<server>-mcp src/awslabs/<server>-mcp-server/

# Test locally
docker run -p 9000:9000 -v ~/.aws:/root/.aws:ro virons-<server>-mcp

# Deploy all
docker-compose -f docker-compose.core.yml up -d

# Check health
curl http://localhost:9000/health

# View logs
docker-compose -f docker-compose.core.yml logs -f <service>

# Security scan
trivy image virons-<server>-mcp
```
