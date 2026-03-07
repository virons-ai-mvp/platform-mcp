# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for Phase 2 tools (state, drift, extended services)."""

from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_registry():
    registry = MagicMock()
    client = AsyncMock()
    registry.get_client = AsyncMock(return_value=client)
    return registry, client


@pytest.mark.asyncio
class TestStateService:
    async def test_get_state(self, mock_registry):
        from virons.infrastructure_mcp_server.application.state_drift_service import StateService

        registry, client = mock_registry
        client.call_tool.return_value = {"state": "data"}

        service = StateService(registry)
        result = await service.get_state("terraform", "test-stack")

        assert "state" in result

    async def test_lock_state(self, mock_registry):
        from virons.infrastructure_mcp_server.application.state_drift_service import StateService

        registry, client = mock_registry
        client.call_tool.return_value = {"locked": True}

        service = StateService(registry)
        result = await service.lock_state("terraform", "test-stack")

        assert result["locked"] is True

    async def test_backup_state(self, mock_registry):
        from virons.infrastructure_mcp_server.application.state_drift_service import StateService

        registry, client = mock_registry
        client.call_tool.return_value = {"backup_id": "state-backup-123"}

        service = StateService(registry)
        result = await service.backup_state("terraform", "test-stack")

        assert "backup_id" in result


@pytest.mark.asyncio
class TestDriftService:
    async def test_get_drift_status(self, mock_registry):
        from virons.infrastructure_mcp_server.application.state_drift_service import DriftService

        registry, client = mock_registry
        client.call_tool.return_value = {"status": "no_drift"}

        service = DriftService(registry)
        result = await service.get_drift_status("cdk", "test-stack")

        assert result["status"] == "no_drift"

    async def test_remediate_drift(self, mock_registry):
        from virons.infrastructure_mcp_server.application.state_drift_service import DriftService

        registry, client = mock_registry
        client.call_tool.return_value = {"remediated": True}

        service = DriftService(registry)
        result = await service.remediate_drift("cdk", "test-stack")

        assert result["remediated"] is True


@pytest.mark.asyncio
class TestExtendedSecurityService:
    async def test_check_compliance(self, mock_registry):
        from virons.infrastructure_mcp_server.application.extended_security_service import (
            ExtendedSecurityService,
        )

        registry, client = mock_registry
        audit = AsyncMock()
        client.call_tool.return_value = {"compliant": True}

        service = ExtendedSecurityService(registry, audit)
        result = await service.check_compliance("cdk", "test-stack", ["BaFin", "GDPR"])

        assert result["compliant"] is True
        audit.write_audit.assert_called_once()

    async def test_rotate_secrets(self, mock_registry):
        from virons.infrastructure_mcp_server.application.extended_security_service import (
            ExtendedSecurityService,
        )

        registry, client = mock_registry
        audit = AsyncMock()
        client.call_tool.return_value = {"rotated": True}

        service = ExtendedSecurityService(registry, audit)
        result = await service.rotate_secrets("cdk", "test-stack")

        assert result["rotated"] is True


@pytest.mark.asyncio
class TestExtendedCostService:
    async def test_estimate_cost(self, mock_registry):
        from virons.infrastructure_mcp_server.application.extended_services import (
            ExtendedCostService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"estimated_cost": 500.0}

        service = ExtendedCostService(registry)
        result = await service.estimate_cost("cdk", "./template.json")

        assert result["estimated_cost"] == 500.0

    async def test_get_cost_forecast(self, mock_registry):
        from virons.infrastructure_mcp_server.application.extended_services import (
            ExtendedCostService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"forecast": []}

        service = ExtendedCostService(registry)
        result = await service.get_cost_forecast("cdk", "test-stack", 30)

        assert "forecast" in result

    async def test_set_budget(self, mock_registry):
        from virons.infrastructure_mcp_server.application.extended_services import (
            ExtendedCostService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"budget_set": True}

        service = ExtendedCostService(registry)
        result = await service.set_budget("cdk", "test-stack", 1000.0, "USD")

        assert result["budget_set"] is True


@pytest.mark.asyncio
class TestExtendedResourceService:
    async def test_get_resource_info(self, mock_registry):
        from virons.infrastructure_mcp_server.application.extended_services import (
            ExtendedResourceService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"id": "res-123", "type": "EC2"}

        service = ExtendedResourceService(registry)
        result = await service.get_resource_info("cdk", "res-123")

        assert result["id"] == "res-123"

    async def test_search_resources(self, mock_registry):
        from virons.infrastructure_mcp_server.application.extended_services import (
            ExtendedResourceService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"resources": []}

        service = ExtendedResourceService(registry)
        result = await service.search_resources("cdk", {"env": "prod"})

        assert "resources" in result


@pytest.mark.asyncio
class TestNetworkService:
    async def test_get_vpc_info(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            NetworkService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"vpc_id": "vpc-123", "cidr": "10.0.0.0/16"}

        service = NetworkService(registry)
        result = await service.get_vpc_info("cdk", "vpc-123")

        assert result["vpc_id"] == "vpc-123"

    async def test_test_connectivity(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            NetworkService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"reachable": True}

        service = NetworkService(registry)
        result = await service.test_connectivity("cdk", "10.0.1.10", "10.0.2.20")

        assert result["reachable"] is True


@pytest.mark.asyncio
class TestDatabaseService:
    async def test_get_database_info(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            DatabaseService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"db_id": "db-123", "engine": "postgres"}

        service = DatabaseService(registry)
        result = await service.get_database_info("cdk", "db-123")

        assert result["engine"] == "postgres"

    async def test_backup_database(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            DatabaseService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"backup_id": "db-backup-123"}

        service = DatabaseService(registry)
        result = await service.backup_database("cdk", "db-123")

        assert "backup_id" in result


@pytest.mark.asyncio
class TestComputeService:
    async def test_start_instance(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            ComputeService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"state": "starting"}

        service = ComputeService(registry)
        result = await service.start_instance("cdk", "i-123")

        assert result["state"] == "starting"

    async def test_stop_instance(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            ComputeService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"state": "stopping"}

        service = ComputeService(registry)
        result = await service.stop_instance("cdk", "i-123")

        assert result["state"] == "stopping"


@pytest.mark.asyncio
class TestStorageService:
    async def test_list_buckets(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            StorageService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"buckets": []}

        service = StorageService(registry)
        result = await service.list_buckets("cdk")

        assert "buckets" in result

    async def test_sync_bucket(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            StorageService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"synced": True}

        service = StorageService(registry)
        result = await service.sync_bucket("cdk", "s3://source", "s3://target")

        assert result["synced"] is True


@pytest.mark.asyncio
class TestDeploymentService:
    async def test_create_pipeline(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            DeploymentService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"pipeline_id": "pipe-123"}

        service = DeploymentService(registry)
        result = await service.create_pipeline("cdk", "my-pipeline", {})

        assert "pipeline_id" in result

    async def test_rollback_deployment(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            DeploymentService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"rolled_back": True}

        service = DeploymentService(registry)
        result = await service.rollback_deployment("cdk", "test-stack", "v1.0")

        assert result["rolled_back"] is True


@pytest.mark.asyncio
class TestMultiRegionService:
    async def test_list_regions(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            MultiRegionService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"regions": ["eu-central-1", "us-east-1"]}

        service = MultiRegionService(registry)
        result = await service.list_regions("cdk")

        assert len(result["regions"]) == 2

    async def test_replicate_stack(self, mock_registry):
        from virons.infrastructure_mcp_server.application.infrastructure_extended_services import (
            MultiRegionService,
        )

        registry, client = mock_registry
        client.call_tool.return_value = {"replicated": True}

        service = MultiRegionService(registry)
        result = await service.replicate_stack("cdk", "test-stack", "us-east-1")

        assert result["replicated"] is True
