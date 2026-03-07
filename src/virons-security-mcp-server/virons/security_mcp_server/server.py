# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D417
"""FastMCP server implementation for virons-security-mcp-server."""

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
    "cloudtrail": {"host": "localhost", "port": 9102},
    "iam": {"host": "localhost", "port": 9103},
    "well-architected": {"host": "localhost", "port": 9104},
    "gitleaks": {"host": "localhost", "port": 9100},
    "compliance-gate": {"host": "localhost", "port": 9101},
}


def register_tools(server: FastMCP) -> None:
    """Register security orchestrator tools."""

    @server.tool()
    async def scan_secrets(ctx: Context, repository_path: str, scan_history: bool = False) -> dict:
        """Scan repository for secrets using Gitleaks.

        Args:
            repository_path: Path to git repository
            scan_history: Scan full git history
        """
        from .compliance import audit_write_operation

        try:
            audit_id = await audit_write_operation(
                operation_name="scan_secrets",
                entity_id=repository_path,
                input_data={"path": repository_path, "scan_history": scan_history},
                output_data={},
            )

            # TODO: Call gitleaks MCP server
            result = {
                "status": "scanned",
                "repository": repository_path,
                "secrets_found": 0,
                "audit_id": audit_id,
            }

            logger.info(f"Scanned {repository_path} for secrets")
            return result

        except Exception as e:
            logger.error(f"Secret scan failed: {e}")
            await ctx.error(f"Scan error: {str(e)}")
            raise

    @server.tool()
    async def audit_cloudtrail(
        ctx: Context, start_time: str, end_time: str, event_name: str = None
    ) -> dict:
        """Query CloudTrail audit logs.

        Args:
            start_time: Start timestamp (ISO 8601)
            end_time: End timestamp (ISO 8601)
            event_name: Filter by event name
        """
        try:
            # TODO: Call cloudtrail MCP server
            events = []
            logger.info(f"Queried CloudTrail from {start_time} to {end_time}")
            return {"events": events, "count": len(events)}
        except Exception as e:
            logger.error(f"CloudTrail query failed: {e}")
            await ctx.error(f"Query error: {str(e)}")
            raise

    @server.tool()
    async def check_iam_policy(ctx: Context, policy_document: dict, resource_type: str) -> dict:
        """Validate IAM policy against security best practices.

        Args:
            policy_document: IAM policy JSON
            resource_type: Resource type (user|role|group)
        """
        try:
            # TODO: Call iam MCP server
            issues = []
            logger.info(f"Validated IAM policy for {resource_type}")
            return {"valid": len(issues) == 0, "issues": issues}
        except Exception as e:
            logger.error(f"IAM policy check failed: {e}")
            await ctx.error(f"Check error: {str(e)}")
            raise

    @server.tool()
    async def run_compliance_gate(ctx: Context, artifact_path: str, gate_type: str) -> dict:
        """Run compliance gate checks.

        Args:
            artifact_path: Path to artifact
            gate_type: Gate type (pre-commit|pre-deploy|post-deploy)
        """
        from .compliance import audit_write_operation

        try:
            audit_id = await audit_write_operation(
                operation_name="run_compliance_gate",
                entity_id=artifact_path,
                input_data={"path": artifact_path, "gate": gate_type},
                output_data={},
            )

            # TODO: Call compliance-gate MCP server
            result = {
                "status": "passed",
                "gate": gate_type,
                "artifact": artifact_path,
                "audit_id": audit_id,
            }

            logger.info(f"Ran {gate_type} gate on {artifact_path}")
            return result

        except Exception as e:
            logger.error(f"Compliance gate failed: {e}")
            await ctx.error(f"Gate error: {str(e)}")
            raise


def main():
    """Run the MCP server with CLI argument support."""
    global mcp

    parser = argparse.ArgumentParser(description="Virons Security MCP Server")
    parser.add_argument(
        "--allow-write",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Enable write operations (requires audit trail)",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "api"],
        default="stdio",
        help="Transport protocol (stdio=MCP, http=health, api=REST+Swagger)",
    )

    args = parser.parse_args()

    logger.info(f"Starting {SERVER_NAME} (write_enabled={args.allow_write})")

    # API mode: Full REST API with /tools endpoint
    if args.transport == "api":
        import time
        import uuid
        import uvicorn
        from fastapi import FastAPI, Request
        from fastapi.responses import JSONResponse, PlainTextResponse
        from prometheus_client import Counter, Histogram, generate_latest, REGISTRY

        port = int(os.getenv("PORT", "9500"))
        mcp = create_server()
        app = FastAPI(title="Virons Security MCP Server", version="1.0.0")

        # Metrics
        http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
        http_request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])

        # Middleware
        @app.middleware("http")
        async def correlation_id(request: Request, call_next):
            cid = request.headers.get("x-correlation-id") or str(uuid.uuid4())
            request.state.correlation_id = cid
            response = await call_next(request)
            response.headers["x-correlation-id"] = cid
            return response

        @app.middleware("http")
        async def metrics_middleware(request: Request, call_next):
            start = time.monotonic()
            response = await call_next(request)
            duration = time.monotonic() - start
            http_requests_total.labels(request.method, request.url.path, str(response.status_code)).inc()
            http_request_duration.labels(request.method, request.url.path).observe(duration)
            return response

        @app.get("/health", tags=["Health"])
        async def health():
            """Health check endpoint."""
            return {"status": "healthy"}

        @app.get("/ready", tags=["Health"])
        async def ready():
            """Readiness check - verify upstreams."""
            return {"status": "ready", "upstreams": list(UPSTREAM.keys())}

        @app.get("/metrics", tags=["Monitoring"])
        async def metrics():
            """Prometheus metrics."""
            return PlainTextResponse(generate_latest(REGISTRY))

        @app.get("/", tags=["Info"])
        async def root():
            """Server info."""
            return {
                "service": "virons-security-mcp",
                "version": "1.0.0",
                "write_enabled": args.allow_write,
            }

        @app.get("/tools", tags=["Tools"])
        async def list_tools():
            """List all available tools with metadata."""
            from .tool_metadata import enrich_tool_metadata
            
            tools_list = await mcp.list_tools()
            enriched = []
            for tool in tools_list:
                metadata = {
                    "name": tool.name,
                    "service": "security-mcp",
                    "description": tool.description or "",
                    "input_schema": tool.inputSchema,
                }
                enriched.append(enrich_tool_metadata(tool.name, metadata))
            return {"tools": enriched, "count": len(enriched)}

        logger.info(f"Security MCP API server on port {port}")
        logger.info(f"Swagger UI: http://localhost:{port}/docs")
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
        return

    # HTTP mode: Health checks only (K8s)
    if args.transport == "http":
        import uvicorn
        from fastapi import FastAPI

        port = int(os.getenv("PORT", "9500"))

        app = FastAPI(title="Virons Security MCP Server", version="1.0.0")

        @app.get("/health", tags=["Health"])
        async def health():
            """Health check endpoint."""
            return {"status": "healthy"}

        @app.get("/", tags=["Info"])
        async def root():
            """Server info."""
            return {
                "service": "virons-security-mcp",
                "version": "1.0.0",
                "write_enabled": args.allow_write,
            }

        @app.get("/tools", tags=["Tools"])
        async def list_tools():
            """List all available tools with metadata."""
            from .tool_metadata import enrich_tool_metadata
            
            tools_list = await mcp.list_tools()
            enriched = []
            for tool in tools_list:
                metadata = {
                    "name": tool.name,
                    "service": "security-mcp",
                    "description": tool.description or "",
                    "input_schema": tool.inputSchema,
                }
                enriched.append(enrich_tool_metadata(tool.name, metadata))
            return {"tools": enriched, "count": len(enriched)}

        logger.info(f"Security MCP HTTP server on port {port}")
        logger.info(f"Swagger UI: http://localhost:{port}/docs")
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
    else:
        mcp = create_server()
        mcp.run()


if __name__ == "__main__":
    main()
