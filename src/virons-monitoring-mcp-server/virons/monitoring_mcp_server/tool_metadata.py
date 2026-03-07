# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tool metadata enrichment for monitoring MCP server."""

TOOL_EXAMPLES = {
    "query_metrics": {
        "category": "monitoring",
        "examples": [{"description": "Query CloudWatch metrics", "parameters": {"namespace": "AWS/Lambda", "metric_name": "Invocations", "start_time": "2026-03-07T00:00:00Z", "end_time": "2026-03-07T23:59:59Z"}}]
    },
    "create_alert": {
        "category": "monitoring",
        "examples": [{"description": "Create CloudWatch alarm", "parameters": {"alarm_name": "high-error-rate", "metric_name": "Errors", "threshold": 10, "comparison": "GreaterThanThreshold"}}]
    },
    "create_dashboard": {
        "category": "monitoring",
        "examples": [{"description": "Create CloudWatch dashboard", "parameters": {"dashboard_name": "production-overview", "widgets": [{"type": "metric", "properties": {"metrics": [["AWS/Lambda", "Invocations"]]}}]}}]
    },
    "search_logs": {
        "category": "monitoring",
        "examples": [{"description": "Search CloudWatch Logs", "parameters": {"log_group": "/aws/lambda/payment-processor", "query": "fields @timestamp, @message | filter @message like /ERROR/", "start_time": "2026-03-07T00:00:00Z"}}]
    }
}


def enrich_tool_metadata(tool_name: str, base_metadata: dict) -> dict:
    """Enrich tool metadata with monitoring-specific examples."""
    enrichment = TOOL_EXAMPLES.get(tool_name, {})
    if enrichment:
        base_metadata["category"] = enrichment.get("category", "monitoring")
        base_metadata["examples"] = enrichment.get("examples", [])
    return base_metadata
