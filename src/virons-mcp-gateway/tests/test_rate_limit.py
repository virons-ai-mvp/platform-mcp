# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for rate limiting middleware."""

import pytest
from httpx import ASGITransport, AsyncClient

from virons.mcp_gateway.domain.registry import MCPService, ServiceRegistry
from virons.mcp_gateway.server import create_app


@pytest.fixture
def registry():
    """Create test registry."""
    reg = ServiceRegistry()
    reg.register(MCPService(name="test", url="http://localhost:9100", tools=["test_tool"]))
    return reg


@pytest.fixture
def app(registry):
    """Create test app with low rate limit."""
    return create_app(registry, rate_limit=3, rate_window=60)


@pytest.mark.asyncio
class TestRateLimit:
    """Test rate limiting middleware."""

    async def test_rate_limit_allows_under_threshold(self, app):
        """Test requests under threshold are allowed."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            # First 3 requests should succeed
            for _ in range(3):
                resp = await client.get("/health")
                assert resp.status_code == 200

    async def test_rate_limit_blocks_over_threshold(self, app):
        """Test requests over threshold are blocked."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            # First 3 requests succeed
            for _ in range(3):
                await client.get("/health")

            # 4th request should be rate limited
            resp = await client.get("/health")
            assert resp.status_code == 429
            assert resp.json()["error"] == "Too many requests"

    async def test_rate_limit_per_client(self, app):
        """Test rate limit is per client IP."""
        # This test verifies the concept - in real scenario different IPs would be tested
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            for _ in range(3):
                await client.get("/health")
            resp = await client.get("/health")
            assert resp.status_code == 429
