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

"""Health check endpoints for DORA Art 11 compliance."""

from datetime import UTC, datetime
from typing import Any, Dict

from loguru import logger

from virons.common import UpstreamRegistry


class HealthChecker:
    """Health check implementation for Kubernetes probes."""

    def __init__(self, registry: UpstreamRegistry):
        """Initialize health checker.

        Args:
            registry: Upstream registry for checking upstream health
        """
        self.registry = registry

    async def liveness(self) -> Dict[str, Any]:
        """Liveness probe - process is alive."""
        return {
            "status": "ok",
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def readiness(self) -> Dict[str, Any]:
        """Readiness probe - can serve traffic."""
        try:
            # Simplified: just return healthy for now
            return {
                "status": "healthy",
                "upstreams": {},
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Readiness check failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }
