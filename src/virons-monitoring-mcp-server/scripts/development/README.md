# Monitoring MCP Server - Development Scripts

## Overview

Scripts for local development and testing.

## Scripts

**start-api.sh** - Start API server locally
```bash
#!/bin/bash
cd "$(dirname "$0")/../.."
export PORT=9520
export LOG_LEVEL=DEBUG
python -m virons.monitoring_mcp_server.server --transport api
```

## Navigation

← [Scripts](../)
