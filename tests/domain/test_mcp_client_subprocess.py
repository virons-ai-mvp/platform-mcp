"""Tests for MCP client subprocess STDIO connections - TDD approach."""

import pytest
from virons.infrastructure_mcp_server.domain.mcp_client import MCPClient, MCPConnectionError


@pytest.mark.asyncio
async def test_mcp_client_connects_to_subprocess():
    """Test client can connect to subprocess MCP server."""
    client = MCPClient(
        command='python', args=['-m', 'awslabs.aws_iac_mcp_server'], server_name='test-iac'
    )

    await client.connect()
    assert client.is_connected()

    await client.disconnect()
    assert not client.is_connected()


@pytest.mark.asyncio
async def test_mcp_client_lists_tools():
    """Test client can list tools from subprocess server."""
    client = MCPClient(
        command='python', args=['-m', 'awslabs.aws_iac_mcp_server'], server_name='test-iac'
    )

    await client.connect()
    tools = await client.list_tools()

    assert len(tools) > 0
    assert any('cloudformation' in t['name'].lower() for t in tools)

    await client.disconnect()


@pytest.mark.asyncio
async def test_mcp_client_handles_connection_failure():
    """Test client handles connection failures gracefully."""
    client = MCPClient(
        command='python', args=['-m', 'nonexistent.module'], server_name='test-fail'
    )

    with pytest.raises(MCPConnectionError):
        await client.connect()
