# AWS Labs MCP Servers Deployment Plan

## Your 4 Virons MCP Servers

### 1. Monitoring MCP (:9520)
**Upstreams needed:**
- CloudWatch :9109
- Prometheus :9110
- Grafana :9111 (optional - no AWS Labs equivalent)
- Elasticsearch :9112 (optional - no AWS Labs equivalent)

### 2. Security MCP (:9500)
**Upstreams needed:**
- CloudTrail :9102
- IAM :9103
- Well-Architected :9104
- Gitleaks :9100 (custom - keep as is)
- Compliance Gate :9101 (custom - keep as is)

### 3. Operations MCP (:9510)
**Upstreams needed:**
- EKS :9121
- Lambda :9122
- ECS :9123
- StepFunctions :9124
- EC2 :9125
- S3 :9126

### 4. Infrastructure MCP (:9530)
**Upstreams needed:**
- CDK :9140
- CloudFormation :9141
- Terraform :9142
- IAC :9143

## AWS Labs Servers to Deploy

### Priority 1: Essential (Deploy First)

| AWS Labs Server | Port | For Virons MCP | Tools |
|----------------|------|----------------|-------|
| `cloudwatch-mcp-server` | 9109 | Monitoring | 11 tools |
| `iam-mcp-server` | 9103 | Security | 29 tools |
| `cloudtrail-mcp-server` | 9102 | Security | 5 tools |
| `eks-mcp-server` | 9121 | Operations | 10 tools |
| `lambda-tool-mcp-server` | 9122 | Operations | 9 tools |
| `ecs-mcp-server` | 9123 | Operations | 14 tools |

### Priority 2: Infrastructure (Deploy Second)

| AWS Labs Server | Port | For Virons MCP | Tools |
|----------------|------|----------------|-------|
| `cdk-mcp-server` | 9140 | Infrastructure | CDK operations |
| `cfn-mcp-server` | 9141 | Infrastructure | CloudFormation |
| `terraform-mcp-server` | 9142 | Infrastructure | Terraform |
| `aws-iac-mcp-server` | 9143 | Infrastructure | IaC operations |

### Priority 3: Additional (Deploy Third)

| AWS Labs Server | Port | For Virons MCP | Tools |
|----------------|------|----------------|-------|
| `stepfunctions-tool-mcp-server` | 9124 | Operations | 8 tools |
| `prometheus-mcp-server` | 9110 | Monitoring | 4 tools |
| `well-architected-security-mcp-server` | 9104 | Security | Security checks |
| `core-mcp-server` | 9125/9126 | Operations | EC2, S3 |

## Deployment Steps

### Step 1: Check AWS Labs Servers Availability

```bash
cd /Users/amjadalissaalkhalaf/repos/virons-fintech/virons-ai-mvp/platform-mcp/src/awslabs

# Check which servers exist
ls -d cloudwatch-mcp-server iam-mcp-server cloudtrail-mcp-server \
      eks-mcp-server lambda-tool-mcp-server ecs-mcp-server \
      cdk-mcp-server cfn-mcp-server terraform-mcp-server aws-iac-mcp-server \
      stepfunctions-tool-mcp-server prometheus-mcp-server \
      well-architected-security-mcp-server core-mcp-server 2>/dev/null
```

### Step 2: Create Deployment Script

Create `scripts/deploy-awslabs-servers.sh`:

```bash
#!/bin/bash
set -e

AWSLABS_DIR="/Users/amjadalissaalkhalaf/repos/virons-fintech/virons-ai-mvp/platform-mcp/src/awslabs"
AWS_REGION="${AWS_REGION:-us-east-1}"
AWS_PROFILE="${AWS_PROFILE:-default}"

echo "🚀 Deploying AWS Labs MCP Servers..."

# Priority 1: Essential servers
declare -A SERVERS=(
    ["cloudwatch-mcp-server"]="9109"
    ["iam-mcp-server"]="9103"
    ["cloudtrail-mcp-server"]="9102"
    ["eks-mcp-server"]="9121"
    ["lambda-tool-mcp-server"]="9122"
    ["ecs-mcp-server"]="9123"
)

for server in "${!SERVERS[@]}"; do
    port="${SERVERS[$server]}"
    echo "📦 Starting $server on port $port..."
    
    if [ -d "$AWSLABS_DIR/$server" ]; then
        cd "$AWSLABS_DIR/$server"
        
        # Start server in background
        AWS_REGION=$AWS_REGION AWS_PROFILE=$AWS_PROFILE \
        uvx "awslabs.${server}@latest" --port $port > "/tmp/${server}.log" 2>&1 &
        
        echo "✅ $server started (PID: $!)"
        sleep 2
    else
        echo "⚠️  $server not found, skipping..."
    fi
done

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Check server status:"
for server in "${!SERVERS[@]}"; do
    port="${SERVERS[$server]}"
    echo "  curl http://localhost:$port/health"
done
```

### Step 3: Create Docker Compose (Alternative)

Create `docker-compose.awslabs.yml`:

```yaml
version: '3.8'

services:
  # Priority 1: Essential servers
  cloudwatch-mcp:
    build: ./src/awslabs/cloudwatch-mcp-server
    container_name: awslabs-cloudwatch
    ports:
      - "9109:9109"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped

  iam-mcp:
    build: ./src/awslabs/iam-mcp-server
    container_name: awslabs-iam
    ports:
      - "9103:9103"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - IAM_READONLY_MODE=false
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped

  cloudtrail-mcp:
    build: ./src/awslabs/cloudtrail-mcp-server
    container_name: awslabs-cloudtrail
    ports:
      - "9102:9102"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped

  eks-mcp:
    build: ./src/awslabs/eks-mcp-server
    container_name: awslabs-eks
    ports:
      - "9121:9121"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped

  lambda-mcp:
    build: ./src/awslabs/lambda-tool-mcp-server
    container_name: awslabs-lambda
    ports:
      - "9122:9122"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped

  ecs-mcp:
    build: ./src/awslabs/ecs-mcp-server
    container_name: awslabs-ecs
    ports:
      - "9123:9123"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped

  # Priority 2: Infrastructure servers
  cdk-mcp:
    build: ./src/awslabs/cdk-mcp-server
    container_name: awslabs-cdk
    ports:
      - "9140:9140"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped

  cfn-mcp:
    build: ./src/awslabs/cfn-mcp-server
    container_name: awslabs-cfn
    ports:
      - "9141:9141"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped

  terraform-mcp:
    build: ./src/awslabs/terraform-mcp-server
    container_name: awslabs-terraform
    ports:
      - "9142:9142"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped

  iac-mcp:
    build: ./src/awslabs/aws-iac-mcp-server
    container_name: awslabs-iac
    ports:
      - "9143:9143"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped

  # Priority 3: Additional servers
  stepfunctions-mcp:
    build: ./src/awslabs/stepfunctions-tool-mcp-server
    container_name: awslabs-stepfunctions
    ports:
      - "9124:9124"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped

  prometheus-mcp:
    build: ./src/awslabs/prometheus-mcp-server
    container_name: awslabs-prometheus
    ports:
      - "9110:9110"
    environment:
      - PROMETHEUS_URL=${PROMETHEUS_URL:-http://localhost:9090}
      - FASTMCP_LOG_LEVEL=ERROR
    restart: unless-stopped

  well-architected-mcp:
    build: ./src/awslabs/well-architected-security-mcp-server
    container_name: awslabs-well-architected
    ports:
      - "9104:9104"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_PROFILE=${AWS_PROFILE:-default}
      - FASTMCP_LOG_LEVEL=ERROR
    volumes:
      - ~/.aws:/root/.aws:ro
    restart: unless-stopped
```

### Step 4: Test Deployment

Create `scripts/test-awslabs-servers.sh`:

```bash
#!/bin/bash

echo "🧪 Testing AWS Labs MCP Servers..."

# Test essential servers
declare -A SERVERS=(
    ["CloudWatch"]="9109"
    ["IAM"]="9103"
    ["CloudTrail"]="9102"
    ["EKS"]="9121"
    ["Lambda"]="9122"
    ["ECS"]="9123"
    ["CDK"]="9140"
    ["CloudFormation"]="9141"
    ["Terraform"]="9142"
    ["IAC"]="9143"
)

for name in "${!SERVERS[@]}"; do
    port="${SERVERS[$name]}"
    echo -n "Testing $name (:$port)... "
    
    if curl -s -f "http://localhost:$port/health" > /dev/null 2>&1; then
        echo "✅ OK"
    else
        echo "❌ FAILED"
    fi
done

echo ""
echo "Testing tool discovery..."
for name in "${!SERVERS[@]}"; do
    port="${SERVERS[$name]}"
    count=$(curl -s "http://localhost:$port/tools" 2>/dev/null | jq '.tools | length' 2>/dev/null || echo "0")
    echo "  $name: $count tools"
done
```

## Quick Start Commands

### Option 1: UVX (Fastest for testing)

```bash
# Start essential servers
uvx awslabs.cloudwatch-mcp-server@latest --port 9109 &
uvx awslabs.iam-mcp-server@latest --port 9103 &
uvx awslabs.cloudtrail-mcp-server@latest --port 9102 &
uvx awslabs.eks-mcp-server@latest --port 9121 &
uvx awslabs.lambda-tool-mcp-server@latest --port 9122 &
uvx awslabs.ecs-mcp-server@latest --port 9123 &

# Wait and test
sleep 5
curl http://localhost:9109/health
curl http://localhost:9103/health
```

### Option 2: Docker Compose (Production)

```bash
# Build and start all servers
docker-compose -f docker-compose.awslabs.yml up -d

# Check status
docker-compose -f docker-compose.awslabs.yml ps

# View logs
docker-compose -f docker-compose.awslabs.yml logs -f cloudwatch-mcp

# Stop all
docker-compose -f docker-compose.awslabs.yml down
```

## Verification

After deployment, verify your Virons MCPs can discover tools:

```bash
# Test Monitoring MCP
curl http://localhost:9520/tools | jq '.tools | length'
# Should show 62+ tools

# Test Security MCP
curl http://localhost:9500/tools | jq '.tools | length'
# Should show 64+ tools

# Test Operations MCP
curl http://localhost:9510/tools | jq '.tools | length'
# Should show 66+ tools

# Test Infrastructure MCP
curl http://localhost:9530/tools | jq '.tools | length'
# Should show tools from CDK, CFN, Terraform, IAC
```

## Next Steps

1. **Review this plan** - Confirm which servers you need
2. **Choose deployment method** - UVX for testing, Docker for production
3. **Deploy Priority 1 servers** - Essential 6 servers first
4. **Test integration** - Verify tool discovery works
5. **Deploy remaining servers** - Add infrastructure and additional servers
6. **Update documentation** - Document your deployment
