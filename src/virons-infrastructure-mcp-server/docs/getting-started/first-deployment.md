# First Deployment Tutorial

**Version**: 1.0
**Last Updated**: 2026-03-07
**Duration**: 15 minutes

## Overview

This tutorial walks you through deploying your first infrastructure stack using the Virons Infrastructure MCP Server.

## Prerequisites

- Virons Infrastructure MCP Server installed ([Installation Guide](./installation.md))
- AWS credentials configured
- At least one upstream MCP server running (CDK, Terraform, or CloudFormation)

## Step 1: Start the Server

### Option A: MCP Protocol (stdio)
```bash
# Start server
python -m virons.infrastructure_mcp_server.server --transport stdio
```

### Option B: REST API
```bash
# Start API server
python -m virons.infrastructure_mcp_server.server --transport api --port 8080

# Verify server is running
curl http://localhost:8080/health
```

## Step 2: List Available Tools

### Using MCP Client
```python
# client.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def list_tools():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "virons.infrastructure_mcp_server.server", "--transport", "stdio"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()

            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

asyncio.run(list_tools())
```

### Using REST API
```bash
# List available tools
curl http://localhost:8080/api/info | jq '.available_tools'
```

**Expected Output**:
```json
{
  "available_tools": [
    "deploy_infrastructure",
    "destroy_infrastructure",
    "list_stacks",
    "get_stack_outputs",
    "get_infrastructure_info"
  ]
}
```

## Step 3: Deploy a Simple VPC Stack

### Using CDK

**Create Stack Definition** (`vpc-stack.ts`):
```typescript
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class VpcStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new ec2.Vpc(this, 'MyVpc', {
      maxAzs: 2,
      natGateways: 1,
    });
  }
}
```

**Deploy via MCP**:
```python
# deploy_vpc.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def deploy_vpc():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "virons.infrastructure_mcp_server.server", "--transport", "stdio"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "deploy_infrastructure",
                arguments={
                    "stack_name": "my-first-vpc",
                    "tool": "cdk",
                    "region": "eu-central-1",
                }
            )

            print(result.content[0].text)

asyncio.run(deploy_vpc())
```

**Deploy via REST API**:
```bash
curl -X POST http://localhost:8080/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "stack_name": "my-first-vpc",
    "tool": "cdk",
    "region": "eu-central-1"
  }'
```

**Expected Output**:
```json
{
  "status": "success",
  "stack_name": "my-first-vpc",
  "outputs": {
    "VpcId": "vpc-0123456789abcdef0",
    "PublicSubnetIds": "subnet-abc,subnet-def",
    "PrivateSubnetIds": "subnet-ghi,subnet-jkl"
  },
  "duration_ms": 45000
}
```

## Step 4: Verify Deployment

### List Deployed Stacks
```bash
# Using REST API
curl http://localhost:8080/api/stacks?tool=cdk&region=eu-central-1 | jq
```

**Expected Output**:
```json
{
  "stacks": [
    {
      "name": "my-first-vpc",
      "status": "CREATE_COMPLETE",
      "created_at": "2026-03-07T10:00:00Z"
    }
  ]
}
```

### Get Stack Outputs
```python
# get_outputs.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def get_outputs():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "virons.infrastructure_mcp_server.server", "--transport", "stdio"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "get_stack_outputs",
                arguments={
                    "stack_name": "my-first-vpc",
                    "tool": "cdk",
                    "region": "eu-central-1",
                }
            )

            print(result.content[0].text)

asyncio.run(get_outputs())
```

### Verify in AWS Console
```bash
# Using AWS CLI
aws cloudformation describe-stacks \
  --stack-name my-first-vpc \
  --region eu-central-1 \
  --query 'Stacks[0].Outputs'
```

## Step 5: Check Audit Logs

### View Compliance Logs
```bash
# Check local logs
tail -f logs/compliance.log

# Check S3 audit logs
aws s3 ls s3://virons-audit-logs/$(date +%Y/%m/%d)/ --recursive
```

**Expected Log Entry**:
```json
{
  "timestamp": "2026-03-07T10:00:00Z",
  "action": "deploy_infrastructure",
  "user_id": "user@example.com",
  "stack_name": "my-first-vpc",
  "tool": "cdk",
  "region": "eu-central-1",
  "status": "success",
  "duration_ms": 45000,
  "regulation": "BaFin_MaRisk_AT_8.1"
}
```

## Step 6: Monitor Metrics

### View Prometheus Metrics
```bash
# Get metrics
curl http://localhost:8080/metrics

# Filter deployment metrics
curl http://localhost:8080/metrics | grep mcp_tool_duration
```

**Expected Metrics**:
```
mcp_tool_duration_seconds{tool="deploy_infrastructure",status="success"} 45.0
mcp_tool_calls_total{tool="deploy_infrastructure"} 1
mcp_audit_log_writes_total 1
```

### View Grafana Dashboard
```bash
# Open Grafana (if deployed)
open http://grafana.virons.ai/d/infrastructure-mcp
```

## Step 7: Update the Stack

### Modify Stack
```typescript
// vpc-stack.ts - Add a tag
new ec2.Vpc(this, 'MyVpc', {
  maxAzs: 2,
  natGateways: 1,
  tags: {
    Environment: 'tutorial',
  },
});
```

### Redeploy
```bash
curl -X POST http://localhost:8080/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "stack_name": "my-first-vpc",
    "tool": "cdk",
    "region": "eu-central-1"
  }'
```

**Expected Output**:
```json
{
  "status": "success",
  "stack_name": "my-first-vpc",
  "change_set": "UPDATE",
  "duration_ms": 30000
}
```

## Step 8: Clean Up

### Destroy Stack
```python
# destroy_vpc.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def destroy_vpc():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "virons.infrastructure_mcp_server.server", "--transport", "stdio"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "destroy_infrastructure",
                arguments={
                    "stack_name": "my-first-vpc",
                    "tool": "cdk",
                    "region": "eu-central-1",
                }
            )

            print(result.content[0].text)

asyncio.run(destroy_vpc())
```

**Using REST API**:
```bash
curl -X POST http://localhost:8080/api/destroy \
  -H "Content-Type: application/json" \
  -d '{
    "stack_name": "my-first-vpc",
    "tool": "cdk",
    "region": "eu-central-1"
  }'
```

**Expected Output**:
```json
{
  "status": "success",
  "stack_name": "my-first-vpc",
  "message": "Stack destroyed successfully",
  "duration_ms": 60000
}
```

### Verify Deletion
```bash
# Check stack is gone
curl http://localhost:8080/api/stacks?tool=cdk&region=eu-central-1 | jq

# Should return empty list
{"stacks": []}
```

## Common Issues

### Issue: Server Not Starting
```bash
# Check port availability
lsof -i :8080

# Use different port
python -m virons.infrastructure_mcp_server.server --transport api --port 8081
```

### Issue: AWS Credentials Not Found
```bash
# Configure AWS CLI
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_REGION=eu-central-1
```

### Issue: Upstream Server Not Reachable
```bash
# Check CDK server is running
curl http://cdk-server:9140/health

# Start CDK server if needed
cdk-mcp-server --port 9140
```

### Issue: Deployment Timeout
```bash
# Increase timeout
curl -X POST http://localhost:8080/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "stack_name": "my-first-vpc",
    "tool": "cdk",
    "region": "eu-central-1",
    "timeout": 600
  }'
```

## Next Steps

### Deploy More Complex Stacks
- EKS cluster
- RDS database
- S3 buckets with policies
- Lambda functions

### Explore Other Tools
- Try Terraform deployments
- Try CloudFormation templates
- Compare tool performance

### Set Up Monitoring
- Configure Grafana dashboards
- Set up PagerDuty alerts
- Enable CloudWatch integration

### Production Deployment
- Deploy to Kubernetes
- Configure high availability
- Set up backup and DR
- Enable compliance logging

## Additional Resources

- [Architecture Documentation](../architecture/)
- [API Reference](../reference/api-reference.md)
- [Troubleshooting Guide](./troubleshooting.md)
- [Operations Runbooks](../operations/runbooks/)

## Example Projects

### Simple VPC
```bash
git clone https://github.com/virons-ai/examples
cd examples/simple-vpc
python deploy.py
```

### EKS Cluster
```bash
cd examples/eks-cluster
python deploy.py
```

### Multi-Region Setup
```bash
cd examples/multi-region
python deploy.py
```

## Support

- **Documentation**: https://docs.virons.ai
- **Examples**: https://github.com/virons-ai/examples
- **Issues**: https://github.com/virons-ai/virons-infrastructure-mcp-server/issues
- **Slack**: #support on Virons Slack

---

**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
