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
"""Deploy service for infrastructure orchestration."""

from typing import Any, Dict

from loguru import logger

from virons.common import UpstreamRegistry
from virons.common.residency import enforce_region

from ..models import StackDeploymentResult


class DeploymentError(Exception):
    """Raised when deployment fails."""

    pass


class DeployService:
    """Service for deploying infrastructure stacks."""

    def __init__(self, registry: UpstreamRegistry, audit: Any):
        self.registry = registry
        self.audit = audit

    async def deploy_infrastructure(
        self, tool: str, stack_name: str, template_path: str, parameters: Dict[str, Any]
    ) -> StackDeploymentResult:
        """Deploy infrastructure stack with compliance checks."""
        # GDPR Art 25: Enforce EU data residency
        if "region" in parameters:
            enforce_region(parameters["region"])

        try:
            # Get upstream client
            client = await self.registry.get_client(tool)

            # Call upstream tool
            result = await client.call_tool(
                "deploy_stack",
                {
                    "stack_name": stack_name,
                    "template_path": template_path,
                    "parameters": parameters,
                },
            )

            # BaFin AT 8.1: Audit trail
            audit_id = await self.audit.write_audit(
                service_name="infrastructure",
                calculation_type="deploy",
                entity_id=stack_name,
                input_data={
                    "tool": tool,
                    "template_path": template_path,
                    "parameters": parameters,
                },
                output_data=result,
            )

            logger.info(f"Deployed stack {stack_name} using {tool}, audit_id={audit_id}")

            return StackDeploymentResult(
                status="deployed", stack_name=stack_name, tool=tool, audit_id=audit_id
            )

        except Exception as e:
            logger.error(f"Deployment failed for {stack_name}: {e}")
            raise DeploymentError(f"Deployment failed: {e}")
