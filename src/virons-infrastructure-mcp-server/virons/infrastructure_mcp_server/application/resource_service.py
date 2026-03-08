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
"""Resource management service."""

from typing import Any, Dict

from virons.common import UpstreamRegistry


class ResourceService:
    """Service for resource management."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def list_resources(self, tool: str) -> Dict[str, Any]:
        """List all resources."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("list_all_resources", {})

    async def tag_resource(
        self, tool: str, resource_id: str, tags: Dict[str, str]
    ) -> Dict[str, Any]:
        """Tag resource."""
        client = await self.registry.get_client(tool)
        return await client.call_tool("tag_resource", {"resource_id": resource_id, "tags": tags})
