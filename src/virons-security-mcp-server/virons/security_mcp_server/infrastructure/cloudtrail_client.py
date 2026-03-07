"""CloudTrail client for audit logs."""
from typing import Optional
from .upstream_client import UpstreamClient


class CloudTrailClient(UpstreamClient):
    """Client for CloudTrail MCP server."""

    def __init__(self, base_url: str = "http://localhost:9102"):
        super().__init__(base_url, "cloudtrail")

    async def lookup_events(
        self,
        start_time: str,
        end_time: str,
        event_name: Optional[str] = None,
        correlation_id: Optional[str] = None
    ) -> dict:
        """Query CloudTrail events."""
        args = {"start_time": start_time, "end_time": end_time}
        if event_name:
            args["event_name"] = event_name
        
        return await self.call_tool("lookup_events", args, correlation_id)
