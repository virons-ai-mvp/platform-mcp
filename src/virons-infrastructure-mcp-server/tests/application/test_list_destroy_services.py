# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for list and destroy services."""

from unittest.mock import AsyncMock, Mock

import pytest

from virons.infrastructure_mcp_server.application.destroy_service import (
    ConfirmationRequiredError,
    DestroyService,
)
from virons.infrastructure_mcp_server.application.list_service import ListService


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
async def test_list_stacks_aggregates_from_upstream(mock_registry):
    """Test list service aggregates stacks from upstream server."""
    mock_client = AsyncMock()
    mock_client.call_tool.return_value = {"stacks": [{"name": "stack-1"}, {"name": "stack-2"}]}
    mock_registry.get_client = AsyncMock(return_value=mock_client)

    service = ListService(registry=mock_registry)
    result = await service.list_stacks(tool="cdk")

    assert len(result["stacks"]) == 2
    assert result["tool"] == "cdk"


@pytest.mark.asyncio
async def test_destroy_infrastructure_audits_operation(mock_registry, mock_audit):
    """Test destroy service creates audit trail (BaFin AT 8.1)."""
    mock_client = AsyncMock()
    mock_client.call_tool.return_value = {"status": "destroyed"}
    mock_registry.get_client = AsyncMock(return_value=mock_client)

    service = DestroyService(registry=mock_registry, audit=mock_audit)

    await service.destroy_infrastructure(tool="cdk", stack_name="my-stack", confirm=True)

    mock_audit.write_audit.assert_called_once()
    call_args = mock_audit.write_audit.call_args[1]
    assert call_args["calculation_type"] == "destroy"


@pytest.mark.asyncio
async def test_destroy_infrastructure_requires_confirmation(mock_registry, mock_audit):
    """Test destroy service requires explicit confirmation flag."""
    service = DestroyService(registry=mock_registry, audit=mock_audit)

    with pytest.raises(ConfirmationRequiredError):
        await service.destroy_infrastructure(tool="cdk", stack_name="my-stack", confirm=False)
