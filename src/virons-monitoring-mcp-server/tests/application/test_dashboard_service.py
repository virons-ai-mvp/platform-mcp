"""Tests for DashboardService - TDD."""
import pytest
from unittest.mock import AsyncMock, patch
from virons.monitoring_mcp_server.application.dashboard_service import DashboardService
from virons.monitoring_mcp_server.domain.dashboard import Dashboard, Panel


@pytest.mark.asyncio
async def test_create_dashboard():
    """Test dashboard creation."""
    service = DashboardService()
    dashboard = Dashboard(
        name="System Metrics",
        panels=[Panel("CPU", "cpu_usage", "graph")]
    )
    
    mock_result = {"dashboard_id": "123", "url": "/d/123", "name": "System Metrics"}
    
    with patch.object(service.grafana, 'create_dashboard', new=AsyncMock(return_value=mock_result)):
        result = await service.create_dashboard(dashboard)
        
        assert result["name"] == "System Metrics"
        assert "dashboard_id" in result


@pytest.mark.asyncio
async def test_create_dashboard_with_multiple_panels():
    """Test dashboard with multiple panels."""
    service = DashboardService()
    dashboard = Dashboard(
        name="Test",
        panels=[
            Panel("CPU", "cpu", "graph"),
            Panel("Memory", "memory", "stat")
        ]
    )
    
    with patch.object(service.grafana, 'create_dashboard', new=AsyncMock(return_value={})) as mock:
        await service.create_dashboard(dashboard)
        
        mock.assert_called_once()
        args, kwargs = mock.call_args
        panels_data = args[1] if len(args) > 1 else kwargs.get("panels")
        assert len(panels_data) == 2


@pytest.mark.asyncio
async def test_create_dashboard_propagates_correlation_id():
    """Test correlation ID propagation."""
    service = DashboardService()
    dashboard = Dashboard(name="Test", panels=[Panel("CPU", "cpu", "graph")])
    
    with patch.object(service.grafana, 'create_dashboard', new=AsyncMock(return_value={})) as mock:
        await service.create_dashboard(dashboard, correlation_id="test-123")
        
        mock.assert_called_once()
        args, kwargs = mock.call_args
        assert kwargs.get("correlation_id") == "test-123" or (len(args) > 3 and args[3] == "test-123")
