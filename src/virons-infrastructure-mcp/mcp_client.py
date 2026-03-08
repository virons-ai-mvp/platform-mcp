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

"""MCP Client - Invoke MCP servers via stdio subprocess."""

import asyncio
import json
from typing import Any


async def invoke_mcp_server(
    server_path: str, tool_name: str, arguments: dict[str, Any]
) -> dict[str, Any]:
    """Invoke an MCP server via stdio subprocess.

    Args:
        server_path: Path to MCP server (e.g., "../awslabs/eks-mcp-server/server.py")
        tool_name: Tool to invoke
        arguments: Tool arguments

    Returns:
        Tool result as dict
    """
    request = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'tools/call',
        'params': {'name': tool_name, 'arguments': arguments},
    }

    proc = await asyncio.create_subprocess_exec(
        'python',
        server_path,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate(json.dumps(request).encode())

    if proc.returncode != 0:
        return {'error': f'MCP server failed: {stderr.decode()}', 'delegate': server_path}

    try:
        response = json.loads(stdout.decode())
        return response.get('result', {})
    except json.JSONDecodeError:
        return {'error': 'Invalid JSON response', 'delegate': server_path}
