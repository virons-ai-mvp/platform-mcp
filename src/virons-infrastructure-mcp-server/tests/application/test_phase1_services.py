# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for Phase 1 tools (stack info, resource, monitoring, security, backup, cost, infrastructure)."""

from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_registry():
    registry = MagicMock()
    client = AsyncMock()
    registry.get_client = AsyncMock(return_value=client)
    return registry, client


@pytest.mark.asyncio
class TestStackInfoService:
    async def test_get_stack_info(self, mock_registry):
        from virons.infrastructure_mcp_server.application.stack_info_service import (
            StackInfoService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"name": "test-stack", "status": "deployed"}

        service = StackInfoService(registry)
        result = await service.get_stack_info("cdk", "test-stack")

        assert result["name"] == "test-stack"
        client.call_tool.assert_called_once_with("describe_stack", {"stack_name": "test-stack"})

    async def test_get_stack_outputs(self, mock_registry):
        from virons.infrastructure_mcp_server.application.stack_info_service import (
            StackInfoService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"outputs": {"key": "value"}}

        service = StackInfoService(registry)
        result = await service.get_stack_outputs("cdk", "test-stack")

        assert "outputs" in result
        client.call_tool.assert_called_once()

    async def test_validate_template(self, mock_registry):
        from virons.infrastructure_mcp_server.application.stack_info_service import (
            StackInfoService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"valid": True}

        service = StackInfoService(registry)
        result = await service.validate_template("cdk", "./template.json")

        assert result["valid"] is True


@pytest.mark.asyncio
class TestResourceService:
    async def test_list_resources(self, mock_registry):
        from virons.infrastructure_mcp_server.application.resource_service import ResourceService

        registry, client = mock_registry
        client.call_tool.return_value = {"resources": []}

        service = ResourceService(registry)
        result = await service.list_resources("cdk")

        assert "resources" in result

    async def test_tag_resource(self, mock_registry):
        from virons.infrastructure_mcp_server.application.resource_service import ResourceService

        registry, client = mock_registry
        client.call_tool.return_value = {"status": "tagged"}

        service = ResourceService(registry)
        result = await service.tag_resource("cdk", "res-123", {"env": "prod"})

        assert result["status"] == "tagged"


@pytest.mark.asyncio
class TestMonitoringService:
    async def test_get_health_status(self, mock_registry):
        from virons.infrastructure_mcp_server.application.monitoring_service import (
            MonitoringService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"status": "healthy"}

        service = MonitoringService(registry)
        result = await service.get_health_status("cdk", "test-stack")

        assert result["status"] == "healthy"

    async def test_get_metrics(self, mock_registry):
        from virons.infrastructure_mcp_server.application.monitoring_service import (
            MonitoringService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"datapoints": []}

        service = MonitoringService(registry)
        result = await service.get_metrics("cdk", "test-stack", "CPUUtilization")

        assert "datapoints" in result


@pytest.mark.asyncio
class TestSecurityService:
    async def test_scan_security(self, mock_registry):
        from virons.infrastructure_mcp_server.application.security_service import SecurityService

        registry, client = mock_registry
        audit = AsyncMock()
        client.call_tool.return_value = {"findings": []}

        service = SecurityService(registry, audit)
        result = await service.scan_security("cdk", "test-stack")

        assert "findings" in result
        audit.write_audit.assert_called_once()

    async def test_detect_drift(self, mock_registry):
        from virons.infrastructure_mcp_server.application.security_service import SecurityService

        registry, client = mock_registry
        audit = AsyncMock()
        client.call_tool.return_value = {"drifted": False}

        service = SecurityService(registry, audit)
        result = await service.detect_drift("cdk", "test-stack")

        assert "drifted" in result


@pytest.mark.asyncio
class TestBackupService:
    async def test_create_backup(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_services import (
            BackupService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"backup_id": "backup-123"}

        service = BackupService(registry)
        result = await service.create_backup("cdk", "test-stack")

        assert "backup_id" in result

    async def test_list_backups(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_services import (
            BackupService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"backups": []}

        service = BackupService(registry)
        result = await service.list_backups("cdk", "test-stack")

        assert "backups" in result


@pytest.mark.asyncio
class TestCostService:
    async def test_get_cost_breakdown(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_services import (
            CostService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"total": 100.0}

        service = CostService(registry)
        result = await service.get_cost_breakdown("cdk", "test-stack")

        assert "total" in result


@pytest.mark.asyncio
class TestInfrastructureService:
    async def test_list_vpcs(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_services import (
            InfrastructureService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"vpcs": []}

        service = InfrastructureService(registry)
        result = await service.list_vpcs("cdk")

        assert "vpcs" in result

    async def test_list_databases(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_services import (
            InfrastructureService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"databases": []}

        service = InfrastructureService(registry)
        result = await service.list_databases("cdk")

        assert "databases" in result

    async def test_list_instances(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_services import (
            InfrastructureService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"instances": []}

        service = InfrastructureService(registry)
        result = await service.list_instances("cdk")

        assert "instances" in result
