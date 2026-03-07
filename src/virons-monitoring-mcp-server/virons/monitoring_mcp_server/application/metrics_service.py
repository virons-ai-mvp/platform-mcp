"""Application service for metrics - orchestration layer."""
from typing import List
from ..domain.metric import Metric, MetricQuery
from ..infrastructure.cloudwatch_client import CloudWatchClient
from ..infrastructure.prometheus_client import PrometheusClient
from loguru import logger


class MetricsService:
    """Application service for querying metrics from multiple sources."""
    
    def __init__(self):
        self.cloudwatch = CloudWatchClient("http://localhost:9109")
        self.prometheus = PrometheusClient("http://localhost:9110")
    
    async def query_metrics(self, query: MetricQuery, correlation_id: str = None) -> List[Metric]:
        """Query metrics from appropriate source."""
        try:
            if query.source == "cloudwatch":
                return await self.cloudwatch.query_metrics(
                    query.metric_name,
                    query.start_time,
                    query.end_time,
                    correlation_id
                )
            elif query.source == "prometheus":
                return await self.prometheus.query_range(
                    query.metric_name,
                    query.start_time,
                    query.end_time,
                    correlation_id=correlation_id
                )
            else:
                raise ValueError(f"Unsupported source: {query.source}")
        
        except Exception as e:
            logger.error(f"Metrics query failed: {e}")
            raise
