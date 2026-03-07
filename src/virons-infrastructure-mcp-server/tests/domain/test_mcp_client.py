# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for MCP client interface."""

from unittest.mock import patch

import pytest

from virons.infrastructure_mcp_server.domain.mcp_client import (
    MCPClient,
    MCPConnectionError,
    MCPTransientError,
)


@pytest.mark.asyncio
async def test_client_connects_to_upstream():
    """Test client establishes connection to upstream MCP server."""
    client = MCPClient(host="localhost", port=9140, transport="stdio")
    await client.connect()
    assert client.is_connected()
    await client.disconnect()


@pytest.mark.asyncio
async def test_client_lists_tools():
    """Test client retrieves available tools from upstream."""
    client = MCPClient(host="localhost", port=9140)
    await client.connect()
    tools = await client.list_tools()
    assert len(tools) > 0
    assert "name" in tools[0]
    await client.disconnect()


@pytest.mark.asyncio
async def test_client_calls_tool():
    """Test client invokes tool on upstream server."""
    client = MCPClient(host="localhost", port=9140)
    await client.connect()
    result = await client.call_tool("list_stacks", {})
    assert isinstance(result, dict)
    await client.disconnect()


@pytest.mark.asyncio
async def test_client_handles_connection_error():
    """Test client raises appropriate error on connection failure."""
    client = MCPClient(host="invalid", port=9999)
    with pytest.raises(MCPConnectionError):
        await client.connect()


@pytest.mark.asyncio
async def test_client_retries_on_transient_error():
    """Test client retries failed requests with exponential backoff."""
    client = MCPClient(host="localhost", port=9140, max_retries=3)
    await client.connect()

    with patch.object(
        client,
        "_send_request",
        side_effect=[MCPTransientError(), MCPTransientError(), {"result": "success"}],
    ):
        result = await client.call_tool("test", {})
        assert result == {"result": "success"}

    await client.disconnect()
