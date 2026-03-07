# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D417
"""FastMCP server implementation for virons-operations-mcp-server."""

import argparse
import os
import sys

from loguru import logger
from mcp.server.fastmcp import Context, FastMCP

from .compliance import setup_compliance_hooks
from .consts import SERVER_DEPENDENCIES, SERVER_INSTRUCTIONS, SERVER_NAME

# Configure logging
logger.remove()
logger.add(sys.stderr, level=os.getenv("FASTMCP_LOG_LEVEL", "WARNING"))

mcp = None


def create_server() -> FastMCP:
    """Create and configure the FastMCP server instance.

    Returns:
        Configured FastMCP server
    """
    server = FastMCP(
        SERVER_NAME,
        instructions=SERVER_INSTRUCTIONS,
        dependencies=SERVER_DEPENDENCIES,
    )

    # Register compliance hooks
    setup_compliance_hooks(server)

    # Register orchestrator tools
    register_tools(server)

    return server


# Upstream MCP servers
UPSTREAM = {
    "eks": {"host": "localhost", "port": 9121},
    "lambda": {"host": "localhost", "port": 9122},
    "ecs": {"host": "localhost", "port": 9123},
    "stepfunctions": {"host": "localhost", "port": 9124},
}


def register_tools(server: FastMCP) -> None:
    """Register operations orchestrator tools."""

    @server.tool()
    async def list_clusters(ctx: Context) -> dict:
        """List EKS clusters.

        Returns:
            List of cluster information
        """
        try:
            # TODO: Call eks MCP server
            clusters = []
            logger.info("Listed EKS clusters")
            return {"clusters": clusters}
        except Exception as e:
            logger.error(f"List clusters failed: {e}")
            await ctx.error(f"Error: {str(e)}")
            raise

    @server.tool()
    async def deploy_lambda(
        ctx: Context, function_name: str, runtime: str, handler: str, code_path: str
    ) -> dict:
        """Deploy Lambda function.

        Args:
            function_name: Function name
            runtime: Runtime (python3.10, nodejs20.x, etc)
            handler: Handler path
            code_path: Path to deployment package
        """
        from .compliance import audit_write_operation

        try:
            audit_id = await audit_write_operation(
                operation_name="deploy_lambda",
                entity_id=function_name,
                input_data={"runtime": runtime, "handler": handler, "code": code_path},
                output_data={},
            )

            # TODO: Call lambda MCP server
            result = {
                "function_name": function_name,
                "runtime": runtime,
                "handler": handler,
                "code_path": code_path,
                "audit_id": audit_id,
            }

            logger.info(f"Deployed Lambda function: {function_name}")
            return result

        except Exception as e:
            logger.error(f"Lambda deployment failed: {e}")
            await ctx.error(f"Deployment error: {str(e)}")
            raise

    @server.tool()
    async def deploy_ecs_service(
        ctx: Context, service_name: str, cluster: str, task_definition: str, desired_count: int
    ) -> dict:
        """Deploy ECS service.

        Args:
            service_name: Service name
            cluster: ECS cluster name
            task_definition: Task definition ARN
            desired_count: Desired task count
        """
        from .compliance import audit_write_operation

        try:
            audit_id = await audit_write_operation(
                operation_name="deploy_ecs_service",
                entity_id=service_name,
                input_data={
                    "cluster": cluster,
                    "task_def": task_definition,
                    "count": desired_count,
                },
                output_data={},
            )

            # TODO: Call ecs MCP server
            result = {
                "service_name": service_name,
                "cluster": cluster,
                "task_definition": task_definition,
                "desired_count": desired_count,
                "audit_id": audit_id,
            }

            logger.info(f"Deployed ECS service: {service_name}")
            return result

        except Exception as e:
            logger.error(f"ECS deployment failed: {e}")
            await ctx.error(f"Deployment error: {str(e)}")
            raise

    @server.tool()
    async def start_workflow(ctx: Context, state_machine_arn: str, input_data: dict) -> dict:
        """Start Step Functions workflow execution.

        Args:
            state_machine_arn: State machine ARN
            input_data: Workflow input data
        """
        from .compliance import audit_write_operation

        try:
            audit_id = await audit_write_operation(
                operation_name="start_workflow",
                entity_id=state_machine_arn,
                input_data=input_data,
                output_data={},
            )

            # TODO: Call stepfunctions MCP server
            execution_arn = f"{state_machine_arn}:execution-123"
            result = {
                "execution_arn": execution_arn,
                "state_machine": state_machine_arn,
                "status": "RUNNING",
                "audit_id": audit_id,
            }

            logger.info(f"Started workflow: {state_machine_arn}")
            return result

        except Exception as e:
            logger.error(f"Workflow start failed: {e}")
            await ctx.error(f"Start error: {str(e)}")
            raise


def main():
    """Run the MCP server with CLI argument support."""
    global mcp

    parser = argparse.ArgumentParser(description="Virons Operations MCP Server")
    parser.add_argument(
        "--allow-write",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Enable write operations (requires audit trail)",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport protocol (stdio for MCP, http for K8s probes)",
    )

    args = parser.parse_args()

    logger.info(f"Starting {SERVER_NAME} (write_enabled={args.allow_write})")

    if args.transport == "http":
        import os

        import uvicorn
        from fastapi import FastAPI

        port = int(os.getenv("PORT", "9510"))

        app = FastAPI(title="Virons Operations MCP Server", version="1.0.0")

        @app.get("/health", tags=["Health"])
        async def health():
            """Health check endpoint."""
            return {"status": "healthy"}

        @app.get("/", tags=["Info"])
        async def root():
            """Server info."""
            return {
                "service": "virons-operations-mcp",
                "version": "1.0.0",
                "write_enabled": args.allow_write,
            }

        logger.info(f"Operations MCP HTTP server on port {port}")
        logger.info(f"Swagger UI: http://localhost:{port}/docs")
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
    else:
        mcp = create_server()
        mcp.run()


if __name__ == "__main__":
    main()
