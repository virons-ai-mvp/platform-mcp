# AWS Labs MCP Servers Integration Architecture

## Overview

You have **65+ AWS Labs MCP servers** in `platform-mcp/src/awslabs/`. These are **upstream servers** that provide direct AWS API access. Your current 3 orchestrator MCPs (Monitoring, Security, Operations) should integrate with relevant AWS Labs servers as upstreams.

## Current Architecture (Completed)

```
┌─────────────────────────────────────────────────────────────┐
│  Your 3 Orchestrator MCPs (Virons)                          │
│  - Monitoring MCP :9520 (12 core + 50+ proxy = 62+ tools)  │
│  - Security MCP :9500 (14 core + 50+ proxy = 64+ tools)    │
│  - Operations MCP :9510 (16 core + 50+ proxy = 66+ tools)  │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ (proxy pattern)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Placeholder Upstreams (Currently Mocked)                    │
│  - CloudWatch :9109, Prometheus :9110, etc.                 │
│  - CloudTrail :9102, IAM :9103, etc.                        │
│  - EKS :9121, Lambda :9122, EC2 :9125, S3 :9126, etc.      │
└─────────────────────────────────────────────────────────────┘
```

## Recommended Integration Architecture

### Option 1: Direct Replacement (RECOMMENDED)

**Replace placeholder upstreams with AWS Labs servers:**

```
┌─────────────────────────────────────────────────────────────┐
│  Your 3 Orchestrator MCPs (Virons)                          │
│  - Monitoring MCP :9520                                      │
│  - Security MCP :9500                                        │
│  - Operations MCP :9510                                      │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ (proxy pattern - already implemented)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  AWS Labs MCP Servers (Real Upstreams)                      │
│  - cloudwatch-mcp-server :9109                              │
│  - iam-mcp-server :9103                                     │
│  - cloudtrail-mcp-server :9102                              │
│  - eks-mcp-server :9121                                     │
│  - lambda-tool-mcp-server :9122                             │
│  - ecs-mcp-server :9123                                     │
│  - stepfunctions-tool-mcp-server :9124                      │
│  - (and 58+ more...)                                        │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ (AWS SDK/API calls)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  AWS Services (Real Cloud)                                   │
│  - CloudWatch, IAM, CloudTrail, EKS, Lambda, etc.           │
└─────────────────────────────────────────────────────────────┘
```

**Why this works:**
- ✅ Your proxy pattern is already implemented
- ✅ AWS Labs servers provide real AWS API access
- ✅ No code changes needed in your orchestrators
- ✅ Just update port mappings and start AWS Labs servers

### Option 2: Hybrid (If you need custom logic)

Keep some custom upstreams for business logic, use AWS Labs for standard operations.

## Mapping: Your Orchestrators → AWS Labs Servers

### Monitoring MCP (:9520) → AWS Labs Upstreams

| Your Upstream Port | AWS Labs Server | Tools Provided |
|-------------------|-----------------|----------------|
| :9109 CloudWatch | `cloudwatch-mcp-server` | get_metric_data, get_metric_metadata, get_recommended_metric_alarms, analyze_metric, get_active_alarms, get_alarm_history, describe_log_groups, analyze_log_group, execute_log_insights_query, get_logs_insight_query_results, cancel_logs_insight_query |
| :9110 Prometheus | `prometheus-mcp-server` | query_prometheus, query_range, get_targets, get_alerts |
| :9111 Grafana | (No AWS Labs equivalent) | Keep custom or skip |
| :9112 Elasticsearch | (No AWS Labs equivalent) | Keep custom or skip |

**Additional AWS Labs servers for Monitoring:**
- `cloudwatch-applicationsignals-mcp-server` - Application Signals metrics
- `cloudwatch-appsignals-mcp-server` - AppSignals observability

### Security MCP (:9500) → AWS Labs Upstreams

| Your Upstream Port | AWS Labs Server | Tools Provided |
|-------------------|-----------------|----------------|
| :9100 Gitleaks | (No AWS Labs equivalent) | Keep custom |
| :9101 Compliance Gate | (No AWS Labs equivalent) | Keep custom |
| :9102 CloudTrail | `cloudtrail-mcp-server` | lookup_events, get_trail_status, start_logging, stop_logging, describe_trails |
| :9103 IAM | `iam-mcp-server` | list_users, get_user, create_user, delete_user, list_roles, create_role, list_policies, get_managed_policy_document, attach_user_policy, detach_user_policy, create_access_key, delete_access_key, simulate_principal_policy, list_groups, get_group, create_group, delete_group, add_user_to_group, remove_user_from_group, attach_group_policy, detach_group_policy, put_user_policy, get_user_policy, delete_user_policy, put_role_policy, get_role_policy, delete_role_policy, list_user_policies, list_role_policies |
| :9104 Well-Architected | `well-architected-security-mcp-server` | Security pillar checks |

### Operations MCP (:9510) → AWS Labs Upstreams

| Your Upstream Port | AWS Labs Server | Tools Provided |
|-------------------|-----------------|----------------|
| :9121 EKS | `eks-mcp-server` | list_clusters, describe_cluster, create_cluster, delete_cluster, update_cluster_config, list_nodegroups, describe_nodegroup, create_nodegroup, delete_nodegroup, update_nodegroup_config |
| :9122 Lambda | `lambda-tool-mcp-server` | list_functions, get_function, create_function, delete_function, update_function_code, update_function_configuration, invoke_function, list_layers, publish_layer_version |
| :9123 ECS | `ecs-mcp-server` | list_clusters, describe_clusters, create_cluster, delete_cluster, list_services, describe_services, create_service, update_service, delete_service, list_tasks, describe_tasks, run_task, stop_task |
| :9124 StepFunctions | `stepfunctions-tool-mcp-server` | list_state_machines, describe_state_machine, create_state_machine, delete_state_machine, start_execution, stop_execution, describe_execution, list_executions |
| :9125 EC2 | `core-mcp-server` or `aws-api-mcp-server` | describe_instances, start_instances, stop_instances, terminate_instances, create_security_group, authorize_security_group_ingress |
| :9126 S3 | `core-mcp-server` or `aws-api-mcp-server` | list_buckets, create_bucket, delete_bucket, put_object, get_object, delete_object, list_objects |

**Additional AWS Labs servers for Operations:**
- `aws-serverless-mcp-server` - Serverless operations (Lambda, API Gateway, etc.)
- `cfn-mcp-server` - CloudFormation stack management
- `cdk-mcp-server` - AWS CDK operations
- `terraform-mcp-server` - Terraform operations

## Implementation Steps

### Step 1: Identify Required AWS Labs Servers

Based on your current setup, you need:

**Essential (Replace placeholders):**
1. `cloudwatch-mcp-server` → :9109
2. `iam-mcp-server` → :9103
3. `cloudtrail-mcp-server` → :9102
4. `eks-mcp-server` → :9121
5. `lambda-tool-mcp-server` → :9122
6. `ecs-mcp-server` → :9123
7. `stepfunctions-tool-mcp-server` → :9124

**Optional (Additional capabilities):**
8. `prometheus-mcp-server` → :9110
9. `well-architected-security-mcp-server` → :9104
10. `aws-serverless-mcp-server` → :9127 (new)
11. `dynamodb-mcp-server` → :9128 (new)
12. `s3-tables-mcp-server` → :9129 (new)

### Step 2: Deploy AWS Labs Servers

**Option A: Docker Compose (Recommended)**

Create `docker-compose.awslabs.yml`:

```yaml
version: '3.8'

services:
  # Monitoring upstreams
  cloudwatch-mcp:
    build: ./src/awslabs/cloudwatch-mcp-server
    ports:
      - "9109:9109"
    environment:
      - AWS_REGION=${AWS_REGION}
      - AWS_PROFILE=${AWS_PROFILE}
    volumes:
      - ~/.aws:/root/.aws:ro
    command: ["--port", "9109"]

  prometheus-mcp:
    build: ./src/awslabs/prometheus-mcp-server
    ports:
      - "9110:9110"
    environment:
      - PROMETHEUS_URL=${PROMETHEUS_URL}
    command: ["--port", "9110"]

  # Security upstreams
  cloudtrail-mcp:
    build: ./src/awslabs/cloudtrail-mcp-server
    ports:
      - "9102:9102"
    environment:
      - AWS_REGION=${AWS_REGION}
      - AWS_PROFILE=${AWS_PROFILE}
    volumes:
      - ~/.aws:/root/.aws:ro
    command: ["--port", "9102"]

  iam-mcp:
    build: ./src/awslabs/iam-mcp-server
    ports:
      - "9103:9103"
    environment:
      - AWS_REGION=${AWS_REGION}
      - AWS_PROFILE=${AWS_PROFILE}
      - IAM_READONLY_MODE=false
    volumes:
      - ~/.aws:/root/.aws:ro
    command: ["--port", "9103"]

  well-architected-mcp:
    build: ./src/awslabs/well-architected-security-mcp-server
    ports:
      - "9104:9104"
    environment:
      - AWS_REGION=${AWS_REGION}
      - AWS_PROFILE=${AWS_PROFILE}
    volumes:
      - ~/.aws:/root/.aws:ro
    command: ["--port", "9104"]

  # Operations upstreams
  eks-mcp:
    build: ./src/awslabs/eks-mcp-server
    ports:
      - "9121:9121"
    environment:
      - AWS_REGION=${AWS_REGION}
      - AWS_PROFILE=${AWS_PROFILE}
    volumes:
      - ~/.aws:/root/.aws:ro
    command: ["--port", "9121"]

  lambda-mcp:
    build: ./src/awslabs/lambda-tool-mcp-server
    ports:
      - "9122:9122"
    environment:
      - AWS_REGION=${AWS_REGION}
      - AWS_PROFILE=${AWS_PROFILE}
    volumes:
      - ~/.aws:/root/.aws:ro
    command: ["--port", "9122"]

  ecs-mcp:
    build: ./src/awslabs/ecs-mcp-server
    ports:
      - "9123:9123"
    environment:
      - AWS_REGION=${AWS_REGION}
      - AWS_PROFILE=${AWS_PROFILE}
    volumes:
      - ~/.aws:/root/.aws:ro
    command: ["--port", "9123"]

  stepfunctions-mcp:
    build: ./src/awslabs/stepfunctions-tool-mcp-server
    ports:
      - "9124:9124"
    environment:
      - AWS_REGION=${AWS_REGION}
      - AWS_PROFILE=${AWS_PROFILE}
    volumes:
      - ~/.aws:/root/.aws:ro
    command: ["--port", "9124"]
```

**Start all AWS Labs servers:**
```bash
docker-compose -f docker-compose.awslabs.yml up -d
```

**Option B: UVX (Local Development)**

```bash
# Start each server in separate terminal
uvx awslabs.cloudwatch-mcp-server@latest --port 9109 &
uvx awslabs.iam-mcp-server@latest --port 9103 &
uvx awslabs.cloudtrail-mcp-server@latest --port 9102 &
uvx awslabs.eks-mcp-server@latest --port 9121 &
uvx awslabs.lambda-tool-mcp-server@latest --port 9122 &
uvx awslabs.ecs-mcp-server@latest --port 9123 &
uvx awslabs.stepfunctions-tool-mcp-server@latest --port 9124 &
```

### Step 3: Update Your Orchestrator Configuration

**No code changes needed!** Your proxy pattern already works. Just verify URLs:

```python
# src/virons-monitoring-mcp-server/virons/monitoring_mcp_server/server.py
UPSTREAM = {
    "cloudwatch": "http://localhost:9109",  # Now points to AWS Labs server
    "prometheus": "http://localhost:9110",  # Now points to AWS Labs server
    # ... rest unchanged
}

# src/virons-security-mcp-server/virons/security_mcp_server/server.py
UPSTREAM = {
    "cloudtrail": "http://localhost:9102",  # Now points to AWS Labs server
    "iam": "http://localhost:9103",         # Now points to AWS Labs server
    "well_architected": "http://localhost:9104",  # Now points to AWS Labs server
    # ... rest unchanged
}

# src/virons-operations-mcp-server/virons/operations_mcp_server/server.py
UPSTREAM = {
    "eks": "http://localhost:9121",              # Now points to AWS Labs server
    "lambda": "http://localhost:9122",           # Now points to AWS Labs server
    "ecs": "http://localhost:9123",              # Now points to AWS Labs server
    "stepfunctions": "http://localhost:9124",    # Now points to AWS Labs server
    # ... rest unchanged
}
```

### Step 4: Test Integration

```bash
# 1. Start AWS Labs upstreams
docker-compose -f docker-compose.awslabs.yml up -d

# 2. Verify upstreams are running
curl http://localhost:9109/health  # CloudWatch
curl http://localhost:9103/health  # IAM
curl http://localhost:9121/health  # EKS

# 3. Start your orchestrators
docker-compose up -d virons-monitoring-mcp virons-security-mcp virons-operations-mcp

# 4. Test tool discovery (should now show real AWS tools)
curl http://localhost:9520/tools | jq '.tools | length'  # Should show 62+ tools
curl http://localhost:9500/tools | jq '.tools | length'  # Should show 64+ tools
curl http://localhost:9510/tools | jq '.tools | length'  # Should show 66+ tools

# 5. Test a real AWS operation
curl -X POST http://localhost:9500/tools/list_users \
  -H "Content-Type: application/json" \
  -d '{}' | jq
```

## Benefits of This Architecture

### 1. **Separation of Concerns**
- **Your orchestrators:** Business logic, audit trails, correlation IDs, DDD
- **AWS Labs servers:** Direct AWS API access, authentication, error handling

### 2. **Maintainability**
- AWS Labs servers are maintained by AWS
- You focus on business logic, not AWS API changes
- Updates to AWS APIs handled upstream

### 3. **Scalability**
- Each AWS Labs server can scale independently
- Your orchestrators remain lightweight
- Easy to add new AWS services

### 4. **Testing**
- Mock AWS Labs servers for unit tests
- Real AWS Labs servers for integration tests
- No need to mock AWS SDK directly

### 5. **Security**
- AWS credentials only in AWS Labs servers
- Your orchestrators don't need AWS credentials
- Centralized IAM policy management

## Custom Upstreams (Keep These)

Some of your upstreams don't have AWS Labs equivalents. Keep these custom:

1. **Gitleaks (:9100)** - Secret scanning (custom)
2. **Compliance Gate (:9101)** - Custom compliance checks
3. **Grafana (:9111)** - If you use Grafana (not AWS native)
4. **Elasticsearch (:9112)** - If you use self-hosted ES

## Recommended Next Steps

1. **Start with 3 essential servers:**
   - `cloudwatch-mcp-server` (:9109)
   - `iam-mcp-server` (:9103)
   - `eks-mcp-server` (:9121)

2. **Test integration:**
   - Verify tool discovery works
   - Test a few core tools
   - Check audit trails still work

3. **Gradually add more:**
   - Add Lambda, ECS, StepFunctions
   - Add CloudTrail for security
   - Add additional services as needed

4. **Document the setup:**
   - Update UPSTREAM_INTEGRATION.md
   - Add AWS Labs server deployment guide
   - Document IAM permissions needed

## IAM Permissions Required

Each AWS Labs server needs specific IAM permissions. Example for CloudWatch:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "cloudwatch:DescribeAlarms",
      "cloudwatch:DescribeAlarmHistory",
      "cloudwatch:GetMetricData",
      "cloudwatch:ListMetrics",
      "logs:DescribeLogGroups",
      "logs:StartQuery",
      "logs:GetQueryResults",
      "logs:StopQuery"
    ],
    "Resource": "*"
  }]
}
```

See each AWS Labs server's README for specific permissions.

## Conclusion

**Recommendation:** Use Option 1 (Direct Replacement) with AWS Labs servers as your upstreams.

**Why:**
- ✅ Your proxy architecture is already perfect for this
- ✅ AWS Labs servers provide production-ready AWS API access
- ✅ No code changes needed in your orchestrators
- ✅ Maintained by AWS, not you
- ✅ Just update port mappings and deploy

**Effort:** ~2-4 hours to deploy and test
**Benefit:** Real AWS integration with minimal code
