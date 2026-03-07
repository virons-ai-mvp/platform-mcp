# API Reference

**Version**: 1.0
**Last Updated**: 2026-03-07

## Overview

Complete API reference for the Virons Infrastructure MCP Server, including MCP protocol tools and REST API endpoints.

## Base URLs

- **MCP Protocol**: stdio transport
- **REST API**: `http://localhost:8080/api`
- **Swagger UI**: `http://localhost:8080/api/docs`
- **ReDoc**: `http://localhost:8080/api/redoc`

## MCP Protocol Tools

### deploy_infrastructure

Deploy infrastructure using specified IaC tool.

**Parameters**:
```json
{
  "stack_name": "string (required)",
  "tool": "cdk | terraform | cloudformation (required)",
  "region": "string (required)",
  "timeout": "integer (optional, default: 300)"
}
```

**Returns**:
```json
{
  "status": "success | failed",
  "stack_name": "string",
  "outputs": {"key": "value"},
  "duration_ms": "integer"
}
```

**Example**:
```python
result = await session.call_tool(
    "deploy_infrastructure",
    arguments={
        "stack_name": "my-vpc",
        "tool": "cdk",
        "region": "eu-central-1"
    }
)
```

### destroy_infrastructure

Destroy deployed infrastructure stack.

**Parameters**:
```json
{
  "stack_name": "string (required)",
  "tool": "cdk | terraform | cloudformation (required)",
  "region": "string (required)"
}
```

**Returns**:
```json
{
  "status": "success | failed",
  "stack_name": "string",
  "message": "string",
  "duration_ms": "integer"
}
```

**Example**:
```python
result = await session.call_tool(
    "destroy_infrastructure",
    arguments={
        "stack_name": "my-vpc",
        "tool": "cdk",
        "region": "eu-central-1"
    }
)
```

### list_stacks

List all deployed stacks for a tool and region.

**Parameters**:
```json
{
  "tool": "cdk | terraform | cloudformation (required)",
  "region": "string (required)"
}
```

**Returns**:
```json
{
  "stacks": [
    {
      "name": "string",
      "status": "string",
      "created_at": "ISO8601 timestamp"
    }
  ]
}
```

**Example**:
```python
result = await session.call_tool(
    "list_stacks",
    arguments={
        "tool": "cdk",
        "region": "eu-central-1"
    }
)
```

### get_stack_outputs

Get outputs from a deployed stack.

**Parameters**:
```json
{
  "stack_name": "string (required)",
  "tool": "cdk | terraform | cloudformation (required)",
  "region": "string (required)"
}
```

**Returns**:
```json
{
  "stack_name": "string",
  "outputs": {"key": "value"}
}
```

**Example**:
```python
result = await session.call_tool(
    "get_stack_outputs",
    arguments={
        "stack_name": "my-vpc",
        "tool": "cdk",
        "region": "eu-central-1"
    }
)
```

### get_infrastructure_info

Get information about the infrastructure server.

**Parameters**: None

**Returns**:
```json
{
  "version": "string",
  "available_tools": ["string"],
  "upstream_servers": {
    "cdk": {"host": "string", "port": "integer"},
    "terraform": {"host": "string", "port": "integer"},
    "cloudformation": {"host": "string", "port": "integer"}
  }
}
```

**Example**:
```python
result = await session.call_tool("get_infrastructure_info", arguments={})
```

## REST API Endpoints

### Health Check

**GET** `/health`

Check server health status.

**Response**:
```json
{
  "status": "healthy | unhealthy",
  "version": "1.0.0",
  "uptime_seconds": 3600
}
```

**Example**:
```bash
curl http://localhost:8080/health
```

### Metrics

**GET** `/metrics`

Get Prometheus metrics.

**Response**: Prometheus text format

**Metrics**:
- `mcp_tool_duration_seconds` - Tool execution duration
- `mcp_tool_calls_total` - Total tool calls
- `mcp_tool_errors_total` - Total errors
- `mcp_audit_log_writes_total` - Audit log writes

**Example**:
```bash
curl http://localhost:8080/metrics
```

### Deploy Infrastructure

**POST** `/api/deploy`

Deploy infrastructure stack.

**Request Body**:
```json
{
  "stack_name": "string",
  "tool": "cdk | terraform | cloudformation",
  "region": "string",
  "timeout": 300
}
```

**Response**:
```json
{
  "status": "success | failed",
  "stack_name": "string",
  "outputs": {"key": "value"},
  "duration_ms": 45000
}
```

**Status Codes**:
- `200` - Success
- `400` - Invalid request
- `500` - Server error

**Example**:
```bash
curl -X POST http://localhost:8080/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "stack_name": "my-vpc",
    "tool": "cdk",
    "region": "eu-central-1"
  }'
```

### Destroy Infrastructure

**POST** `/api/destroy`

Destroy infrastructure stack.

**Request Body**:
```json
{
  "stack_name": "string",
  "tool": "cdk | terraform | cloudformation",
  "region": "string"
}
```

**Response**:
```json
{
  "status": "success | failed",
  "stack_name": "string",
  "message": "Stack destroyed successfully",
  "duration_ms": 60000
}
```

**Example**:
```bash
curl -X POST http://localhost:8080/api/destroy \
  -H "Content-Type: application/json" \
  -d '{
    "stack_name": "my-vpc",
    "tool": "cdk",
    "region": "eu-central-1"
  }'
```

### List Stacks

**GET** `/api/stacks`

List deployed stacks.

**Query Parameters**:
- `tool` (required): cdk | terraform | cloudformation
- `region` (required): AWS region

**Response**:
```json
{
  "stacks": [
    {
      "name": "my-vpc",
      "status": "CREATE_COMPLETE",
      "created_at": "2026-03-07T10:00:00Z"
    }
  ]
}
```

**Example**:
```bash
curl "http://localhost:8080/api/stacks?tool=cdk&region=eu-central-1"
```

### Get Stack Outputs

**GET** `/api/stacks/{stack_name}/outputs`

Get stack outputs.

**Path Parameters**:
- `stack_name` (required): Stack name

**Query Parameters**:
- `tool` (required): cdk | terraform | cloudformation
- `region` (required): AWS region

**Response**:
```json
{
  "stack_name": "my-vpc",
  "outputs": {
    "VpcId": "vpc-0123456789abcdef0",
    "SubnetIds": "subnet-abc,subnet-def"
  }
}
```

**Example**:
```bash
curl "http://localhost:8080/api/stacks/my-vpc/outputs?tool=cdk&region=eu-central-1"
```

### Get Server Info

**GET** `/api/info`

Get server information.

**Response**:
```json
{
  "version": "1.0.0",
  "available_tools": [
    "deploy_infrastructure",
    "destroy_infrastructure",
    "list_stacks",
    "get_stack_outputs",
    "get_infrastructure_info"
  ],
  "upstream_servers": {
    "cdk": {"host": "cdk-server", "port": 9140},
    "terraform": {"host": "terraform-server", "port": 9142},
    "cloudformation": {"host": "cfn-server", "port": 9141}
  }
}
```

**Example**:
```bash
curl http://localhost:8080/api/info
```

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Invalid request parameters |
| `STACK_NOT_FOUND` | 404 | Stack does not exist |
| `DEPLOYMENT_FAILED` | 500 | Deployment failed |
| `TIMEOUT` | 504 | Operation timed out |
| `UPSTREAM_ERROR` | 502 | Upstream server error |
| `INTERNAL_ERROR` | 500 | Internal server error |

### Example Error Response

```json
{
  "error": {
    "code": "DEPLOYMENT_FAILED",
    "message": "Failed to deploy stack: Resource limit exceeded",
    "details": {
      "stack_name": "my-vpc",
      "tool": "cdk",
      "region": "eu-central-1"
    }
  }
}
```

## Rate Limiting

- **Limit**: 100 requests per minute per client
- **Header**: `X-RateLimit-Remaining`
- **Response**: 429 Too Many Requests

## Authentication

### API Key (Optional)

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8080/api/deploy
```

### IAM Authentication (Kubernetes)

Uses Kubernetes service account with IAM role.

## Pagination

For endpoints returning lists:

**Query Parameters**:
- `limit` (default: 100, max: 1000)
- `offset` (default: 0)

**Response**:
```json
{
  "items": [],
  "total": 250,
  "limit": 100,
  "offset": 0
}
```

## Webhooks

### Deployment Events

**POST** to configured webhook URL

**Payload**:
```json
{
  "event": "deployment.completed",
  "timestamp": "2026-03-07T10:00:00Z",
  "data": {
    "stack_name": "my-vpc",
    "status": "success",
    "duration_ms": 45000
  }
}
```

## SDK Examples

### Python
```python
from virons_infrastructure_mcp_server import InfrastructureClient

client = InfrastructureClient(base_url="http://localhost:8080")

# Deploy
result = client.deploy(
    stack_name="my-vpc",
    tool="cdk",
    region="eu-central-1"
)

# List stacks
stacks = client.list_stacks(tool="cdk", region="eu-central-1")

# Destroy
client.destroy(stack_name="my-vpc", tool="cdk", region="eu-central-1")
```

### TypeScript
```typescript
import { InfrastructureClient } from '@virons/infrastructure-mcp-client';

const client = new InfrastructureClient({
  baseUrl: 'http://localhost:8080'
});

// Deploy
const result = await client.deploy({
  stackName: 'my-vpc',
  tool: 'cdk',
  region: 'eu-central-1'
});

// List stacks
const stacks = await client.listStacks({
  tool: 'cdk',
  region: 'eu-central-1'
});
```

### cURL
```bash
# Deploy
curl -X POST http://localhost:8080/api/deploy \
  -H "Content-Type: application/json" \
  -d '{"stack_name": "my-vpc", "tool": "cdk", "region": "eu-central-1"}'

# List
curl "http://localhost:8080/api/stacks?tool=cdk&region=eu-central-1"

# Destroy
curl -X POST http://localhost:8080/api/destroy \
  -H "Content-Type: application/json" \
  -d '{"stack_name": "my-vpc", "tool": "cdk", "region": "eu-central-1"}'
```

## OpenAPI Specification

Full OpenAPI 3.0 specification available at:
- **JSON**: `http://localhost:8080/api/openapi.json`
- **Swagger UI**: `http://localhost:8080/api/docs`
- **ReDoc**: `http://localhost:8080/api/redoc`

## Versioning

API version is included in responses:
```json
{
  "version": "1.0.0",
  "api_version": "v1"
}
```

Breaking changes will increment major version.

## Support

- **Swagger UI**: http://localhost:8080/api/docs
- **Documentation**: https://docs.virons.ai
- **Issues**: https://github.com/virons-ai/virons-infrastructure-mcp-server/issues

---

**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
