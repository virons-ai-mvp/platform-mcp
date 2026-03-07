# MCP Gateway - Core Implementation

## Overview

Gateway implementation coordinating 4 backend MCP servers and providing unified API.

## Structure

```
mcp_gateway/
├── application/       # Use cases (tool execution, discovery)
├── domain/           # Business logic (gateway router, registry)
├── infrastructure/   # External integrations (config, metrics)
├── server.py         # FastAPI server with middleware
├── config.py         # Configuration
└── consts.py         # Constants
```

## Key Components

**server.py** - Main entry point
- FastAPI server with middleware stack
- Rate limiting (100 req/60s per IP)
- Correlation ID propagation
- Prometheus metrics collection
- Tool execution routing

**domain/gateway.py** - GatewayRouter
- Routes tool execution to correct backend
- Handles tool not found errors
- Aggregates health checks

**domain/registry.py** - ServiceRegistry
- Discovers tools from backends on startup
- Maintains tool-to-service mapping
- Lists all available tools

**infrastructure/config.py** - Configuration
- Loads services.json
- Backend service definitions

**infrastructure/metrics.py** - Metrics
- Prometheus metrics (requests, duration)
- Custom metrics registry

## Middleware Stack

```python
1. rate_limit_middleware - Rate limiting per IP
2. correlation_id - x-correlation-id header
3. metrics_middleware - Prometheus metrics
```

## Tool Discovery

```python
@app.on_event("startup")
async def discover_tools():
    # Wait for backends to be ready
    await asyncio.sleep(2)
    
    # Discover from each backend
    for service in config.services:
        await registry.discover_tools(service.name, service.url, client)
```

## Navigation

← [MCP Gateway](../..)  
→ [Application Layer](application/)  
→ [Domain Layer](domain/)  
→ [Infrastructure Layer](infrastructure/)
