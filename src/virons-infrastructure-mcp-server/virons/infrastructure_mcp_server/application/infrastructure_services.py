# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D107, D102
"""Backup and cost management services."""

from typing import Any, Dict

from ..domain.upstream_registry import UpstreamRegistry


class BackupService:
    """Service for backup management."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def create_backup(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """Create backup."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("create_backup", {"stack_name": stack_name})

    async def list_backups(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """List backups."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("list_backups", {"stack_name": stack_name})


class CostService:
    """Service for cost management."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def get_cost_breakdown(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """Get cost breakdown."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_costs", {"stack_name": stack_name})


class InfrastructureService:
    """Service for infrastructure queries."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def list_vpcs(self, tool: str) -> Dict[str, Any]:
        """List VPCs."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("list_vpcs", {})

    async def list_databases(self, tool: str) -> Dict[str, Any]:
        """List databases."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("list_databases", {})

    async def list_instances(self, tool: str) -> Dict[str, Any]:
        """List instances."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("list_instances", {})
