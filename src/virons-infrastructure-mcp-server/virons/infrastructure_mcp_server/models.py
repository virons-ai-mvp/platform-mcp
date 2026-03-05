# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Pydantic models for virons-infrastructure-mcp-server."""

from pydantic import BaseModel, Field


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

