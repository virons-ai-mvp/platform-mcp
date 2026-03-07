"""Grafana client for dashboards."""
from .upstream_client import UpstreamClient


class GrafanaClient(UpstreamClient):
    """Client for Grafana MCP server."""
    
    async def create_dashboard(
        self,
        name: str,
        panels: list,
        tags: list = None,
        correlation_id: str = None
    ) -> dict:
        """Create Grafana dashboard."""
        result = await self.call_tool(
            "create_dashboard",
            {
                "title": name,
                "panels": panels,
                "tags": tags or []
            },
            correlation_id
        )
        
        return {
            "dashboard_id": result.get("id", name),
            "url": result.get("url", f"/d/{name}"),
            "name": name
        }
