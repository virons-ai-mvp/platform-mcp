# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""FastMCP server implementation for virons-monitoring-mcp-server."""

import argparse
import os
import sys
from mcp.server.fastmcp import FastMCP, Context
from loguru import logger

from .compliance import setup_compliance_hooks
from .consts import SERVER_NAME, SERVER_INSTRUCTIONS, SERVER_DEPENDENCIES


# Configure logging
logger.remove()
logger.add(sys.stderr, level=os.getenv('FASTMCP_LOG_LEVEL', 'WARNING'))

mcp = None


def create_server() -> FastMCP:
    """Create and configure the FastMCP server instance.
    
    Returns:
        Configured FastMCP server
    """
    server = FastMCP(
        SERVER_NAME,
        instructions=SERVER_INSTRUCTIONS,
        dependencies=SERVER_DEPENDENCIES,
    )
    
    # Register compliance hooks
    setup_compliance_hooks(server)
    
    # Register orchestrator tools
    register_tools(server)
    
    return server


# Upstream MCP servers
UPSTREAM = {
    "cloudwatch": {"host": "localhost", "port": 9190},
    "prometheus": {"image": "ghcr.io/pab1it0/prometheus-mcp-server"},
    "grafana": {"image": "mcp/grafana"},
    "elasticsearch": {"image": "mcp/elasticsearch"},
}


def register_tools(server: FastMCP) -> None:
    """Register monitoring orchestrator tools."""
    
    @server.tool()
    async def query_metrics(
        ctx: Context,
        metric_name: str,
        start_time: str,
        end_time: str,
        source: str = "cloudwatch"
    ) -> dict:
        """Query metrics from CloudWatch, Prometheus, or Elasticsearch.
        
        Args:
            metric_name: Metric name
            start_time: Start time (ISO 8601)
            end_time: End time (ISO 8601)
            source: Metric source (cloudwatch|prometheus|elasticsearch)
        """
        try:
            # TODO: Call upstream MCP server based on source
            datapoints = []
            logger.info(f"Queried {metric_name} from {source}")
            return {"metric": metric_name, "datapoints": datapoints, "source": source}
        except Exception as e:
            logger.error(f"Metric query failed: {e}")
            await ctx.error(f"Query error: {str(e)}")
            raise
    
    @server.tool()
    async def create_alert(
        ctx: Context,
        name: str,
        metric: str,
        threshold: float,
        comparison: str
    ) -> dict:
        """Create monitoring alert rule.
        
        Args:
            name: Alert name
            metric: Metric to monitor
            threshold: Alert threshold
            comparison: Comparison operator (gt|lt|eq)
        """
        from .compliance import audit_write_operation
        
        try:
            audit_id = await audit_write_operation(
                operation_name="create_alert",
                entity_id=name,
                input_data={"metric": metric, "threshold": threshold, "comparison": comparison},
                output_data={},
            )
            
            # TODO: Call cloudwatch/prometheus MCP server
            result = {
                "name": name,
                "metric": metric,
                "threshold": threshold,
                "comparison": comparison,
                "audit_id": audit_id,
            }
            
            logger.info(f"Created alert: {name}")
            return result
            
        except Exception as e:
            logger.error(f"Alert creation failed: {e}")
            await ctx.error(f"Creation error: {str(e)}")
            raise
    
    @server.tool()
    async def create_dashboard(
        ctx: Context,
        name: str,
        panels: list
    ) -> dict:
        """Create Grafana dashboard.
        
        Args:
            name: Dashboard name
            panels: List of panel configurations
        """
        from .compliance import audit_write_operation
        
        try:
            audit_id = await audit_write_operation(
                operation_name="create_dashboard",
                entity_id=name,
                input_data={"panels": panels},
                output_data={},
            )
            
            # TODO: Call grafana MCP server
            result = {
                "name": name,
                "panels": panels,
                "audit_id": audit_id,
            }
            
            logger.info(f"Created dashboard: {name}")
            return result
            
        except Exception as e:
            logger.error(f"Dashboard creation failed: {e}")
            await ctx.error(f"Creation error: {str(e)}")
            raise
    
    @server.tool()
    async def search_logs(
        ctx: Context,
        query: str,
        start_time: str,
        end_time: str,
        source: str = "elasticsearch"
    ) -> dict:
        """Search logs in Elasticsearch or CloudWatch.
        
        Args:
            query: Search query
            start_time: Start time (ISO 8601)
            end_time: End time (ISO 8601)
            source: Log source (elasticsearch|cloudwatch)
        """
        try:
            # TODO: Call elasticsearch/cloudwatch MCP server
            logs = []
            logger.info(f"Searched logs in {source}")
            return {"query": query, "logs": logs, "source": source}
        except Exception as e:
            logger.error(f"Log search failed: {e}")
            await ctx.error(f"Search error: {str(e)}")
            raise



def main():
    """Run the MCP server with CLI argument support."""
    global mcp
    
    parser = argparse.ArgumentParser(description="Virons Monitoring MCP Server")
    parser.add_argument(
        "--allow-write",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Enable write operations (requires audit trail)",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport protocol (stdio for MCP, http for K8s probes)",
    )
    
    args = parser.parse_args()
    
    logger.info(f"Starting {SERVER_NAME} (write_enabled={args.allow_write})")
    
    mcp = create_server()
    mcp.run()


if __name__ == "__main__":
    main()
