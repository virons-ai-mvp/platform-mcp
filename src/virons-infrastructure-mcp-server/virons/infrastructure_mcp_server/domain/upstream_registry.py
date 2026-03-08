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

"""Upstream server registry for managing multiple MCP connections."""

from typing import Any, Dict

from loguru import logger

from .mcp_client import MCPClient


class UnknownServerError(Exception):
    """Raised when requesting a client for an unknown server."""

    pass


class UpstreamRegistry:
    """Registry for managing upstream MCP server connections."""

    def __init__(self, config: Dict[str, Dict[str, Any]]):
        """Initialize registry with upstream server configuration.

        Config format:
        {
            "server_name": {
                "command": "python",
                "args": ["-m", "module.name"],
                "description": "Server description"
            }
        }
        """
        self.servers = config
        self._clients: Dict[str, MCPClient] = {}

    async def get_client(self, server_name: str) -> MCPClient:
        """Get or create a connected client for the specified server."""
        if server_name not in self.servers:
            raise UnknownServerError(f"Unknown server: {server_name}")

        if server_name in self._clients:
            return self._clients[server_name]

        config = self.servers[server_name]
        client = MCPClient(
            command=config["command"],
            args=config["args"],
            server_name=server_name,
        )

        await client.connect()
        self._clients[server_name] = client
        logger.info(f"Created and cached client for {server_name}")

        return client

    async def check_health(self) -> Dict[str, Dict[str, Any]]:
        """Check health of all upstream servers."""
        health = {}

        for server_name in self.servers:
            try:
                client = await self.get_client(server_name)
                if client.is_connected():
                    health[server_name] = {"status": "healthy"}
                else:
                    health[server_name] = {"status": "unhealthy", "reason": "not connected"}
            except Exception as e:
                health[server_name] = {"status": "unhealthy", "reason": str(e)}

        return health

    async def close_all(self) -> None:
        """Close all client connections."""
        for client in self._clients.values():
            await client.disconnect()
        self._clients.clear()
        logger.info("Closed all upstream connections")
