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

"""MCP client for communicating with upstream MCP servers."""

import asyncio
from loguru import logger
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Any, Dict, List, Optional


class MCPConnectionError(Exception):
    """Raised when connection to upstream MCP server fails."""

    pass


class MCPTransientError(Exception):
    """Raised when a transient error occurs that can be retried."""

    pass


class MCPClient:
    """Client for communicating with upstream MCP servers via subprocess STDIO."""

    def __init__(
        self,
        command: str,
        args: list[str],
        server_name: str,
        max_retries: int = 3,
    ):
        """Initialize MCP client.

        Args:
            command: Command to execute (e.g., '/app/.venv/bin/python')
            args: Command arguments (e.g., ['-m', 'module.server'])
            server_name: Name of the upstream server
            max_retries: Maximum number of retries for transient errors
        """
        self.command = command
        self.args = args
        self.server_name = server_name
        self.max_retries = max_retries
        self._session: Optional[ClientSession] = None
        self._stdio_context = None
        self._connected = False

    async def connect(self) -> None:
        """Establish connection to upstream MCP server via subprocess."""
        try:
            server_params = StdioServerParameters(command=self.command, args=self.args, env=None)

            # Store context manager for proper cleanup
            self._stdio_context = stdio_client(server_params)
            read, write = await self._stdio_context.__aenter__()

            self._session = ClientSession(read, write)
            await self._session.__aenter__()
            await self._session.initialize()

            self._connected = True
            logger.info(f'Connected to upstream MCP server: {self.server_name}')
        except Exception as e:
            logger.error(f'Failed to connect to {self.server_name}: {e}')
            raise MCPConnectionError(f'Connection failed: {e}')

    async def disconnect(self) -> None:
        """Close connection to upstream MCP server."""
        if self._session:
            try:
                await self._session.__aexit__(None, None, None)
            except Exception as e:
                logger.warning(f'Error closing session: {e}')

        if self._stdio_context:
            try:
                await self._stdio_context.__aexit__(None, None, None)
            except Exception as e:
                logger.warning(f'Error closing stdio context: {e}')

        self._connected = False
        logger.info(f'Disconnected from upstream MCP server: {self.server_name}')

    def is_connected(self) -> bool:
        """Check if client is connected to upstream server."""
        return self._connected

    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from upstream server."""
        if not self._connected:
            raise MCPConnectionError('Not connected to upstream server')

        try:
            result = await self._session.list_tools()
            return [{'name': tool.name, 'description': tool.description} for tool in result.tools]
        except Exception as e:
            logger.error(f'Failed to list tools from {self.server_name}: {e}')
            raise

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the upstream server with retry logic."""
        if not self._connected:
            raise MCPConnectionError('Not connected to upstream server')

        for attempt in range(self.max_retries):
            try:
                result = await self._send_request(tool_name, arguments)
                return result
            except MCPTransientError as e:
                if attempt < self.max_retries - 1:
                    wait_time = 2**attempt
                    logger.warning(f'Transient error, retrying in {wait_time}s: {e}')
                    await asyncio.sleep(wait_time)
                else:
                    raise

        raise MCPConnectionError(f'Failed after {self.max_retries} retries')

    async def _send_request(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Send request to upstream server."""
        try:
            result = await self._session.call_tool(tool_name, arguments)

            # result.content is a list of content items
            if result.content:
                # Extract text from first content item
                first_content = result.content[0]
                if hasattr(first_content, 'text'):
                    return {'result': first_content.text}
                else:
                    return {'result': str(first_content)}

            return {'result': None}
        except Exception as e:
            logger.error(f'Request failed for {tool_name}: {e}')
            raise MCPTransientError(str(e))
