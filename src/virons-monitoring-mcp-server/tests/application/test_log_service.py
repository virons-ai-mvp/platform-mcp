"""Tests for LogService - TDD."""
import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime
from virons.monitoring_mcp_server.application.log_service import LogService
from virons.monitoring_mcp_server.domain.log_entry import LogQuery, LogEntry


@pytest.mark.asyncio
async def test_search_logs():
    """Test log search."""
    service = LogService()
    query = LogQuery(
        query="error",
        start_time="2026-03-07T00:00:00Z",
        end_time="2026-03-07T01:00:00Z",
        source="elasticsearch"
    )
    
    mock_logs = [
        LogEntry(
            timestamp=datetime.now(),
            message="Error occurred",
            level="ERROR",
            source="elasticsearch",
            labels={"app": "api"}
        )
    ]
    
    with patch.object(service.elasticsearch, 'search', new=AsyncMock(return_value=mock_logs)):
        result = await service.search_logs(query)
        
        assert len(result) == 1
        assert result[0].message == "Error occurred"
        assert result[0].level == "ERROR"


@pytest.mark.asyncio
async def test_search_logs_propagates_correlation_id():
    """Test correlation ID propagation."""
    service = LogService()
    query = LogQuery(
        query="error",
        start_time="2026-03-07T00:00:00Z",
        end_time="2026-03-07T01:00:00Z",
        source="elasticsearch"
    )
    
    with patch.object(service.elasticsearch, 'search', new=AsyncMock(return_value=[])) as mock:
        await service.search_logs(query, correlation_id="test-123")
        
        mock.assert_called_once()
        args, kwargs = mock.call_args
        assert kwargs.get("correlation_id") == "test-123" or (len(args) > 4 and args[4] == "test-123")


@pytest.mark.asyncio
async def test_search_logs_handles_errors():
    """Test error handling."""
    service = LogService()
    query = LogQuery(
        query="error",
        start_time="2026-03-07T00:00:00Z",
        end_time="2026-03-07T01:00:00Z",
        source="elasticsearch"
    )
    
    with patch.object(service.elasticsearch, 'search', new=AsyncMock(side_effect=Exception("Network error"))):
        with pytest.raises(Exception, match="Network error"):
            await service.search_logs(query)
