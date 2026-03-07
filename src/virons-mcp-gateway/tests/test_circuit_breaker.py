# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for circuit breaker."""

from datetime import datetime, timedelta
from unittest.mock import patch

from virons.mcp_gateway.domain.gateway import _CircuitBreaker


class TestCircuitBreaker:
    """Test circuit breaker functionality."""

    def test_circuit_breaker_starts_closed(self):
        """Test circuit breaker starts in closed state."""
        cb = _CircuitBreaker(threshold=5, timeout=60)
        assert not cb.is_open

    def test_circuit_breaker_opens_after_threshold(self):
        """Test circuit breaker opens after threshold failures."""
        cb = _CircuitBreaker(threshold=3, timeout=60)
        cb.record_failure()
        cb.record_failure()
        assert not cb.is_open
        cb.record_failure()
        assert cb.is_open

    def test_circuit_breaker_closes_after_timeout(self):
        """Test circuit breaker closes after timeout period."""
        cb = _CircuitBreaker(threshold=2, timeout=1)
        cb.record_failure()
        cb.record_failure()
        assert cb.is_open

        # Mock time passing
        future = datetime.now() + timedelta(seconds=2)
        with patch("virons.mcp_gateway.domain.gateway.datetime") as mock_dt:
            mock_dt.now.return_value = future
            assert not cb.is_open

    def test_circuit_breaker_resets_on_success(self):
        """Test circuit breaker resets failure count on success."""
        cb = _CircuitBreaker(threshold=3, timeout=60)
        cb.record_failure()
        cb.record_failure()
        assert not cb.is_open
        cb.record_success()
        cb.record_failure()
        cb.record_failure()
        assert not cb.is_open  # Should not open, count was reset

    def test_circuit_breaker_stays_open_during_timeout(self):
        """Test circuit breaker stays open during timeout period."""
        cb = _CircuitBreaker(threshold=2, timeout=60)
        cb.record_failure()
        cb.record_failure()
        assert cb.is_open
        # Still within timeout
        assert cb.is_open
