# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""MCP client for communicating with upstream MCP servers."""

import asyncio
from typing import Any, Dict, List, Optional

from loguru import logger
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPConnectionError(Exception):
    """Raised when connection to upstream MCP server fails."""

    pass


class MCPTransientError(Exception):
    """Raised when a transient error occurs that can be retried."""

    pass


class MCPClient:
    """Client for communicating with upstream MCP servers."""

    def __init__(
        self,
        host: str,
        port: int,
        transport: str = "stdio",
        max_retries: int = 3,
        server_name: Optional[str] = None,
    ):
        self.host = host
        self.port = port
        self.transport = transport
        self.max_retries = max_retries
        self.server_name = server_name or f"{host}:{port}"
        self._session: Optional[ClientSession] = None
        self._connected = False

    async def connect(self) -> None:
        """Establish connection to upstream MCP server."""
        try:
            if self.transport == "stdio":
                server_params = StdioServerParameters(
                    command="python", args=["-m", "mcp.server.stdio"], env=None
                )

                read, write = await stdio_client(server_params)
                self._session = ClientSession(read, write)
                await self._session.__aenter__()
                self._connected = True
                logger.info(f"Connected to upstream MCP server: {self.server_name}")
            else:
                raise NotImplementedError(f"Transport {self.transport} not yet implemented")
        except Exception as e:
            logger.error(f"Failed to connect to {self.server_name}: {e}")
            raise MCPConnectionError(f"Connection failed: {e}")

    async def disconnect(self) -> None:
        """Close connection to upstream MCP server."""
        if self._session:
            await self._session.__aexit__(None, None, None)
            self._connected = False
            logger.info(f"Disconnected from upstream MCP server: {self.server_name}")

    def is_connected(self) -> bool:
        """Check if client is connected to upstream server."""
        return self._connected

    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from upstream server."""
        if not self._connected:
            raise MCPConnectionError("Not connected to upstream server")

        try:
            result = await self._session.list_tools()
            return [{"name": tool.name, "description": tool.description} for tool in result.tools]
        except Exception as e:
            logger.error(f"Failed to list tools from {self.server_name}: {e}")
            raise

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the upstream server with retry logic."""
        if not self._connected:
            raise MCPConnectionError("Not connected to upstream server")

        for attempt in range(self.max_retries):
            try:
                result = await self._send_request(tool_name, arguments)
                return result
            except MCPTransientError as e:
                if attempt < self.max_retries - 1:
                    wait_time = 2**attempt
                    logger.warning(f"Transient error, retrying in {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)
                else:
                    raise

        raise MCPConnectionError(f"Failed after {self.max_retries} retries")

    async def _send_request(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Send request to upstream server."""
        try:
            result = await self._session.call_tool(tool_name, arguments)
            return {"content": result.content}
        except Exception as e:
            logger.error(f"Request failed for {tool_name}: {e}")
            raise MCPTransientError(str(e))
