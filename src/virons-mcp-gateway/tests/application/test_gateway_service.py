# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for gateway service."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from virons.mcp_gateway.application.gateway_service import GatewayService


@pytest.fixture
def mock_httpx():
    """Mock httpx client."""
    with patch("virons.mcp_gateway.application.gateway_service.httpx.AsyncClient") as mock:
        client = AsyncMock()
        mock.return_value = client
        yield client


@pytest.mark.asyncio
class TestGatewayService:
    """Test gateway routing service."""

    async def test_route_tool_success(self, mock_httpx):
        """Test successful tool routing."""
        mock_httpx.post = AsyncMock(
            return_value=MagicMock(status_code=200, json=lambda: {"result": "success"})
        )

        service = GatewayService()
        result = await service.route_tool("infrastructure", "deploy", {"stack": "test"})

        assert result["result"] == "success"
        mock_httpx.post.assert_called_once()

    async def test_route_tool_unknown_server(self, mock_httpx):
        """Test routing to unknown server."""
        service = GatewayService()
        result = await service.route_tool("unknown", "tool", {})

        assert "error" in result
        assert "Unknown server" in result["error"]

    async def test_list_servers(self, mock_httpx):
        """Test listing servers."""
        service = GatewayService()
        result = await service.list_servers()

        assert "servers" in result
        assert len(result["servers"]) > 0

    async def test_health_check_success(self, mock_httpx):
        """Test health check."""
        mock_httpx.get = AsyncMock(return_value=MagicMock(status_code=200))

        service = GatewayService()
        result = await service.health_check("infrastructure")

        assert result["status"] == "healthy"
        assert result["server"] == "infrastructure"
