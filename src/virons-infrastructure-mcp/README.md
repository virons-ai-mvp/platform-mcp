# Virons Infrastructure MCP Server

**Port**: 9100
**Purpose**: AWS/EKS infrastructure operations

## Tools

### `list_accounts`
List AWS accounts from Organizations.

**Input**:
- `filter` (string, optional): Filter pattern

**Output**: List of AWS accounts with ID, name, status

### `list_ec2`
List EC2 instances in an account/region.

**Input**:
- `account` (string, required): AWS account ID
- `region` (string, default: eu-central-1): AWS region
- `tags` (object, optional): Tag filters

**Output**: List of EC2 instances with ID, type, state

### `get_costs`
Get cost analysis for a time period.

**Input**:
- `period` (string, required): Time period (e.g., "30d")
- `filters` (object, optional): Cost filters

**Output**: Total cost and breakdown by service

### `validate_cloudformation`
Validate CloudFormation template syntax.

**Input**:
- `template` (string, required): CloudFormation template YAML/JSON

**Output**: Validation result with warnings

### `deploy_stack`
Deploy CloudFormation stack.

**Input**:
- `template` (string, required): CloudFormation template
- `params` (object, optional): Stack parameters

**Output**: Stack ID and deployment status

### `eks_list_clusters`
List EKS clusters in a region.

**Input**:
- `region` (string, default: eu-central-1): AWS region

**Output**: List of EKS clusters with name, status, version

## Usage

```bash
# Run locally
cd src/virons-infrastructure-mcp
python server.py

# Build Docker image
docker build -t virons-infrastructure-mcp .

# Run container
docker run -p 9100:9100 virons-infrastructure-mcp
```

## Integration

Register in MCP Gateway:
```yaml
# config/servers.yaml
servers:
  - name: infrastructure
    url: http://virons-infrastructure-mcp:9100
    tools: [list_accounts, list_ec2, get_costs, validate_cloudformation, deploy_stack, eks_list_clusters]
```
