"""IAM client for policy validation."""
from typing import Optional
from .upstream_client import UpstreamClient


class IAMClient(UpstreamClient):
    """Client for IAM MCP server."""

    def __init__(self, base_url: str = "http://localhost:9103"):
        super().__init__(base_url, "iam")

    async def validate_policy(
        self,
        policy_document: dict,
        resource_type: str,
        correlation_id: Optional[str] = None
    ) -> dict:
        """Validate IAM policy."""
        return await self.call_tool(
            "validate_policy",
            {"policy": policy_document, "resource_type": resource_type},
            correlation_id
        )
