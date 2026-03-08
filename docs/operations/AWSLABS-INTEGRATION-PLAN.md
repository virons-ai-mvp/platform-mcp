# AWS Labs MCP Servers Integration Plan

## Executive Summary

**Objective**: Integrate 10 missing AWS Labs MCP servers to enable full functionality of 90 tools across the Virons MCP platform.

**Current State**: 70+ AWS Labs servers available in `src/awslabs/`, 10 required for platform functionality.

**Timeline**: 2-3 days for Phase 1 (critical servers), 1 week for full integration.

## Required Servers (Priority Order)

### Phase 1: Infrastructure Tools (Critical)

| Server | Port | Purpose | Tools Enabled | Status |
|--------|------|---------|---------------|--------|
| **aws-iac-mcp-server** | 9143 | Unified IaC (replaces cdk/cfn/terraform) | All infrastructure deployment | ⚠️ Missing |
| **cloudtrail-mcp-server** | 9102 | Audit trail analysis | audit_cloudtrail | ⚠️ Missing |
| **iam-mcp-server** | 9103 | IAM policy management | check_iam_policy | ⚠️ Missing |

**Rationale**: AWS Labs deprecated individual cdk/cfn/terraform servers in favor of unified `aws-iac-mcp-server`. This single server provides all IaC functionality.

### Phase 2: Security & Monitoring (High Priority)

| Server | Port | Purpose | Tools Enabled | Status |
|--------|------|---------|---------------|--------|
| **well-architected-security-mcp-server** | 9104 | Security best practices | run_compliance_gate | ⚠️ Missing |
| **cloudwatch-mcp-server** | 9301 | CloudWatch integration | create_alert | ⚠️ Missing |

### Phase 3: Optional Enhancements

| Server | Port | Purpose | Benefit | Status |
|--------|------|---------|---------|--------|
| **eks-mcp-server** | 9200 | EKS cluster management | Enhanced k8s operations | ✅ Available |
| **lambda-tool-mcp-server** | 9400 | Lambda management | Serverless operations | ✅ Available |
| **dynamodb-mcp-server** | 9500 | DynamoDB operations | Database management | ✅ Available |

## Architecture Changes

### Current Upstream Configuration

**infrastructure-mcp** expects 4 separate servers:
```python
UPSTREAM_CONFIG = {
    "cdk": {"host": "localhost", "port": 9140},
    "cfn": {"host": "localhost", "port": 9141},
    "terraform": {"host": "localhost", "port": 9142},
    "iac": {"host": "localhost", "port": 9143},
}
```

### Proposed Configuration

**Consolidate to single IaC server**:
```python
UPSTREAM_CONFIG = {
    "iac": {"host": "localhost", "port": 9143},  # Unified IaC server
}
```

**Benefits**:
- Single server to deploy and maintain
- Consistent API across IaC tools
- Reduced resource footprint
- Simplified configuration

## Implementation Steps

### Step 1: Deploy AWS IaC MCP Server

```bash
# Navigate to server directory
cd src/awslabs/aws-iac-mcp-server

# Build Docker image
docker build -t virons-aws-iac-mcp:latest .

# Add to docker-compose.yml
```

**Docker Compose Entry**:
```yaml
virons-aws-iac-mcp:
  image: virons-aws-iac-mcp:latest
  container_name: virons-aws-iac-mcp
  ports:
    - "9143:9143"
  environment:
    - AWS_PROFILE=virons-management
    - AWS_REGION=eu-central-1
  networks:
    - virons-mcp
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:9143/health"]
    interval: 30s
    timeout: 10s
    retries: 3
```

### Step 2: Deploy Security Servers

**CloudTrail MCP**:
```yaml
virons-cloudtrail-mcp:
  build: ./src/awslabs/cloudtrail-mcp-server
  container_name: virons-cloudtrail-mcp
  ports:
    - "9102:9102"
  environment:
    - AWS_PROFILE=virons-management
    - AWS_REGION=eu-central-1
  networks:
    - virons-mcp
```

**IAM MCP**:
```yaml
virons-iam-mcp:
  build: ./src/awslabs/iam-mcp-server
  container_name: virons-iam-mcp
  ports:
    - "9103:9103"
  environment:
    - AWS_PROFILE=virons-management
    - AWS_REGION=eu-central-1
  networks:
    - virons-mcp
```

**Well-Architected Security MCP**:
```yaml
virons-well-architected-mcp:
  build: ./src/awslabs/well-architected-security-mcp-server
  container_name: virons-well-architected-mcp
  ports:
    - "9104:9104"
  environment:
    - AWS_PROFILE=virons-management
    - AWS_REGION=eu-central-1
  networks:
    - virons-mcp
```

### Step 3: Update Infrastructure MCP Configuration

**File**: `src/virons-infrastructure-mcp-server/virons/infrastructure_mcp_server/server.py`

```python
# OLD (lines 59-66)
UPSTREAM_CONFIG = {
    "cdk": {"host": "localhost", "port": 9140, "transport": "stdio"},
    "cfn": {"host": "localhost", "port": 9141, "transport": "stdio"},
    "terraform": {"host": "localhost", "port": 9142, "transport": "stdio"},
    "iac": {"host": "localhost", "port": 9143, "transport": "stdio"},
}

# NEW
UPSTREAM_CONFIG = {
    "iac": {"host": "localhost", "port": 9143, "transport": "http"},
}
```

### Step 4: Update Security MCP Configuration

**File**: `src/virons-security-mcp-server/virons/security_mcp_server/server.py`

```python
# Update lines 45-50
UPSTREAM = {
    "cloudtrail": {"host": "localhost", "port": 9102},
    "iam": {"host": "localhost", "port": 9103},
    "well-architected": {"host": "localhost", "port": 9104},
    "gitleaks": {"host": "localhost", "port": 9100},  # Already running
}
```

### Step 5: Deploy Monitoring Servers

**CloudWatch MCP**:
```yaml
virons-cloudwatch-mcp:
  build: ./src/awslabs/cloudwatch-mcp-server
  container_name: virons-cloudwatch-mcp
  ports:
    - "9301:9301"
  environment:
    - AWS_PROFILE=virons-management
    - AWS_REGION=eu-central-1
  networks:
    - virons-mcp
```

### Step 6: Update Monitoring MCP Configuration

**File**: `src/virons-monitoring-mcp-server/virons/monitoring_mcp_server/server.py`

```python
UPSTREAM = {
    "prometheus": {"host": "localhost", "port": 9300},  # Already running
    "cloudwatch": {"host": "localhost", "port": 9301},
}
```

## Testing Strategy

### Phase 1: Individual Server Testing

```bash
# Test IaC server
curl http://localhost:9143/tools | jq

# Test CloudTrail server
curl http://localhost:9102/tools | jq

# Test IAM server
curl http://localhost:9103/tools | jq
```

### Phase 2: Integration Testing

```bash
# Test infrastructure-mcp with IaC upstream
curl -X POST http://localhost:9100/tools/deploy_infrastructure \
  -H "Content-Type: application/json" \
  -d '{"template": "test.yaml"}'

# Test security-mcp with CloudTrail upstream
curl -X POST http://localhost:9500/tools/audit_cloudtrail \
  -H "Content-Type: application/json" \
  -d '{"trail_name": "test-trail"}'
```

### Phase 3: End-to-End Testing

```bash
# Run comprehensive platform status check
python3 scripts/platform-status.py

# Verify all 90 tools are functional
python3 scripts/test-tool-execution.py
```

## Resource Requirements

### Compute

| Server | CPU | Memory | Disk |
|--------|-----|--------|------|
| aws-iac-mcp | 500m | 512Mi | 1Gi |
| cloudtrail-mcp | 200m | 256Mi | 512Mi |
| iam-mcp | 200m | 256Mi | 512Mi |
| well-architected-mcp | 200m | 256Mi | 512Mi |
| cloudwatch-mcp | 200m | 256Mi | 512Mi |

**Total Additional**: 1.3 CPU, 1.5Gi memory, 3Gi disk

### Network

- All servers communicate via `virons-mcp` Docker network
- No external network access required
- Internal DNS resolution via Docker

## Security Considerations

### AWS Credentials

**Current**: Shared AWS profile mounted via Docker volume
**Recommendation**: Use IAM roles for service accounts (IRSA) in production

```yaml
# Development (current)
environment:
  - AWS_PROFILE=virons-management

# Production (recommended)
serviceAccount:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::412179655775:role/virons-mcp-role
```

### Network Policies

```yaml
# Restrict upstream access
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mcp-upstream-policy
spec:
  podSelector:
    matchLabels:
      app: virons-infrastructure-mcp
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: virons-aws-iac-mcp
      ports:
        - protocol: TCP
          port: 9143
```

### Secrets Management

**Current**: AWS credentials in environment variables
**Recommendation**: Use AWS Secrets Manager

```python
import boto3

def get_aws_credentials():
    client = boto3.client('secretsmanager', region_name='eu-central-1')
    secret = client.get_secret_value(SecretId='virons/mcp/aws-credentials')
    return json.loads(secret['SecretString'])
```

## Rollback Plan

### If Integration Fails

1. **Revert docker-compose.yml**:
   ```bash
   git checkout HEAD -- docker-compose.yml
   docker-compose up -d
   ```

2. **Revert server configurations**:
   ```bash
   git checkout HEAD -- src/virons-*-mcp-server/virons/*/server.py
   docker-compose restart
   ```

3. **Verify platform status**:
   ```bash
   python3 scripts/platform-status.py
   ```

### Graceful Degradation

If upstream servers fail:
- Tools return clear error messages
- Platform remains operational
- No cascading failures

## Success Criteria

### Phase 1 Complete

- ✅ AWS IaC MCP server deployed and responding
- ✅ CloudTrail MCP server deployed and responding
- ✅ IAM MCP server deployed and responding
- ✅ Infrastructure-mcp successfully calls IaC upstream
- ✅ Security-mcp successfully calls CloudTrail/IAM upstreams

### Phase 2 Complete

- ✅ Well-Architected MCP server deployed
- ✅ CloudWatch MCP server deployed
- ✅ All security tools functional
- ✅ All monitoring tools functional

### Final Validation

- ✅ All 90 tools callable via HTTP
- ✅ All 90 tools return valid responses (not errors)
- ✅ Platform status check shows 100% operational
- ✅ No performance degradation
- ✅ All health checks passing

## Timeline

### Day 1: Infrastructure Servers
- Morning: Deploy aws-iac-mcp-server
- Afternoon: Update infrastructure-mcp configuration
- Evening: Test and validate

### Day 2: Security Servers
- Morning: Deploy cloudtrail-mcp, iam-mcp, well-architected-mcp
- Afternoon: Update security-mcp configuration
- Evening: Test and validate

### Day 3: Monitoring & Final Testing
- Morning: Deploy cloudwatch-mcp
- Afternoon: Update monitoring-mcp configuration
- Evening: Comprehensive testing and validation

## Documentation Updates

### Files to Update

1. **README.md** - Update status badges and tool counts
2. **docs/operations/UPSTREAM-SERVICES.md** - Mark servers as deployed
3. **docs/domain/tools/TOOL_CATALOG.md** - Update tool availability
4. **scripts/check-upstream-services.py** - Add new servers to check list

### New Documentation

1. **docs/operations/AWSLABS-DEPLOYMENT.md** - Deployment procedures
2. **docs/operations/AWSLABS-TROUBLESHOOTING.md** - Common issues and fixes
3. **docs/architecture/UPSTREAM-ARCHITECTURE.md** - Upstream integration patterns

## Monitoring & Alerting

### Metrics to Track

- Upstream server response times
- Tool execution success rates
- Error rates by upstream server
- Resource utilization (CPU, memory)

### Alerts to Configure

- Upstream server down (critical)
- High error rate (warning)
- Slow response times (warning)
- Resource exhaustion (critical)

## Next Steps

1. **Review and approve plan** - Stakeholder sign-off
2. **Prepare AWS credentials** - Ensure virons-management profile configured
3. **Schedule deployment window** - Coordinate with team
4. **Execute Phase 1** - Deploy infrastructure servers
5. **Validate Phase 1** - Run tests and verify functionality
6. **Execute Phase 2** - Deploy security servers
7. **Validate Phase 2** - Run tests and verify functionality
8. **Execute Phase 3** - Deploy monitoring servers
9. **Final validation** - Comprehensive platform testing
10. **Documentation** - Update all relevant docs

## Questions & Decisions

### Open Questions

1. **AWS Credentials**: Use shared profile or IRSA?
2. **Resource Limits**: Are proposed limits sufficient?
3. **Deployment Window**: When to deploy (off-hours)?
4. **Rollback Trigger**: What error rate triggers rollback?

### Decisions Needed

- [ ] Approve resource allocation
- [ ] Approve deployment timeline
- [ ] Approve security configuration
- [ ] Approve monitoring strategy
