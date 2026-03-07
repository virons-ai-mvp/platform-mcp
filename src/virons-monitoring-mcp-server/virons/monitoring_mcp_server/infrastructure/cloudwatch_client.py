"""CloudWatch client for metrics and logs."""
from typing import List, Dict
from datetime import datetime
from .upstream_client import UpstreamClient
from ..domain.metric import Metric


class CloudWatchClient(UpstreamClient):
    """Client for CloudWatch MCP server."""
    
    async def query_metrics(
        self, 
        metric_name: str, 
        start_time: str, 
        end_time: str,
        correlation_id: str = None
    ) -> List[Metric]:
        """Query CloudWatch metrics."""
        result = await self.call_tool(
            "get_metric_statistics",
            {
                "namespace": "AWS/EC2",
                "metric_name": metric_name,
                "start_time": start_time,
                "end_time": end_time,
                "period": 300,
                "statistics": ["Average"]
            },
            correlation_id
        )
        
        # Convert to domain entities
        metrics = []
        for datapoint in result.get("datapoints", []):
            metrics.append(Metric(
                name=metric_name,
                value=datapoint.get("Average", 0.0),
                timestamp=datetime.fromisoformat(datapoint.get("Timestamp", start_time).replace("Z", "+00:00")),
                labels={"namespace": "AWS/EC2"},
                source="cloudwatch"
            ))
        
        return metrics
    
    async def create_alarm(
        self,
        name: str,
        metric: str,
        threshold: float,
        comparison: str,
        correlation_id: str = None
    ) -> dict:
        """Create CloudWatch alarm."""
        result = await self.call_tool(
            "put_metric_alarm",
            {
                "alarm_name": name,
                "metric_name": metric,
                "threshold": threshold,
                "comparison_operator": comparison.upper(),
                "evaluation_periods": 1,
                "period": 300
            },
            correlation_id
        )
        
        return {"alarm_id": result.get("alarm_arn", name), "name": name}
    
    async def put_metric_data(
        self,
        namespace: str,
        metric_data: List[dict],
        correlation_id: str = None
    ) -> dict:
        """Publish custom metrics to CloudWatch."""
        result = await self.call_tool(
            "put_metric_data",
            {
                "namespace": namespace,
                "metric_data": metric_data
            },
            correlation_id
        )
        
        return result
