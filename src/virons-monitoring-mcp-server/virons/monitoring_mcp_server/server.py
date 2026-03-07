# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: D417
"""FastMCP server implementation for virons-monitoring-mcp-server."""

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
    "cloudwatch": {"host": "localhost", "port": 9190},
    "prometheus": {"image": "ghcr.io/pab1it0/prometheus-mcp-server"},
    "grafana": {"image": "mcp/grafana"},
    "elasticsearch": {"image": "mcp/elasticsearch"},
}


def register_tools(server: FastMCP) -> None:
    """Register monitoring orchestrator tools."""

    @server.tool()
    async def query_metrics(
        ctx: Context, metric_name: str, start_time: str, end_time: str, source: str = "cloudwatch"
    ) -> dict:
        """Query metrics from CloudWatch, Prometheus, or Elasticsearch.

        Args:
            metric_name: Metric name
            start_time: Start time (ISO 8601)
            end_time: End time (ISO 8601)
            source: Metric source (cloudwatch|prometheus|elasticsearch)
        """
        try:
            # TODO: Call upstream MCP server based on source
            datapoints = []
            logger.info(f"Queried {metric_name} from {source}")
            return {"metric": metric_name, "datapoints": datapoints, "source": source}
        except Exception as e:
            logger.error(f"Metric query failed: {e}")
            await ctx.error(f"Query error: {str(e)}")
            raise

    @server.tool()
    async def create_alert(
        ctx: Context, name: str, metric: str, threshold: float, comparison: str
    ) -> dict:
        """Create monitoring alert rule.

        Args:
            name: Alert name
            metric: Metric to monitor
            threshold: Alert threshold
            comparison: Comparison operator (gt|lt|eq)
        """
        from .compliance import audit_write_operation

        try:
            audit_id = await audit_write_operation(
                operation_name="create_alert",
                entity_id=name,
                input_data={"metric": metric, "threshold": threshold, "comparison": comparison},
                output_data={},
            )

            # TODO: Call cloudwatch/prometheus MCP server
            result = {
                "name": name,
                "metric": metric,
                "threshold": threshold,
                "comparison": comparison,
                "audit_id": audit_id,
            }

            logger.info(f"Created alert: {name}")
            return result

        except Exception as e:
            logger.error(f"Alert creation failed: {e}")
            await ctx.error(f"Creation error: {str(e)}")
            raise

    @server.tool()
    async def create_dashboard(ctx: Context, name: str, panels: list) -> dict:
        """Create Grafana dashboard.

        Args:
            name: Dashboard name
            panels: List of panel configurations
        """
        from .compliance import audit_write_operation

        try:
            audit_id = await audit_write_operation(
                operation_name="create_dashboard",
                entity_id=name,
                input_data={"panels": panels},
                output_data={},
            )

            # TODO: Call grafana MCP server
            result = {
                "name": name,
                "panels": panels,
                "audit_id": audit_id,
            }

            logger.info(f"Created dashboard: {name}")
            return result

        except Exception as e:
            logger.error(f"Dashboard creation failed: {e}")
            await ctx.error(f"Creation error: {str(e)}")
            raise

    @server.tool()
    async def search_logs(
        ctx: Context, query: str, start_time: str, end_time: str, source: str = "elasticsearch"
    ) -> dict:
        """Search logs in Elasticsearch or CloudWatch.

        Args:
            query: Search query
            start_time: Start time (ISO 8601)
            end_time: End time (ISO 8601)
            source: Log source (elasticsearch|cloudwatch)
        """
        try:
            # TODO: Call elasticsearch/cloudwatch MCP server
            logs = []
            logger.info(f"Searched logs in {source}")
            return {"query": query, "logs": logs, "source": source}
        except Exception as e:
            logger.error(f"Log search failed: {e}")
            await ctx.error(f"Search error: {str(e)}")
            raise


def main():
    """Run the MCP server with CLI argument support."""
    global mcp

    parser = argparse.ArgumentParser(description="Virons Monitoring MCP Server")
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
        from prometheus_client import Counter, Histogram, generate_latest, REGISTRY

        port = int(os.getenv("PORT", "9520"))
        mcp = create_server()
        app = FastAPI(title="Virons Monitoring MCP Server", version="1.0.0")

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
            return {"status": "healthy"}

        @app.get("/ready", tags=["Health"])
        async def ready():
            return {"status": "ready", "upstreams": list(UPSTREAM.keys())}

        @app.get("/metrics", tags=["Monitoring"])
        async def metrics():
            return PlainTextResponse(generate_latest(REGISTRY))

        @app.get("/", tags=["Info"])
        async def root():
            return {"service": "virons-monitoring-mcp", "version": "1.0.0", "write_enabled": args.allow_write}

        @app.get("/tools", tags=["Tools"])
        async def list_tools():
            from .tool_metadata import enrich_tool_metadata
            tools_list = await mcp.list_tools()
            enriched = []
            for tool in tools_list:
                metadata = {"name": tool.name, "service": "monitoring-mcp", "description": tool.description or "", "input_schema": tool.inputSchema}
                enriched.append(enrich_tool_metadata(tool.name, metadata))
            return {"tools": enriched, "count": len(enriched)}

        logger.info(f"Monitoring MCP API server on port {port}")
        logger.info(f"Swagger UI: http://localhost:{port}/docs")
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
        return

    # HTTP mode: Health checks only (K8s)
    if args.transport == "http":

        import uvicorn
        from fastapi import FastAPI

        port = int(os.getenv("PORT", "9520"))

        app = FastAPI(title="Virons Monitoring MCP Server", version="1.0.0")

        @app.get("/health", tags=["Health"])
        async def health():
            """Health check endpoint."""
            return {"status": "healthy"}

        @app.get("/", tags=["Info"])
        async def root():
            """Server info."""
            return {
                "service": "virons-monitoring-mcp",
                "version": "1.0.0",
                "write_enabled": args.allow_write,
            }

        logger.info(f"Monitoring MCP HTTP server on port {port}")
        logger.info(f"Swagger UI: http://localhost:{port}/docs")
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
    else:
        mcp = create_server()
        mcp.run()


if __name__ == "__main__":
    main()
