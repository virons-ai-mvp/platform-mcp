# Expert DevOps Engineer Agent
**Version**: 2.0.0
**Role**: CI/CD, Infrastructure Automation, Observability
**Stack**: Terraform, GitHub Actions, AWS, Docker
**Risk Level**: HIGH (0.85)

## Purpose
Automate infrastructure deployment, CI/CD pipelines, and observability for Virons AI platform.

## CI/CD Pipeline (GitHub Actions)

### Terraform Validation
```yaml
name: Terraform Validate
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform fmt -check
      - run: terraform init
      - run: terraform validate
      - run: make security-scan
```

### Terraform Deployment
```yaml
name: Terraform Deploy
on:
  push:
    branches: [main]
    paths: ['infrastructure/terraform/**']
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::412179655775:role/github-actions-terraform
          aws-region: eu-central-1
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform plan
      - run: terraform apply -auto-approve
```

## Infrastructure as Code

### Terraform Structure
```text
infrastructure/terraform/
├── modules/          # Reusable modules
│   ├── networking/
│   ├── security/
│   ├── compute/
│   ├── database/
│   └── ai/
├── environments/     # Environment configs
│   ├── dev/
│   ├── staging/
│   ├── demo/
│   └── production/
└── terraform.tf      # Provider config
```

### Best Practices
- **State Management**: S3 backend + DynamoDB locks
- **Module Versioning**: Git tags for modules
- **Variable Validation**: Input validation rules
- **Output Documentation**: Clear output descriptions
- **Resource Tagging**: Environment, Project, ManagedBy

## Container Management

### Docker Best Practices
```dockerfile
## Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
EXPOSE 8080
CMD ["node", "server.js"]
```

### ECS Deployment
- **Task Definition**: CPU/memory limits
- **Health Checks**: HTTP endpoint checks
- **Auto-scaling**: Target tracking (CPU 70%)
- **Blue/Green**: Zero-downtime deployments

## Observability

### CloudWatch Dashboards
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/ECS", "CPUUtilization"],
          ["AWS/RDS", "DatabaseConnections"],
          ["AWS/ElastiCache", "CacheHits"]
        ],
        "period": 300,
        "stat": "Average",
        "region": "eu-central-1",
        "title": "Virons Platform Overview"
      }
    }
  ]
}
```

### Logging Strategy
- **Application Logs**: CloudWatch Logs
- **Infrastructure Logs**: VPC Flow Logs, CloudTrail
- **Retention**: 7 years (compliance)
- **Analysis**: CloudWatch Insights

### Alerting
- **Critical**: RDS CPU > 80%, ECS task failures
- **Warning**: ALB 5xx > 1%, high latency
- **SNS**: Email notifications to admin

## Security

### Secrets Management
- **AWS Secrets Manager**: API keys, credentials
- **KMS Encryption**: All secrets encrypted
- **IAM Roles**: No hardcoded credentials
- **Rotation**: Automated rotation where possible

### Compliance
- **GDPR**: Data encryption, audit logging
- **BaFin**: Security controls, monitoring
- **DORA**: Resilience, incident response

## Quick Reference

```bash
## Terraform workflow
cd infrastructure/terraform/environments/demo
terraform init
terraform plan
terraform apply

## Docker build
docker build -t virons-api:latest .
docker push 412179655775.dkr.ecr.eu-central-1.amazonaws.com/virons-api:latest

## ECS deployment
aws ecs update-service --cluster virons-demo --service api --force-new-deployment

## Logs
aws logs tail /ecs/virons-demo-api --follow
```

---
**Version**: 2.0.0
**Last Updated**: February 25, 2026
**Virons AI Platform**
