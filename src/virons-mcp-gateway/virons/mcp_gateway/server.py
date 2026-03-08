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

"""MCP Gateway Server - Single entry point for all Virons MCP servers."""

import time
import uuid
from collections import defaultdict
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from loguru import logger
from prometheus_client import generate_latest

from .domain.gateway import GatewayRouter, ToolNotFoundError
from .domain.registry import ServiceRegistry
from .infrastructure.config import load_config
from .infrastructure.metrics import (
    http_request_duration,
    http_requests_total,
)
from .infrastructure.metrics import (
    registry as metrics_registry,
)


def create_app(
    service_registry: ServiceRegistry | None = None,
    rate_limit: int = 100,
    rate_window: int = 60,
) -> FastAPI:
    """Create FastAPI HTTP server with middleware."""
    app = FastAPI(title="Virons MCP Gateway", version="1.0.0")

    if service_registry is None:
        service_registry = ServiceRegistry()
        cfg_path = Path(__file__).parent / "config" / "services.json"
        if cfg_path.exists():
            cfg = load_config(str(cfg_path))

            # Register all services first
            for svc in cfg.services:
                service_registry.register(svc)

            # Discover tools on startup
            @app.on_event("startup")
            async def discover_tools():
                import asyncio

                import httpx

                # Wait for services to be ready
                await asyncio.sleep(2)

                async with httpx.AsyncClient(timeout=10.0) as client:
                    for svc in cfg.services:
                        # Retry discovery up to 3 times
                        for attempt in range(3):
                            try:
                                await service_registry.discover_tools(svc.name, svc.url, client)
                                logger.info(
                                    f"Discovered tools from {svc.name}: {len(service_registry._tool_metadata)} total"
                                )
                                break
                            except Exception:
                                if attempt < 2:
                                    await asyncio.sleep(1)
                                else:
                                    logger.warning(
                                        f"Failed to discover tools from {svc.name} after 3 attempts"
                                    )
                logger.info(f"Total tools discovered: {len(service_registry.list_tools())}")

    router = GatewayRouter(service_registry)

    # Rate limiter state
    _hits: dict[str, list[float]] = defaultdict(list)

    # Middleware
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.monotonic()
        window_start = now - rate_window
        hits = _hits[client_ip]
        _hits[client_ip] = [t for t in hits if t > window_start]
        if len(_hits[client_ip]) >= rate_limit:
            return JSONResponse({"error": "Too many requests"}, status_code=429)
        _hits[client_ip].append(now)
        return await call_next(request)

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
        endpoint = request.url.path
        http_requests_total.labels(request.method, endpoint, str(response.status_code)).inc()
        http_request_duration.labels(request.method, endpoint).observe(duration)
        return response

    # Routes
    @app.post(
        "/tools/{tool_name}",
        status_code=200,
        responses={
            200: {
                "description": "Tool executed successfully. The backend service processed the request and returned results.",
                "content": {"application/json": {"example": {"result": "success", "data": {}}}},
            },
            400: {
                "description": "Invalid request body. The JSON payload is malformed or missing required fields. Check your request syntax.",
                "content": {
                    "application/json": {
                        "example": {"error": "Invalid JSON: Expecting value at line 1"}
                    }
                },
            },
            401: {
                "description": "Authentication required. Include 'Authorization: Bearer <token>' header in your request.",
                "content": {
                    "application/json": {"example": {"error": "Missing authorization header"}}
                },
            },
            404: {
                "description": "Tool not found. The requested tool does not exist in any registered MCP service. Use GET /tools to see available tools.",
                "content": {
                    "application/json": {"example": {"error": "Tool 'unknown_tool' not found"}}
                },
            },
            500: {
                "description": "Internal server error. An unexpected error occurred in the gateway. Check logs for details.",
                "content": {
                    "application/json": {"example": {"error": "Internal processing error"}}
                },
            },
            502: {
                "description": "Bad gateway. The backend MCP service is unreachable or returned an invalid response. The service may be down or experiencing network issues.",
                "content": {
                    "application/json": {"example": {"error": "Backend service connection failed"}}
                },
            },
            503: {
                "description": "Service unavailable. The gateway or backend service is temporarily unavailable. Retry after a short delay.",
                "content": {
                    "application/json": {"example": {"error": "Service temporarily unavailable"}}
                },
            },
        },
    )
    async def execute_tool(tool_name: str, request: Request):
        """Execute a tool on the appropriate MCP backend service.

        This endpoint routes tool execution requests to the correct backend service based on
        the tool name. The gateway maintains a registry of which service provides each tool.

        Args:
            tool_name: Name of the tool to execute (e.g., 'deploy_infrastructure', 'scan_security')
            request: HTTP request containing tool parameters in JSON body

        Returns:
            Tool execution result from the backend service

        Example:
            POST /tools/deploy_infrastructure
            Headers: Authorization: Bearer <token>
            Body: {"tool": "terraform", "stack_name": "my-stack", "template_path": "/path/to/template"}
        """
        auth = request.headers.get("authorization")
        if not auth:
            return JSONResponse({"error": "Missing authorization header"}, status_code=401)

        try:
            body = await request.json()
        except Exception as e:
            return JSONResponse({"error": f"Invalid JSON: {str(e)}"}, status_code=400)

        try:
            result = await router.execute_tool(tool_name, body, auth)
            return JSONResponse(result, status_code=200)
        except ToolNotFoundError as exc:
            return JSONResponse({"error": str(exc)}, status_code=404)
        except Exception as exc:
            error_msg = str(exc)
            if "connection" in error_msg.lower() or "unavailable" in error_msg.lower():
                return JSONResponse({"error": error_msg}, status_code=502)
            return JSONResponse({"error": error_msg}, status_code=500)

    @app.get(
        "/tools",
        status_code=200,
        responses={
            200: {
                "description": "Successfully retrieved list of all available tools across all MCP services. Each tool includes its name and the service that provides it.",
                "content": {
                    "application/json": {
                        "example": {
                            "tools": [
                                {"name": "deploy_infrastructure", "service": "infrastructure-mcp"}
                            ]
                        }
                    }
                },
            },
            500: {
                "description": "Internal server error while retrieving tool registry. The gateway may be misconfigured or unable to access its service registry.",
                "content": {
                    "application/json": {"example": {"error": "Failed to retrieve tools"}}
                },
            },
        },
    )
    async def list_tools():
        """List all available tools from all registered MCP services.

        Returns a comprehensive list of tools that can be executed through this gateway.
        Each tool entry includes the tool name and which backend service provides it.
        Use this endpoint to discover available capabilities before executing tools.

        Returns:
            JSON object with 'tools' array containing tool names and service mappings

        Example response:
            {
                "tools": [
                    {"name": "deploy_infrastructure", "service": "infrastructure-mcp"},
                    {"name": "scan_security", "service": "security-mcp"}
                ]
            }
        """
        try:
            tools = service_registry.list_tools()
            return JSONResponse({"tools": tools}, status_code=200)
        except Exception as exc:
            return JSONResponse({"error": str(exc)}, status_code=500)

    @app.get(
        "/health",
        status_code=200,
        responses={
            200: {
                "description": "Gateway is healthy and operational. All internal components are functioning correctly. This does not guarantee backend services are available - use /ready for that.",
                "content": {
                    "application/json": {
                        "example": {"status": "healthy", "gateway": "virons-mcp-gateway"}
                    }
                },
            },
            503: {
                "description": "Gateway is unhealthy. Critical internal components have failed. The gateway cannot process requests reliably. Check logs and restart if necessary.",
                "content": {
                    "application/json": {
                        "example": {"status": "unhealthy", "error": "Component failure"}
                    }
                },
            },
        },
    )
    async def health():
        """Health check endpoint for the gateway itself (liveness probe).

        This endpoint checks if the gateway process is alive and its internal components
        are functioning. It does NOT check backend service availability - use /ready for that.
        Kubernetes liveness probes should use this endpoint.

        Returns:
            200: Gateway is healthy and can accept requests
            503: Gateway has internal failures and should be restarted

        Example response:
            {"status": "healthy", "gateway": "virons-mcp-gateway", "uptime": 3600}
        """
        try:
            health_data = await router.health_check()
            return JSONResponse(
                {"status": "healthy", "gateway": "virons-mcp-gateway", **health_data},
                status_code=200,
            )
        except Exception as exc:
            return JSONResponse({"status": "unhealthy", "error": str(exc)}, status_code=503)

    @app.get(
        "/ready",
        status_code=200,
        responses={
            200: {
                "description": "Gateway and all backend services are ready to accept requests. All health checks passed. Safe to route production traffic.",
                "content": {
                    "application/json": {
                        "example": {"ready": True, "services": {"infrastructure-mcp": "healthy"}}
                    }
                },
            },
            503: {
                "description": "Gateway or one or more backend services are not ready. Do not route traffic until this returns 200. Check which services are failing in the response body.",
                "content": {
                    "application/json": {
                        "example": {
                            "ready": False,
                            "services": {"infrastructure-mcp": "unhealthy"},
                        }
                    }
                },
            },
        },
    )
    async def ready():
        """Readiness check for gateway and all backend services (readiness probe).

        This endpoint checks if the gateway AND all registered backend MCP services
        are ready to handle requests. Use this for Kubernetes readiness probes and
        load balancer health checks. Traffic should only be routed when this returns 200.

        Returns:
            200: Gateway and all backends are ready
            503: Gateway or one or more backends are not ready (see response for details)

        Example response:
            {
                "ready": true,
                "services": {
                    "infrastructure-mcp": "healthy",
                    "security-mcp": "healthy"
                }
            }
        """
        try:
            readiness = await router.readiness_check()
            status = 200 if readiness["ready"] else 503
            return JSONResponse(readiness, status_code=status)
        except Exception as exc:
            return JSONResponse({"ready": False, "error": str(exc)}, status_code=503)

    @app.get(
        "/metrics",
        status_code=200,
        responses={
            200: {
                "description": "Prometheus-formatted metrics successfully retrieved. Includes request counts, durations, error rates, and circuit breaker states. Scrape this endpoint with Prometheus.",
                "content": {
                    "text/plain": {
                        "example": '# HELP http_requests_total Total HTTP requests\n# TYPE http_requests_total counter\nhttp_requests_total{method="GET",endpoint="/tools",status="200"} 42'
                    }
                },
            },
            500: {
                "description": "Failed to generate metrics. The metrics collector may be misconfigured or unable to serialize data.",
                "content": {
                    "application/json": {"example": {"error": "Metrics generation failed"}}
                },
            },
        },
    )
    async def metrics():
        """Prometheus metrics endpoint for monitoring and observability.

        Exposes operational metrics in Prometheus text format for scraping.
        Configure your Prometheus server to scrape this endpoint for monitoring.

        Metrics include:
        - http_requests_total: Total requests by method, endpoint, and status
        - http_request_duration_seconds: Request latency histogram
        - circuit_breaker_state: Circuit breaker status per backend service
        - tool_execution_count: Tool execution counts

        Returns:
            Prometheus text format metrics (text/plain)

        Example:
            # HELP http_requests_total Total HTTP requests
            # TYPE http_requests_total counter
            http_requests_total{method="POST",endpoint="/tools/deploy",status="200"} 156
        """
        try:
            return PlainTextResponse(
                generate_latest(metrics_registry),
                media_type="text/plain; version=0.0.4",
                status_code=200,
            )
        except Exception as exc:
            return JSONResponse({"error": str(exc)}, status_code=500)

    @app.get(
        "/",
        status_code=200,
        responses={
            200: {
                "description": "Gateway information and available endpoints. Use this to discover the API structure.",
                "content": {
                    "application/json": {
                        "example": {
                            "service": "virons-mcp-gateway",
                            "version": "1.0.0",
                            "endpoints": {},
                        }
                    }
                },
            },
        },
    )
    async def root():
        """Gateway information and API discovery endpoint.

        Returns basic information about the gateway and links to all available endpoints.
        Use this as a starting point to explore the API.

        Returns:
            Gateway metadata and endpoint map

        Example response:
            {
                "service": "virons-mcp-gateway",
                "version": "1.0.0",
                "endpoints": {
                    "tools": "/tools",
                    "execute": "/tools/{tool_name}",
                    "health": "/health",
                    "ready": "/ready",
                    "metrics": "/metrics",
                    "docs": "/docs"
                }
            }
        """
        return JSONResponse(
            {
                "service": "virons-mcp-gateway",
                "version": "1.0.0",
                "endpoints": {
                    "tools": "/tools",
                    "execute": "/tools/{tool_name}",
                    "health": "/health",
                    "ready": "/ready",
                    "metrics": "/metrics",
                    "docs": "/docs",
                },
            },
            status_code=200,
        )

    # Global error handlers
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        """Handle 404 Not Found errors.

        The requested endpoint does not exist. Check the URL path and use GET / to see available endpoints.
        """
        return JSONResponse(
            {
                "error": "Endpoint not found",
                "path": request.url.path,
                "message": "The requested endpoint does not exist. Use GET / to see available endpoints.",
            },
            status_code=404,
        )

    @app.exception_handler(405)
    async def method_not_allowed_handler(request: Request, exc):
        """Handle 405 Method Not Allowed errors.

        The HTTP method is not supported for this endpoint. Check the API documentation for allowed methods.
        """
        return JSONResponse(
            {
                "error": "Method not allowed",
                "method": request.method,
                "path": request.url.path,
                "message": f"HTTP method {request.method} is not allowed for {request.url.path}. Check API documentation for allowed methods.",
            },
            status_code=405,
        )

    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc):
        """Handle 500 Internal Server Error.

        An unexpected error occurred. This indicates a bug or misconfiguration. Check logs for details.
        """
        return JSONResponse(
            {
                "error": "Internal server error",
                "message": "An unexpected error occurred. Check server logs for details. If this persists, contact support.",
            },
            status_code=500,
        )

    return app


def main():
    """Run the MCP gateway server."""
    import argparse
    import os

    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9000)
    args = parser.parse_args()

    port = int(os.getenv("PORT", args.port))
    app = create_app()
    logger.info(f"Gateway HTTP server on port {port}")
    logger.info(f"Swagger UI: http://localhost:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")


if __name__ == "__main__":
    main()
