# Copyright Virons Fintech. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    "cloudtrail": {
        "command": "/app/.venv/bin/python",
        "args": ["-m", "awslabs.cloudtrail_mcp_server.server"],
        "description": "AWS CloudTrail MCP Server",
    },
    "iam": {
        "command": "/app/.venv/bin/python",
        "args": ["-m", "awslabs.iam_mcp_server.server"],
        "description": "AWS IAM MCP Server",
    },
    "well_architected": {
        "command": "/app/.venv/bin/python",
        "args": ["-m", "awslabs.well_architected_security_mcp_server.server"],
        "description": "AWS Well-Architected Security MCP Server",
    },
}

# Global proxy instance
_proxy = None


def get_proxy():
    """Get or create upstream proxy instance."""
    global _proxy
    if _proxy is None:
        from virons.common.upstream_proxy import UpstreamProxy

        _proxy = UpstreamProxy(UPSTREAM)
    return _proxy


def register_tools(server: FastMCP) -> None:
    """Register security orchestrator tools."""
    # Register core orchestrated tools (with business logic)
    register_core_tools(server)

    # Register proxy tools (auto-forwarded from upstreams)
    register_proxy_tools(server)


def register_core_tools(server: FastMCP) -> None:
    """Register core tools with orchestration logic."""

    @server.tool()
    async def scan_secrets(ctx: Context, repository_path: str, scan_history: bool = False) -> dict:
        """Scan repository for secrets using Gitleaks.

        Args:
            repository_path: Path to git repository
            scan_history: Scan full git history
        """
        from .application.secret_scan_service import SecretScanService
        from .compliance import audit_write_operation

        try:
            correlation_id = (
                ctx.request_context.get("correlation_id")
                if hasattr(ctx, "request_context")
                else None
            )

            service = SecretScanService()
            findings = await service.scan_repository(repository_path, scan_history, correlation_id)

            audit_id = await audit_write_operation(
                operation_name="scan_secrets",
                entity_id=repository_path,
                input_data={"path": repository_path, "scan_history": scan_history},
                output_data={"secrets_found": len(findings)},
            )

            result = {
                "status": "scanned",
                "repository": repository_path,
                "secrets_found": len(findings),
                "findings": findings,
                "audit_id": audit_id,
            }

            logger.info(f"Scanned {repository_path} for secrets - found {len(findings)}")
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
        from .application.audit_service import AuditService

        try:
            correlation_id = (
                ctx.request_context.get("correlation_id")
                if hasattr(ctx, "request_context")
                else None
            )

            service = AuditService()
            events = await service.query_events(start_time, end_time, event_name, correlation_id)

            logger.info(
                f"Queried CloudTrail from {start_time} to {end_time} - found {len(events)} events"
            )
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
        from .application.policy_validation_service import PolicyValidationService

        try:
            correlation_id = (
                ctx.request_context.get("correlation_id")
                if hasattr(ctx, "request_context")
                else None
            )

            service = PolicyValidationService()
            result = await service.validate_policy(policy_document, resource_type, correlation_id)

            logger.info(
                f"Validated IAM policy for {resource_type} - valid: {result.get('valid', False)}"
            )
            return result
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
        from .application.compliance_service import ComplianceService
        from .compliance import audit_write_operation

        try:
            correlation_id = (
                ctx.request_context.get("correlation_id")
                if hasattr(ctx, "request_context")
                else None
            )

            service = ComplianceService()
            gate_result = await service.run_gate(artifact_path, gate_type, correlation_id)

            audit_id = await audit_write_operation(
                operation_name="run_compliance_gate",
                entity_id=artifact_path,
                input_data={"path": artifact_path, "gate": gate_type},
                output_data={"status": gate_result.get("status", "unknown")},
            )

            result = {
                "status": gate_result.get("status", "unknown"),
                "gate": gate_type,
                "artifact": artifact_path,
                "checks_passed": gate_result.get("checks_passed", 0),
                "checks_failed": gate_result.get("checks_failed", 0),
                "audit_id": audit_id,
            }

            logger.info(f"Ran {gate_type} gate on {artifact_path} - status: {result['status']}")
            return result

        except Exception as e:
            logger.error(f"Compliance gate failed: {e}")
            await ctx.error(f"Gate error: {str(e)}")
            raise


def register_proxy_tools(server: FastMCP) -> None:
    """Register proxy tools that auto-forward to upstreams."""
    import asyncio

    # Core tools we've already implemented
    core_tools = {"scan_secrets", "audit_cloudtrail", "check_iam_policy", "run_compliance_gate"}

    async def discover_and_register():
        """Discover upstream tools and register proxies."""
        proxy = get_proxy()

        try:
            discovered = await proxy.discover_tools()
            total_tools = sum(len(tools) for tools in discovered.values())
            logger.info(f"Discovered {total_tools} tools from {len(discovered)} upstreams")

            for upstream_name, tool_names in discovered.items():
                for tool_name in tool_names:
                    if tool_name not in core_tools:
                        register_proxy_tool(server, tool_name, upstream_name)

        except Exception as e:
            logger.warning(f"Failed to discover upstream tools: {e}")

    try:
        asyncio.create_task(discover_and_register())
    except RuntimeError:
        logger.debug("Event loop not ready, deferring tool discovery")


def register_proxy_tool(server: FastMCP, tool_name: str, upstream_name: str) -> None:
    """Register a single proxy tool."""

    @server.tool(name=tool_name)
    async def proxy_handler(ctx: Context, **kwargs) -> dict:
        """Auto-generated proxy handler."""
        proxy = get_proxy()
        correlation_id = (
            ctx.request_context.get("correlation_id") if hasattr(ctx, "request_context") else None
        )

        try:
            result = await proxy.call_tool(tool_name, kwargs, correlation_id)
            logger.debug(f"Proxied {tool_name} to {upstream_name}")
            return result
        except Exception as e:
            logger.error(f"Proxy call {tool_name} failed: {e}")
            await ctx.error(f"Proxy error: {str(e)}")
            raise

    proxy_handler.__doc__ = f"[Proxy] Forward to {upstream_name}.{tool_name}"


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
        from fastapi.responses import PlainTextResponse
        from prometheus_client import REGISTRY, Counter, Histogram, generate_latest

        port = int(os.getenv("PORT", "9500"))
        mcp = create_server()
        app = FastAPI(title="Virons Security MCP Server", version="1.0.0")

        # Metrics
        http_requests_total = Counter(
            "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
        )
        http_request_duration = Histogram(
            "http_request_duration_seconds", "HTTP request duration", ["method", "endpoint"]
        )

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
            http_requests_total.labels(
                request.method, request.url.path, str(response.status_code)
            ).inc()
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

        @app.post("/tools/{tool_name}", tags=["Tools"])
        async def execute_tool(tool_name: str, request: dict):
            """Execute a tool by name."""
            try:
                content, result = await mcp.call_tool(tool_name, request)
                return result
            except Exception as e:
                return {"error": f"Error executing tool {tool_name}: {str(e)}"}

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
