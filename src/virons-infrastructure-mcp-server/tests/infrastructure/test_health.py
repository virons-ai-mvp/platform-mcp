# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for health check endpoints (DORA Art 11 compliance)."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from virons.infrastructure_mcp_server.infrastructure.health import HealthChecker


@pytest.fixture
def mock_registry():
    """Mock upstream registry."""
    registry = MagicMock()
    registry.health_check = AsyncMock()
    return registry


class TestHealthChecker:
    """Test health check endpoints."""

    @pytest.mark.asyncio
    async def test_liveness_always_returns_ok(self, mock_registry):
        """Liveness probe always returns OK if process is running."""
        checker = HealthChecker(registry=mock_registry)

        result = await checker.liveness()

        assert result["status"] == "ok"
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_readiness_ok_when_upstreams_healthy(self, mock_registry):
        """Readiness probe returns OK when all upstreams are healthy."""
        mock_registry.health_check.return_value = {
            "cdk": {"status": "healthy"},
            "cfn": {"status": "healthy"},
        }

        checker = HealthChecker(registry=mock_registry)
        result = await checker.readiness()

        assert result["status"] == "ok"
        assert result["upstreams"]["cdk"]["status"] == "healthy"
        assert result["upstreams"]["cfn"]["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_readiness_degraded_when_upstream_unhealthy(self, mock_registry):
        """Readiness probe returns degraded when any upstream is unhealthy."""
        mock_registry.health_check.return_value = {
            "cdk": {"status": "healthy"},
            "cfn": {"status": "unhealthy", "error": "connection refused"},
        }

        checker = HealthChecker(registry=mock_registry)
        result = await checker.readiness()

        assert result["status"] == "degraded"
        assert result["upstreams"]["cfn"]["status"] == "unhealthy"

    @pytest.mark.asyncio
    async def test_readiness_handles_registry_error(self, mock_registry):
        """Readiness probe handles registry errors gracefully."""
        mock_registry.health_check.side_effect = Exception("Registry error")

        checker = HealthChecker(registry=mock_registry)
        result = await checker.readiness()

        assert result["status"] == "error"
        assert "Registry error" in result["error"]
