"""Prometheus client for metrics."""
from typing import List
from datetime import datetime
from .upstream_client import UpstreamClient
from ..domain.metric import Metric


class PrometheusClient(UpstreamClient):
    """Client for Prometheus MCP server."""
    
    async def query_range(
        self,
        query: str,
        start_time: str,
        end_time: str,
        step: str = "5m",
        correlation_id: str = None
    ) -> List[Metric]:
        """Query Prometheus range."""
        result = await self.call_tool(
            "query_range",
            {
                "query": query,
                "start": start_time,
                "end": end_time,
                "step": step
            },
            correlation_id
        )
        
        # Convert to domain entities
        metrics = []
        for series in result.get("data", {}).get("result", []):
            metric_name = series.get("metric", {}).get("__name__", query)
            labels = series.get("metric", {})
            
            for value in series.get("values", []):
                timestamp, val = value
                metrics.append(Metric(
                    name=metric_name,
                    value=float(val),
                    timestamp=datetime.fromtimestamp(timestamp),
                    labels=labels,
                    source="prometheus"
                ))
        
        return metrics
