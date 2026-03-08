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

"""MCP client for connecting to backend MCP servers via stdio."""

from typing import Any

from loguru import logger
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPBackendClient:
    """Manages stdio connection to a backend MCP server."""

    def __init__(self, name: str, command: str, args: list[str] | None = None):
        """Initialize MCP backend client.

        Args:
            name: Backend service name
            command: Command to launch the MCP server
            args: Command arguments
        """
        self.name = name
        self.command = command
        self.args = args or []
        self._session: ClientSession | None = None
        self._context_manager = None

    async def connect(self) -> None:
        """Establish stdio connection to backend server."""
        if self._session:
            return

        server_params = StdioServerParameters(
            command=self.command,
            args=self.args,
        )

        self._context_manager = stdio_client(server_params)
        read, write = await self._context_manager.__aenter__()

        self._session = ClientSession(read, write)
        await self._session.__aenter__()
        await self._session.initialize()

        logger.info(f"Connected to backend MCP server: {self.name}")

    async def disconnect(self) -> None:
        """Close connection to backend server."""
        if self._session:
            await self._session.__aexit__(None, None, None)
            self._session = None

        if self._context_manager:
            await self._context_manager.__aexit__(None, None, None)
            self._context_manager = None

        logger.info(f"Disconnected from backend MCP server: {self.name}")

    async def list_tools(self) -> list[dict[str, Any]]:
        """Discover tools from backend server.

        Returns:
            List of tool definitions with name, description, and inputSchema
        """
        if not self._session:
            await self.connect()

        result = await self._session.list_tools()

        tools = []
        for tool in result.tools:
            tools.append(
                {
                    "name": tool.name,
                    "description": tool.description or "",
                    "inputSchema": tool.inputSchema,
                }
            )

        logger.debug(f"Discovered {len(tools)} tools from {self.name}")
        return tools

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Execute tool on backend server.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        if not self._session:
            await self.connect()

        result = await self._session.call_tool(tool_name, arguments=arguments)
        return result
