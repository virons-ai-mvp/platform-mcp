#!/usr/bin/env python3
"""Validate MCP server configuration."""

import json
from pathlib import Path


def validate_servers():
    """Validate all MCP servers are properly configured."""
    # Check gateway config
    config_path = Path('src/virons-mcp-gateway/virons/mcp_gateway/config/services.json')
    with open(config_path) as f:
        config = json.load(f)

    configured_servers = {s['name'] for s in config['services']}
    print(f'📋 Gateway configured with {len(configured_servers)} servers\n')

    # Check actual servers
    src_path = Path('src')
    actual_servers = set()

    for server_dir in src_path.glob('virons-*-mcp'):
        server_name = server_dir.name
        actual_servers.add(server_name)

        server_py = server_dir / 'server.py'
        pyproject = server_dir / 'pyproject.toml'

        # Check files exist
        has_server = server_py.exists()
        has_pyproject = pyproject.exists()

        # Count tools
        if has_server:
            content = server_py.read_text()
            tool_count = content.count('Tool(')
            has_list_tools = '@server.list_tools()' in content
            has_call_tool = '@server.call_tool()' in content
        else:
            tool_count = 0
            has_list_tools = False
            has_call_tool = False

        # Check if in gateway config
        in_config = server_name in configured_servers

        status = '✅' if (has_server and has_pyproject and in_config and tool_count > 0) else '⚠️'

        print(f'{status} {server_name}')
        print(
            f'   Server: {"✓" if has_server else "✗"} | '
            f'Pyproject: {"✓" if has_pyproject else "✗"} | '
            f'Gateway: {"✓" if in_config else "✗"} | '
            f'Tools: {tool_count}'
        )

        if not has_list_tools and has_server:
            print('   ⚠️  Missing @server.list_tools()')
        if not has_call_tool and has_server:
            print('   ⚠️  Missing @server.call_tool()')

    # Check for servers in config but not in src
    missing = configured_servers - actual_servers
    if missing:
        print('\n⚠️  Servers in config but not found:')
        for s in missing:
            print(f'   - {s}')

    # Check for servers in src but not in config
    extra = actual_servers - configured_servers
    if extra:
        print('\n⚠️  Servers in src but not in config:')
        for s in extra:
            print(f'   - {s}')

    print(f'\n📊 Summary: {len(actual_servers)} servers, {len(configured_servers)} configured')


if __name__ == '__main__':
    validate_servers()
