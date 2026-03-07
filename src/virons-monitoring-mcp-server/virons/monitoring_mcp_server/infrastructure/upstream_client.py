"""Base upstream client - minimal implementation to pass tests."""
import asyncio
from typing import Optional
import httpx
from loguru import logger


class UpstreamClient:
    """Base client for upstream MCP servers with retry and circuit breaker."""
    
    def __init__(self, base_url: str, timeout: float = 5.0, max_retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self._failures = 0
        self._circuit_open = False
    
    async def call_tool(self, tool_name: str, params: dict, correlation_id: Optional[str] = None) -> dict:
        """Call upstream tool with retry and circuit breaker."""
        if self._circuit_open:
            raise Exception("Circuit breaker open")
        
        headers = {}
        if correlation_id:
            headers["x-correlation-id"] = correlation_id
        
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/tools/{tool_name}",
                        json=params,
                        headers=headers
                    )
                    response.raise_for_status()
                    self._failures = 0
                    return response.json()
            except Exception as e:
                self._failures += 1
                if self._failures >= 5:
                    self._circuit_open = True
                
                if attempt == self.max_retries - 1:
                    logger.error(f"Upstream call failed: {e}")
                    raise
                
                await asyncio.sleep(2 ** attempt)
        
        raise Exception("Max retries exceeded")
