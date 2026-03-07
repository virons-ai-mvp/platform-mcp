"""Secret scanning application service."""
from typing import Optional
from loguru import logger
from ..infrastructure.gitleaks_client import GitleaksClient


class SecretScanService:
    """Service for scanning repositories for secrets."""

    def __init__(self):
        self.gitleaks = GitleaksClient()

    async def scan_repository(
        self,
        repository_path: str,
        scan_history: bool = False,
        correlation_id: Optional[str] = None
    ) -> list:
        """Scan repository and return findings."""
        try:
            result = await self.gitleaks.scan_repository(
                repository_path,
                scan_history,
                correlation_id
            )
            return result.get("findings", [])
        except Exception as e:
            logger.error(f"Secret scan failed: {e}")
            raise
