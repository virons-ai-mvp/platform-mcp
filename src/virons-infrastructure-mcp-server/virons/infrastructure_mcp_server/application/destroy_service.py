# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D107
"""Destroy service for infrastructure orchestration."""

from typing import Any

from loguru import logger

from ..domain.upstream_registry import UpstreamRegistry


class ConfirmationRequiredError(Exception):
    """Raised when confirmation is required but not provided."""

    pass


class DestroyService:
    """Service for destroying infrastructure stacks."""

    def __init__(self, registry: UpstreamRegistry, audit: Any):
        self.registry = registry
        self.audit = audit

    async def destroy_infrastructure(
        self, tool: str, stack_name: str, confirm: bool = False
    ) -> dict:
        """Destroy infrastructure stack with confirmation and audit."""
        if not confirm:
            raise ConfirmationRequiredError(
                "Destroy operation requires explicit confirmation (confirm=True)"
            )

        try:
            client = await self.registry.get_client(tool)
            result = await client.call_tool("destroy_stack", {"stack_name": stack_name})

            # BaFin AT 8.1: Audit trail
            audit_id = await self.audit.write_audit(
                service_name="infrastructure",
                calculation_type="destroy",
                entity_id=stack_name,
                input_data={"tool": tool, "stack_name": stack_name},
                output_data=result,
            )

            logger.info(f"Destroyed stack {stack_name} using {tool}, audit_id={audit_id}")

            return {
                "status": "destroyed",
                "stack_name": stack_name,
                "tool": tool,
                "audit_id": audit_id,
            }

        except Exception as e:
            logger.error(f"Destroy failed for {stack_name}: {e}")
            raise
