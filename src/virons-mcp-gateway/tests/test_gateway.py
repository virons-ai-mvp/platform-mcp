# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for gateway router."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from virons.mcp_gateway.domain.gateway import (
    CircuitBreakerOpenError,
    GatewayRouter,
    ToolNotFoundError,
)
from virons.mcp_gateway.domain.registry import MCPService, ServiceRegistry


@pytest.fixture
def registry():
    """Create test registry."""
    reg = ServiceRegistry()
    reg.register(MCPService(name="infra", url="http://localhost:9100", tools=["deploy"]))
    reg.register(MCPService(name="security", url="http://localhost:9500", tools=["scan"]))
    return reg


@pytest.fixture
def router(registry):
    """Create test router."""
    return GatewayRouter(registry, timeout=5.0, circuit_breaker_threshold=3)


class TestGatewayRouter:
    """Test gateway router functionality."""

    @pytest.mark.asyncio
    async def test_execute_tool_success(self, router):
        """Test successful tool execution."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"result": "success"}
        mock_resp.raise_for_status = MagicMock()

        with patch.object(router._client, "post", new_callable=AsyncMock, return_value=mock_resp):
            result = await router.execute_tool("deploy", {"param": "value"}, "Bearer token")
            assert result == {"result": "success"}

    @pytest.mark.asyncio
    async def test_execute_tool_not_found(self, router):
        """Test tool not found raises error."""
        with pytest.raises(ToolNotFoundError, match="Tool not found: nonexistent"):
            await router.execute_tool("nonexistent", {}, "Bearer token")

    @pytest.mark.asyncio
    async def test_execute_tool_circuit_breaker_open(self, router):
        """Test circuit breaker opens after failures."""
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = Exception("Connection failed")

        with patch.object(router._client, "post", new_callable=AsyncMock, return_value=mock_resp):
            # Trigger 3 failures
            for _ in range(3):
                with pytest.raises(Exception):
                    await router.execute_tool("deploy", {}, "Bearer token")

            # Circuit breaker should be open
            with pytest.raises(CircuitBreakerOpenError, match="Circuit breaker open for infra"):
                await router.execute_tool("deploy", {}, "Bearer token")

    @pytest.mark.asyncio
    async def test_health_check_all_healthy(self, router):
        """Test health check with all services healthy."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"status": "ok"}
        mock_resp.raise_for_status = MagicMock()

        with patch.object(router._client, "get", new_callable=AsyncMock, return_value=mock_resp):
            result = await router.health_check()
            assert len(result["services"]) == 2
            assert all(s["status"] == "healthy" for s in result["services"])

    @pytest.mark.asyncio
    async def test_health_check_one_unhealthy(self, router):
        """Test health check with one service unhealthy."""

        async def mock_get(url, **kwargs):
            resp = MagicMock()
            if "9100" in url:
                resp.json.return_value = {"status": "ok"}
                resp.raise_for_status = MagicMock()
            else:
                resp.raise_for_status.side_effect = Exception("Service down")
            return resp

        with patch.object(router._client, "get", side_effect=mock_get):
            result = await router.health_check()
            healthy = [s for s in result["services"] if s["status"] == "healthy"]
            unhealthy = [s for s in result["services"] if s["status"] == "unhealthy"]
            assert len(healthy) == 1
            assert len(unhealthy) == 1

    @pytest.mark.asyncio
    async def test_readiness_check_ready(self, router):
        """Test readiness check when all services healthy."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"status": "ok"}
        mock_resp.raise_for_status = MagicMock()

        with patch.object(router._client, "get", new_callable=AsyncMock, return_value=mock_resp):
            result = await router.readiness_check()
            assert result["ready"] is True

    @pytest.mark.asyncio
    async def test_readiness_check_not_ready(self, router):
        """Test readiness check when service unhealthy."""
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = Exception("Service down")

        with patch.object(router._client, "get", new_callable=AsyncMock, return_value=mock_resp):
            result = await router.readiness_check()
            assert result["ready"] is False

    @pytest.mark.asyncio
    async def test_close(self, router):
        """Test router cleanup."""
        with patch.object(router._client, "aclose", new_callable=AsyncMock) as mock_close:
            await router.close()
            mock_close.assert_called_once()
