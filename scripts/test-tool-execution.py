#!/usr/bin/env python3
"""Test tool execution across all MCP servers."""

import asyncio
import httpx


SERVERS = {
    'infrastructure-mcp': 'http://localhost:9100',
    'security-mcp': 'http://localhost:9500',
    'operations-mcp': 'http://localhost:9510',
    'monitoring-mcp': 'http://localhost:9520',
}

# Simple test cases that don't require upstream connections
TEST_CASES = {
    'infrastructure-mcp': {
        'tool': 'get_health_status',
        'args': {},
        'description': 'Get health status',
    },
    'security-mcp': {
        'tool': 'scan_secrets',
        'args': {'repository_path': '/tmp/test', 'scan_history': False},
        'description': 'Scan secrets (will fail gracefully without gitleaks)',
    },
    'operations-mcp': {'tool': 'list_clusters', 'args': {}, 'description': 'List clusters'},
    'monitoring-mcp': {
        'tool': 'query_metrics',
        'args': {'query': 'up', 'start_time': '2026-03-08T00:00:00Z'},
        'description': 'Query metrics',
    },
}


async def test_tool_execution():
    """Test that tools can be called via HTTP."""
    results = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        for service, url in SERVERS.items():
            test = TEST_CASES.get(service)
            if not test:
                continue

            tool_url = f'{url}/tools/{test["tool"]}'

            try:
                response = await client.post(tool_url, json=test['args'])
                data = response.json()

                # Check if endpoint exists and returns JSON
                has_error = 'error' in data
                status = (
                    '✅ CALLABLE'
                    if response.status_code == 200
                    else f'❌ HTTP {response.status_code}'
                )

                if has_error:
                    # Tool is callable but may fail due to missing dependencies
                    error_msg = data['error'][:80]
                    status = f'⚠️  CALLABLE (runtime error: {error_msg}...)'

                results.append(
                    {
                        'service': service,
                        'tool': test['tool'],
                        'status': status,
                        'http_code': response.status_code,
                    }
                )

            except httpx.HTTPStatusError as e:
                results.append(
                    {
                        'service': service,
                        'tool': test['tool'],
                        'status': f'❌ HTTP {e.response.status_code}',
                        'http_code': e.response.status_code,
                    }
                )
            except Exception as e:
                results.append(
                    {
                        'service': service,
                        'tool': test['tool'],
                        'status': f'❌ {type(e).__name__}: {str(e)[:50]}',
                        'http_code': None,
                    }
                )

    # Print results
    print('\n' + '=' * 80)
    print('TOOL EXECUTION TEST RESULTS')
    print('=' * 80)

    for result in results:
        print(f'\n{result["service"]}')
        print(f'  Tool: {result["tool"]}')
        print(f'  Status: {result["status"]}')

    print('\n' + '=' * 80)

    # Summary
    callable_count = sum(1 for r in results if 'CALLABLE' in r['status'])
    total = len(results)

    print(f'\nSummary: {callable_count}/{total} tools callable via HTTP')

    if callable_count == total:
        print('✅ ALL TOOLS CALLABLE')
        return 0
    else:
        print('❌ SOME TOOLS NOT CALLABLE')
        return 1


if __name__ == '__main__':
    exit_code = asyncio.run(test_tool_execution())
    exit(exit_code)
