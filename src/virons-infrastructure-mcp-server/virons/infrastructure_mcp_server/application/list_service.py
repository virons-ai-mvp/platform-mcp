# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D107
"""List service for infrastructure orchestration."""

from typing import Any, Dict

from loguru import logger

from ..domain.upstream_registry import UpstreamRegistry


class ListService:
    """Service for listing infrastructure stacks."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def list_stacks(self, tool: str) -> Dict[str, Any]:
        """List stacks from upstream server."""
        try:
            client = await self.registry.get_client(tool)
            result = await client.call_tool("list_stacks", {})

            logger.info(f"Listed stacks from {tool}")

            return {"tool": tool, "stacks": result.get("stacks", [])}

        except Exception as e:
            logger.error(f"Failed to list stacks from {tool}: {e}")
            raise
