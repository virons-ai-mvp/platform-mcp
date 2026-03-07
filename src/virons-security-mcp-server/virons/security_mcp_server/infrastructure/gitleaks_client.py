"""Gitleaks client for secret scanning."""
from typing import Optional
from .upstream_client import UpstreamClient


class GitleaksClient(UpstreamClient):
    """Client for Gitleaks MCP server."""

    def __init__(self, base_url: str = "http://localhost:9100"):
        super().__init__(base_url, "gitleaks")

    async def scan_repository(
        self,
        repository_path: str,
        scan_history: bool = False,
        correlation_id: Optional[str] = None
    ) -> dict:
        """Scan repository for secrets."""
        return await self.call_tool(
            "scan",
            {
                "path": repository_path,
                "scan_history": scan_history
            },
            correlation_id
        )
