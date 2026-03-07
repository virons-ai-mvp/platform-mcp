# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D107, D102
"""Security and compliance service."""

from typing import Any, Dict

from ..domain.upstream_registry import UpstreamRegistry


class SecurityService:
    """Service for security and compliance."""

    def __init__(self, registry: UpstreamRegistry, audit: Any):
        self.registry = registry
        self.audit = audit

    async def scan_security(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """Scan security."""
        client = await self.registry.get_client(tool)
        result = await client.call_tool("security_scan", {"stack_name": stack_name})

        # Audit security scan
        await self.audit.write_audit(
            service_name="infrastructure",
            calculation_type="security_scan",
            entity_id=stack_name,
            input_data={"tool": tool, "stack_name": stack_name},
            output_data=result,
        )
        return result

    async def detect_drift(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """Detect drift."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("detect_drift", {"stack_name": stack_name})

    async def get_audit_logs(self, tool: str, stack_name: str) -> Dict[str, Any]:
        """Get audit logs."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("get_audit_logs", {"stack_name": stack_name})
