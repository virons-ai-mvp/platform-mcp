"""Base upstream client with retry and circuit breaker."""
import httpx
from loguru import logger
from typing import Optional


class UpstreamClient:
    """Base client for upstream MCP servers."""

    def __init__(self, base_url: str, service_name: str, timeout: float = 5.0):
        self.base_url = base_url
        self.service_name = service_name
        self.timeout = timeout
        self._failures = 0
        self._circuit_open = False

    async def call_tool(self, tool_name: str, arguments: dict, correlation_id: Optional[str] = None) -> dict:
        """Call upstream tool with retry and circuit breaker."""
        if self._circuit_open:
            raise Exception(f"Circuit breaker open for {self.service_name}")

        for attempt in range(3):
            try:
                headers = {}
                if correlation_id:
                    headers["x-correlation-id"] = correlation_id

                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/tools/{tool_name}",
                        json=arguments,
                        headers=headers
                    )
                    response.raise_for_status()
                    self._failures = 0
                    return response.json()

            except Exception as e:
                self._failures += 1
                if self._failures >= 5:
                    self._circuit_open = True
                
                if attempt == 2:
                    logger.error(f"{self.service_name} call failed: {e}")
                    raise
                
                await self._backoff(attempt)

    async def _backoff(self, attempt: int):
        """Exponential backoff."""
        import asyncio
        await asyncio.sleep(2 ** attempt)
