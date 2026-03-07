# Monitoring MCP Server - Operations Scripts

## Overview

Scripts for deployment and operational tasks.

## Scripts

**healthcheck.sh** - Health check for monitoring
```bash
#!/bin/bash
HOST=${1:-localhost}
PORT=${2:-9520}

if ! curl -sf "http://${HOST}:${PORT}/health" > /dev/null; then
  echo "ERROR: Liveness check failed"
  exit 1
fi

echo "OK: Service is healthy"
exit 0
```

## Navigation

← [Scripts](../)
