# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for domain models."""

import pytest
from pydantic import ValidationError

from virons.infrastructure_mcp_server.models import (
    InfrastructureTool,
    Stack,
    StackDeploymentRequest,
    StackDeploymentResult,
    StackStatus,
)


def test_stack_deployment_request_validation():
    """Test StackDeploymentRequest validates required fields."""
    with pytest.raises(ValidationError):
        StackDeploymentRequest(tool="cdk")  # Missing stack_name

    request = StackDeploymentRequest(
        tool="cdk",
        stack_name="my-stack",
        template_path="/path/to/template",
        parameters={"key": "value"},
    )
    assert request.tool == "cdk"
    assert request.stack_name == "my-stack"


def test_stack_deployment_result_immutable():
    """Test StackDeploymentResult is immutable value object."""
    result = StackDeploymentResult(
        status="deployed", stack_name="my-stack", tool="cdk", audit_id="audit-123"
    )
    with pytest.raises(ValidationError):
        result.status = "failed"


def test_infrastructure_tool_enum():
    """Test InfrastructureTool enum validates tool names."""
    assert InfrastructureTool.CDK.value == "cdk"
    assert InfrastructureTool.CFN.value == "cfn"
    with pytest.raises(ValueError):
        InfrastructureTool("invalid")


def test_stack_entity_lifecycle():
    """Test Stack entity tracks deployment lifecycle."""
    stack = Stack(name="my-stack", tool=InfrastructureTool.CDK)
    assert stack.status == StackStatus.PENDING

    stack.mark_deploying()
    assert stack.status == StackStatus.DEPLOYING

    stack.mark_deployed(outputs={"url": "https://..."})
    assert stack.status == StackStatus.DEPLOYED
    assert stack.outputs["url"] == "https://..."
