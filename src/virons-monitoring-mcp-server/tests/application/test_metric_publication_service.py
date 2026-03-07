"""Tests for metric publication service."""
import pytest
from unittest.mock import AsyncMock, patch
from virons.monitoring_mcp_server.application.metric_publication_service import MetricPublicationService


@pytest.mark.asyncio
async def test_publish_metrics():
    service = MetricPublicationService()
    
    with patch.object(service.cloudwatch, 'put_metric_data', new_callable=AsyncMock) as mock_put:
        mock_put.return_value = {"status": "success"}
        
        result = await service.publish_metrics(
            "Custom/App",
            [{"name": "cpu", "value": 75.0, "timestamp": "2026-03-07T10:00:00Z"}]
        )
        
        assert result["status"] == "success"
        mock_put.assert_called_once()


@pytest.mark.asyncio
async def test_publish_metrics_with_correlation_id():
    service = MetricPublicationService()
    
    with patch.object(service.cloudwatch, 'put_metric_data', new_callable=AsyncMock) as mock_put:
        mock_put.return_value = {"status": "success"}
        
        await service.publish_metrics(
            "Custom/App",
            [{"name": "cpu", "value": 75.0, "timestamp": "2026-03-07T10:00:00Z"}],
            "corr-123"
        )
        
        call_args = mock_put.call_args
        assert call_args[1]["correlation_id"] == "corr-123"


@pytest.mark.asyncio
async def test_publish_metrics_handles_errors():
    service = MetricPublicationService()
    
    with patch.object(service.cloudwatch, 'put_metric_data', new_callable=AsyncMock) as mock_put:
        mock_put.side_effect = Exception("Publish failed")
        
        with pytest.raises(Exception, match="Publish failed"):
            await service.publish_metrics("Custom/App", [])
