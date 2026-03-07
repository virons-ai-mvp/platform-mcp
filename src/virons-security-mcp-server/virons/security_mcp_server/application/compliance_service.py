"""Compliance gate service."""
from typing import Optional
from loguru import logger
from ..infrastructure.compliance_gate_client import ComplianceGateClient


class ComplianceService:
    """Service for running compliance gates."""

    def __init__(self):
        self.gate_client = ComplianceGateClient()

    async def run_gate(
        self,
        artifact_path: str,
        gate_type: str,
        correlation_id: Optional[str] = None
    ) -> dict:
        """Run compliance gate and return results."""
        try:
            result = await self.gate_client.run_gate(
                artifact_path,
                gate_type,
                correlation_id
            )
            return result
        except Exception as e:
            logger.error(f"Compliance gate failed: {e}")
            raise
