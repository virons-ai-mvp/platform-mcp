# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for deploy service."""

from unittest.mock import AsyncMock, Mock

import pytest

from virons.common.residency import DataResidencyError
from virons.infrastructure_mcp_server.application.deploy_service import (
    DeployService,
)


@pytest.fixture
def mock_registry():
    """Mock upstream registry."""
    return Mock()


@pytest.fixture
def mock_audit():
    """Mock audit service."""
    audit = AsyncMock()
    audit.write_audit = AsyncMock(return_value="audit-123")
    return audit


@pytest.mark.asyncio
async def test_deploy_infrastructure_calls_upstream(mock_registry, mock_audit):
    """Test deploy service routes to correct upstream server."""
    mock_client = AsyncMock()
    mock_client.call_tool.return_value = {"status": "deployed"}
    mock_registry.get_client = AsyncMock(return_value=mock_client)

    service = DeployService(registry=mock_registry, audit=mock_audit)
    result = await service.deploy_infrastructure(
        tool="cdk", stack_name="my-stack", template_path="/path", parameters={}
    )

    mock_client.call_tool.assert_called_once()
    assert result.status == "deployed"


@pytest.mark.asyncio
async def test_deploy_infrastructure_audits_operation(mock_registry, mock_audit):
    """Test deploy service creates audit trail (BaFin AT 8.1)."""
    mock_client = AsyncMock()
    mock_client.call_tool.return_value = {"status": "deployed"}
    mock_registry.get_client = AsyncMock(return_value=mock_client)

    service = DeployService(registry=mock_registry, audit=mock_audit)

    await service.deploy_infrastructure(
        tool="cdk", stack_name="my-stack", template_path="/path", parameters={}
    )

    mock_audit.write_audit.assert_called_once()
    call_args = mock_audit.write_audit.call_args[1]
    assert call_args["service_name"] == "infrastructure"
    assert call_args["calculation_type"] == "deploy"
    assert call_args["entity_id"] == "my-stack"


@pytest.mark.asyncio
async def test_deploy_infrastructure_enforces_region(mock_registry, mock_audit):
    """Test deploy service enforces EU data residency (GDPR Art 25)."""
    service = DeployService(registry=mock_registry, audit=mock_audit)

    with pytest.raises(DataResidencyError):
        await service.deploy_infrastructure(
            tool="cdk",
            stack_name="my-stack",
            template_path="/path",
            parameters={"region": "us-east-1"},
        )


@pytest.mark.asyncio
async def test_deploy_infrastructure_returns_audit_id(mock_registry, mock_audit):
    """Test deploy service returns audit ID in result."""
    mock_client = AsyncMock()
    mock_client.call_tool.return_value = {"status": "deployed"}
    mock_registry.get_client = AsyncMock(return_value=mock_client)

    service = DeployService(registry=mock_registry, audit=mock_audit)

    result = await service.deploy_infrastructure(
        tool="cdk", stack_name="my-stack", template_path="/path", parameters={}
    )

    assert result.audit_id == "audit-123"
