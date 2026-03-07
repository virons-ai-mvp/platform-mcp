"""Domain entities for logs - DDD approach."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class LogEntry:
    """Log entry entity - core domain object."""
    timestamp: datetime
    message: str
    level: str  # INFO, WARN, ERROR
    source: str  # elasticsearch, cloudwatch
    labels: Dict[str, str]
    
    def __post_init__(self):
        if not self.message:
            raise ValueError("Log message required")
        if self.level not in ["INFO", "WARN", "ERROR", "DEBUG"]:
            raise ValueError(f"Invalid log level: {self.level}")


@dataclass
class LogQuery:
    """Value object for log queries."""
    query: str
    start_time: str  # ISO 8601
    end_time: str    # ISO 8601
    source: str = "elasticsearch"  # elasticsearch|cloudwatch
    size: int = 100
    
    def __post_init__(self):
        if not self.query:
            raise ValueError("Query required")
        if self.source not in ["elasticsearch", "cloudwatch"]:
            raise ValueError(f"Invalid source: {self.source}")
        if self.size < 1 or self.size > 10000:
            raise ValueError("Size must be between 1 and 10000")
