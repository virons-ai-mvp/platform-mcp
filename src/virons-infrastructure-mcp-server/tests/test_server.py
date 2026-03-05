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
        "get_cdk_guidance",
        {"question": "How do I create a Lambda function with CDK?"}
    )
    assert result is not None
    assert len(result) > 0
    data = json.loads(result[0].text)
    assert "guidance" in data
    assert isinstance(data["guidance"], str)
    assert len(data["guidance"]) > 0
