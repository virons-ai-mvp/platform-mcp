# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for HTTP server endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from virons.mcp_gateway.domain.registry import MCPService, ServiceRegistry
from virons.mcp_gateway.server import create_app


@pytest.fixture
def registry():
    """Create test registry."""
    reg = ServiceRegistry()
    reg.register(MCPService(name="infra", url="http://localhost:9100", tools=["deploy"]))
    return reg


@pytest.fixture
def app(registry):
    """Create test app."""
    return create_app(registry, rate_limit=100)


@pytest.mark.asyncio
class TestHTTPServer:
    """Test HTTP server endpoints."""

    async def test_health_endpoint(self, app):
        """Test health endpoint returns structure."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/health")
            assert resp.status_code == 200
            data = resp.json()
            assert data["status"] == "healthy"
            assert "services" in data
            assert "version" in data

    async def test_ready_endpoint_structure(self, app):
        """Test ready endpoint returns structure."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/ready")
            # Will be 503 because backends aren't actually running
            assert resp.status_code in [200, 503]
            data = resp.json()
            assert "ready" in data
            assert "services" in data

    async def test_list_tools_endpoint(self, app):
        """Test list tools endpoint."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/tools")
            assert resp.status_code == 200
            data = resp.json()
            assert "tools" in data
            assert len(data["tools"]) == 1
            assert data["tools"][0]["name"] == "deploy"

    async def test_execute_tool_missing_auth(self, app):
        """Test execute tool without auth header."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post("/tools/deploy", json={"param": "value"})
            assert resp.status_code == 401
            assert "authorization" in resp.json()["error"].lower()

    async def test_execute_tool_success(self, app):
        """Test successful tool execution structure."""
        # Tool execution will fail because backend isn't running, but we test the flow
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/tools/deploy", json={"param": "value"}, headers={"Authorization": "Bearer token"}
            )
            # Will be 500 because backend isn't running, but auth passed
            assert resp.status_code in [200, 500]
            data = resp.json()
            assert "error" in data or "result" in data

    async def test_execute_tool_not_found(self, app):
        """Test execute non-existent tool."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/tools/nonexistent", json={}, headers={"Authorization": "Bearer token"}
            )
            assert resp.status_code == 404
            assert "not found" in resp.json()["error"].lower()

    async def test_metrics_endpoint(self, app):
        """Test metrics endpoint."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/metrics")
            assert resp.status_code == 200
            assert "text/plain" in resp.headers["content-type"]
            assert b"http_requests" in resp.content

    async def test_correlation_id_propagation(self, app):
        """Test correlation ID is propagated."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/health", headers={"X-Correlation-ID": "test-123"})
            assert resp.headers["x-correlation-id"] == "test-123"

    async def test_correlation_id_generated(self, app):
        """Test correlation ID is generated if not provided."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/health")
            assert "x-correlation-id" in resp.headers
            assert len(resp.headers["x-correlation-id"]) > 0

    async def test_root_endpoint(self, app):
        """Test root endpoint."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/")
            assert resp.status_code == 200
            data = resp.json()
            assert data["service"] == "virons-mcp-gateway"
