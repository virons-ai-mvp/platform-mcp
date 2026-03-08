# Copyright Virons Fintech. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for MCPClient subprocess STDIO connections."""

import pytest

from virons.infrastructure_mcp_server.domain.mcp_client import MCPClient


@pytest.mark.asyncio
async def test_mcp_client_subprocess_connection():
    """Test that MCPClient can connect to a subprocess MCP server."""
    client = MCPClient(
        command="python",
        args=["-m", "awslabs.aws_iac_mcp_server"],
        server_name="test-iac",
    )

    await client.connect()
    assert client.is_connected()

    tools = await client.list_tools()
    assert len(tools) > 0

    await client.disconnect()


@pytest.mark.asyncio
async def test_mcp_client_multiple_calls():
    """Test that MCPClient subprocess stays alive across multiple calls."""
    client = MCPClient(
        command="python",
        args=["-m", "awslabs.aws_iac_mcp_server"],
        server_name="test-iac",
    )

    await client.connect()

    # First call
    tools1 = await client.list_tools()
    assert len(tools1) > 0

    # Second call - subprocess should still be alive
    tools2 = await client.list_tools()
    assert len(tools2) > 0
    assert len(tools1) == len(tools2)

    await client.disconnect()


@pytest.mark.asyncio
async def test_mcp_client_graceful_failure():
    """Test that MCPClient handles connection failures gracefully."""
    client = MCPClient(
        command="python",
        args=["-m", "nonexistent.module"],
        server_name="test-fail",
    )

    with pytest.raises(Exception):
        await client.connect()

    assert not client.is_connected()
