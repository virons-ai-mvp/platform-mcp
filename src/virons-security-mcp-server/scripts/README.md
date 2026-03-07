# Security MCP Server - Scripts

## Overview

Operational scripts for security MCP server development and deployment.

## Structure

```
scripts/
├── development/          # Development scripts
│   ├── start-api.sh     # Start API server locally
│   └── run-tests.sh     # Run test suite
└── operations/          # Operations scripts
    ├── healthcheck.sh   # Health check script
    └── deploy.sh        # Deployment script
```

## Development Scripts

**start-api.sh** - Start API server
```bash
./scripts/development/start-api.sh
# Starts on http://localhost:9500
# Swagger UI: http://localhost:9500/docs
```

**run-tests.sh** - Run tests
```bash
./scripts/development/run-tests.sh
# Runs pytest with coverage
```

## Operations Scripts

**healthcheck.sh** - Health check
```bash
./scripts/operations/healthcheck.sh
# Checks /health and /ready endpoints
# Exit 0 if healthy, 1 if unhealthy
```

**deploy.sh** - Deploy to environment
```bash
./scripts/operations/deploy.sh [env]
# env: dev, staging, prod
```

## Navigation

← [Security MCP Server](..)
