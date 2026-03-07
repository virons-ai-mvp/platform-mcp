# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for Prometheus metrics."""

from prometheus_client import REGISTRY

from virons.mcp_gateway.infrastructure.metrics import (
    http_request_duration,
    http_requests_total,
    registry,
)


class TestMetrics:
    """Test Prometheus metrics functionality."""

    def test_http_requests_total_counter_exists(self):
        """Test http_requests_total counter is registered."""
        assert http_requests_total is not None
        assert http_requests_total._name == "http_requests"

    def test_http_request_duration_histogram_exists(self):
        """Test http_request_duration histogram is registered."""
        assert http_request_duration is not None
        assert http_request_duration._name == "http_request_duration_seconds"

    def test_metrics_counter_increments(self):
        """Test counter increments correctly."""
        before = http_requests_total.labels(
            method="GET", endpoint="/test", status="200"
        )._value.get()
        http_requests_total.labels(method="GET", endpoint="/test", status="200").inc()
        after = http_requests_total.labels(
            method="GET", endpoint="/test", status="200"
        )._value.get()
        assert after == before + 1

    def test_metrics_histogram_observes(self):
        """Test histogram observes values."""
        http_request_duration.labels(method="POST", endpoint="/tools/test").observe(0.5)
        # Just verify it doesn't raise an error
        assert True

    def test_metrics_registry_is_prometheus_registry(self):
        """Test registry is the Prometheus registry."""
        assert registry is REGISTRY
