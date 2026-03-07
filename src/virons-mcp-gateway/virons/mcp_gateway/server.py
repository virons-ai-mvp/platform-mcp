# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""MCP Gateway Server - Single entry point for all Virons MCP servers."""

from loguru import logger
from mcp.server.fastmcp import FastMCP

from .application.gateway_service import GatewayService


def create_server() -> FastMCP:
    """Create and configure the MCP gateway server."""
    server = FastMCP("virons-mcp-gateway")
    gateway = GatewayService()

    @server.tool()
    async def route_tool(server_name: str, tool_name: str, **kwargs) -> dict:
        """Route a tool call to the appropriate MCP server.

        Args:
            server_name: Target server (infrastructure, security, operations, monitoring)
            tool_name: Tool to execute on the target server
            **kwargs: Tool arguments
        """
        return await gateway.route_tool(server_name, tool_name, kwargs)

    @server.tool()
    async def list_servers() -> dict:
        """List all available MCP servers."""
        return await gateway.list_servers()

    @server.tool()
    async def health_check(server_name: str) -> dict:
        """Check health status of a specific MCP server.

        Args:
            server_name: Server to check (infrastructure, security, operations, monitoring)
        """
        return await gateway.health_check(server_name)

    @server.tool()
    async def infrastructure_deploy(tool: str, **kwargs) -> dict:
        """Deploy infrastructure (routes to infrastructure server)."""
        return await gateway.route_tool("infrastructure", tool, kwargs)

    @server.tool()
    async def security_scan(tool: str, **kwargs) -> dict:
        """Security operations (routes to security server)."""
        return await gateway.route_tool("security", tool, kwargs)

    @server.tool()
    async def operations_execute(tool: str, **kwargs) -> dict:
        """Operations tasks (routes to operations server)."""
        return await gateway.route_tool("operations", tool, kwargs)

    @server.tool()
    async def monitoring_query(tool: str, **kwargs) -> dict:
        """Monitoring queries (routes to monitoring server)."""
        return await gateway.route_tool("monitoring", tool, kwargs)

    logger.info(f"MCP Gateway initialized with {len(server.list_tools())} tools")
    return server


def main():
    """Run the MCP gateway server."""
    server = create_server()
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
