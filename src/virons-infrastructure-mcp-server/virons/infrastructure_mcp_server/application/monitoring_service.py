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
"""Monitoring and observability service."""

from typing import Any, Dict

from virons.common import UpstreamRegistry


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
