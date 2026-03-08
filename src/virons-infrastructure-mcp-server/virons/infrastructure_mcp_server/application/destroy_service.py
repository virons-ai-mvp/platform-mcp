# Copyright Virons Fintech. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ruff: noqa: D107
"""Destroy service for infrastructure orchestration."""

from typing import Any

from loguru import logger

from virons.common import UpstreamRegistry


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
