# Tool Documentation Standard

## Purpose

AI agents need comprehensive, consistent tool documentation to make informed decisions about which tools to use. This document defines the standard format for all MCP tool documentation.

## Standard Format

Every tool MUST have a docstring following this format:

```python
@server.tool()
async def tool_name(param1: str, param2: int, param3: dict = None) -> dict:
    """Brief one-line description of what the tool does.

    Args:
        param1: Description of param1, including valid values if applicable
        param2: Description of param2, including units or ranges
        param3: Optional description of param3 (optional)
    
    Returns:
        Description of return value structure
    
    Examples:
        - Use case 1: Brief description
        - Use case 2: Brief description
    """
    return await service.method(param1, param2, param3)
```

## Required Elements

### 1. Brief Description (Required)
- Single line describing the tool's purpose
- Should be action-oriented (starts with a verb)
- Must be clear and specific

**Good examples:**
- "Deploy infrastructure using CDK, CloudFormation, Terraform, or IaC."
- "Get detailed stack information including status, resources, and outputs."
- "Rotate secrets and credentials for a stack."

**Bad examples:**
- "Stack info." (too vague)
- "This tool gets information." (not specific)
- "Use this to deploy things." (unclear)

### 2. Args Section (Required if tool has parameters)
- List each parameter with its description
- Include valid values, formats, or constraints
- Mark optional parameters with "(optional)"
- Include default values if applicable

**Format:**
```
Args:
    param_name: Type and description, valid values (constraints)
    optional_param: Description (optional, default: value)
```

**Examples:**
```
Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack to query
    start_time: Start timestamp in ISO 8601 format
    threshold: Alert threshold value (must be positive number)
    parameters: Deployment parameters (optional)
```

### 3. Returns Section (Recommended)
- Describe the structure of the return value
- Include key fields that will be present
- Mention any important data transformations

**Examples:**
```
Returns:
    Dictionary containing:
        - status: Stack status (CREATE_COMPLETE, UPDATE_IN_PROGRESS, etc.)
        - resources: List of stack resources
        - outputs: Stack output values
```

### 4. Examples Section (Recommended)
- Provide 1-3 real-world use cases
- Keep examples brief (one line each)
- Focus on when/why to use the tool

**Examples:**
```
Examples:
    - Deploy production VPC with custom CIDR range
    - Update API stack with new Lambda function version
    - Check compliance before production deployment
```

## Tool Categories

Tools should be categorized for easier discovery:

- **deployment**: Infrastructure deployment and updates
- **query**: Information retrieval and status checks
- **monitoring**: Health checks, metrics, logs, alarms
- **security**: Security scans, compliance, audits
- **backup**: Backup and restore operations
- **cost**: Cost analysis and optimization
- **network**: VPC, subnet, connectivity operations
- **database**: Database management operations
- **compute**: EC2, Lambda, ECS operations
- **storage**: S3 and storage operations
- **state**: State management and drift detection

## Common Parameter Descriptions

Use consistent descriptions for common parameters:

| Parameter | Standard Description |
|-----------|---------------------|
| `tool` | IaC tool (cdk\|cfn\|terraform\|iac) |
| `stack_name` | Name of the stack |
| `template_path` | Path to template file or directory |
| `parameters` | Deployment parameters (optional) |
| `resource_id` | Resource identifier (ARN, ID, or name) |
| `start_time` | Start timestamp (ISO 8601 format) |
| `end_time` | End timestamp (ISO 8601 format) |
| `metric_name` | CloudWatch metric name |
| `region` | AWS region code (e.g., eu-central-1) |
| `backup_id` | Backup identifier |
| `tags` | Dictionary of tag key-value pairs |

## Validation Checklist

Before committing tool documentation, verify:

- [ ] Brief description is clear and action-oriented
- [ ] All parameters are documented in Args section
- [ ] Optional parameters are marked as "(optional)"
- [ ] Valid values or constraints are specified where applicable
- [ ] Return value structure is described (if complex)
- [ ] At least one example use case is provided
- [ ] Tool is assigned to appropriate category
- [ ] Consistent terminology with other tools
- [ ] No typos or grammatical errors

## Anti-Patterns to Avoid

### ❌ Too Vague
```python
async def get_info(tool: str, name: str) -> dict:
    """Get info."""
```

### ❌ Missing Args
```python
async def deploy_stack(tool: str, stack_name: str, template: str) -> dict:
    """Deploy infrastructure stack."""
```

### ❌ Inconsistent Format
```python
async def list_items(tool: str) -> dict:
    """Lists all the items in the system
    
    tool - the tool to use
    """
```

### ✅ Correct Format
```python
async def deploy_infrastructure(
    tool: str, 
    stack_name: str, 
    template_path: str,
    parameters: dict = None
) -> dict:
    """Deploy infrastructure using CDK, CloudFormation, Terraform, or IaC.

    Args:
        tool: IaC tool (cdk|cfn|terraform|iac)
        stack_name: Name for the new stack
        template_path: Path to template file or directory
        parameters: Deployment parameters (optional)
    
    Returns:
        Dictionary containing deployment status and stack ARN
    
    Examples:
        - Deploy production VPC with Terraform
        - Create API Gateway stack with CDK
    """
    return await deploy_service.deploy(tool, stack_name, template_path, parameters)
```

## Automated Validation

Use the provided script to validate tool documentation:

```bash
./scripts/validate-tool-docs.sh
```

This checks:
- All tools have docstrings
- Docstrings follow the standard format
- All parameters are documented
- No missing Args sections

## For AI Agent Consumption

When tools are exposed via the gateway `/tools` endpoint, the documentation should be formatted as:

```
tool_name - Brief description

Args:
    param1: Description
    param2: Description (optional)

Examples:
    - Use case 1
    - Use case 2
```

This format is optimized for AI agents to:
1. Quickly understand what the tool does
2. Know what parameters are required
3. See valid values and constraints
4. Understand when to use the tool

## Maintenance

- Review tool documentation quarterly
- Update examples when new use cases emerge
- Keep descriptions synchronized with implementation
- Add clarifications based on user feedback
- Update this standard as patterns evolve

## References

- [MCP Server Standard](../architecture/mcp-server-standard.md)
- [Tool Metadata](../../src/virons-infrastructure-mcp-server/virons/infrastructure_mcp_server/tool_metadata.py)
- [Gateway API](../../src/virons-mcp-gateway/README.md)
