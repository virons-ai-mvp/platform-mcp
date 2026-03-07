"""Domain entities for alerts - DDD approach."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Alert:
    """Alert entity - core domain object."""
    name: str
    metric: str
    threshold: float
    comparison: str  # gt, lt, eq
    enabled: bool = True
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Alert name required")
        if not self.metric:
            raise ValueError("Metric required")
        if self.comparison not in ["gt", "lt", "eq"]:
            raise ValueError(f"Invalid comparison: {self.comparison}")
    
    def evaluate(self, value: float) -> bool:
        """Evaluate if alert should trigger."""
        if self.comparison == "gt":
            return value > self.threshold
        elif self.comparison == "lt":
            return value < self.threshold
        else:  # eq
            return value == self.threshold
