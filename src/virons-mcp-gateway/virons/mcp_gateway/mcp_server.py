# Copyright Virons Fintech. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""FastMCP gateway server that aggregates backend MCP servers."""

from contextlib import asynccontextmanager
from typing import Any

from loguru import logger
from mcp.server.fastmcp import Context, FastMCP

from .infrastructure.mcp_client import MCPBackendClient


class MCPGateway:
    """MCP Gateway that aggregates tools from backend MCP servers."""

    def __init__(self, backend_configs: dict[str, dict[str, Any]]):
        """Initialize MCP gateway.

        Args:
            backend_configs: Dict mapping service name to config with 'command' and 'args'
        """
        self.backends: dict[str, MCPBackendClient] = {}
        self.tool_to_backend: dict[str, str] = {}
        self.backend_configs = backend_configs
        self._initialized = False

        # Create lifespan context manager for initialization
        @asynccontextmanager
        async def lifespan(server: FastMCP):
            # Initialize backends synchronously during startup
            await self._initialize_backends()
            yield
            # Cleanup on shutdown
            await self.cleanup()

        self.mcp = FastMCP(
            "Virons MCP Gateway",
            instructions="""
Gateway aggregating 90+ tools from infrastructure, security, operations, and monitoring MCP servers.
Provides unified access to AWS CDK, CloudFormation, Terraform, IAM, CloudTrail, and monitoring tools.
""",
            lifespan=lifespan,
        )

        # Register a simple info tool that works immediately
        @self.mcp.tool()
        def gateway_info() -> str:
            """Get information about the MCP gateway."""
            status = "ready" if self._initialized else "initializing"
            return f"Virons MCP Gateway ({status}) - {len(self.tool_to_backend)} tools from {len(self.backends)} backends"

    async def _initialize_backends(self) -> None:
        """Initialize backends - connect and discover tools."""
        if self._initialized:
            return

        logger.info("Initializing backends...")

        for name, config in self.backend_configs.items():
            client = MCPBackendClient(
                name=name,
                command=config["command"],
                args=config.get("args", []),
            )

            try:
                await client.connect()
                tools = await client.list_tools()

                self.backends[name] = client

                # Register each tool
                for tool in tools:
                    tool_name = tool["name"]
                    self.tool_to_backend[tool_name] = name

                    # Register tool with FastMCP
                    self._register_tool(tool_name, tool["description"], tool["inputSchema"])

                logger.info(f"Registered {len(tools)} tools from {name}")
            except Exception as e:
                logger.error(f"Failed to connect to {name}: {e}")

        self._initialized = True
        logger.info(
            f"Gateway initialized with {len(self.tool_to_backend)} tools from {len(self.backends)} backends"
        )

    def _register_tool(self, name: str, description: str, input_schema: dict) -> None:
        """Register a tool with FastMCP that proxies to backend."""

        # Create a closure that captures the tool name
        async def tool_handler(ctx: Context, **kwargs) -> Any:
            backend_name = self.tool_to_backend.get(name)
            if not backend_name:
                raise ValueError(f"Tool {name} not found in registry")

            backend = self.backends.get(backend_name)
            if not backend:
                raise ValueError(f"Backend {backend_name} not available")

            try:
                result = await backend.call_tool(name, kwargs)

                # Return the result content
                if hasattr(result, "content") and result.content:
                    # If there's text content, return it
                    for content in result.content:
                        if hasattr(content, "text"):
                            return content.text
                    # Otherwise return the first content item
                    return str(result.content[0])

                return result
            except Exception as e:
                logger.error(f"Error calling tool {name} on {backend_name}: {e}")
                raise

        # Set function metadata
        tool_handler.__name__ = name
        tool_handler.__doc__ = description

        # Register with FastMCP
        self.mcp.tool()(tool_handler)

    async def cleanup(self) -> None:
        """Disconnect from all backend servers."""
        for client in self.backends.values():
            await client.disconnect()

    def run(self, transport: str = "stdio") -> None:
        """Run the MCP gateway server.

        Args:
            transport: Transport type ('stdio' or 'sse')
        """
        self.mcp.run(transport=transport)
