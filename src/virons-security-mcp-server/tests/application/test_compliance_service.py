"""Tests for compliance service."""
import pytest
from unittest.mock import AsyncMock, patch
from virons.security_mcp_server.application.compliance_service import ComplianceService


@pytest.mark.asyncio
async def test_run_gate():
    service = ComplianceService()
    
    with patch.object(service.gate_client, 'run_gate', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = {
            "status": "passed",
            "checks_passed": 10,
            "checks_failed": 0
        }
        
        result = await service.run_gate("/artifact.jar", "pre-deploy")
        
        assert result["status"] == "passed"
        assert result["checks_passed"] == 10


@pytest.mark.asyncio
async def test_run_gate_with_correlation_id():
    service = ComplianceService()
    
    with patch.object(service.gate_client, 'run_gate', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = {"status": "passed"}
        
        await service.run_gate("/artifact.jar", "post-deploy", "corr-123")
        
        mock_run.assert_called_once_with("/artifact.jar", "post-deploy", "corr-123")


@pytest.mark.asyncio
async def test_run_gate_handles_errors():
    service = ComplianceService()
    
    with patch.object(service.gate_client, 'run_gate', new_callable=AsyncMock) as mock_run:
        mock_run.side_effect = Exception("Gate failed")
        
        with pytest.raises(Exception, match="Gate failed"):
            await service.run_gate("/artifact.jar", "pre-commit")
