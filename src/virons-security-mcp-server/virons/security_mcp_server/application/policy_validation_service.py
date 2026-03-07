"""Policy validation service."""
from typing import Optional
from loguru import logger
from ..infrastructure.iam_client import IAMClient


class PolicyValidationService:
    """Service for validating IAM policies."""

    def __init__(self):
        self.iam = IAMClient()

    async def validate_policy(
        self,
        policy_document: dict,
        resource_type: str,
        correlation_id: Optional[str] = None
    ) -> dict:
        """Validate IAM policy and return issues."""
        try:
            result = await self.iam.validate_policy(
                policy_document,
                resource_type,
                correlation_id
            )
            return result
        except Exception as e:
            logger.error(f"Policy validation failed: {e}")
            raise
