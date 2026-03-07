# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tool metadata enrichment with real-world examples."""

TOOL_EXAMPLES = {
    "deploy_infrastructure": {
        "category": "deployment",
        "examples": [
            {
                "description": "Deploy a Terraform stack",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-vpc",
                    "template_path": "./terraform/vpc",
                    "parameters": {"region": "eu-central-1", "cidr": "10.0.0.0/16"}
                }
            },
            {
                "description": "Deploy a CDK stack",
                "parameters": {
                    "tool": "cdk",
                    "stack_name": "api-gateway-stack",
                    "template_path": "./cdk/api-gateway",
                    "parameters": {"stage": "production"}
                }
            }
        ]
    },
    "destroy_infrastructure": {
        "category": "deployment",
        "examples": [
            {
                "description": "Destroy a test environment",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "test-environment",
                    "confirm": True
                }
            }
        ]
    },
    "list_stacks": {
        "category": "query",
        "examples": [
            {
                "description": "List all CloudFormation stacks",
                "parameters": {"tool": "cfn"}
            },
            {
                "description": "List all Terraform stacks",
                "parameters": {"tool": "terraform"}
            }
        ]
    },
    "get_stack_info": {
        "category": "query",
        "examples": [
            {
                "description": "Get detailed information about a stack",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-vpc"
                }
            }
        ]
    },
    "update_stack": {
        "category": "deployment",
        "examples": [
            {
                "description": "Update stack with new template",
                "parameters": {
                    "tool": "cfn",
                    "stack_name": "api-stack",
                    "template_path": "./cloudformation/api-v2.yaml",
                    "parameters": {"InstanceType": "t3.medium"}
                }
            }
        ]
    },
    "scan_security": {
        "category": "security",
        "examples": [
            {
                "description": "Run security scan on production stack",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-vpc"
                }
            }
        ]
    },
    "get_cost_breakdown": {
        "category": "cost",
        "examples": [
            {
                "description": "Get cost breakdown for a stack",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-database"
                }
            }
        ]
    },
    "create_backup": {
        "category": "backup",
        "examples": [
            {
                "description": "Create backup of production stack",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-database"
                }
            }
        ]
    },
    "list_backups": {
        "category": "backup",
        "examples": [
            {
                "description": "List all backups for a stack",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-database"
                }
            }
        ]
    },
    "restore_backup": {
        "category": "backup",
        "examples": [
            {
                "description": "Restore from a specific backup",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-database",
                    "backup_id": "backup-20260307-143000"
                }
            }
        ]
    },
    "backup_state": {
        "category": "backup",
        "examples": [
            {
                "description": "Backup Terraform state",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-vpc"
                }
            }
        ]
    },
    "restore_state": {
        "category": "backup",
        "examples": [
            {
                "description": "Restore Terraform state from backup",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-vpc",
                    "backup_id": "state-backup-20260307-120000"
                }
            }
        ]
    },
    "get_health_status": {
        "category": "monitoring",
        "examples": [
            {
                "description": "Check health of production stack",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-api"
                }
            }
        ]
    },
    "get_metrics": {
        "category": "monitoring",
        "examples": [
            {
                "description": "Get CPU metrics for a stack",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-api",
                    "metric_name": "CPUUtilization"
                }
            }
        ]
    },
    "estimate_cost": {
        "category": "cost",
        "examples": [
            {
                "description": "Estimate cost before deployment",
                "parameters": {
                    "tool": "terraform",
                    "template_path": "./terraform/new-service"
                }
            }
        ]
    },
    "get_cost_forecast": {
        "category": "cost",
        "examples": [
            {
                "description": "Forecast costs for next 30 days",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-cluster",
                    "days": 30
                }
            }
        ]
    },
    "rotate_secrets": {
        "category": "security",
        "examples": [
            {
                "description": "Rotate secrets for a stack",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-api"
                }
            }
        ]
    },
    "check_compliance": {
        "category": "security",
        "examples": [
            {
                "description": "Check BaFin compliance",
                "parameters": {
                    "tool": "terraform",
                    "stack_name": "production-database",
                    "rules": ["encryption-at-rest", "backup-retention", "audit-logging"]
                }
            }
        ]
    }
}


def enrich_tool_metadata(tool_name: str, base_metadata: dict) -> dict:
    """Enrich tool metadata with real-world examples and categories."""
    enrichment = TOOL_EXAMPLES.get(tool_name, {})
    
    if enrichment:
        base_metadata["category"] = enrichment.get("category", "general")
        base_metadata["examples"] = enrichment.get("examples", [])
    
    return base_metadata
