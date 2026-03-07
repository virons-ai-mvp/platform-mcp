# Monitoring MCP Server - Core Implementation

## Overview

Monitoring orchestration layer coordinating 4 upstream MCP servers for metrics, dashboards, and alerts.

## Structure

```
monitoring_mcp_server/
├── application/       # Use cases (future: metrics aggregation)
├── domain/           # Business logic (future: alert rules)
├── infrastructure/   # External integrations (future: monitoring clients)
├── server.py         # FastMCP server (stdio/http/api modes)
├── compliance.py     # Audit logging
├── consts.py         # Constants
├── models.py         # Data models
└── tool_metadata.py  # Tool enrichment with examples
```

## Tools

```python
@server.tool()
async def query_metrics(source: str, query: str, start: str, end: str = None)
  # Query metrics from CloudWatch/Prometheus

@server.tool()
async def create_dashboard(name: str, panels: list, datasource: str)
  # Create Grafana dashboard

@server.tool()
async def set_alert(name: str, condition: str, threshold: float, notification: str)
  # Configure alert rules

@server.tool()
async def check_system_health()
  # Aggregate system health from all sources
```

## Upstreams

```python
UPSTREAM = {
    "cloudwatch": {"host": "localhost", "port": 9109},
    "prometheus": {"host": "localhost", "port": 9110},
    "grafana": {"host": "localhost", "port": 9111},
    "elasticsearch": {"host": "localhost", "port": 9112},
}
```

## Navigation

← [Monitoring MCP Server](../..)  
→ [Application Layer](application/)  
→ [Domain Layer](domain/)  
→ [Infrastructure Layer](infrastructure/)
