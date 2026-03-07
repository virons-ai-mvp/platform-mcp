"""Application service for logs - orchestration layer."""
from typing import List
from ..domain.log_entry import LogEntry, LogQuery
from ..infrastructure.elasticsearch_client import ElasticsearchClient
from loguru import logger


class LogService:
    """Application service for searching logs."""
    
    def __init__(self):
        self.elasticsearch = ElasticsearchClient("http://localhost:9112")
    
    async def search_logs(self, query: LogQuery, correlation_id: str = None) -> List[LogEntry]:
        """Search logs from appropriate source."""
        try:
            if query.source == "elasticsearch":
                return await self.elasticsearch.search(
                    query.query,
                    query.start_time,
                    query.end_time,
                    query.size,
                    correlation_id
                )
            else:
                # CloudWatch logs would go here
                raise ValueError(f"Unsupported source: {query.source}")
        
        except Exception as e:
            logger.error(f"Log search failed: {e}")
            raise
