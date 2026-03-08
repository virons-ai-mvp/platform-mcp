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

"""Virons Security MCP Server - Security Orchestrator.

Orchestrates:
- AWS IAM MCP, SecurityHub, GuardDuty
- Custom security services (posture assessment, incident response)
"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool


server = Server('virons-security-mcp')

DELEGATES = {
    'iam': 'http://iam-mcp-server:9050',
    'custom_security': 'http://virons-security-service:7040',
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""


async def _list_tools_impl() -> list[Tool]:
    return [
        # IAM Security (from iam-mcp-server)
        Tool(
            name='analyze_iam_policy',
            description='Analyze IAM policy for risks',
            inputSchema={
                'type': 'object',
                'properties': {'policy': {'type': 'string'}},
                'required': ['policy'],
            },
        ),
        Tool(
            name='simulate_iam_policy',
            description='Simulate IAM policy actions',
            inputSchema={
                'type': 'object',
                'properties': {'policy': {'type': 'string'}, 'actions': {'type': 'array'}},
                'required': ['policy', 'actions'],
            },
        ),
        Tool(
            name='check_least_privilege',
            description='Check least privilege compliance',
            inputSchema={
                'type': 'object',
                'properties': {'role_name': {'type': 'string'}},
                'required': ['role_name'],
            },
        ),
        Tool(
            name='list_iam_access_keys',
            description='List IAM access keys',
            inputSchema={
                'type': 'object',
                'properties': {'user_name': {'type': 'string'}},
                'required': ['user_name'],
            },
        ),
        # Security Posture
        Tool(
            name='assess_security_posture',
            description='Assess overall security posture',
            inputSchema={
                'type': 'object',
                'properties': {'accounts': {'type': 'array'}},
                'required': ['accounts'],
            },
        ),
        Tool(
            name='list_security_findings',
            description='List security findings from SecurityHub',
            inputSchema={'type': 'object', 'properties': {'severity': {'type': 'string'}}},
        ),
        Tool(
            name='get_compliance_score',
            description='Get security compliance score',
            inputSchema={
                'type': 'object',
                'properties': {'framework': {'type': 'string'}},
                'required': ['framework'],
            },
        ),
        # Threat Detection
        Tool(
            name='list_guardduty_findings',
            description='List GuardDuty threat findings',
            inputSchema={'type': 'object', 'properties': {'severity': {'type': 'string'}}},
        ),
        Tool(
            name='analyze_threat_intel',
            description='Analyze threat intelligence',
            inputSchema={
                'type': 'object',
                'properties': {'indicator': {'type': 'string'}},
                'required': ['indicator'],
            },
        ),
        # Incident Response
        Tool(
            name='trigger_incident_response',
            description='Execute incident response playbook',
            inputSchema={
                'type': 'object',
                'properties': {'incident_id': {'type': 'string'}, 'action': {'type': 'string'}},
                'required': ['incident_id', 'action'],
            },
        ),
        Tool(
            name='isolate_resource',
            description='Isolate compromised resource',
            inputSchema={
                'type': 'object',
                'properties': {'resource_id': {'type': 'string'}},
                'required': ['resource_id'],
            },
        ),
        Tool(
            name='revoke_credentials',
            description='Revoke compromised credentials',
            inputSchema={
                'type': 'object',
                'properties': {'credential_id': {'type': 'string'}},
                'required': ['credential_id'],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute tool."""
    result = {
        'tool': name,
        'arguments': arguments,
        'delegate': DELEGATES.get('custom_security', 'custom'),
    }
    return [TextContent(type='text', text=json.dumps(result, indent=2))]


async def main():
    """Run server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == '__main__':
    asyncio.run(main())
