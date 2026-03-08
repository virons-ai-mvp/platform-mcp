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

#!/usr/bin/env python3
"""Test script to verify MCP gateway functionality."""

import asyncio

from virons.mcp_gateway.infrastructure.mcp_client import MCPBackendClient


async def test_backend_connection():
    """Test connecting to a backend MCP server."""
    print("Testing backend MCP connection...")

    # Test with infrastructure server
    client = MCPBackendClient(
        name="infrastructure-mcp",
        command="uv",
        args=["run", "virons-infrastructure-mcp-server", "--transport", "stdio"],
    )

    try:
        await client.connect()
        print("✓ Connected to infrastructure-mcp")

        tools = await client.list_tools()
        print(f"✓ Discovered {len(tools)} tools")

        if tools:
            print("\nFirst 3 tools:")
            for tool in tools[:3]:
                print(f"  - {tool['name']}: {tool['description'][:60]}...")

        await client.disconnect()
        print("✓ Disconnected successfully")

    except Exception as e:
        print(f"✗ Error: {e}")
        raise


async def test_gateway():
    """Test the full gateway."""
    print("\n\nTesting MCP Gateway...")

    from virons.mcp_gateway.mcp_server import MCPGateway

    backend_configs = {
        "infrastructure-mcp": {
            "command": "uv",
            "args": ["run", "virons-infrastructure-mcp-server", "--transport", "stdio"],
        }
    }

    gateway = MCPGateway(backend_configs)

    try:
        await gateway.initialize()
        print(f"✓ Gateway initialized with {len(gateway.tool_to_backend)} tools")
        print(f"✓ Connected to {len(gateway.backends)} backends")

        # Show tool distribution
        backend_counts = {}
        for tool_name, backend_name in gateway.tool_to_backend.items():
            backend_counts[backend_name] = backend_counts.get(backend_name, 0) + 1

        print("\nTool distribution:")
        for backend, count in backend_counts.items():
            print(f"  {backend}: {count} tools")

        await gateway.cleanup()
        print("\n✓ Gateway cleanup successful")

    except Exception as e:
        print(f"✗ Error: {e}")
        raise


if __name__ == "__main__":
    print("=" * 60)
    print("Virons MCP Gateway Test Suite")
    print("=" * 60)

    asyncio.run(test_backend_connection())
    asyncio.run(test_gateway())

    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
