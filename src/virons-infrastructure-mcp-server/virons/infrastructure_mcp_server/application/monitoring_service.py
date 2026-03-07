# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D107, D102
"""Monitoring and observability service."""

from typing import Any, Dict

from ..domain.upstream_registry import UpstreamRegistry


class MonitoringService:
    """Service for monitoring and observability."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def get_health_status(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """Get health status."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_health", {"stack_name": stack_name})

    async def get_metrics(self, tool: str, stack_name: str, metric_name: str) -> Dict[str, Any]:
        """Get metrics."""
        client = await self.registry.get_client(tool)
        return await client.call_tool(
            "get_metrics", {"stack_name": stack_name, "metric_name": metric_name}
        )

    async def get_alarms(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """Get alarms."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("list_alarms", {"stack_name": stack_name})
