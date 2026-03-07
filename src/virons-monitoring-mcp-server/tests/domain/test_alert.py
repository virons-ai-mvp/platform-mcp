"""Tests for Alert domain entity - TDD."""
import pytest
from virons.monitoring_mcp_server.domain.alert import Alert


def test_alert_creation():
    """Test alert entity creation."""
    alert = Alert(
        name="high_cpu",
        metric="cpu_usage",
        threshold=80.0,
        comparison="gt"
    )
    
    assert alert.name == "high_cpu"
    assert alert.metric == "cpu_usage"
    assert alert.threshold == 80.0
    assert alert.comparison == "gt"
    assert alert.enabled is True


def test_alert_requires_name():
    """Test alert validation - name required."""
    with pytest.raises(ValueError, match="Alert name required"):
        Alert(name="", metric="cpu", threshold=80.0, comparison="gt")


def test_alert_requires_metric():
    """Test alert validation - metric required."""
    with pytest.raises(ValueError, match="Metric required"):
        Alert(name="test", metric="", threshold=80.0, comparison="gt")


def test_alert_validates_comparison():
    """Test alert validates comparison operator."""
    with pytest.raises(ValueError, match="Invalid comparison"):
        Alert(name="test", metric="cpu", threshold=80.0, comparison="invalid")


def test_alert_evaluate_gt():
    """Test alert evaluation - greater than."""
    alert = Alert(name="test", metric="cpu", threshold=80.0, comparison="gt")
    
    assert alert.evaluate(85.0) is True
    assert alert.evaluate(75.0) is False
    assert alert.evaluate(80.0) is False


def test_alert_evaluate_lt():
    """Test alert evaluation - less than."""
    alert = Alert(name="test", metric="cpu", threshold=20.0, comparison="lt")
    
    assert alert.evaluate(15.0) is True
    assert alert.evaluate(25.0) is False
    assert alert.evaluate(20.0) is False


def test_alert_evaluate_eq():
    """Test alert evaluation - equals."""
    alert = Alert(name="test", metric="cpu", threshold=50.0, comparison="eq")
    
    assert alert.evaluate(50.0) is True
    assert alert.evaluate(49.0) is False
