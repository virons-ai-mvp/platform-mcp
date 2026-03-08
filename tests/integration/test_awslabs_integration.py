"""Integration tests for AWS Labs MCP servers.

Tests verify upstream connectivity and tool functionality following TDD principles.
"""

import pytest


@pytest.mark.asyncio
async def test_infrastructure_connects_to_iac_upstream():
    """Test infrastructure-mcp connects to AWS IaC upstream."""
    from virons.infrastructure_mcp_server.domain.upstream_registry import UpstreamRegistry

    config = {
        'iac': {
            'command': 'python',
            'args': ['-m', 'awslabs.aws_iac_mcp_server'],
            'description': 'AWS IaC',
        }
    }

    registry = UpstreamRegistry(config)
    client = await registry.get_client('iac')

    assert client.is_connected()

    tools = await client.list_tools()
    assert len(tools) > 0

    await registry.close_all()


@pytest.mark.asyncio
async def test_security_connects_to_cloudtrail_upstream():
    """Test security-mcp connects to CloudTrail upstream."""
    from virons.infrastructure_mcp_server.domain.upstream_registry import UpstreamRegistry

    config = {
        'cloudtrail': {
            'command': 'python',
            'args': ['-m', 'awslabs.cloudtrail_mcp_server'],
            'description': 'AWS CloudTrail',
        }
    }

    registry = UpstreamRegistry(config)
    client = await registry.get_client('cloudtrail')

    assert client.is_connected()
    await registry.close_all()


@pytest.mark.asyncio
async def test_monitoring_connects_to_cloudwatch_upstream():
    """Test monitoring-mcp connects to CloudWatch upstream."""
    from virons.infrastructure_mcp_server.domain.upstream_registry import UpstreamRegistry

    config = {
        'cloudwatch': {
            'command': 'python',
            'args': ['-m', 'awslabs.cloudwatch_mcp_server'],
            'description': 'AWS CloudWatch',
        }
    }

    registry = UpstreamRegistry(config)
    client = await registry.get_client('cloudwatch')

    assert client.is_connected()
    await registry.close_all()
