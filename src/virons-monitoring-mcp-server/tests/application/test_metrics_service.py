"""Tests for MetricsService - TDD."""
import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime
from virons.monitoring_mcp_server.application.metrics_service import MetricsService
from virons.monitoring_mcp_server.domain.metric import MetricQuery, Metric


@pytest.mark.asyncio
async def test_query_metrics_from_cloudwatch():
    """Test querying metrics from CloudWatch."""
    service = MetricsService()
    query = MetricQuery(
        metric_name="CPUUtilization",
        start_time="2026-03-07T00:00:00Z",
        end_time="2026-03-07T01:00:00Z",
        source="cloudwatch"
    )
    
    mock_metrics = [
        Metric(
            name="CPUUtilization",
            value=75.5,
            timestamp=datetime.now(),
            labels={"namespace": "AWS/EC2"},
            source="cloudwatch"
        )
    ]
    
    with patch.object(service.cloudwatch, 'query_metrics', new=AsyncMock(return_value=mock_metrics)):
        result = await service.query_metrics(query)
        
        assert len(result) == 1
        assert result[0].name == "CPUUtilization"
        assert result[0].source == "cloudwatch"


@pytest.mark.asyncio
async def test_query_metrics_from_prometheus():
    """Test querying metrics from Prometheus."""
    service = MetricsService()
    query = MetricQuery(
        metric_name="cpu_usage",
        start_time="2026-03-07T00:00:00Z",
        end_time="2026-03-07T01:00:00Z",
        source="prometheus"
    )
    
    mock_metrics = [
        Metric(
            name="cpu_usage",
            value=80.0,
            timestamp=datetime.now(),
            labels={"job": "node"},
            source="prometheus"
        )
    ]
    
    with patch.object(service.prometheus, 'query_range', new=AsyncMock(return_value=mock_metrics)):
        result = await service.query_metrics(query)
        
        assert len(result) == 1
        assert result[0].name == "cpu_usage"
        assert result[0].source == "prometheus"


@pytest.mark.asyncio
async def test_query_metrics_propagates_correlation_id():
    """Test correlation ID propagation."""
    service = MetricsService()
    query = MetricQuery(
        metric_name="cpu_usage",
        start_time="2026-03-07T00:00:00Z",
        end_time="2026-03-07T01:00:00Z",
        source="cloudwatch"
    )
    
    with patch.object(service.cloudwatch, 'query_metrics', new=AsyncMock(return_value=[])) as mock:
        await service.query_metrics(query, correlation_id="test-123")
        
        mock.assert_called_once()
        # Check positional and keyword args
        args, kwargs = mock.call_args
        assert kwargs.get("correlation_id") == "test-123" or (len(args) > 3 and args[3] == "test-123")


@pytest.mark.asyncio
async def test_query_metrics_handles_errors():
    """Test error handling."""
    service = MetricsService()
    query = MetricQuery(
        metric_name="cpu_usage",
        start_time="2026-03-07T00:00:00Z",
        end_time="2026-03-07T01:00:00Z",
        source="cloudwatch"
    )
    
    with patch.object(service.cloudwatch, 'query_metrics', new=AsyncMock(side_effect=Exception("Network error"))):
        with pytest.raises(Exception, match="Network error"):
            await service.query_metrics(query)
