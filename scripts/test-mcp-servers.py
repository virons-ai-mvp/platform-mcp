#!/usr/bin/env python3
"""Sanity test MCP servers can start and list tools."""

import asyncio
import json
import random
from pathlib import Path


SERVERS = [
    'virons-infrastructure-mcp',
    'virons-forensic-mcp',
    'virons-compliance-mcp',
    'virons-security-mcp',
    'virons-ml-mcp',
]


async def test_server(server_name: str) -> bool:
    """Test if MCP server can start and list tools."""
    server_path = Path(__file__).parent.parent / 'src' / server_name / 'server.py'

    if not server_path.exists():
        print(f'❌ {server_name}: server.py not found')
        return False

    request = {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list', 'params': {}}

    try:
        proc = await asyncio.create_subprocess_exec(
            'python3',
            str(server_path),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await asyncio.wait_for(
            proc.communicate(json.dumps(request).encode()), timeout=5.0
        )

        if proc.returncode != 0:
            print(f'❌ {server_name}: exit code {proc.returncode}')
            return False

        response = json.loads(stdout.decode())
        tools = response.get('result', {}).get('tools', [])
        print(f'✅ {server_name}: {len(tools)} tools available')
        return True

    except asyncio.TimeoutError:
        print(f'⏱️  {server_name}: timeout')
        proc.kill()
        return False
    except Exception as e:
        print(f'❌ {server_name}: {type(e).__name__}: {e}')
        return False


async def main():
    """Run tests."""
    selected = random.sample(SERVERS, min(3, len(SERVERS)))
    print(f'🎲 Testing {len(selected)} random MCP servers...\n')

    results = await asyncio.gather(*[test_server(s) for s in selected])

    passed = sum(results)
    print(f'\n📊 Results: {passed}/{len(selected)} passed')


if __name__ == '__main__':
    asyncio.run(main())
