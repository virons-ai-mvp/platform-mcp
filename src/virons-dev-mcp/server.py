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

"""Virons Dev MCP Server - DevOps Orchestrator.

Orchestrates:
- Git repo research MCP
- Custom CI/CD services
- Code analysis tools
"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool


server = Server('virons-dev-mcp')

DELEGATES = {
    'git': 'http://git-repo-research-mcp-server:9070',
    'cicd': 'http://virons-cicd-service:7070',
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""


async def _list_tools_impl() -> list[Tool]:
    return [
        # Git Research MCP
        Tool(
            name='create_research_repository',
            description='Index Git repo with FAISS/Bedrock',
            inputSchema={
                'type': 'object',
                'properties': {'repository_path': {'type': 'string'}},
                'required': ['repository_path'],
            },
        ),
        Tool(
            name='search_research_repository',
            description='Semantic search in indexed repo',
            inputSchema={
                'type': 'object',
                'properties': {'repository_name': {'type': 'string'}, 'query': {'type': 'string'}},
                'required': ['repository_name', 'query'],
            },
        ),
        Tool(
            name='repository_summary',
            description='Get repo directory structure',
            inputSchema={
                'type': 'object',
                'properties': {'repository_name': {'type': 'string'}},
                'required': ['repository_name'],
            },
        ),
        Tool(
            name='list_repositories',
            description='List indexed repositories',
            inputSchema={'type': 'object'},
        ),
        Tool(
            name='access_file_or_directory',
            description='Access repo files/dirs',
            inputSchema={
                'type': 'object',
                'properties': {'filepath': {'type': 'string'}},
                'required': ['filepath'],
            },
        ),
        Tool(
            name='search_repos_on_github',
            description='Search GitHub repos by org/keywords',
            inputSchema={
                'type': 'object',
                'properties': {'org': {'type': 'string'}},
                'required': ['org'],
            },
        ),
        Tool(
            name='delete_research_repository',
            description='Delete indexed repository',
            inputSchema={
                'type': 'object',
                'properties': {'repository_name': {'type': 'string'}},
                'required': ['repository_name'],
            },
        ),
        # CI/CD
        Tool(
            name='trigger_build',
            description='Trigger CI/CD build',
            inputSchema={
                'type': 'object',
                'properties': {'pipeline': {'type': 'string'}},
                'required': ['pipeline'],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute tool."""
    result = {'tool': name, 'arguments': arguments, 'delegate': DELEGATES.get('git', 'custom')}
    return [TextContent(type='text', text=json.dumps(result, indent=2))]


async def main():
    """Run server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == '__main__':
    asyncio.run(main())
