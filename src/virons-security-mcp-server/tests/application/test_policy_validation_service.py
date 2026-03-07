"""Tests for policy validation service."""
import pytest
from unittest.mock import AsyncMock, patch
from virons.security_mcp_server.application.policy_validation_service import PolicyValidationService


@pytest.mark.asyncio
async def test_validate_policy():
    service = PolicyValidationService()
    
    with patch.object(service.iam, 'validate_policy', new_callable=AsyncMock) as mock_validate:
        mock_validate.return_value = {
            "valid": False,
            "issues": [{"severity": "high", "message": "Wildcard action", "rule": "no-wildcards"}]
        }
        
        result = await service.validate_policy({"Version": "2012-10-17"}, "role")
        
        assert result["valid"] is False
        assert len(result["issues"]) == 1


@pytest.mark.asyncio
async def test_validate_policy_with_correlation_id():
    service = PolicyValidationService()
    
    with patch.object(service.iam, 'validate_policy', new_callable=AsyncMock) as mock_validate:
        mock_validate.return_value = {"valid": True, "issues": []}
        
        await service.validate_policy({"Version": "2012-10-17"}, "user", "corr-123")
        
        mock_validate.assert_called_once_with({"Version": "2012-10-17"}, "user", "corr-123")


@pytest.mark.asyncio
async def test_validate_policy_handles_errors():
    service = PolicyValidationService()
    
    with patch.object(service.iam, 'validate_policy', new_callable=AsyncMock) as mock_validate:
        mock_validate.side_effect = Exception("Validation failed")
        
        with pytest.raises(Exception, match="Validation failed"):
            await service.validate_policy({}, "role")
