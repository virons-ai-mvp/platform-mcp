# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Health check endpoints for DORA Art 11 compliance."""

from datetime import UTC, datetime
from typing import Any, Dict

from loguru import logger

from ..domain.upstream_registry import UpstreamRegistry


class HealthChecker:
    """Health check implementation for Kubernetes probes."""

    def __init__(self, registry: UpstreamRegistry):
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
