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
"""List service for infrastructure orchestration."""

from typing import Any, Dict

from loguru import logger

from virons.common import UpstreamRegistry


class ListService:
    """Service for listing infrastructure stacks."""

    def __init__(self, registry: UpstreamRegistry):
        self.registry = registry

    async def list_stacks(self, tool: str) -> Dict[str, Any]:
        """List stacks from upstream server."""
        try:
            client = await self.registry.get_client(tool)
            result = await client.call_tool("list_stacks", {})

            logger.info(f"Listed stacks from {tool}")

            return {"tool": tool, "stacks": result.get("stacks", [])}

        except Exception as e:
            logger.error(f"Failed to list stacks from {tool}: {e}")
            raise
