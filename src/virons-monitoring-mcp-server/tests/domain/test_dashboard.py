"""Tests for Dashboard domain entities - TDD."""
import pytest
from virons.monitoring_mcp_server.domain.dashboard import Dashboard, Panel


def test_panel_creation():
    """Test panel value object creation."""
    panel = Panel(title="CPU Usage", query="cpu_usage", type="graph")
    
    assert panel.title == "CPU Usage"
    assert panel.query == "cpu_usage"
    assert panel.type == "graph"
    assert panel.datasource == "prometheus"


def test_panel_requires_title():
    """Test panel validation - title required."""
    with pytest.raises(ValueError, match="Panel title required"):
        Panel(title="", query="cpu", type="graph")


def test_panel_validates_type():
    """Test panel validates type."""
    with pytest.raises(ValueError, match="Invalid panel type"):
        Panel(title="Test", query="cpu", type="invalid")


def test_dashboard_creation():
    """Test dashboard entity creation."""
    panels = [Panel(title="CPU", query="cpu", type="graph")]
    dashboard = Dashboard(name="System Metrics", panels=panels)
    
    assert dashboard.name == "System Metrics"
    assert len(dashboard.panels) == 1
    assert dashboard.tags == []


def test_dashboard_requires_name():
    """Test dashboard validation - name required."""
    with pytest.raises(ValueError, match="Dashboard name required"):
        Dashboard(name="", panels=[Panel("CPU", "cpu", "graph")])


def test_dashboard_requires_panels():
    """Test dashboard validation - panels required."""
    with pytest.raises(ValueError, match="At least one panel required"):
        Dashboard(name="Test", panels=[])


def test_dashboard_add_panel():
    """Test adding panel to dashboard."""
    dashboard = Dashboard(name="Test", panels=[Panel("CPU", "cpu", "graph")])
    dashboard.add_panel(Panel("Memory", "memory", "stat"))
    
    assert dashboard.panel_count() == 2


def test_dashboard_with_tags():
    """Test dashboard with tags."""
    dashboard = Dashboard(
        name="Test",
        panels=[Panel("CPU", "cpu", "graph")],
        tags=["production", "monitoring"]
    )
    
    assert len(dashboard.tags) == 2
    assert "production" in dashboard.tags
