"""Tests for secret scan service."""
import pytest
from unittest.mock import AsyncMock, patch
from virons.security_mcp_server.application.secret_scan_service import SecretScanService


@pytest.mark.asyncio
async def test_scan_repository():
    service = SecretScanService()
    
    with patch.object(service.gitleaks, 'scan_repository', new_callable=AsyncMock) as mock_scan:
        mock_scan.return_value = {
            "findings": [
                {"type": "aws_key", "file": "config.py", "line": 10, "secret": "AKIA***"}
            ]
        }
        
        result = await service.scan_repository("/repo", False)
        
        assert len(result) == 1
        assert result[0]["type"] == "aws_key"
        mock_scan.assert_called_once()


@pytest.mark.asyncio
async def test_scan_repository_with_history():
    service = SecretScanService()
    
    with patch.object(service.gitleaks, 'scan_repository', new_callable=AsyncMock) as mock_scan:
        mock_scan.return_value = {"findings": []}
        
        await service.scan_repository("/repo", True, "corr-123")
        
        mock_scan.assert_called_once_with("/repo", True, "corr-123")


@pytest.mark.asyncio
async def test_scan_repository_handles_errors():
    service = SecretScanService()
    
    with patch.object(service.gitleaks, 'scan_repository', new_callable=AsyncMock) as mock_scan:
        mock_scan.side_effect = Exception("Scan failed")
        
        with pytest.raises(Exception, match="Scan failed"):
            await service.scan_repository("/repo", False)
