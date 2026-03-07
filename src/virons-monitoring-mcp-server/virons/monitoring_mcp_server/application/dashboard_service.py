"""Application service for dashboards - orchestration layer."""
from ..domain.dashboard import Dashboard
from ..infrastructure.grafana_client import GrafanaClient
from loguru import logger


class DashboardService:
    """Application service for creating and managing dashboards."""
    
    def __init__(self):
        self.grafana = GrafanaClient("http://localhost:9111")
    
    async def create_dashboard(self, dashboard: Dashboard, correlation_id: str = None) -> dict:
        """Create dashboard in Grafana."""
        try:
            # Convert domain entities to API format
            panels_data = [
                {
                    "title": p.title,
                    "query": p.query,
                    "type": p.type,
                    "datasource": p.datasource
                }
                for p in dashboard.panels
            ]
            
            # Call upstream
            result = await self.grafana.create_dashboard(
                dashboard.name,
                panels_data,
                dashboard.tags,
                correlation_id
            )
            
            logger.info(f"Created dashboard: {dashboard.name} with {dashboard.panel_count()} panels")
            return result
        
        except Exception as e:
            logger.error(f"Dashboard creation failed: {e}")
            raise
