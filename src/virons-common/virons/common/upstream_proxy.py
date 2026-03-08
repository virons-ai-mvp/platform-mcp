"""Generic upstream proxy for auto-forwarding tools."""
from typing import Dict, List, Optional
from loguru import logger
import httpx


class UpstreamProxy:
    """Generic proxy that forwards calls to upstream MCP servers."""

    def __init__(self, upstream_configs: Dict[str, Dict]):
        """Initialize proxy with upstream configurations.
        
        Args:
            upstream_configs: Dict of {name: {host, port}} for each upstream
        """
        self.upstreams = upstream_configs
        self._tool_cache: Dict[str, str] = {}  # tool_name -> upstream_name

    async def discover_tools(self) -> Dict[str, List[str]]:
        """Discover all tools from all upstreams.
        
        Returns:
            Dict of {upstream_name: [tool_names]}
        """
        discovered = {}
        
        for name, config in self.upstreams.items():
            try:
                url = f"http://{config['host']}:{config['port']}/tools"
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(url)
                    if response.status_code == 200:
                        tools = response.json().get("tools", [])
                        tool_names = [t["name"] for t in tools]
                        discovered[name] = tool_names
                        
                        # Cache tool -> upstream mapping
                        for tool_name in tool_names:
                            self._tool_cache[tool_name] = name
                        
                        logger.info(f"Discovered {len(tool_names)} tools from {name}")
            except Exception as e:
                logger.warning(f"Failed to discover tools from {name}: {e}")
                discovered[name] = []
        
        return discovered

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict,
        correlation_id: Optional[str] = None
    ) -> dict:
        """Forward tool call to appropriate upstream.
        
        Args:
            tool_name: Name of tool to call
            arguments: Tool arguments
            correlation_id: Optional correlation ID
            
        Returns:
            Tool response from upstream
        """
        # Find which upstream has this tool
        upstream_name = self._tool_cache.get(tool_name)
        if not upstream_name:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        config = self.upstreams[upstream_name]
        url = f"http://{config['host']}:{config['port']}/tools/{tool_name}"
        
        headers = {}
        if correlation_id:
            headers["x-correlation-id"] = correlation_id
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=arguments, headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Proxy call to {upstream_name}.{tool_name} failed: {e}")
            raise

    def get_upstream_for_tool(self, tool_name: str) -> Optional[str]:
        """Get upstream name for a tool."""
        return self._tool_cache.get(tool_name)
