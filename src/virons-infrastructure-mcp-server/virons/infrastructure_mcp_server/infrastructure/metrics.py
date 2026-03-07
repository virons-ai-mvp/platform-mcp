# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Prometheus metrics instrumentation."""

from prometheus_client import Counter, Gauge, Histogram


class MetricsCollector:
    """Collect Prometheus metrics for MCP server."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.tool_calls_total = Counter(
            "mcp_tool_calls_total", "Total MCP tool calls", ["tool", "status"]
        )

        self.tool_duration_seconds = Histogram(
            "mcp_tool_duration_seconds", "Tool execution duration", ["tool"]
        )

        self.upstream_healthy = Gauge(
            "mcp_upstream_healthy", "Upstream server health status", ["server"]
        )

        self.errors_total = Counter("mcp_errors_total", "Total errors", ["error_type"])

        self._initialized = True

    def record_tool_call(self, tool: str, status: str):
        """Record tool call."""
        self.tool_calls_total.labels(tool=tool, status=status).inc()

    def record_tool_duration(self, tool: str, duration: float):
        """Record tool duration."""
        self.tool_duration_seconds.labels(tool=tool).observe(duration)

    def set_upstream_health(self, server: str, healthy: bool):
        """Set upstream health status."""
        self.upstream_healthy.labels(server=server).set(1 if healthy else 0)

    def record_error(self, error_type: str):
        """Record error."""
        self.errors_total.labels(error_type=error_type).inc()
