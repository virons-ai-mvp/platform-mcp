# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Pydantic models for virons-operations-mcp-server."""

from typing import Optional

from pydantic import BaseModel, Field


class ClusterInfo(BaseModel):
    """EKS cluster information."""

    name: str = Field(..., description="Cluster name")
    status: str = Field(..., description="Cluster status")
    version: str = Field(..., description="Kubernetes version")
    endpoint: Optional[str] = Field(None, description="API endpoint")


class FunctionDeployment(BaseModel):
    """Lambda function deployment."""

    function_name: str = Field(..., description="Function name")
    runtime: str = Field(..., description="Runtime (python3.10, nodejs20.x, etc)")
    handler: str = Field(..., description="Handler path")
    code_path: str = Field(..., description="Path to deployment package")
    audit_id: str = Field(..., description="BaFin AT 8.1 audit trail ID")


class ServiceDeployment(BaseModel):
    """ECS service deployment."""

    service_name: str = Field(..., description="Service name")
    cluster: str = Field(..., description="ECS cluster name")
    task_definition: str = Field(..., description="Task definition ARN")
    desired_count: int = Field(..., description="Desired task count")
    audit_id: str = Field(..., description="BaFin AT 8.1 audit trail ID")


class WorkflowExecution(BaseModel):
    """Step Functions workflow execution."""

    execution_arn: str = Field(..., description="Execution ARN")
    state_machine: str = Field(..., description="State machine ARN")
    status: str = Field(..., description="Execution status")
    audit_id: str = Field(..., description="BaFin AT 8.1 audit trail ID")
