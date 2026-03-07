# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for server.py."""

import json

import pytest

from virons.infrastructure_mcp_server.server import create_server


def test_create_server():
    """Test server creation."""
    server = create_server()
    assert server is not None
    assert server.name == "virons.infrastructure-mcp-server"


@pytest.mark.asyncio
async def test_get_cdk_guidance():
    """Test CDK guidance tool."""
    server = create_server()
    result = await server.call_tool(
        "get_cdk_guidance", {"question": "How do I create a Lambda function with CDK?"}
    )
    assert result is not None
    assert len(result) > 0
    data = json.loads(result[0].text)
    assert "guidance" in data
    assert isinstance(data["guidance"], str)
    assert len(data["guidance"]) > 0


@pytest.mark.asyncio
async def test_explain_cdk_nag_rule():
    """Test CDK Nag rule explanation tool."""
    server = create_server()
    result = await server.call_tool("explain_cdk_nag_rule", {"rule_id": "AwsSolutions-IAM4"})
    data = json.loads(result[0].text)
    assert "rule_id" in data
    assert "explanation" in data
    assert isinstance(data["explanation"], str)


@pytest.mark.asyncio
async def test_check_cdk_nag_suppressions():
    """Test CDK Nag suppressions check tool."""
    server = create_server()
    result = await server.call_tool("check_cdk_nag_suppressions", {"stack_path": "/path/to/stack"})
    data = json.loads(result[0].text)
    assert "stack_path" in data
    assert "suppressions" in data
    assert isinstance(data["suppressions"], list)


@pytest.mark.asyncio
async def test_generate_bedrock_agent_schema():
    """Test Bedrock agent schema generation tool."""
    server = create_server()
    result = await server.call_tool(
        "generate_bedrock_agent_schema", {"agent_name": "test-agent", "description": "Test agent"}
    )
    data = json.loads(result[0].text)
    assert "agent_name" in data
    assert "schema" in data
    assert "audit_id" in data


@pytest.mark.asyncio
async def test_get_solutions_construct_pattern():
    """Test Solutions Construct pattern lookup tool."""
    server = create_server()
    result = await server.call_tool(
        "get_solutions_construct_pattern", {"pattern_name": "aws-lambda-dynamodb"}
    )
    data = json.loads(result[0].text)
    assert "pattern_name" in data
    assert "pattern" in data


@pytest.mark.asyncio
async def test_search_genai_cdk_constructs():
    """Test GenAI CDK constructs search tool."""
    server = create_server()
    result = await server.call_tool("search_genai_cdk_constructs", {"query": "bedrock"})
    data = json.loads(result[0].text)
    assert "query" in data
    assert "constructs" in data
    assert isinstance(data["constructs"], list)


@pytest.mark.asyncio
async def test_get_lambda_layer_docs():
    """Test Lambda layer documentation tool."""
    server = create_server()
    result = await server.call_tool(
        "get_lambda_layer_docs", {"layer_name": "AWSLambdaPowertoolsPythonV2"}
    )
    data = json.loads(result[0].text)
    assert "layer_name" in data
    assert "documentation" in data
