# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Pydantic models for virons-security-mcp-server."""

from pydantic import BaseModel, Field


class SecretScanResult(BaseModel):
    """Secret scan result."""
    
    status: str = Field(..., description="Scan status")
    repository: str = Field(..., description="Repository path")
    secrets_found: int = Field(..., description="Number of secrets found")
    audit_id: str = Field(..., description="BaFin AT 8.1 audit trail ID")


class CloudTrailQuery(BaseModel):
    """CloudTrail query result."""
    
    events: list = Field(default_factory=list, description="CloudTrail events")
    count: int = Field(..., description="Event count")


class IAMPolicyCheck(BaseModel):
    """IAM policy validation result."""
    
    valid: bool = Field(..., description="Policy is valid")
    issues: list = Field(default_factory=list, description="Policy issues")


class ComplianceGateResult(BaseModel):
    """Compliance gate result."""
    
    status: str = Field(..., description="Gate status (passed|failed)")
    gate: str = Field(..., description="Gate type")
    artifact: str = Field(..., description="Artifact path")
    audit_id: str = Field(..., description="BaFin AT 8.1 audit trail ID")

