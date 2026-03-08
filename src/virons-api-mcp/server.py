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

"""Virons API MCP Server - API Gateway Orchestrator.

Orchestrates:
- OpenAPI MCP server
- Custom API gateway
- Cache services
"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool


server = Server('virons-api-mcp')

DELEGATES = {
    'openapi': 'http://openapi-mcp-server:9080',
    'gateway': 'http://virons-api-gateway:7080',
    'cache': 'http://elasticache-mcp-server:9081',
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""


async def _list_tools_impl() -> list[Tool]:
    return [
        # ElastiCache Serverless
        Tool(
            name='create_serverless_cache',
            description='Create ElastiCache serverless cache',
            inputSchema={
                'type': 'object',
                'properties': {'cache_name': {'type': 'string'}, 'engine': {'type': 'string'}},
                'required': ['cache_name'],
            },
        ),
        Tool(
            name='describe_serverless_caches',
            description='Describe serverless caches',
            inputSchema={'type': 'object', 'properties': {'cache_name': {'type': 'string'}}},
        ),
        Tool(
            name='delete_serverless_cache',
            description='Delete serverless cache',
            inputSchema={
                'type': 'object',
                'properties': {'cache_name': {'type': 'string'}},
                'required': ['cache_name'],
            },
        ),
        # ElastiCache Clusters
        Tool(
            name='create_cache_cluster',
            description='Create cache cluster',
            inputSchema={
                'type': 'object',
                'properties': {'cluster_id': {'type': 'string'}},
                'required': ['cluster_id'],
            },
        ),
        Tool(
            name='describe_cache_clusters',
            description='Describe cache clusters',
            inputSchema={'type': 'object', 'properties': {'cluster_id': {'type': 'string'}}},
        ),
        Tool(
            name='delete_cache_cluster',
            description='Delete cache cluster',
            inputSchema={
                'type': 'object',
                'properties': {'cluster_id': {'type': 'string'}},
                'required': ['cluster_id'],
            },
        ),
        # Replication Groups
        Tool(
            name='create_replication_group',
            description='Create replication group',
            inputSchema={
                'type': 'object',
                'properties': {'group_id': {'type': 'string'}},
                'required': ['group_id'],
            },
        ),
        Tool(
            name='describe_replication_groups',
            description='Describe replication groups',
            inputSchema={'type': 'object', 'properties': {'group_id': {'type': 'string'}}},
        ),
        # API Gateway
        Tool(
            name='call_rest_api',
            description='Call REST API via gateway',
            inputSchema={
                'type': 'object',
                'properties': {'url': {'type': 'string'}, 'method': {'type': 'string'}},
                'required': ['url', 'method'],
            },
        ),
        Tool(
            name='graphql_query',
            description='Execute GraphQL query',
            inputSchema={
                'type': 'object',
                'properties': {'endpoint': {'type': 'string'}, 'query': {'type': 'string'}},
                'required': ['endpoint', 'query'],
            },
        ),
        Tool(
            name='oauth_token',
            description='Get OAuth token',
            inputSchema={
                'type': 'object',
                'properties': {'provider': {'type': 'string'}},
                'required': ['provider'],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute tool."""
    result = {'tool': name, 'arguments': arguments, 'delegate': DELEGATES.get('cache', 'custom')}
    return [TextContent(type='text', text=json.dumps(result, indent=2))]


async def main():
    """Run server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == '__main__':
    asyncio.run(main())
