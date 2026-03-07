# MCP Gateway - Application Layer

## Overview

Use cases for gateway operations: tool execution, discovery, health checks.

## Structure

```
application/
├── __init__.py
├── tool_executor.py     # Tool execution use case
├── tool_discovery.py    # Tool discovery use case
└── health_checker.py    # Health check aggregation
```

## Responsibilities

- Execute tools on correct backend
- Discover tools from backends
- Aggregate health status
- Handle errors and retries

## Example

```python
class ToolExecutor:
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
    
    async def execute(self, tool_name: str, params: dict, auth: str):
        # 1. Find service for tool
        service = self.registry.get_service_for_tool(tool_name)
        
        # 2. Execute on backend
        result = await self._call_backend(service, tool_name, params, auth)
        
        return result
```

## Navigation

← [Core Implementation](../)
