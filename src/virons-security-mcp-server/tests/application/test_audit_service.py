"""Tests for audit service."""
import pytest
from unittest.mock import AsyncMock, patch
from virons.security_mcp_server.application.audit_service import AuditService


@pytest.mark.asyncio
async def test_query_events():
    service = AuditService()
    
    with patch.object(service.cloudtrail, 'lookup_events', new_callable=AsyncMock) as mock_lookup:
        mock_lookup.return_value = {
            "events": [
                {"EventName": "CreateUser", "EventTime": "2026-03-07T10:00:00Z", "Username": "admin"}
            ]
        }
        
        result = await service.query_events("2026-03-07T00:00:00Z", "2026-03-07T01:00:00Z")
        
        assert len(result) == 1
        assert result[0]["EventName"] == "CreateUser"


@pytest.mark.asyncio
async def test_query_events_with_filter():
    service = AuditService()
    
    with patch.object(service.cloudtrail, 'lookup_events', new_callable=AsyncMock) as mock_lookup:
        mock_lookup.return_value = {"events": []}
        
        await service.query_events("2026-03-07T00:00:00Z", "2026-03-07T01:00:00Z", "CreateUser", "corr-123")
        
        mock_lookup.assert_called_once_with("2026-03-07T00:00:00Z", "2026-03-07T01:00:00Z", "CreateUser", "corr-123")


@pytest.mark.asyncio
async def test_query_events_handles_errors():
    service = AuditService()
    
    with patch.object(service.cloudtrail, 'lookup_events', new_callable=AsyncMock) as mock_lookup:
        mock_lookup.side_effect = Exception("Query failed")
        
        with pytest.raises(Exception, match="Query failed"):
            await service.query_events("2026-03-07T00:00:00Z", "2026-03-07T01:00:00Z")
