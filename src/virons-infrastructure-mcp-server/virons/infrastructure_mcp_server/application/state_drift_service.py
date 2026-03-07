# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D107, D102
"""State and drift management services."""

from typing import Any, Dict

from ..domain.upstream_registry import UpstreamRegistry


class StateService:
    """Service for state management."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def get_state(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_state", {"stack_name": stack_name})

    async def lock_state(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("lock_state", {"stack_name": stack_name})

    async def unlock_state(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("unlock_state", {"stack_name": stack_name})

    async def backup_state(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("backup_state", {"stack_name": stack_name})

    async def restore_state(self, tool: str, stack_name: str, backup_id: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool(
            "restore_state", {"stack_name": stack_name, "backup_id": backup_id}
        )


class DriftService:
    """Service for drift detection and remediation."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def get_drift_status(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_drift_status", {"stack_name": stack_name})

    async def get_drift_details(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_drift_details", {"stack_name": stack_name})

    async def remediate_drift(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("remediate_drift", {"stack_name": stack_name})
