"""Tests for AlertService - TDD."""
import pytest
from unittest.mock import AsyncMock, patch
from virons.monitoring_mcp_server.application.alert_service import AlertService
from virons.monitoring_mcp_server.domain.alert import Alert


@pytest.mark.asyncio
async def test_create_alert():
    """Test alert creation."""
    service = AlertService()
    alert = Alert(
        name="high_cpu",
        metric="cpu_usage",
        threshold=80.0,
        comparison="gt"
    )
    
    mock_result = {"alarm_id": "arn:aws:cloudwatch:alarm:123", "name": "high_cpu"}
    
    with patch.object(service.cloudwatch, 'create_alarm', new=AsyncMock(return_value=mock_result)):
        result = await service.create_alert(alert)
        
        assert result["name"] == "high_cpu"
        assert "alarm_id" in result


@pytest.mark.asyncio
async def test_create_alert_propagates_correlation_id():
    """Test correlation ID propagation."""
    service = AlertService()
    alert = Alert(name="test", metric="cpu", threshold=80.0, comparison="gt")
    
    with patch.object(service.cloudwatch, 'create_alarm', new=AsyncMock(return_value={})) as mock:
        await service.create_alert(alert, correlation_id="test-123")
        
        mock.assert_called_once()
        args, kwargs = mock.call_args
        assert kwargs.get("correlation_id") == "test-123" or (len(args) > 4 and args[4] == "test-123")


@pytest.mark.asyncio
async def test_create_alert_handles_errors():
    """Test error handling."""
    service = AlertService()
    alert = Alert(name="test", metric="cpu", threshold=80.0, comparison="gt")
    
    with patch.object(service.cloudwatch, 'create_alarm', new=AsyncMock(side_effect=Exception("Network error"))):
        with pytest.raises(Exception, match="Network error"):
            await service.create_alert(alert)
