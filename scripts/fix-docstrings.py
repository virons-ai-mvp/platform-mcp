#!/usr/bin/env python3
"""Add missing docstrings to MCP servers."""

import re
from pathlib import Path


def fix_file(path: Path):
    """Fix docstrings in a file."""
    content = path.read_text()

    # Fix list_tools
    content = re.sub(
        r'(@server\.list_tools\(\)\nasync def list_tools\(\) -> list\[Tool\]:)\n(    return)',
        r'\1\n    """List available tools."""\n\2',
        content,
    )

    # Fix call_tool
    content = re.sub(
        r'(@server\.call_tool\(\)\nasync def call_tool\(name: str, arguments: dict\) -> list\[TextContent\]:)\n(    )',
        r'\1\n    """Execute tool."""\n\2',
        content,
    )

    # Fix main
    content = re.sub(
        r'(async def main\(\):)\n(    async with)', r'\1\n    """Run server."""\n\2', content
    )

    path.write_text(content)


for server_dir in Path('src').glob('virons-*-mcp'):
    server_py = server_dir / 'server.py'
    if server_py.exists():
        fix_file(server_py)
        print(f'Fixed {server_py}')


def main():
    """Fix docstrings in MCP servers."""
    pass
