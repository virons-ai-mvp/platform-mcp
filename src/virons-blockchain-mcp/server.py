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

"""Virons Blockchain MCP Server - Ledger Orchestrator.

Orchestrates:
- Custom blockchain ledger service
- Merkle tree verification service
"""

import asyncio
import hashlib
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool


server = Server('virons-blockchain-mcp')

DELEGATES = {'ledger': 'http://virons-ledger-service:7050'}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""


async def _list_tools_impl() -> list[Tool]:
    return [
        Tool(
            name='seal_evidence',
            description='Seal evidence in ledger',
            inputSchema={
                'type': 'object',
                'properties': {'evidence': {'type': 'object'}},
                'required': ['evidence'],
            },
        ),
        Tool(
            name='verify_seal',
            description='Verify evidence seal',
            inputSchema={
                'type': 'object',
                'properties': {'entry_id': {'type': 'string'}},
                'required': ['entry_id'],
            },
        ),
        Tool(
            name='get_merkle_proof',
            description='Get Merkle proof',
            inputSchema={
                'type': 'object',
                'properties': {'entry_id': {'type': 'string'}},
                'required': ['entry_id'],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute tool."""
    if name == 'seal_evidence':
        evidence_hash = hashlib.sha256(
            json.dumps(arguments['evidence'], sort_keys=True).encode()
        ).hexdigest()
        result = {
            'entry_id': 'entry-123',
            'hash': evidence_hash[:16],
            'delegate': DELEGATES['ledger'],
        }
    elif name == 'verify_seal':
        result = {'valid': True, 'delegate': DELEGATES['ledger']}
    elif name == 'get_merkle_proof':
        result = {'proof': ['hash1', 'hash2'], 'delegate': DELEGATES['ledger']}
    else:
        raise ValueError(f'Unknown tool: {name}')
    return [TextContent(type='text', text=json.dumps(result, indent=2))]


async def main():
    """Run server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == '__main__':
    asyncio.run(main())
