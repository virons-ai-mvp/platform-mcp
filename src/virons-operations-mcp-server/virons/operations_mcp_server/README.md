# Operations MCP Server - Core Implementation

## Overview

Operations orchestration layer coordinating 4 upstream MCP servers for deployment, scaling, and rollback operations.

## Structure

```
operations_mcp_server/
├── application/       # Use cases (future: deployment orchestration)
├── domain/           # Business logic (future: deployment strategies)
├── infrastructure/   # External integrations (future: platform clients)
├── server.py         # FastMCP server (stdio/http/api modes)
├── compliance.py     # Audit logging
├── consts.py         # Constants
├── models.py         # Data models
└── tool_metadata.py  # Tool enrichment with examples
```

## Key Files

**server.py** - Main entry point
- FastMCP server with 4 tools
- API mode: FastAPI + Swagger + /tools endpoint
- Middleware: correlation ID, Prometheus metrics
- Health endpoints: /health, /ready, /metrics

**tool_metadata.py** - Tool enrichment
- Real examples for each tool
- Category: deployment
- Input/output schemas

**compliance.py** - Audit trail
- write_audit() for all write operations
- Deployment history tracking

## Tools

```python
@server.tool()
async def deploy_service(platform: str, service_name: str, image: str, replicas: int = 1)
  # Deploy service to EKS/ECS/Lambda

@server.tool()
async def rollback_deployment(platform: str, service_name: str, version: str = None)
  # Rollback to previous version

@server.tool()
async def scale_service(platform: str, service_name: str, replicas: int)
  # Scale service replicas/concurrency

@server.tool()
async def check_deployment_status(platform: str, service_name: str)
  # Check deployment status and health
```

## Upstreams

```python
UPSTREAM = {
    "eks": {"host": "localhost", "port": 9105},
    "lambda": {"host": "localhost", "port": 9106},
    "ecs": {"host": "localhost", "port": 9107},
    "stepfunctions": {"host": "localhost", "port": 9108},
}
```

## Navigation

← [Operations MCP Server](../..)  
→ [Application Layer](application/)  
→ [Domain Layer](domain/)  
→ [Infrastructure Layer](infrastructure/)
