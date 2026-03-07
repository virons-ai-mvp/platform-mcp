"""Audit service for CloudTrail queries."""
from typing import Optional
from loguru import logger
from ..infrastructure.cloudtrail_client import CloudTrailClient


class AuditService:
    """Service for querying audit events."""

    def __init__(self):
        self.cloudtrail = CloudTrailClient()

    async def query_events(
        self,
        start_time: str,
        end_time: str,
        event_name: Optional[str] = None,
        correlation_id: Optional[str] = None
    ) -> list:
        """Query CloudTrail events."""
        try:
            result = await self.cloudtrail.lookup_events(
                start_time,
                end_time,
                event_name,
                correlation_id
            )
            return result.get("events", [])
        except Exception as e:
            logger.error(f"CloudTrail query failed: {e}")
            raise
