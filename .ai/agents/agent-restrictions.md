# Agent Restrictions

**Last Updated**: 2026-02-25
**Compliance**: BaFin MaRisk AT 8.1, GDPR Art 32, DORA Art 11

## NEVER Execute Without Human Approval

### Destructive Operations
- `terraform apply`
- `terraform destroy`
- `terraform taint`
- `aws eks update-cluster-config`
- `aws rds modify-db-instance`
- `aws rds delete-db-instance`
- `aws s3 rb --force`
- Resource deletion in any environment

### State-Changing Operations
- Enabling stopped resources (ECS cluster, RDS, Redis, ALB, CloudFront)
- Modifying security groups
- Changing KMS key policies
- Updating IAM roles/policies
- Modifying VPC routing tables
- Changing budget limits
- Updating DNS records

### Production Environment
- ANY infrastructure change in production
- Scaling operations
- Certificate updates
- Load balancer modifications

## Read-Only Operations (Always Safe)

### Terraform
- `terraform init`
- `terraform validate`
- `terraform plan`
- `terraform fmt`
- `terraform show`
- `terraform state list`

### Testing
- `make test-module MODULE=<name>`
- `make security-scan`
- `go test ./...`
- Terratest execution

### AWS CLI (Describe/List Only)
- `aws eks describe-cluster`
- `aws rds describe-db-instances`
- `aws ec2 describe-*`
- `aws s3 ls`
- `aws cloudwatch get-metric-statistics`
- `aws budgets describe-budgets`

### File Operations
- Reading any file
- Analyzing code
- Generating documentation
- Creating test files

## Require Human Confirmation

### Security Changes
- Modifying security group rules
- Changing KMS encryption settings
- Updating IAM policies
- Adding/removing VPC peering
- Modifying network ACLs

### Cost-Impacting Changes
- Creating new resources
- Changing instance types
- Enabling multi-AZ
- Increasing storage
- Adding NAT gateways

### Compliance-Sensitive
- Removing resource tags
- Changing data residency (must stay eu-central-1)
- Disabling logging
- Modifying backup retention
- Changing encryption settings

## Auto-Reject (Never Allow)

### Security Violations
- Hardcoding AWS credentials
- Hardcoding API keys or secrets
- Disabling KMS encryption
- Public subnet placement (except ALB/CloudFront)
- Overly permissive security groups (0.0.0.0/0 ingress)
- IAM policies with `*` actions

### Compliance Violations
- Resources outside eu-central-1
- Missing required tags (Environment, Project, ManagedBy, CostCenter)
- Skipping TDD workflow
- Deploying without tests
- Removing audit logging

### Cost Violations
- Instance types larger than xlarge without justification
- Creating resources without budget approval
- Enabling expensive services (SageMaker, EMR) without approval

### Process Violations
- Committing directly to main branch
- Skipping code review
- Deploying without plan review
- Modifying Terraform state directly

## Environment-Specific Rules

### Development
- Apply allowed after test pass + human approval
- Cost limit: $400/month
- Can use Spot instances

### Staging
- Apply requires test pass + security scan + approval
- Cost limit: $900/month
- Must mirror production architecture

### Demo
- Apply requires full review
- Cost limit: $1,200/month
- Public access allowed for demos

### Production
- Apply requires: tests + security scan + compliance check + approval
- Cost limit: $2,500/month
- Zero-downtime deployments only
- Rollback plan mandatory
- Change window: Tue-Thu 10:00-16:00 CET

## Escalation Path

**Low Risk** (read-only) → Execute immediately
**Medium Risk** (dev apply) → Request approval, show plan
**High Risk** (prod change) → Full review + approval + monitoring
**Critical** (security/compliance) → Reject + escalate to human

## Audit Requirements

All agent actions must log:
- Timestamp
- Operation attempted
- Risk level
- Approval status
- Execution result
- Rollback status (if applicable)
