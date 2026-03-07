# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""FastAPI REST API with Swagger documentation."""

from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel, Field
from starlette.responses import Response

from .infrastructure.health import HealthChecker
from .infrastructure.metrics import MetricsCollector


class DeployRequest(BaseModel):
    """Deploy infrastructure request."""

    tool: str = Field(..., description="Tool to use: cdk, cfn, terraform, iac")
    stack_name: str = Field(..., description="Stack name")
    template_path: Optional[str] = Field(None, description="Template file path")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Deployment parameters")


class DestroyRequest(BaseModel):
    """Destroy infrastructure request."""

    tool: str = Field(..., description="Tool to use: cdk, cfn, terraform, iac")
    stack_name: str = Field(..., description="Stack name to destroy")
    confirmation: str = Field(..., description="Must be 'yes' to confirm")


class StackInfo(BaseModel):
    """Stack information."""

    name: str
    status: str
    tool: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    checks: Dict[str, Any]


def create_api(
    health_checker: HealthChecker, deploy_service, list_service, destroy_service
) -> FastAPI:
    """Create FastAPI application with Swagger UI.

    Args:
        health_checker: Health checker instance
        deploy_service: Deploy service instance
        list_service: List service instance
        destroy_service: Destroy service instance

    Returns:
        FastAPI application
    """
    app = FastAPI(
        title="Virons Infrastructure MCP Server",
        description="Infrastructure orchestration API - wraps CDK, CloudFormation, Terraform, IaC",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    metrics = MetricsCollector()

    @app.get("/health", tags=["Health"])
    async def health():
        """Simple health check for Docker."""
        return {"status": "healthy"}

    @app.get("/health/live", response_model=HealthResponse, tags=["Health"])
    async def liveness():
        """Liveness probe - checks if server is running."""
        result = await health_checker.liveness()
        return result

    @app.get("/health/ready", response_model=HealthResponse, tags=["Health"])
    async def readiness():
        """Readiness probe - checks if server can handle requests."""
        result = await health_checker.readiness()
        if result["status"] != "healthy":
            raise HTTPException(status_code=503, detail=result)
        return result

    @app.get("/metrics", tags=["Monitoring"])
    async def prometheus_metrics():
        """Prometheus metrics endpoint."""
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @app.post("/api/v1/deploy", response_model=Dict[str, Any], tags=["Infrastructure"])
    async def deploy_infrastructure(request: DeployRequest):
        """Deploy infrastructure using specified tool.

        Supports:
        - AWS CDK
        - CloudFormation
        - Terraform
        - Generic IaC
        """
        try:
            result = await deploy_service.deploy_infrastructure(
                tool=request.tool,
                stack_name=request.stack_name,
                template_path=request.template_path,
                parameters=request.parameters or {},
            )
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/v1/destroy", response_model=Dict[str, Any], tags=["Infrastructure"])
    async def destroy_infrastructure(request: DestroyRequest):
        """Destroy infrastructure stack.

        Requires confirmation='yes' to proceed.
        """
        if request.confirmation != "yes":
            raise HTTPException(status_code=400, detail="Confirmation required")

        try:
            result = await destroy_service.destroy_infrastructure(
                tool=request.tool, stack_name=request.stack_name
            )
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/v1/stacks", response_model=List[StackInfo], tags=["Infrastructure"])
    async def list_stacks(tool: Optional[str] = None):
        """List infrastructure stacks.

        Args:
            tool: Filter by tool (cdk, cfn, terraform, iac)
        """
        try:
            result = await list_service.list_stacks(tool=tool)
            return result.get("stacks", [])
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/v1/info", tags=["Server"])
    async def server_info():
        """Get server information."""
        return {
            "name": "virons-infrastructure-mcp-server",
            "version": "0.1.0",
            "supported_tools": ["cdk", "cfn", "terraform", "iac"],
            "compliance": ["BaFin MaRisk AT 8.1", "GDPR Art 32", "DORA Art 11", "EU AI Act"],
            "features": [
                "Multi-tool orchestration",
                "Compliance logging",
                "Prometheus metrics",
                "Health checks",
                "Swagger API",
            ],
        }

    return app
