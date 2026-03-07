#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Run tests for all Virons MCP servers."""

import os
import subprocess
import sys


SERVERS = [
    'virons-common',
    'virons-infrastructure-mcp-server',
    'virons-security-mcp-server',
    'virons-operations-mcp-server',
    'virons-monitoring-mcp-server',
    'virons-mcp-gateway',
]


def run_tests():
    """Run pytest for each server."""
    failed = []
    for server in SERVERS:
        server_path = f'src/{server}'
        if not os.path.exists(server_path):
            continue

        print(f'Testing {server}...')
        result = subprocess.run(
            ['uv', 'run', 'pytest', 'tests/', '-v', '--tb=short'],
            cwd=server_path,
            capture_output=True,
        )
        if result.returncode != 0:
            failed.append(server)

    if failed:
        print(f'❌ Tests failed: {", ".join(failed)}')
        return False
    return True


if __name__ == '__main__':
    if not run_tests():
        sys.exit(1)
    sys.exit(0)
