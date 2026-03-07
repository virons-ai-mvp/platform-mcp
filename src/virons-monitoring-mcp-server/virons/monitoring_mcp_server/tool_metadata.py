# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tool metadata enrichment for monitoring MCP server."""

TOOL_EXAMPLES = {
    "query_metrics": {
        "category": "monitoring",
        "upstream_service": "cloudwatch/prometheus",
        "examples": [
            {
                "description": "Query CloudWatch CPU metrics",
                "parameters": {
                    "metric_name": "CPUUtilization",
                    "start_time": "2026-03-07T00:00:00Z",
                    "end_time": "2026-03-07T01:00:00Z",
                    "source": "cloudwatch"
                }
            },
            {
                "description": "Query Prometheus metrics",
                "parameters": {
                    "metric_name": "node_cpu_seconds_total",
                    "start_time": "2026-03-07T00:00:00Z",
                    "end_time": "2026-03-07T01:00:00Z",
                    "source": "prometheus"
                }
            }
        ]
    },
    "create_alert": {
        "category": "monitoring",
        "upstream_service": "cloudwatch",
        "examples": [
            {
                "description": "Create high CPU alert",
                "parameters": {
                    "name": "high_cpu_alert",
                    "metric": "CPUUtilization",
                    "threshold": 80.0,
                    "comparison": "gt"
                }
            },
            {
                "description": "Create low memory alert",
                "parameters": {
                    "name": "low_memory_alert",
                    "metric": "MemoryAvailable",
                    "threshold": 1024.0,
                    "comparison": "lt"
                }
            }
        ]
    },
    "create_dashboard": {
        "category": "monitoring",
        "upstream_service": "grafana",
        "examples": [
            {
                "description": "Create system overview dashboard",
                "parameters": {
                    "name": "System Overview",
                    "panels": [
                        {"title": "CPU Usage", "query": "cpu_usage", "type": "graph"},
                        {"title": "Memory Usage", "query": "memory_usage", "type": "stat"},
                        {"title": "Disk I/O", "query": "disk_io", "type": "table"}
                    ]
                }
            }
        ]
    },
    "search_logs": {
        "category": "monitoring",
        "upstream_service": "elasticsearch",
        "examples": [
            {
                "description": "Search error logs",
                "parameters": {
                    "query": "error",
                    "start_time": "2026-03-07T00:00:00Z",
                    "end_time": "2026-03-07T01:00:00Z",
                    "level": "ERROR",
                    "size": 100
                }
            },
            {
                "description": "Search application logs",
                "parameters": {
                    "query": "payment processing",
                    "start_time": "2026-03-07T00:00:00Z",
                    "end_time": "2026-03-07T23:59:59Z",
                    "size": 50
                }
            }
        ]
    }
}


def enrich_tool_metadata(tool_name: str, base_metadata: dict) -> dict:
    """Enrich tool metadata with monitoring-specific examples and upstream info."""
    enrichment = TOOL_EXAMPLES.get(tool_name, {})
    if enrichment:
        base_metadata["category"] = enrichment.get("category", "monitoring")
        base_metadata["examples"] = enrichment.get("examples", [])
        base_metadata["upstream_service"] = enrichment.get("upstream_service", "")
    return base_metadata
