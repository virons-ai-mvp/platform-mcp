#!/usr/bin/env python3
"""Test MCP tool calling via stdio."""

import asyncio
import json
import sys


async def call_tool(server_path: str, tool_name: str, arguments: dict):
    """Call a tool on an MCP server."""
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        server_path,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Initialize
    init_req = {
        'jsonrpc': '2.0',
        'id': 0,
        'method': 'initialize',
        'params': {
            'protocolVersion': '2024-11-05',
            'capabilities': {},
            'clientInfo': {'name': 'test-client', 'version': '1.0.0'},
        },
    }
    proc.stdin.write(json.dumps(init_req).encode() + b'\n')
    await proc.stdin.drain()

    # Read init response
    await proc.stdout.readline()

    # Call tool
    tool_req = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'tools/call',
        'params': {'name': tool_name, 'arguments': arguments},
    }
    proc.stdin.write(json.dumps(tool_req).encode() + b'\n')
    await proc.stdin.drain()

    # Read response
    response = await asyncio.wait_for(proc.stdout.readline(), timeout=10.0)

    proc.terminate()
    await proc.wait()

    return json.loads(response.decode())


async def test_list_iam_users():
    """Test list_iam_users from infrastructure MCP."""
    print('🧪 Testing: list_iam_users')
    try:
        result = await call_tool('src/virons-infrastructure-mcp/server.py', 'list_iam_users', {})
        print(f'✅ Result: {result}')
        return True
    except Exception as e:
        print(f'❌ Error: {e}')
        return False


async def test_check_gdpr():
    """Test check_gdpr_data_flow from compliance MCP."""
    print('\n🧪 Testing: check_gdpr_data_flow')
    try:
        result = await call_tool(
            'src/virons-compliance-mcp/server.py',
            'check_gdpr_data_flow',
            {'data_flow': 'eu-central-1 -> eu-west-1'},
        )
        print(f'✅ Result: {result}')
        return True
    except Exception as e:
        print(f'❌ Error: {e}')
        return False


async def test_seal_evidence():
    """Test seal_evidence from blockchain MCP."""
    print('\n🧪 Testing: seal_evidence')
    try:
        result = await call_tool(
            'src/virons-blockchain-mcp/server.py',
            'seal_evidence',
            {'evidence': {'id': 'test-001', 'data': 'test'}},
        )
        print(f'✅ Result: {result}')
        return True
    except Exception as e:
        print(f'❌ Error: {e}')
        return False


async def main():
    """Test MCP tool calling."""
    print('🚀 Testing MCP tool calling...\n')

    tests = [test_list_iam_users, test_check_gdpr, test_seal_evidence]

    results = []
    for test in tests:
        results.append(await test())

    passed = sum(results)
    print(f'\n📊 Results: {passed}/{len(results)} passed')


if __name__ == '__main__':
    asyncio.run(main())
