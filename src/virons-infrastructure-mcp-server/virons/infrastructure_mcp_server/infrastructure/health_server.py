# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""HTTP server for health check endpoints."""

import asyncio
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict

from loguru import logger

from .health import HealthChecker


class HealthRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for health endpoints."""

    health_checker: HealthChecker = None

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/health/live":
            self._handle_liveness()
        elif self.path == "/health/ready":
            self._handle_readiness()
        else:
            self.send_error(404)

    def _handle_liveness(self):
        """Handle liveness probe."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.health_checker.liveness())
            loop.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            logger.error(f"Liveness check failed: {e}")
            self.send_error(500)

    def _handle_readiness(self):
        """Handle readiness probe."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.health_checker.readiness())
            loop.close()

            status_code = 200 if result["status"] == "healthy" else 503
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            logger.error(f"Readiness check failed: {e}")
            self.send_error(500)

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


class HealthServer:
    """HTTP server for Kubernetes health probes."""

    def __init__(self, health_checker: HealthChecker, port: int = 8080):
        self.health_checker = health_checker
        self.port = port
        self.server = None

    async def handle_liveness(self) -> Dict[str, Any]:
        """Handle liveness probe."""
        return await self.health_checker.liveness()

    async def handle_readiness(self) -> Dict[str, Any]:
        """Handle readiness probe."""
        return await self.health_checker.readiness()

    def start(self):
        """Start HTTP server."""
        HealthRequestHandler.health_checker = self.health_checker
        self.server = HTTPServer(("0.0.0.0", self.port), HealthRequestHandler)
        logger.info(f"Health server listening on port {self.port}")
        self.server.serve_forever()

    def stop(self):
        """Stop HTTP server."""
        if self.server:
            self.server.shutdown()
            logger.info("Health server stopped")
