# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D107, D102
"""Stack info service."""

from typing import Any, Dict

from ..domain.upstream_registry import UpstreamRegistry


class StackInfoService:
    """Service for retrieving stack information."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def get_stack_info(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """Get detailed stack information."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("describe_stack", {"stack_name": stack_name})

    async def get_stack_outputs(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """Get stack outputs."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_outputs", {"stack_name": stack_name})

    async def get_stack_resources(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """Get stack resources."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("list_resources", {"stack_name": stack_name})

    async def get_stack_events(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """Get stack events."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_events", {"stack_name": stack_name})

    async def validate_template(self, tool: str, template_path: str) -> Dict[str, Any]:
        """Validate template."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("validate_template", {"template_path": template_path})

    async def update_stack(
        self, tool: str, stack_name: str, template_path: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update stack."""
        client = await self.registry.get_client(tool)
        return await client.call_tool(
            "update_stack",
            {"stack_name": stack_name, "template_path": template_path, "parameters": parameters},
        )
