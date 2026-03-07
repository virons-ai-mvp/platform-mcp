# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D107, D102
"""Resource management service."""

from typing import Any, Dict

from ..domain.upstream_registry import UpstreamRegistry


class ResourceService:
    """Service for resource management."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def list_resources(self, tool: str) -> Dict[str, Any]:
        """List all resources."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("list_all_resources", {})

    async def tag_resource(
        self, tool: str, resource_id: str, tags: Dict[str, str]
    ) -> Dict[str, Any]:
        """Tag resource."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("tag_resource", {"resource_id": resource_id, "tags": tags})
