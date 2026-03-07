# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tool metadata enrichment for operations MCP server."""

TOOL_EXAMPLES = {
    "list_clusters": {
        "category": "query",
        "examples": [{"description": "List ECS clusters in region", "parameters": {"region": "eu-central-1"}}]
    },
    "deploy_lambda": {
        "category": "deployment",
        "examples": [{"description": "Deploy Lambda function", "parameters": {"function_name": "payment-processor", "runtime": "python3.13", "handler": "main.handler", "code_path": "/builds/lambda.zip"}}]
    },
    "deploy_ecs_service": {
        "category": "deployment",
        "examples": [{"description": "Deploy ECS service", "parameters": {"cluster": "production", "service_name": "api-service", "task_definition": "api:12", "desired_count": 3}}]
    },
    "start_workflow": {
        "category": "deployment",
        "examples": [{"description": "Start Step Functions workflow", "parameters": {"workflow_arn": "arn:aws:states:eu-central-1:123456789012:stateMachine:payment-flow", "input": {"transaction_id": "tx-12345"}}}]
    }
}


def enrich_tool_metadata(tool_name: str, base_metadata: dict) -> dict:
    """Enrich tool metadata with operations-specific examples."""
    enrichment = TOOL_EXAMPLES.get(tool_name, {})
    if enrichment:
        base_metadata["category"] = enrichment.get("category", "deployment")
        base_metadata["examples"] = enrichment.get("examples", [])
    return base_metadata
