# AWS Labs MCP Servers - Quick Reference

## Your 4 Virons MCP Servers

| Virons MCP | Port | AWS Labs Upstreams Needed |
|------------|------|---------------------------|
| **Monitoring** | :9520 | CloudWatch :9109, Prometheus :9110 |
| **Security** | :9500 | IAM :9103, CloudTrail :9102, Well-Architected :9104 |
| **Operations** | :9510 | EKS :9121, Lambda :9122, ECS :9123, StepFunctions :9124 |
| **Infrastructure** | :9530 | CDK :9140, CFN :9141, Terraform :9142, IAC :9143 |

## AWS Labs Servers Status

✅ **All 14 servers found and ready to deploy**

### Priority 1: Essential (6 servers)
- `cloudwatch-mcp-server` → :9109 (11 tools)
- `iam-mcp-server` → :9103 (29 tools)
- `cloudtrail-mcp-server` → :9102 (5 tools)
- `eks-mcp-server` → :9121 (10 tools)
- `lambda-tool-mcp-server` → :9122 (9 tools)
- `ecs-mcp-server` → :9123 (14 tools)

### Priority 2: Infrastructure (4 servers)
- `cdk-mcp-server` → :9140
- `cfn-mcp-server` → :9141
- `terraform-mcp-server` → :9142
- `aws-iac-mcp-server` → :9143

### Priority 3: Additional (4 servers)
- `stepfunctions-tool-mcp-server` → :9124 (8 tools)
- `prometheus-mcp-server` → :9110 (4 tools)
- `well-architected-security-mcp-server` → :9104
- `core-mcp-server` → :9125/9126 (EC2, S3)

## Quick Deploy Commands

### Deploy Priority 1 (Essential)
```bash
cd /Users/amjadalissaalkhalaf/repos/virons-fintech/virons-ai-mvp/platform-mcp
./scripts/deploy-awslabs-priority1.sh
```

### Deploy Priority 2 (Infrastructure)
```bash
./scripts/deploy-awslabs-priority2.sh
```

### Check Status
```bash
# Check running processes
ps aux | grep uvx

# Test health endpoints
curl http://localhost:9109/health  # CloudWatch
curl http://localhost:9103/health  # IAM
curl http://localhost:9121/health  # EKS

# Check tool counts
curl http://localhost:9109/tools | jq '.tools | length'
```

### View Logs
```bash
# All logs
tail -f /tmp/*.log

# Specific server
tail -f /tmp/cloudwatch-mcp-server.log
```

### Stop All Servers
```bash
# Kill all uvx processes
pkill -f "uvx awslabs"

# Or kill specific server
pkill -f "cloudwatch-mcp-server"
```

## Testing Integration

### 1. Start AWS Labs Servers
```bash
./scripts/deploy-awslabs-priority1.sh
sleep 30  # Wait for startup
```

### 2. Test AWS Labs Servers
```bash
curl http://localhost:9109/tools | jq '.tools[] | .name'
curl http://localhost:9103/tools | jq '.tools[] | .name'
```

### 3. Start Your Virons MCPs
```bash
docker-compose up -d virons-monitoring-mcp
docker-compose up -d virons-security-mcp
docker-compose up -d virons-operations-mcp
```

### 4. Test Tool Discovery
```bash
# Monitoring MCP should discover CloudWatch tools
curl http://localhost:9520/tools | jq '.tools | length'

# Security MCP should discover IAM + CloudTrail tools
curl http://localhost:9500/tools | jq '.tools | length'

# Operations MCP should discover EKS + Lambda + ECS tools
curl http://localhost:9510/tools | jq '.tools | length'
```

### 5. Test a Real AWS Operation
```bash
# List IAM users via Security MCP
curl -X POST http://localhost:9500/tools/list_users \
  -H "Content-Type: application/json" \
  -d '{}' | jq

# Get CloudWatch metrics via Monitoring MCP
curl -X POST http://localhost:9520/tools/get_metric_data \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "AWS/EC2",
    "metric_name": "CPUUtilization",
    "start_time": "2026-03-07T00:00:00Z",
    "end_time": "2026-03-07T01:00:00Z"
  }' | jq
```

## Troubleshooting

### Server won't start
```bash
# Check logs
tail -f /tmp/cloudwatch-mcp-server.log

# Check if port is in use
lsof -i :9109

# Check AWS credentials
aws sts get-caller-identity
```

### Tools not discovered
```bash
# Check upstream connectivity
curl http://localhost:9109/health

# Check Virons MCP logs
docker-compose logs virons-monitoring-mcp

# Restart Virons MCP
docker-compose restart virons-monitoring-mcp
```

### AWS API errors
```bash
# Check IAM permissions
aws iam get-user

# Check CloudWatch permissions
aws cloudwatch list-metrics --namespace AWS/EC2 --max-items 1

# Check region
echo $AWS_REGION
```

## Architecture

```
┌─────────────────────────────────────┐
│  Your Virons MCPs                   │
│  - Monitoring :9520                 │
│  - Security :9500                   │
│  - Operations :9510                 │
│  - Infrastructure :9530             │
└─────────────────────────────────────┘
              │
              │ (proxy - auto-discovery)
              ▼
┌─────────────────────────────────────┐
│  AWS Labs MCP Servers               │
│  - cloudwatch :9109                 │
│  - iam :9103                        │
│  - eks :9121                        │
│  - lambda :9122                     │
│  - (and 10 more...)                 │
└─────────────────────────────────────┘
              │
              │ (AWS SDK)
              ▼
┌─────────────────────────────────────┐
│  AWS Services                       │
│  - CloudWatch, IAM, EKS, etc.       │
└─────────────────────────────────────┘
```

## Files Created

- `docs/AWSLABS_INTEGRATION.md` - Complete architecture guide
- `docs/AWSLABS_DEPLOYMENT_PLAN.md` - Detailed deployment plan
- `scripts/deploy-awslabs-priority1.sh` - Deploy essential servers
- `scripts/deploy-awslabs-priority2.sh` - Deploy infrastructure servers
- `docs/AWSLABS_QUICK_REFERENCE.md` - This file

## Next Steps

1. ✅ Review this quick reference
2. ⏳ Deploy Priority 1 servers: `./scripts/deploy-awslabs-priority1.sh`
3. ⏳ Test integration
4. ⏳ Deploy Priority 2 if needed
5. ⏳ Document your deployment
