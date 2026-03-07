# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D107
"""Gateway service for routing to MCP servers."""

from typing import Any, Dict

import httpx
from loguru import logger

from .config import GATEWAY_CONFIG


class GatewayService:
    """Routes requests to appropriate MCP servers."""

    def __init__(self):
        self.servers = GATEWAY_CONFIG
        self.client = httpx.AsyncClient(timeout=30.0)

    async def route_tool(
        self, server: str, tool: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Route tool call to appropriate server."""
        if server not in self.servers:
            return {"error": f"Unknown server: {server}"}

        config = self.servers[server]
        if not config.enabled:
            return {"error": f"Server disabled: {server}"}

        try:
            response = await self.client.post(
                f"{config.url}/tools/{tool}",
                json=arguments,
                timeout=config.timeout,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error routing to {server}: {e}")
            return {"error": str(e)}

    async def list_servers(self) -> Dict[str, Any]:
        """List all configured servers."""
        return {
            "servers": [
                {
                    "name": cfg.name,
                    "url": cfg.url,
                    "enabled": cfg.enabled,
                }
                for cfg in self.servers.values()
            ]
        }

    async def health_check(self, server: str) -> Dict[str, Any]:
        """Check health of a specific server."""
        if server not in self.servers:
            return {"error": f"Unknown server: {server}"}

        config = self.servers[server]
        try:
            response = await self.client.get(f"{config.url}/health", timeout=5.0)
            return {"server": server, "status": "healthy", "code": response.status_code}
        except httpx.HTTPError as e:
            return {"server": server, "status": "unhealthy", "error": str(e)}

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
