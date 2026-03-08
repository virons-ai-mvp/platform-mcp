#!/usr/bin/env python3
"""Validate AWS Labs MCP integration."""

import asyncio
import sys
from virons.common import MCPClient


async def test_infrastructure_iac():
    """Test infrastructure-mcp IaC connection."""
    print('Testing infrastructure-mcp → AWS Labs IaC...')
    client = MCPClient(
        command='/app/.venv/bin/python',
        args=['-m', 'awslabs.aws_iac_mcp_server.server'],
        server_name='iac',
    )

    try:
        await client.connect()
        assert client.is_connected(), 'Failed to connect'

        tools = await client.list_tools()
        assert len(tools) == 9, f'Expected 9 tools, got {len(tools)}'

        # Test multiple calls
        tools2 = await client.list_tools()
        assert len(tools2) == 9, 'Second call failed'

        print(f'  ✅ Connected, {len(tools)} tools available')
        print('  ✅ Multiple calls work')

        await client.disconnect()
        assert not client.is_connected(), 'Failed to disconnect'
        print('  ✅ Disconnected cleanly')

        return True
    except Exception as e:
        print(f'  ❌ Error: {e}')
        return False


async def main():
    """Run all validation tests."""
    print('\n🔍 AWS Labs MCP Integration Validation\n')

    results = []

    # Test infrastructure
    results.append(await test_infrastructure_iac())

    print(f'\n{"=" * 50}')
    passed = sum(results)
    total = len(results)
    print(f'Results: {passed}/{total} tests passed')

    if passed == total:
        print('✅ All tests passed!')
        return 0
    else:
        print('❌ Some tests failed')
        return 1


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
