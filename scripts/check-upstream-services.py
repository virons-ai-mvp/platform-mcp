#!/usr/bin/env python3
"""Check upstream service configuration and connectivity."""

import asyncio
import httpx
from typing import Dict


# Expected upstream services per MCP server
UPSTREAM_REQUIREMENTS = {
    'infrastructure-mcp': {
        'port': 9100,
        'upstreams': [
            {'name': 'cdk', 'port': 9140, 'type': 'AWS CDK MCP'},
            {'name': 'cfn', 'port': 9141, 'type': 'CloudFormation MCP'},
            {'name': 'terraform', 'port': 9142, 'type': 'Terraform MCP'},
            {'name': 'iac', 'port': 9143, 'type': 'IaC MCP'},
        ],
    },
    'security-mcp': {
        'port': 9500,
        'upstreams': [
            {'name': 'cloudtrail', 'port': 9102, 'type': 'CloudTrail MCP'},
            {'name': 'iam', 'port': 9103, 'type': 'IAM MCP'},
            {'name': 'well-architected', 'port': 9104, 'type': 'Well-Architected MCP'},
            {'name': 'gitleaks', 'port': 9100, 'type': 'Gitleaks MCP'},
            {'name': 'compliance-gate', 'port': 9101, 'type': 'Compliance Gate MCP'},
        ],
    },
    'operations-mcp': {
        'port': 9510,
        'upstreams': [
            {'name': 'kubernetes', 'port': 9200, 'type': 'Kubernetes MCP'},
            {'name': 'helm', 'port': 9201, 'type': 'Helm MCP'},
        ],
    },
    'monitoring-mcp': {
        'port': 9520,
        'upstreams': [
            {'name': 'prometheus', 'port': 9300, 'type': 'Prometheus MCP'},
            {'name': 'grafana', 'port': 9301, 'type': 'Grafana MCP'},
            {'name': 'elasticsearch', 'port': 9302, 'type': 'Elasticsearch MCP'},
        ],
    },
}


async def check_service(host: str, port: int, name: str) -> Dict:
    """Check if a service is reachable."""
    url = f'http://{host}:{port}/health'
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(url)
            return {
                'name': name,
                'port': port,
                'status': '✅ RUNNING'
                if response.status_code == 200
                else f'⚠️  HTTP {response.status_code}',
                'reachable': True,
            }
    except httpx.ConnectError:
        return {'name': name, 'port': port, 'status': '❌ NOT RUNNING', 'reachable': False}
    except Exception as e:
        return {
            'name': name,
            'port': port,
            'status': f'❌ ERROR: {type(e).__name__}',
            'reachable': False,
        }


async def check_all_upstreams():
    """Check all upstream services."""
    print('=' * 80)
    print('UPSTREAM SERVICE CONFIGURATION CHECK')
    print('=' * 80)

    all_missing = []

    for service, config in UPSTREAM_REQUIREMENTS.items():
        print(f'\n{service.upper()} (port {config["port"]})')
        print(f'  Required upstreams: {len(config["upstreams"])}')

        tasks = [
            check_service('localhost', upstream['port'], upstream['name'])
            for upstream in config['upstreams']
        ]
        results = await asyncio.gather(*tasks)

        running = sum(1 for r in results if r['reachable'])
        missing = [r for r in results if not r['reachable']]

        for result in results:
            print(f'    {result["status"]} {result["name"]} (port {result["port"]})')

        print(f'  Status: {running}/{len(results)} upstreams running')

        if missing:
            all_missing.extend([(service, m) for m in missing])

    print('\n' + '=' * 80)
    print('SUMMARY')
    print('=' * 80)

    if all_missing:
        print(f'\n❌ {len(all_missing)} upstream services NOT RUNNING:\n')
        for service, upstream in all_missing:
            print(f'  • {upstream["name"]} (port {upstream["port"]}) - required by {service}')

        print('\n⚠️  MCP servers will work but tools requiring upstreams will fail')
        print('\nOptions:')
        print('  1. Deploy AWS Labs MCP servers (recommended for production)')
        print('  2. Configure servers to work standalone (mock mode)')
        print('  3. Accept that upstream-dependent tools will fail gracefully')

        return 1
    else:
        print('\n✅ All upstream services are running')
        return 0


if __name__ == '__main__':
    exit_code = asyncio.run(check_all_upstreams())
    exit(exit_code)
