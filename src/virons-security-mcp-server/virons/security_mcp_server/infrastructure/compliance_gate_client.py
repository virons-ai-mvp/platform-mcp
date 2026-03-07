"""Compliance gate client."""
from typing import Optional
from .upstream_client import UpstreamClient


class ComplianceGateClient(UpstreamClient):
    """Client for Compliance-gate MCP server."""

    def __init__(self, base_url: str = "http://localhost:9101"):
        super().__init__(base_url, "compliance-gate")

    async def run_gate(
        self,
        artifact_path: str,
        gate_type: str,
        correlation_id: Optional[str] = None
    ) -> dict:
        """Run compliance gate checks."""
        return await self.call_tool(
            "run_gate",
            {"artifact": artifact_path, "gate": gate_type},
            correlation_id
        )
