# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Pydantic models for virons-infrastructure-mcp-server."""

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class InfrastructureTool(str, Enum):
    """Supported infrastructure tools."""

    CDK = "cdk"
    CFN = "cfn"
    TERRAFORM = "terraform"
    IAC = "iac"


class StackStatus(str, Enum):
    """Stack deployment status."""

    PENDING = "pending"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    FAILED = "failed"
    DESTROYING = "destroying"
    DESTROYED = "destroyed"


class StackDeploymentRequest(BaseModel):
    """Request to deploy infrastructure stack."""

    tool: str
    stack_name: str
    template_path: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class StackDeploymentResult(BaseModel):
    """Result of stack deployment operation."""

    model_config = ConfigDict(frozen=True)

    status: str
    stack_name: str
    tool: str
    audit_id: str


class Stack(BaseModel):
    """Stack entity with lifecycle management."""

    name: str
    tool: InfrastructureTool
    status: StackStatus = StackStatus.PENDING
    outputs: Dict[str, Any] = Field(default_factory=dict)

    def mark_deploying(self) -> None:
        """Mark stack as deploying."""
        self.status = StackStatus.DEPLOYING

    def mark_deployed(self, outputs: Optional[Dict[str, Any]] = None) -> None:
        """Mark stack as deployed."""
        self.status = StackStatus.DEPLOYED
        if outputs:
            self.outputs = outputs

    def mark_failed(self) -> None:
        """Mark stack as failed."""
        self.status = StackStatus.FAILED


# Legacy models for backward compatibility
class DeployRequest(BaseModel):
    """Infrastructure deployment request."""

    tool: str = Field(..., description="IaC tool: cdk|cfn|terraform|iac")
    stack_name: str = Field(..., description="Stack/deployment name")
    template_path: str = Field(..., description="Path to template/config")
    parameters: dict = Field(default_factory=dict, description="Deployment parameters")


class DeployResponse(BaseModel):
    """Infrastructure deployment response."""

    status: str = Field(..., description="Deployment status")
    stack_name: str = Field(..., description="Stack name")
    tool: str = Field(..., description="IaC tool used")
    audit_id: str = Field(..., description="BaFin AT 8.1 audit trail ID")


class StackInfo(BaseModel):
    """Stack information."""

    name: str = Field(..., description="Stack name")
    status: str = Field(..., description="Stack status")
    created_at: str = Field(..., description="Creation timestamp")
