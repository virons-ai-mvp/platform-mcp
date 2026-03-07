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
    "cloudwatch": {"host": "localhost", "port": 9109},
    "prometheus": {"host": "localhost", "port": 9110},
    "grafana": {"host": "localhost", "port": 9111},
    "elasticsearch": {"host": "localhost", "port": 9112},
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
    """Register monitoring orchestrator tools."""
    
    # Register core orchestrated tools (with business logic)
    register_core_tools(server)
    
    # Register proxy tools (auto-forwarded from upstreams)
    register_proxy_tools(server)


def register_core_tools(server: FastMCP) -> None:
    """Register core tools with orchestration logic."""

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
        from .application.metrics_service import MetricsService
        from .domain.metric import MetricQuery
        
        try:
            service = MetricsService()
            query = MetricQuery(metric_name, start_time, end_time, source)
            
            # Get correlation ID from context if available
            correlation_id = getattr(ctx, 'correlation_id', None)
            
            metrics = await service.query_metrics(query, correlation_id)
            
            datapoints = [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "value": m.value,
                    "labels": m.labels
                }
                for m in metrics
            ]
            
            logger.info(f"Queried {metric_name} from {source}: {len(datapoints)} points")
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
        from .application.alert_service import AlertService
        from .domain.alert import Alert

        try:
            # Create domain entity
            alert = Alert(name, metric, threshold, comparison)
            
            # Audit write operation
            audit_id = await audit_write_operation(
                operation_name="create_alert",
                entity_id=name,
                input_data={"metric": metric, "threshold": threshold, "comparison": comparison},
                output_data={},
            )

            # Create alert via service
            service = AlertService()
            correlation_id = getattr(ctx, 'correlation_id', None)
            result = await service.create_alert(alert, correlation_id)
            
            result["audit_id"] = audit_id
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
        from .application.dashboard_service import DashboardService
        from .domain.dashboard import Dashboard, Panel

        try:
            # Convert panels to domain entities
            panel_entities = [
                Panel(
                    title=p.get("title", "Untitled"),
                    query=p.get("query", ""),
                    type=p.get("type", "graph"),
                    datasource=p.get("datasource", "prometheus")
                )
                for p in panels
            ]
            
            # Create domain entity
            dashboard = Dashboard(name, panel_entities, tags=panels[0].get("tags", []) if panels else [])
            
            # Audit write operation
            audit_id = await audit_write_operation(
                operation_name="create_dashboard",
                entity_id=name,
                input_data={"panels": panels},
                output_data={},
            )

            # Create dashboard via service
            service = DashboardService()
            correlation_id = getattr(ctx, 'correlation_id', None)
            result = await service.create_dashboard(dashboard, correlation_id)
            
            result["audit_id"] = audit_id
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
        from .application.log_service import LogService
        from .domain.log_entry import LogQuery
        
        try:
            service = LogService()
            log_query = LogQuery(query, start_time, end_time, source)
            
            # Get correlation ID from context if available
            correlation_id = getattr(ctx, 'correlation_id', None)
            
            logs = await service.search_logs(log_query, correlation_id)
            
            log_entries = [
                {
                    "timestamp": log.timestamp.isoformat(),
                    "message": log.message,
                    "level": log.level,
                    "labels": log.labels
                }
                for log in logs
            ]
            
            logger.info(f"Searched logs in {source}: {len(log_entries)} entries")
            return {"query": query, "logs": log_entries, "source": source}
        except Exception as e:
            logger.error(f"Log search failed: {e}")
            await ctx.error(f"Search error: {str(e)}")
            raise


def register_proxy_tools(server: FastMCP) -> None:
    """Register proxy tools that auto-forward to upstreams.
    
    This discovers all tools from upstream servers and creates
    pass-through handlers for tools not already registered.
    """
    import asyncio
    
    # Core tools we've already implemented (skip these)
    core_tools = {
        "query_metrics",
        "create_alert", 
        "create_dashboard",
        "search_logs"
    }
    
    async def discover_and_register():
        """Discover upstream tools and register proxies."""
        proxy = get_proxy()
        
        try:
            discovered = await proxy.discover_tools()
            total_tools = sum(len(tools) for tools in discovered.values())
            logger.info(f"Discovered {total_tools} tools from {len(discovered)} upstreams")
            
            # Register proxy handler for each discovered tool
            for upstream_name, tool_names in discovered.items():
                for tool_name in tool_names:
                    if tool_name not in core_tools:
                        register_proxy_tool(server, tool_name, upstream_name)
                        
        except Exception as e:
            logger.warning(f"Failed to discover upstream tools: {e}")
            logger.info("Proxy tools will be registered on-demand")
    
    # Run discovery in background (non-blocking)
    try:
        asyncio.create_task(discover_and_register())
    except RuntimeError:
        # No event loop yet, will discover on first call
        logger.debug("Event loop not ready, deferring tool discovery")


def register_proxy_tool(server: FastMCP, tool_name: str, upstream_name: str) -> None:
    """Register a single proxy tool."""
    
    @server.tool(name=tool_name)
    async def proxy_handler(ctx: Context, **kwargs) -> dict:
        """Auto-generated proxy handler."""
        proxy = get_proxy()
        correlation_id = ctx.request_context.get("correlation_id") if hasattr(ctx, "request_context") else None
        
        try:
            result = await proxy.call_tool(tool_name, kwargs, correlation_id)
            logger.debug(f"Proxied {tool_name} to {upstream_name}")
            return result
        except Exception as e:
            logger.error(f"Proxy call {tool_name} failed: {e}")
            await ctx.error(f"Proxy error: {str(e)}")
            raise
    
    # Update docstring
    proxy_handler.__doc__ = f"[Proxy] Forward to {upstream_name}.{tool_name}"


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
