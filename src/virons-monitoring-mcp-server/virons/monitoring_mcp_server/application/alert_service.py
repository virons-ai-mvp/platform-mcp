"""Application service for alerts - orchestration layer."""
from ..domain.alert import Alert
from ..infrastructure.cloudwatch_client import CloudWatchClient
from loguru import logger


class AlertService:
    """Application service for creating and managing alerts."""
    
    def __init__(self):
        self.cloudwatch = CloudWatchClient("http://localhost:9109")
    
    async def create_alert(self, alert: Alert, correlation_id: str = None) -> dict:
        """Create alert in upstream monitoring system."""
        try:
            # Validate alert
            if not alert.enabled:
                logger.warning(f"Creating disabled alert: {alert.name}")
            
            # Call upstream (CloudWatch for now)
            result = await self.cloudwatch.create_alarm(
                alert.name,
                alert.metric,
                alert.threshold,
                alert.comparison,
                correlation_id
            )
            
            logger.info(f"Created alert: {alert.name}")
            return result
        
        except Exception as e:
            logger.error(f"Alert creation failed: {e}")
            raise
