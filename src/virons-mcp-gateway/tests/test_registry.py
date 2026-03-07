# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for service registry."""

from virons.mcp_gateway.domain.registry import MCPService, ServiceRegistry


class TestServiceRegistry:
    """Test service registry functionality."""

    def test_register_service(self):
        """Test registering a service."""
        registry = ServiceRegistry()
        service = MCPService(
            name="infrastructure-mcp",
            url="http://localhost:9100",
            tools=["terraform_validate", "kubectl_apply"],
        )
        registry.register(service)
        assert len(registry.list_all()) == 1

    def test_find_by_tool(self):
        """Test finding service by tool name."""
        registry = ServiceRegistry()
        service = MCPService(
            name="infrastructure-mcp",
            url="http://localhost:9100",
            tools=["terraform_validate"],
        )
        registry.register(service)
        found = registry.find_by_tool("terraform_validate")
        assert found is not None
        assert found.name == "infrastructure-mcp"

    def test_find_by_tool_not_found(self):
        """Test finding non-existent tool returns None."""
        registry = ServiceRegistry()
        found = registry.find_by_tool("nonexistent_tool")
        assert found is None

    def test_list_all(self):
        """Test listing all services."""
        registry = ServiceRegistry()
        service1 = MCPService(name="infra", url="http://localhost:9100", tools=["tool1"])
        service2 = MCPService(name="security", url="http://localhost:9500", tools=["tool2"])
        registry.register(service1)
        registry.register(service2)
        services = registry.list_all()
        assert len(services) == 2
        assert service1 in services
        assert service2 in services

    def test_list_tools(self):
        """Test listing all tools with service mapping."""
        registry = ServiceRegistry()
        service = MCPService(
            name="infrastructure-mcp",
            url="http://localhost:9100",
            tools=["terraform_validate", "kubectl_apply"],
        )
        registry.register(service)
        tools = registry.list_tools()
        assert len(tools) == 2
        assert {"name": "terraform_validate", "service": "infrastructure-mcp"} in tools
        assert {"name": "kubectl_apply", "service": "infrastructure-mcp"} in tools

    def test_multiple_services_with_tools(self):
        """Test multiple services with different tools."""
        registry = ServiceRegistry()
        infra = MCPService(name="infra", url="http://localhost:9100", tools=["deploy"])
        security = MCPService(name="security", url="http://localhost:9500", tools=["scan"])
        registry.register(infra)
        registry.register(security)

        assert registry.find_by_tool("deploy").name == "infra"
        assert registry.find_by_tool("scan").name == "security"
        assert len(registry.list_tools()) == 2
