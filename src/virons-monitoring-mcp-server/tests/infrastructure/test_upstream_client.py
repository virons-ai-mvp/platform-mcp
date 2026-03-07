"""Tests for UpstreamClient - TDD approach."""
import pytest
from unittest.mock import AsyncMock, patch
from virons.monitoring_mcp_server.infrastructure.upstream_client import UpstreamClient


@pytest.mark.asyncio
async def test_call_tool_success():
    """Test successful upstream call."""
    client = UpstreamClient("http://localhost:9109")
    
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={"result": "success"})
        mock_response.raise_for_status = AsyncMock()
        
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        
        result = await client.call_tool("query_metrics", {"metric": "cpu"})
        
        assert result == {"result": "success"}


@pytest.mark.asyncio
async def test_call_tool_with_correlation_id():
    """Test correlation ID propagation."""
    client = UpstreamClient("http://localhost:9109")
    
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={"result": "success"})
        mock_response.raise_for_status = AsyncMock()
        
        mock_post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value.post = mock_post
        
        await client.call_tool("query_metrics", {"metric": "cpu"}, correlation_id="test-123")
        
        # Verify correlation ID in headers
        call_args = mock_post.call_args
        assert call_args[1]["headers"]["x-correlation-id"] == "test-123"


@pytest.mark.asyncio
async def test_call_tool_retry_on_failure():
    """Test retry logic with exponential backoff."""
    client = UpstreamClient("http://localhost:9109", max_retries=3)
    
    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            side_effect=[Exception("Network error"), Exception("Network error"), 
                        AsyncMock(json=lambda: {"result": "success"}, raise_for_status=AsyncMock())]
        )
        
        with patch("asyncio.sleep") as mock_sleep:
            result = await client.call_tool("query_metrics", {"metric": "cpu"})
            
            assert result == {"result": "success"}
            assert mock_sleep.call_count == 2  # 2 retries before success


@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_failures():
    """Test circuit breaker opens after 5 failures."""
    client = UpstreamClient("http://localhost:9109", max_retries=1)
    
    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            side_effect=Exception("Network error")
        )
        
        # Trigger 5 failures
        for _ in range(5):
            with pytest.raises(Exception):
                await client.call_tool("query_metrics", {"metric": "cpu"})
        
        # Circuit should be open now
        with pytest.raises(Exception, match="Circuit breaker open"):
            await client.call_tool("query_metrics", {"metric": "cpu"})
