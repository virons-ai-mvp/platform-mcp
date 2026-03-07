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


class ServiceRegistry:
    """Maps tool names to MCP backend services."""

    def __init__(self) -> None:
        self._services: dict[str, MCPService] = {}
        self._tool_map: dict[str, str] = {}

    def register(self, service: MCPService) -> None:
        """Register a service and its tools."""
        self._services[service.name] = service
        for tool in service.tools:
            self._tool_map[tool] = service.name

    def find_by_tool(self, tool_name: str) -> MCPService | None:
        """Find service by tool name."""
        svc_name = self._tool_map.get(tool_name)
        return self._services.get(svc_name) if svc_name else None

    def list_all(self) -> list[MCPService]:
        """List all registered services."""
        return list(self._services.values())

    def list_tools(self) -> list[dict[str, str]]:
        """List all tools with service mapping."""
        return [{"name": tool, "service": svc} for tool, svc in self._tool_map.items()]
