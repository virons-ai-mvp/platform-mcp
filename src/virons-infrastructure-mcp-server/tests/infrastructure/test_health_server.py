# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for HTTP health server."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from virons.infrastructure_mcp_server.infrastructure.health_server import HealthServer


@pytest.fixture
def mock_health_checker():
    """Mock health checker."""
    checker = MagicMock()
    checker.liveness = AsyncMock(return_value={"status": "ok"})
    checker.readiness = AsyncMock(return_value={"status": "ok"})
    return checker


class TestHealthServer:
    """Test HTTP health server."""

    @pytest.mark.asyncio
    async def test_server_starts_on_port(self, mock_health_checker):
        """Health server starts on configured port."""
        server = HealthServer(health_checker=mock_health_checker, port=8080)

        assert server.port == 8080
        assert server.health_checker == mock_health_checker

    @pytest.mark.asyncio
    async def test_liveness_endpoint_returns_json(self, mock_health_checker):
        """GET /health/live returns JSON response."""
        server = HealthServer(health_checker=mock_health_checker, port=8080)

        # Simulate request
        response = await server.handle_liveness()

        assert response["status"] == "ok"
        mock_health_checker.liveness.assert_called_once()

    @pytest.mark.asyncio
    async def test_readiness_endpoint_returns_json(self, mock_health_checker):
        """GET /health/ready returns JSON response."""
        server = HealthServer(health_checker=mock_health_checker, port=8080)

        # Simulate request
        response = await server.handle_readiness()

        assert response["status"] == "ok"
        mock_health_checker.readiness.assert_called_once()
