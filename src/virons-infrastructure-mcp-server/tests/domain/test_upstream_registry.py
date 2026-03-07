# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for upstream server registry."""

import pytest

from virons.infrastructure_mcp_server.domain.upstream_registry import (
    UnknownServerError,
    UpstreamRegistry,
)


@pytest.fixture
def test_config():
    """Test configuration for upstream servers."""
    return {
        "cdk": {"host": "localhost", "port": 9140, "transport": "stdio"},
        "cfn": {"host": "localhost", "port": 9141, "transport": "stdio"},
    }


def test_registry_loads_configuration(test_config):
    """Test registry loads upstream server config."""
    registry = UpstreamRegistry(test_config)
    assert len(registry.servers) == 2
    assert "cdk" in registry.servers
    assert "cfn" in registry.servers


@pytest.mark.asyncio
async def test_registry_gets_client_for_server(test_config):
    """Test registry returns connected client for server name."""
    registry = UpstreamRegistry(test_config)
    client = await registry.get_client("cdk")
    assert client.is_connected()
    assert client.server_name == "cdk"
    await registry.close_all()


@pytest.mark.asyncio
async def test_registry_caches_clients(test_config):
    """Test registry reuses existing client connections."""
    registry = UpstreamRegistry(test_config)
    client1 = await registry.get_client("cdk")
    client2 = await registry.get_client("cdk")
    assert client1 is client2
    await registry.close_all()


@pytest.mark.asyncio
async def test_registry_health_check(test_config):
    """Test registry checks health of all upstream servers."""
    registry = UpstreamRegistry(test_config)
    health = await registry.check_health()
    assert "cdk" in health
    assert "cfn" in health
    assert health["cdk"]["status"] in ["healthy", "unhealthy"]
    await registry.close_all()


@pytest.mark.asyncio
async def test_registry_raises_on_unknown_server(test_config):
    """Test registry raises error for unknown server name."""
    registry = UpstreamRegistry(test_config)
    with pytest.raises(UnknownServerError):
        await registry.get_client("unknown")
