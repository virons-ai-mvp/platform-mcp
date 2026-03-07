"""Tests for Metric domain entities - TDD."""
import pytest
from datetime import datetime
from virons.monitoring_mcp_server.domain.metric import Metric, MetricQuery


def test_metric_creation():
    """Test metric entity creation."""
    metric = Metric(
        name="cpu_usage",
        value=75.5,
        timestamp=datetime.now(),
        labels={"host": "server1"},
        source="prometheus"
    )
    
    assert metric.name == "cpu_usage"
    assert metric.value == 75.5
    assert metric.source == "prometheus"


def test_metric_requires_name():
    """Test metric validation - name required."""
    with pytest.raises(ValueError, match="Metric name required"):
        Metric(
            name="",
            value=75.5,
            timestamp=datetime.now(),
            labels={},
            source="prometheus"
        )


def test_metric_requires_value():
    """Test metric validation - value required."""
    with pytest.raises(ValueError, match="Metric value required"):
        Metric(
            name="cpu_usage",
            value=None,
            timestamp=datetime.now(),
            labels={},
            source="prometheus"
        )


def test_metric_query_creation():
    """Test metric query value object."""
    query = MetricQuery(
        metric_name="cpu_usage",
        start_time="2026-03-07T00:00:00Z",
        end_time="2026-03-07T01:00:00Z",
        source="prometheus"
    )
    
    assert query.metric_name == "cpu_usage"
    assert query.source == "prometheus"


def test_metric_query_validates_source():
    """Test metric query validates source."""
    with pytest.raises(ValueError, match="Invalid source"):
        MetricQuery(
            metric_name="cpu_usage",
            start_time="2026-03-07T00:00:00Z",
            end_time="2026-03-07T01:00:00Z",
            source="invalid"
        )


def test_metric_query_defaults_to_cloudwatch():
    """Test metric query defaults to cloudwatch."""
    query = MetricQuery(
        metric_name="cpu_usage",
        start_time="2026-03-07T00:00:00Z",
        end_time="2026-03-07T01:00:00Z"
    )
    
    assert query.source == "cloudwatch"
