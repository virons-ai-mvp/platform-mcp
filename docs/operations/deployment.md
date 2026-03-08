# Virons MCP Deployment Guide

## Local Deployment

### Prerequisites
- Docker and Docker Compose
- Python 3.13+
- uv package manager

### Quick Start

```bash
# From virons-mcp-gateway directory
cd src/virons-mcp-gateway
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Services
- Gateway: http://localhost:9000
- Infrastructure MCP: http://localhost:9100
- Security MCP: http://localhost:9200
- Operations MCP: http://localhost:9300
- Monitoring MCP: http://localhost:9400

### Health Checks
```bash
curl http://localhost:9000/health
curl http://localhost:9100/health/live
```

## AWS ECS Deployment

### Prerequisites
- AWS CLI configured
- Docker
- AWS account with ECS permissions
- Terraform (optional)

### Option 1: Deployment Scripts

```bash
# Deploy Infrastructure MCP
cd src/virons-infrastructure-mcp-server
./deploy-ecs.sh

# Deploy Gateway
cd src/virons-mcp-gateway
./deploy-ecs.sh
```

### Option 2: Terraform

```bash
cd infrastructure/terraform/ecs

# Initialize
terraform init

# Plan
terraform plan -var="aws_region=eu-central-1"

# Apply
terraform apply -var="aws_region=eu-central-1"
```

### Manual ECS Setup

1. **Create ECS Cluster**
```bash
aws ecs create-cluster --cluster-name virons-mcp-cluster --region eu-central-1
```

2. **Create ECR Repositories**
```bash
aws ecr create-repository --repository-name virons-infrastructure-mcp --region eu-central-1
aws ecr create-repository --repository-name virons-mcp-gateway --region eu-central-1
```

3. **Build and Push Images**
```bash
# Infrastructure MCP
cd src/virons-infrastructure-mcp-server
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com
docker build -t virons-infrastructure-mcp:latest -f Dockerfile ../..
docker tag virons-infrastructure-mcp:latest $AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/virons-infrastructure-mcp:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/virons-infrastructure-mcp:latest

# Gateway
cd src/virons-mcp-gateway
docker build -t virons-mcp-gateway:latest -f Dockerfile ../..
docker tag virons-mcp-gateway:latest $AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/virons-mcp-gateway:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/virons-mcp-gateway:latest
```

4. **Register Task Definitions**
```bash
# Update task definitions with your AWS account ID and region
envsubst < ecs-task-definition.json > /tmp/task-def.json
aws ecs register-task-definition --cli-input-json file:///tmp/task-def.json --region eu-central-1
```

5. **Create Services**
```bash
aws ecs create-service \
  --cluster virons-mcp-cluster \
  --service-name virons-infrastructure-mcp \
  --task-definition virons-infrastructure-mcp \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx]}" \
  --region eu-central-1
```

### Environment Variables

**Infrastructure MCP:**
- `PORT=9100`
- `LOG_LEVEL=INFO`
- `AWS_REGION=eu-central-1`

**Gateway:**
- `PORT=9000`
- `LOG_LEVEL=INFO`
- `AWS_REGION=eu-central-1`

### IAM Permissions

Task execution role needs:
- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`
- `ecr:GetDownloadUrlForLayer`
- `ecr:BatchGetImage`
- `logs:CreateLogStream`
- `logs:PutLogEvents`

Task role needs:
- Service-specific AWS permissions (CDK, CloudFormation, etc.)

### Monitoring

CloudWatch Log Groups:
- `/ecs/virons-infrastructure-mcp`
- `/ecs/virons-mcp-gateway`

### Scaling

Update desired count:
```bash
aws ecs update-service \
  --cluster virons-mcp-cluster \
  --service virons-infrastructure-mcp \
  --desired-count 2 \
  --region eu-central-1
```

### Troubleshooting

**Check service status:**
```bash
aws ecs describe-services \
  --cluster virons-mcp-cluster \
  --services virons-infrastructure-mcp \
  --region eu-central-1
```

**View logs:**
```bash
aws logs tail /ecs/virons-infrastructure-mcp --follow --region eu-central-1
```

**Check task health:**
```bash
aws ecs describe-tasks \
  --cluster virons-mcp-cluster \
  --tasks <task-id> \
  --region eu-central-1
```

## Production Considerations

1. **Networking**
   - Use private subnets
   - Configure VPC endpoints for AWS services
   - Set up Application Load Balancer

2. **Security**
   - Enable encryption at rest
   - Use AWS Secrets Manager for sensitive data
   - Implement least privilege IAM policies
   - Enable VPC Flow Logs

3. **Monitoring**
   - Enable Container Insights
   - Set up CloudWatch alarms
   - Configure X-Ray tracing

4. **High Availability**
   - Deploy across multiple AZs
   - Use auto-scaling
   - Configure health checks

5. **Cost Optimization**
   - Use Fargate Spot for non-critical workloads
   - Right-size task resources
   - Enable auto-scaling based on metrics
