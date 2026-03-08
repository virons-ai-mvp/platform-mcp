# MCP Gateway - Domain Layer

## Overview

Business logic for gateway: routing, registry, tool management.

## Structure

```
domain/
├── __init__.py
├── gateway.py          # GatewayRouter - routes tool execution
└── registry.py         # ServiceRegistry - tool discovery & mapping
```

## Key Classes

**GatewayRouter** - Routes tool execution
```python
class GatewayRouter:
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
    
    async def execute_tool(self, tool_name: str, params: dict, auth: str):
        service = self.registry.get_service_for_tool(tool_name)
        if not service:
            raise ToolNotFoundError(tool_name)
        return await self._execute_on_backend(service, tool_name, params, auth)
```

**ServiceRegistry** - Maintains tool-to-service mapping
```python
class ServiceRegistry:
    def __init__(self):
        self._tool_metadata = {}
    
    async def discover_tools(self, service_name: str, url: str, client):
        response = await client.get(f"{url}/tools")
        tools = response.json()["tools"]
        for tool in tools:
            self._tool_metadata[tool["name"]] = service_name
```

## Navigation

← [Core Implementation](../)
