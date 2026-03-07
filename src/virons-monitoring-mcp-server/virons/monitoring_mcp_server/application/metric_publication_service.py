"""Metric publication service."""
from typing import List, Optional
from loguru import logger
from ..infrastructure.cloudwatch_client import CloudWatchClient


class MetricPublicationService:
    """Service for publishing custom metrics."""

    def __init__(self):
        self.cloudwatch = CloudWatchClient("http://localhost:9109")

    async def publish_metrics(
        self,
        namespace: str,
        metric_data: List[dict],
        correlation_id: Optional[str] = None
    ) -> dict:
        """Publish metrics to CloudWatch."""
        try:
            result = await self.cloudwatch.put_metric_data(
                namespace,
                metric_data,
                correlation_id=correlation_id
            )
            return result
        except Exception as e:
            logger.error(f"Metric publication failed: {e}")
            raise
