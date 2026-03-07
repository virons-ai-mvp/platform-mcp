"""Domain entities for metric publication."""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MetricDatum:
    """Single metric data point to publish."""
    name: str
    value: float
    timestamp: str
    unit: Optional[str] = None
    dimensions: Optional[dict] = None

    def __post_init__(self):
        if not self.name:
            raise ValueError("Metric name is required")
        if self.value is None:
            raise ValueError("Metric value is required")


@dataclass
class MetricData:
    """Collection of metrics to publish."""
    namespace: str
    metric_data: List[MetricDatum]

    def __post_init__(self):
        if not self.namespace:
            raise ValueError("Namespace is required")
