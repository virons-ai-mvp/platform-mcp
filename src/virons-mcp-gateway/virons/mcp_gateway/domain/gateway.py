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

"""Gateway router — routes tool calls to MCP backends with circuit breaker."""

import time
from datetime import datetime, timedelta
from typing import Any, Optional

import httpx
from loguru import logger

from .registry import ServiceRegistry


class ToolNotFoundError(Exception):
    """Tool not found in registry."""


class CircuitBreakerOpenError(Exception):
    """Circuit breaker is open."""


class _CircuitBreaker:
    """Per-service circuit breaker."""

    __slots__ = ("_threshold", "_timeout", "_failure_count", "_open_until")

    def __init__(self, threshold: int = 5, timeout: int = 60) -> None:
        self._threshold = threshold
        self._timeout = timeout
        self._failure_count = 0
        self._open_until: Optional[datetime] = None

    @property
    def is_open(self) -> bool:
        """Check if circuit breaker is open."""
        if self._open_until is None:
            return False
        if datetime.now() > self._open_until:
            self._open_until = None
            self._failure_count = 0
            return False
        return True

    def record_failure(self) -> None:
        """Record a failure."""
        self._failure_count += 1
        if self._failure_count >= self._threshold:
            self._open_until = datetime.now() + timedelta(seconds=self._timeout)

    def record_success(self) -> None:
        """Record a success and reset failure count."""
        self._failure_count = 0


class GatewayRouter:
    """Routes tool execution requests to MCP backend services."""

    def __init__(
        self,
        registry: ServiceRegistry,
        timeout: float = 30.0,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_timeout: int = 60,
    ) -> None:
        """Initialize gateway router with dependencies."""
        self._registry = registry
        self._client = httpx.AsyncClient(timeout=timeout)
        self._cb_threshold = circuit_breaker_threshold
        self._cb_timeout = circuit_breaker_timeout
        self._breakers: dict[str, _CircuitBreaker] = {}

    def _breaker(self, service_name: str) -> _CircuitBreaker:
        """Get or create circuit breaker for service."""
        if service_name not in self._breakers:
            self._breakers[service_name] = _CircuitBreaker(self._cb_threshold, self._cb_timeout)
        return self._breakers[service_name]

    async def execute_tool(self, tool_name: str, params: Any, auth_token: str) -> Any:
        """Execute tool on backend service."""
        service = self._registry.find_by_tool(tool_name)
        if not service:
            raise ToolNotFoundError(f"Tool not found: {tool_name}")

        cb = self._breaker(service.name)
        if cb.is_open:
            raise CircuitBreakerOpenError(f"Circuit breaker open for {service.name}")

        start = time.monotonic()

        try:
            # Check if stdio mode
            if service.url.startswith("stdio://"):
                from ..infrastructure.mcp_stdio import invoke_mcp_stdio

                result = await invoke_mcp_stdio(
                    service.command,
                    service.cwd,
                    "tools/call",
                    {"name": tool_name, "arguments": params},
                )
            else:
                # HTTP mode
                url = f"{service.url}/tools/{tool_name}"
                resp = await self._client.post(
                    url,
                    json=params,
                    headers={"Authorization": auth_token, "Content-Type": "application/json"},
                )
                resp.raise_for_status()
                result = resp.json()

            cb.record_success()
            duration = time.monotonic() - start
            logger.info(
                f"Backend OK service={service.name} tool={tool_name} duration={duration:.3f}s"
            )
            return result
        except Exception as exc:
            cb.record_failure()
            duration = time.monotonic() - start
            logger.error(
                f"Backend failed service={service.name} tool={tool_name} duration={duration:.3f}s error={exc}"
            )
            raise

    async def health_check(self) -> dict[str, Any]:
        """Check health of all backend services."""
        services = self._registry.list_all()
        checks = []
        for svc in services:
            try:
                resp = await self._client.get(f"{svc.url}/health", timeout=5.0)
                resp.raise_for_status()
                checks.append(
                    {"name": svc.name, "status": "healthy", "url": svc.url, "details": resp.json()}
                )
            except Exception as exc:
                checks.append(
                    {"name": svc.name, "status": "unhealthy", "url": svc.url, "error": str(exc)}
                )
        return {"services": checks, "version": "1.0.0"}

    async def readiness_check(self) -> dict[str, Any]:
        """Check if gateway is ready to serve requests."""
        health = await self.health_check()
        ready = all(s["status"] == "healthy" for s in health["services"])
        return {"ready": ready, "services": health["services"]}

    async def close(self) -> None:
        """Close HTTP client."""
        await self._client.aclose()
