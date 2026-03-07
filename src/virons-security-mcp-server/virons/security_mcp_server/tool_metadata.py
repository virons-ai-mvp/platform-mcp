# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tool metadata enrichment for security MCP server."""

TOOL_EXAMPLES = {
    "scan_secrets": {
        "category": "security",
        "examples": [
            {
                "description": "Scan repository for exposed secrets",
                "parameters": {
                    "repository_path": "/repos/virons-api",
                    "scan_history": False
                }
            },
            {
                "description": "Full history scan for leaked credentials",
                "parameters": {
                    "repository_path": "/repos/payment-service",
                    "scan_history": True
                }
            }
        ]
    },
    "audit_cloudtrail": {
        "category": "security",
        "examples": [
            {
                "description": "Query CloudTrail for suspicious API calls",
                "parameters": {
                    "start_time": "2026-03-01T00:00:00Z",
                    "end_time": "2026-03-07T23:59:59Z",
                    "event_name": "DeleteBucket"
                }
            }
        ]
    },
    "check_iam_policy": {
        "category": "security",
        "examples": [
            {
                "description": "Validate IAM role policy for least privilege",
                "parameters": {
                    "policy_document": {
                        "Version": "2012-10-17",
                        "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]
                    },
                    "resource_type": "role"
                }
            }
        ]
    },
    "run_compliance_gate": {
        "category": "security",
        "examples": [
            {
                "description": "Pre-deploy compliance check",
                "parameters": {
                    "artifact_path": "/builds/api-v2.1.0.zip",
                    "gate_type": "pre-deploy"
                }
            }
        ]
    }
}


def enrich_tool_metadata(tool_name: str, base_metadata: dict) -> dict:
    """Enrich tool metadata with security-specific examples."""
    enrichment = TOOL_EXAMPLES.get(tool_name, {})
    if enrichment:
        base_metadata["category"] = enrichment.get("category", "security")
        base_metadata["examples"] = enrichment.get("examples", [])
    return base_metadata
