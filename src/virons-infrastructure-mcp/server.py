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

"""Virons Infrastructure MCP Server - AWS Infrastructure Orchestrator.

Orchestrates calls to:
- AWS Labs MCP servers (EKS, Cost Explorer, CloudFormation, etc.)
- Custom business services (CMDB, provisioning, inventory).
"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pathlib import Path


server = Server('virons-infrastructure-mcp')

# AWS Labs MCP server paths
AWSLABS_PATH = Path(__file__).parent.parent / 'awslabs'
DELEGATES = {
    'eks': str(AWSLABS_PATH / 'eks-mcp-server' / 'awslabs' / 'eks_mcp_server' / 'server.py'),
    'cost': str(
        AWSLABS_PATH
        / 'cost-explorer-mcp-server'
        / 'awslabs'
        / 'cost_explorer_mcp_server'
        / 'server.py'
    ),
    'cfn': str(AWSLABS_PATH / 'cfn-mcp-server' / 'awslabs' / 'cfn_mcp_server' / 'server.py'),
    'iam': str(AWSLABS_PATH / 'iam-mcp-server' / 'awslabs' / 'iam_mcp_server' / 'server.py'),
    'cloudwatch': str(
        AWSLABS_PATH / 'cloudwatch-mcp-server' / 'awslabs' / 'cloudwatch_mcp_server' / 'server.py'
    ),
    'network': str(
        AWSLABS_PATH
        / 'aws-network-mcp-server'
        / 'awslabs'
        / 'aws_network_mcp_server'
        / 'server.py'
    ),
    'terraform': str(
        AWSLABS_PATH / 'terraform-mcp-server' / 'awslabs' / 'terraform_mcp_server' / 'server.py'
    ),
}


async def invoke_mcp_server(server_path: str, tool_name: str, arguments: dict) -> dict:
    """Invoke MCP server via stdio subprocess."""
    request = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'tools/call',
        'params': {'name': tool_name, 'arguments': arguments},
    }

    proc = await asyncio.create_subprocess_exec(
        'python3',
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


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""


async def _list_tools_impl() -> list[Tool]:
    """List all available infrastructure tools."""
    return [
        # EKS Tools (from eks-mcp-server)
        Tool(
            name='manage_eks_stacks',
            description='Manage EKS CloudFormation stacks (generate/deploy/describe/delete)',
            inputSchema={
                'type': 'object',
                'properties': {
                    'operation': {
                        'type': 'string',
                        'enum': ['generate', 'deploy', 'describe', 'delete'],
                    },
                    'cluster_name': {'type': 'string'},
                    'template_file': {'type': 'string'},
                },
                'required': ['operation', 'cluster_name'],
            },
        ),
        Tool(
            name='manage_k8s_resource',
            description='Manage Kubernetes resources (create/replace/patch/delete/read)',
            inputSchema={
                'type': 'object',
                'properties': {
                    'operation': {'type': 'string'},
                    'cluster_name': {'type': 'string'},
                    'kind': {'type': 'string'},
                    'api_version': {'type': 'string'},
                    'name': {'type': 'string'},
                    'namespace': {'type': 'string'},
                    'body': {'type': 'object'},
                },
                'required': ['operation', 'cluster_name', 'kind'],
            },
        ),
        Tool(
            name='apply_yaml',
            description='Apply Kubernetes YAML manifests to EKS cluster',
            inputSchema={
                'type': 'object',
                'properties': {
                    'yaml_path': {'type': 'string'},
                    'cluster_name': {'type': 'string'},
                    'namespace': {'type': 'string'},
                    'force': {'type': 'boolean'},
                },
                'required': ['yaml_path', 'cluster_name'],
            },
        ),
        Tool(
            name='list_k8s_resources',
            description='List Kubernetes resources in EKS cluster',
            inputSchema={
                'type': 'object',
                'properties': {
                    'cluster_name': {'type': 'string'},
                    'kind': {'type': 'string'},
                    'api_version': {'type': 'string'},
                    'namespace': {'type': 'string'},
                },
                'required': ['cluster_name', 'kind'],
            },
        ),
        # IAM Tools (from iam-mcp-server)
        Tool(
            name='list_iam_users',
            description='List IAM users with optional filtering',
            inputSchema={'type': 'object', 'properties': {'path_prefix': {'type': 'string'}}},
        ),
        Tool(
            name='get_iam_user',
            description='Get detailed IAM user info including policies and access keys',
            inputSchema={
                'type': 'object',
                'properties': {'user_name': {'type': 'string'}},
                'required': ['user_name'],
            },
        ),
        Tool(
            name='list_iam_roles',
            description='List IAM roles with optional filtering',
            inputSchema={'type': 'object', 'properties': {'path_prefix': {'type': 'string'}}},
        ),
        Tool(
            name='create_iam_role',
            description='Create IAM role with trust policy',
            inputSchema={
                'type': 'object',
                'properties': {
                    'role_name': {'type': 'string'},
                    'trust_policy': {'type': 'object'},
                },
                'required': ['role_name', 'trust_policy'],
            },
        ),
        Tool(
            name='list_iam_groups',
            description='List IAM groups with optional filtering',
            inputSchema={'type': 'object', 'properties': {'path_prefix': {'type': 'string'}}},
        ),
        # Cost Tools (from cost-explorer-mcp-server)
        Tool(
            name='get_cost_and_usage',
            description='Get AWS cost and usage data',
            inputSchema={
                'type': 'object',
                'properties': {
                    'start_date': {'type': 'string'},
                    'end_date': {'type': 'string'},
                    'granularity': {'type': 'string'},
                    'metrics': {'type': 'array'},
                },
                'required': ['start_date', 'end_date'],
            },
        ),
        # CloudFormation Tools (from cfn-mcp-server)
        Tool(
            name='create_stack',
            description='Create CloudFormation stack',
            inputSchema={
                'type': 'object',
                'properties': {
                    'stack_name': {'type': 'string'},
                    'template_body': {'type': 'string'},
                    'parameters': {'type': 'array'},
                },
                'required': ['stack_name', 'template_body'],
            },
        ),
        Tool(
            name='describe_stacks',
            description='Describe CloudFormation stacks',
            inputSchema={'type': 'object', 'properties': {'stack_name': {'type': 'string'}}},
        ),
        # CloudWatch Tools (from cloudwatch-mcp-server)
        Tool(
            name='get_metric_statistics',
            description='Get CloudWatch metric statistics',
            inputSchema={
                'type': 'object',
                'properties': {
                    'namespace': {'type': 'string'},
                    'metric_name': {'type': 'string'},
                    'start_time': {'type': 'string'},
                    'end_time': {'type': 'string'},
                },
                'required': ['namespace', 'metric_name'],
            },
        ),
        # Network Tools (from aws-network-mcp-server)
        Tool(
            name='describe_vpcs',
            description='Describe VPCs',
            inputSchema={'type': 'object', 'properties': {'vpc_ids': {'type': 'array'}}},
        ),
        Tool(
            name='create_vpc',
            description='Create VPC',
            inputSchema={
                'type': 'object',
                'properties': {'cidr_block': {'type': 'string'}},
                'required': ['cidr_block'],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute tool."""
    """Execute infrastructure tool by delegating to appropriate backend."""
    # EKS tools
    if name in ['manage_eks_stacks', 'manage_k8s_resource', 'apply_yaml', 'list_k8s_resources']:
        result = await invoke_mcp_server(
            DELEGATES['eks'], 'tools/call', {'name': name, 'arguments': arguments}
        )
    # IAM tools
    elif name in [
        'list_iam_users',
        'get_iam_user',
        'list_iam_roles',
        'create_iam_role',
        'list_iam_groups',
    ]:
        # Mock response for testing (AWS Labs servers need installation)
        result = {
            'users': [
                {
                    'UserName': 'admin',
                    'UserId': 'AIDAI123',
                    'Arn': 'arn:aws:iam::123456789012:user/admin',
                },
                {
                    'UserName': 'developer',
                    'UserId': 'AIDAI456',
                    'Arn': 'arn:aws:iam::123456789012:user/developer',
                },
            ],
            'delegate': 'iam-mcp-server (mock)',
        }
    # Cost tools
    elif name == 'get_cost_and_usage':
        result = await invoke_mcp_server(
            DELEGATES['cost'], 'tools/call', {'name': name, 'arguments': arguments}
        )
    # CloudFormation tools
    elif name in ['create_stack', 'describe_stacks']:
        result = await invoke_mcp_server(
            DELEGATES['cfn'], 'tools/call', {'name': name, 'arguments': arguments}
        )
    # CloudWatch tools
    elif name == 'get_metric_statistics':
        result = await invoke_mcp_server(
            DELEGATES['cloudwatch'], 'tools/call', {'name': name, 'arguments': arguments}
        )
    # Network tools
    elif name in ['describe_vpcs', 'create_vpc']:
        result = await invoke_mcp_server(
            DELEGATES['network'], 'tools/call', {'name': name, 'arguments': arguments}
        )
    else:
        result = {'error': f'Unknown tool: {name}'}

    return [TextContent(type='text', text=json.dumps(result, indent=2))]


async def main():
    """Run MCP server via stdio."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == '__main__':
    asyncio.run(main())
