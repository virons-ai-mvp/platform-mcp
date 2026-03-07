# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""MCP Gateway Server - Single entry point for all Virons MCP servers."""

import time
import uuid
from collections import defaultdict
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from loguru import logger
from mcp.server.fastmcp import FastMCP
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
            for svc in cfg.services:
                service_registry.register(svc)

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
    @app.post("/tools/{tool_name}")
    async def execute_tool(tool_name: str, request: Request):
        auth = request.headers.get("authorization")
        if not auth:
            return JSONResponse({"error": "Missing authorization header"}, status_code=401)
        try:
            body = await request.json()
            result = await router.execute_tool(tool_name, body, auth)
            return result
        except ToolNotFoundError as exc:
            return JSONResponse({"error": str(exc)}, status_code=404)
        except Exception as exc:
            return JSONResponse({"error": str(exc)}, status_code=500)

    @app.get("/tools")
    async def list_tools():
        return {"tools": service_registry.list_tools()}

    @app.get("/health")
    async def health():
        health_data = await router.health_check()
        return {"status": "healthy", "gateway": "virons-mcp-gateway", **health_data}

    @app.get("/ready")
    async def ready():
        readiness = await router.readiness_check()
        status = 200 if readiness["ready"] else 503
        return JSONResponse(readiness, status_code=status)

    @app.get("/metrics")
    async def metrics():
        return PlainTextResponse(
            generate_latest(metrics_registry), media_type="text/plain; version=0.0.4"
        )

    @app.get("/")
    async def root():
        return {"service": "virons-mcp-gateway", "version": "1.0.0"}

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
