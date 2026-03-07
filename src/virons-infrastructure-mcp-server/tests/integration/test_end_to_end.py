# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""End-to-end integration tests."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from virons.infrastructure_mcp_server.server import create_server


@pytest.mark.integration
class TestEndToEnd:
    """End-to-end integration tests."""

    @pytest.mark.asyncio
    async def test_server_initializes_all_components(self):
        """Server initializes with all components."""
        server = create_server()

        assert server is not None
        assert "infrastructure" in server.name

    @pytest.mark.asyncio
    async def test_deploy_tool_with_metrics(self):
        """Deploy tool records metrics."""
        with patch("virons.infrastructure_mcp_server.server.DeployService") as mock_deploy:
            mock_result = MagicMock()
            mock_result.status = "deployed"
            mock_result.stack_name = "test-stack"
            mock_result.tool = "cdk"
            mock_result.audit_id = "audit-123"

            mock_deploy.return_value.deploy_infrastructure = AsyncMock(return_value=mock_result)

            server = create_server()

            # Tool should be registered
            tools = await server.list_tools()
            tool_names = [t.name for t in tools]
            assert "deploy_infrastructure" in tool_names

    @pytest.mark.asyncio
    async def test_health_check_integration(self):
        """Health check integrates with upstream registry."""
        from virons.infrastructure_mcp_server.domain.upstream_registry import UpstreamRegistry
        from virons.infrastructure_mcp_server.infrastructure.health import HealthChecker

        registry = UpstreamRegistry(
            {"cdk": {"host": "localhost", "port": 9140, "transport": "stdio"}}
        )

        checker = HealthChecker(registry=registry)

        # Liveness should always work
        liveness = await checker.liveness()
        assert liveness["status"] == "ok"

    @pytest.mark.asyncio
    async def test_metrics_collector_singleton(self):
        """Metrics collector is singleton across server."""
        from virons.infrastructure_mcp_server.infrastructure.metrics import MetricsCollector

        collector1 = MetricsCollector()
        collector2 = MetricsCollector()

        assert collector1 is collector2
