"""Domain entities for metrics - DDD approach."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class Metric:
    """Metric entity - core domain object."""
    name: str
    value: float
    timestamp: datetime
    labels: Dict[str, str]
    source: str  # cloudwatch, prometheus, elasticsearch
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Metric name required")
        if self.value is None:
            raise ValueError("Metric value required")


@dataclass
class MetricQuery:
    """Value object for metric queries."""
    metric_name: str
    start_time: str  # ISO 8601
    end_time: str    # ISO 8601
    source: str = "cloudwatch"  # cloudwatch|prometheus|elasticsearch
    
    def __post_init__(self):
        if self.source not in ["cloudwatch", "prometheus", "elasticsearch"]:
            raise ValueError(f"Invalid source: {self.source}")
