# Security MCP Server - Operations Scripts

## Overview

Scripts for deployment and operational tasks.

## Scripts

**healthcheck.sh** - Health check for monitoring
```bash
#!/bin/bash
HOST=${1:-localhost}
PORT=${2:-9500}

# Check liveness
if ! curl -sf "http://${HOST}:${PORT}/health" > /dev/null; then
  echo "ERROR: Liveness check failed"
  exit 1
fi

# Check readiness
if ! curl -sf "http://${HOST}:${PORT}/ready" > /dev/null; then
  echo "ERROR: Readiness check failed"
  exit 1
fi

echo "OK: Service is healthy"
exit 0
```

**deploy.sh** - Deploy to environment
```bash
#!/bin/bash
ENV=${1:-dev}
echo "Deploying security-mcp to $ENV..."
docker-compose -f docker-compose.$ENV.yml up -d virons-security-mcp
```

## Usage

```bash
# Health check
./scripts/operations/healthcheck.sh

# Deploy
./scripts/operations/deploy.sh prod
```

## Navigation

← [Scripts](../)
