"""Elasticsearch client for log search."""
from typing import List
from datetime import datetime
from .upstream_client import UpstreamClient
from ..domain.log_entry import LogEntry


class ElasticsearchClient(UpstreamClient):
    """Client for Elasticsearch MCP server."""
    
    async def search(
        self,
        query: str,
        start_time: str,
        end_time: str,
        size: int = 100,
        correlation_id: str = None
    ) -> List[LogEntry]:
        """Search logs in Elasticsearch."""
        result = await self.call_tool(
            "search",
            {
                "query": query,
                "start_time": start_time,
                "end_time": end_time,
                "size": size
            },
            correlation_id
        )
        
        # Convert to domain entities
        logs = []
        for hit in result.get("hits", []):
            source = hit.get("_source", {})
            logs.append(LogEntry(
                timestamp=datetime.fromisoformat(source.get("timestamp", start_time).replace("Z", "+00:00")),
                message=source.get("message", ""),
                level=source.get("level", "INFO"),
                source="elasticsearch",
                labels=source.get("labels", {})
            ))
        
        return logs
