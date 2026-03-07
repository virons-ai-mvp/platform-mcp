# Operations MCP Server - Development Scripts

## Overview

Scripts for local development and testing.

## Scripts

**start-api.sh** - Start API server locally
```bash
#!/bin/bash
cd "$(dirname "$0")/../.."
export PORT=9510
export LOG_LEVEL=DEBUG
python -m virons.operations_mcp_server.server --transport api
```

**run-tests.sh** - Run test suite with coverage
```bash
#!/bin/bash
cd "$(dirname "$0")/../.."
pytest tests/ -v --cov=virons.operations_mcp_server --cov-report=html --cov-report=term
echo "Coverage report: htmlcov/index.html"
```

## Usage

```bash
# Start server
./scripts/development/start-api.sh

# Run tests
./scripts/development/run-tests.sh
```

## Navigation

← [Scripts](../)
