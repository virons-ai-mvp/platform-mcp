# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Service registry — tool-to-service routing."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MCPService:
    """MCP service definition."""

    name: str
    url: str
    tools: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ToolMetadata:
    """Comprehensive tool metadata for agent decision-making."""

    name: str
    service: str
    description: str
    input_schema: dict
    category: str = ""
    examples: list[dict] = field(default_factory=list)


class ServiceRegistry:
    """Maps tool names to MCP backend services with full metadata."""

    def __init__(self) -> None:
        self._services: dict[str, MCPService] = {}
        self._tool_map: dict[str, str] = {}
        self._tool_metadata: dict[str, ToolMetadata] = {}

    def register(self, service: MCPService) -> None:
        """Register a service and its tools."""
        self._services[service.name] = service
        for tool in service.tools:
            self._tool_map[tool] = service.name

    async def discover_tools(self, service_name: str, service_url: str, client) -> None:
        """Discover tools with full metadata from service /tools endpoint."""
        try:
            resp = await client.get(f"{service_url}/tools", timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                tools_data = data.get("tools", [])
                
                # Extract tool names for registration
                tool_names = [t["name"] for t in tools_data]
                self.register(MCPService(name=service_name, url=service_url, tools=tool_names))
                
                # Store full metadata for each tool
                for tool in tools_data:
                    # Use backend-provided metadata if available, otherwise generate
                    category = tool.get("category") or self._categorize_tool(tool["name"])
                    examples = tool.get("examples") or self._generate_examples(tool)
                    
                    self._tool_metadata[tool["name"]] = ToolMetadata(
                        name=tool["name"],
                        service=service_name,
                        description=tool.get("description", ""),
                        input_schema=tool.get("inputSchema", {}),
                        category=category,
                        examples=examples,
                    )
        except Exception as e:
            # Log error but don't fail - register empty service
            import sys
            print(f"Error discovering tools from {service_name}: {e}", file=sys.stderr)
            self.register(MCPService(name=service_name, url=service_url, tools=[]))

    def _categorize_tool(self, tool_name: str) -> str:
        """Categorize tool based on name patterns (DDD: domain classification)."""
        if any(x in tool_name for x in ["deploy", "destroy", "update", "create"]):
            return "deployment"
        elif any(x in tool_name for x in ["scan", "security", "audit", "compliance"]):
            return "security"
        elif any(x in tool_name for x in ["monitor", "metrics", "health", "logs"]):
            return "monitoring"
        elif any(x in tool_name for x in ["backup", "restore", "snapshot"]):
            return "backup"
        elif any(x in tool_name for x in ["cost", "budget", "billing"]):
            return "cost"
        elif any(x in tool_name for x in ["list", "get", "describe", "info"]):
            return "query"
        return "general"

    def _generate_examples(self, tool: dict) -> list[dict]:
        """Generate usage examples from schema (DDD: documentation pattern)."""
        schema = tool.get("inputSchema", {})
        props = schema.get("properties", {})
        required = schema.get("required", [])
        
        if not props:
            return []
        
        # Generate minimal example with required fields
        example = {}
        for field in required:
            if field in props:
                field_type = props[field].get("type", "string")
                example[field] = self._example_value(field, field_type)
        
        return [{"description": "Basic usage", "parameters": example}] if example else []

    def _example_value(self, field_name: str, field_type: str) -> any:
        """Generate example value based on field name and type."""
        if field_type == "boolean":
            return True if "confirm" in field_name else False
        elif field_type == "integer":
            return 30 if "days" in field_name else 1
        elif field_type == "number":
            return 100.0
        elif "name" in field_name:
            return f"example-{field_name.replace('_', '-')}"
        elif "path" in field_name:
            return "/path/to/resource"
        elif "id" in field_name:
            return "resource-id-123"
        return "example-value"

    def find_by_tool(self, tool_name: str) -> MCPService | None:
        """Find service by tool name."""
        svc_name = self._tool_map.get(tool_name)
        return self._services.get(svc_name) if svc_name else None

    def list_all(self) -> list[MCPService]:
        """List all registered services."""
        return list(self._services.values())

    def list_tools(self) -> list[dict]:
        """List all tools with comprehensive metadata for agent decision-making."""
        return [
            {
                "name": meta.name,
                "service": meta.service,
                "description": meta.description,
                "category": meta.category,
                "input_schema": meta.input_schema,
                "examples": meta.examples,
            }
            for meta in self._tool_metadata.values()
        ]
