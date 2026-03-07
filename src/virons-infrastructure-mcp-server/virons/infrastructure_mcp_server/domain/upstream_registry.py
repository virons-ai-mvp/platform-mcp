# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
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
            host=config["host"],
            port=config["port"],
            transport=config.get("transport", "stdio"),
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
