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

# ruff: noqa: D107, D102
"""Extended security and compliance services."""

from typing import Any, Dict

from virons.common import UpstreamRegistry


class ExtendedSecurityService:
    """Extended security service."""

    def __init__(self, registry: UpstreamRegistry, audit: Any):
        self.registry = registry
        self.audit = audit

    async def check_compliance(self, tool: str, stack_name: str, rules: list) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        result = await client.call_tool(
            "check_compliance", {"stack_name": stack_name, "rules": rules}
        )
        await self.audit.write_audit(
            service_name="infrastructure",
            calculation_type="compliance_check",
            entity_id=stack_name,
            input_data={"tool": tool, "rules": rules},
            output_data=result,
        )
        return result

    async def rotate_secrets(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("rotate_secrets", {"stack_name": stack_name})

    async def scan_vulnerabilities(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("scan_vulnerabilities", {"stack_name": stack_name})

    async def generate_compliance_report(self, tool: str, stack_name: str) -> Dict[str, Any]:
        client = await self.registry.get_client(tool)
        return await client.call_tool("generate_compliance_report", {"stack_name": stack_name})
