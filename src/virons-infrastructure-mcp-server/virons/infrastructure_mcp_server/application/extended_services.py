# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D107, D102
"""Extended backup, cost, monitoring, and resource services."""

from typing import Any, Dict

from ..domain.upstream_registry import UpstreamRegistry


class ExtendedBackupService:
    """Extended backup service."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def restore_backup(self, tool: str, stack_name: str, backup_id: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool(
            "restore_backup", {"stack_name": stack_name, "backup_id": backup_id}
        )

    async def delete_backup(self, tool: str, backup_id: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("delete_backup", {"backup_id": backup_id})

    async def test_recovery(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("test_recovery", {"stack_name": stack_name})


class ExtendedCostService:
    """Extended cost service."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def get_cost_forecast(self, tool: str, stack_name: str, days: int) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool(
            "get_cost_forecast", {"stack_name": stack_name, "days": days}
        )

    async def get_cost_anomalies(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_cost_anomalies", {"stack_name": stack_name})

    async def optimize_costs(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("optimize_costs", {"stack_name": stack_name})

    async def set_budget(
        self, tool: str, stack_name: str, amount: float, currency: str
    ) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool(
            "set_budget", {"stack_name": stack_name, "amount": amount, "currency": currency}
        )

    async def estimate_cost(self, tool: str, template_path: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("estimate_cost", {"template_path": template_path})


class ExtendedMonitoringService:
    """Extended monitoring service."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def create_alarm(
        self, tool: str, stack_name: str, metric: str, threshold: float
    ) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool(
            "create_alarm", {"stack_name": stack_name, "metric": metric, "threshold": threshold}
        )

    async def get_logs(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_logs", {"stack_name": stack_name})

    async def query_logs(self, tool: str, stack_name: str, query: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("query_logs", {"stack_name": stack_name, "query": query})


class ExtendedResourceService:
    """Extended resource service."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def get_resource_info(self, tool: str, resource_id: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_resource_info", {"resource_id": resource_id})

    async def untag_resource(self, tool: str, resource_id: str, tag_keys: list) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool(
            "untag_resource", {"resource_id": resource_id, "tag_keys": tag_keys}
        )

    async def search_resources(
        self, tool: str, tags: Dict[str, str], resource_type: str = None
    ) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool(
            "search_resources", {"tags": tags, "resource_type": resource_type}
        )

    async def get_resource_metrics(
        self, tool: str, resource_id: str, metric_name: str
    ) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool(
            "get_resource_metrics", {"resource_id": resource_id, "metric_name": metric_name}
        )

    async def get_resource_logs(self, tool: str, resource_id: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_resource_logs", {"resource_id": resource_id})

    async def get_resource_cost(self, tool: str, resource_id: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_resource_cost", {"resource_id": resource_id})
