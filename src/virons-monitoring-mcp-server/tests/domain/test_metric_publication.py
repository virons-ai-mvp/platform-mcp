"""Tests for metric publication domain entities."""
import pytest
from virons.monitoring_mcp_server.domain.metric_publication import MetricData, MetricDatum


def test_metric_datum_requires_name():
    with pytest.raises(ValueError):
        MetricDatum(name="", value=100.0, timestamp="2026-03-07T10:00:00Z")


def test_metric_datum_requires_value():
    with pytest.raises(ValueError):
        MetricDatum(name="cpu", value=None, timestamp="2026-03-07T10:00:00Z")


def test_metric_datum_creation():
    datum = MetricDatum(
        name="cpu_usage",
        value=75.5,
        timestamp="2026-03-07T10:00:00Z",
        unit="Percent"
    )
    assert datum.name == "cpu_usage"
    assert datum.value == 75.5
    assert datum.unit == "Percent"


def test_metric_data_requires_namespace():
    with pytest.raises(ValueError):
        MetricData(namespace="", metric_data=[])


def test_metric_data_creation():
    data = MetricData(
        namespace="Custom/App",
        metric_data=[
            MetricDatum("cpu", 75.0, "2026-03-07T10:00:00Z")
        ]
    )
    assert data.namespace == "Custom/App"
    assert len(data.metric_data) == 1
