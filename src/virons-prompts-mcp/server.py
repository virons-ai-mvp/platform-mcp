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

"""Virons Prompts MCP Server - Prompt Library Orchestrator.

Orchestrates:
- Custom prompt registry service
- Version control system
"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool


server = Server('virons-prompts-mcp')

DELEGATES = {'registry': 'http://virons-prompt-registry:7060'}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""


async def _list_tools_impl() -> list[Tool]:
    return [
        Tool(
            name='search_prompts',
            description='Search prompt templates',
            inputSchema={
                'type': 'object',
                'properties': {'query': {'type': 'string'}},
                'required': ['query'],
            },
        ),
        Tool(
            name='get_prompt',
            description='Get prompt by ID',
            inputSchema={
                'type': 'object',
                'properties': {'id': {'type': 'string'}},
                'required': ['id'],
            },
        ),
        Tool(
            name='chain_prompts',
            description='Chain multiple prompts',
            inputSchema={
                'type': 'object',
                'properties': {'prompts': {'type': 'array'}},
                'required': ['prompts'],
            },
        ),
        Tool(
            name='version_prompt',
            description='Version a prompt',
            inputSchema={
                'type': 'object',
                'properties': {'prompt_id': {'type': 'string'}},
                'required': ['prompt_id'],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute tool."""
    if name == 'search_prompts':
        result = {
            'prompts': [{'id': 'prompt-1', 'name': 'Financial Analysis'}],
            'delegate': DELEGATES['registry'],
        }
    elif name == 'get_prompt':
        result = {
            'id': arguments['id'],
            'template': 'Analyze {company}',
            'delegate': DELEGATES['registry'],
        }
    elif name == 'chain_prompts':
        result = {'chained': 'Step 1... Step 2...', 'delegate': DELEGATES['registry']}
    elif name == 'version_prompt':
        result = {'version': '1.1', 'delegate': DELEGATES['registry']}
    else:
        raise ValueError(f'Unknown tool: {name}')
    return [TextContent(type='text', text=json.dumps(result, indent=2))]


async def main():
    """Run server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == '__main__':
    asyncio.run(main())
