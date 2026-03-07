"""Domain entities for audit events."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class AuditEvent:
    """CloudTrail audit event."""
    event_name: str
    timestamp: str
    user: str
    resource: Optional[str] = None

    def __post_init__(self):
        if not self.event_name:
            raise ValueError("Event name is required")
        if not self.timestamp:
            raise ValueError("Timestamp is required")


@dataclass
class AuditQuery:
    """Query for audit events."""
    start_time: str
    end_time: str
    event_name: Optional[str] = None

    def __post_init__(self):
        if not self.start_time:
            raise ValueError("Start time is required")
        if not self.end_time:
            raise ValueError("End time is required")
