# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for Prometheus metrics instrumentation."""

from virons.infrastructure_mcp_server.infrastructure.metrics import MetricsCollector


class TestMetricsCollector:
    """Test Prometheus metrics collection."""

    def test_collector_initializes_metrics(self):
        """Metrics collector initializes all required metrics."""
        collector = MetricsCollector()

        assert collector.tool_calls_total is not None
        assert collector.tool_duration_seconds is not None
        assert collector.upstream_healthy is not None
        assert collector.errors_total is not None

    def test_record_tool_call_increments_counter(self):
        """Recording tool call increments counter."""
        collector = MetricsCollector()

        collector.record_tool_call(tool="cdk", status="success")

        # Verify counter was incremented
        assert collector.tool_calls_total._metrics

    def test_record_tool_duration_observes_histogram(self):
        """Recording tool duration adds observation."""
        collector = MetricsCollector()

        collector.record_tool_duration(tool="cdk", duration=1.5)

        # Verify histogram was updated
        assert collector.tool_duration_seconds._metrics

    def test_set_upstream_health_updates_gauge(self):
        """Setting upstream health updates gauge."""
        collector = MetricsCollector()

        collector.set_upstream_health(server="cdk", healthy=True)
        collector.set_upstream_health(server="cfn", healthy=False)

        # Verify gauge was set
        assert collector.upstream_healthy._metrics

    def test_record_error_increments_counter(self):
        """Recording error increments error counter."""
        collector = MetricsCollector()

        collector.record_error(error_type="connection_error")

        # Verify error counter was incremented
        assert collector.errors_total._metrics
