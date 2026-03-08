#!/usr/bin/env python3
"""Sanity check all MCP gateway tools."""

import requests
import sys


def check_tools():
    """Verify all tools have required fields."""
    try:
        response = requests.get('http://localhost:9000/tools', timeout=5)
        response.raise_for_status()
        data = response.json()

        tools = data.get('tools', [])
        print(f'✓ Found {len(tools)} tools\n')

        errors = []
        warnings = []
        by_service = {}

        for tool in tools:
            name = tool.get('name', 'UNNAMED')
            service = tool.get('service', 'unknown')

            # Track by service
            if service not in by_service:
                by_service[service] = {'total': 0, 'errors': 0}
            by_service[service]['total'] += 1

            # Check required fields
            if not tool.get('name'):
                errors.append('❌ Tool missing name')
                by_service[service]['errors'] += 1
                continue

            if not tool.get('description'):
                errors.append(f'❌ {name}: Missing description')
                by_service[service]['errors'] += 1

            # Accept both camelCase and snake_case
            schema = tool.get('inputSchema') or tool.get('input_schema')
            if not schema or schema == {}:
                errors.append(f'❌ {name} ({service}): Empty or missing input schema')
                by_service[service]['errors'] += 1
            elif schema.get('type') != 'object':
                errors.append(
                    f"❌ {name}: Schema type must be 'object', got '{schema.get('type')}'"
                )
                by_service[service]['errors'] += 1

            # Check Args documentation
            desc = tool.get('description', '')
            has_params = schema and schema.get('properties')
            if has_params and 'Args:' not in desc:
                warnings.append(f'⚠️  {name}: Has parameters but no Args documentation')

            # Check service field
            if not tool.get('service'):
                warnings.append(f'⚠️  {name}: Missing service field')

        # Print results
        if errors:
            print('ERRORS:')
            print('\n'.join(errors))
        if warnings:
            print('\nWARNINGS:')
            print('\n'.join(warnings))

        print(f'\n{"=" * 60}')
        print('BY SERVICE:')
        for svc, stats in sorted(by_service.items()):
            status = '✅' if stats['errors'] == 0 else '❌'
            print(f'{status} {svc}: {stats["total"]} tools, {stats["errors"]} errors')

        print(f'\n{"=" * 60}')
        print(f'Total: {len(tools)} tools | Errors: {len(errors)} | Warnings: {len(warnings)}')

        if errors:
            print('❌ FAILED - Critical issues found')
            return 1
        elif warnings:
            print('⚠️  PASSED with warnings')
            return 0
        else:
            print('✅ PASSED - All tools valid')
            return 0

    except requests.exceptions.ConnectionError:
        print('❌ Cannot connect to gateway at http://localhost:9000')
        print('Run: docker-compose up -d')
        return 1
    except Exception as e:
        print(f'❌ Error: {e}')
        return 1


if __name__ == '__main__':
    sys.exit(check_tools())
