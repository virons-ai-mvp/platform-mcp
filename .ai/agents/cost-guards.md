# Cost Guards

**Purpose**: Prevent unexpected AWS costs from agent actions
**Budget Limits**: Dev $400 | Staging $900 | Demo $1,200 | Production $2,500

## High-Cost Resources (Require Approval)

### Compute
- **EKS Cluster**: $73/month base + node costs
  - Node groups: Require justification for >2 nodes
  - Instance types: m6i.large ($62/month), m6i.xlarge ($124/month)
  - Spot instances preferred for non-critical workloads
- **ECS**: Fargate pricing by vCPU/memory
  - Must justify >2 vCPU or >4GB memory
- **EC2**: Any instance >t3.large requires approval

### Database
- **RDS**: Currently stopped to save costs
  - Multi-AZ: +100% cost, requires justification
  - Instance types: db.t3.medium max for dev/staging
  - Storage: gp3 only, monitor IOPS usage
- **ElastiCache**: Currently stopped
  - Redis: cache.t3.micro for dev, cache.t3.small for staging

### Storage
- **S3**: Lifecycle policies mandatory
  - Intelligent-Tiering for >128KB objects
  - Glacier for archives >90 days
- **EBS**: gp3 only (cheaper than gp2)
  - Delete unattached volumes

### Networking
- **NAT Gateway**: $32/month + data transfer
  - Max 1 per AZ (currently 3 for HA)
- **Load Balancers**: ALB $16/month + LCU costs
  - Currently stopped to save costs
- **Data Transfer**: Monitor cross-AZ and internet egress

### CDN
- **CloudFront**: Currently stopped
  - Enable only when needed for demos/production

## Auto-Reject Scenarios

### Instance Sizing
- Any instance type >xlarge without written justification
- GPU instances (p3, g4) without approval
- High-memory instances (r6i, x2) without approval

### Multi-Region
- Resources outside eu-central-1 (data residency requirement)
- Cross-region replication without approval

### Expensive Services
- SageMaker: Requires approval + cost estimate
- EMR: Requires approval + cluster auto-termination
- Redshift: Not approved for current scope
- Managed Kafka (MSK): Not approved for current scope

### Wasteful Patterns
- Unattached EBS volumes
- Stopped instances running >7 days
- Unused Elastic IPs
- Empty S3 buckets with versioning
- RDS snapshots >30 days without lifecycle

## Cost Estimation Required

### Monthly Recurring Costs
```
EKS Cluster:        $73
NAT Gateways (3):   $96
RDS (stopped):      $0
ElastiCache (stopped): $0
ALB (stopped):      $0
CloudFront (stopped): $0
S3 Storage:         ~$10
CloudWatch:         ~$15
---
Current Total:      ~$194/month
```

### On-Demand Costs (When Enabled)
```
RDS db.t3.medium:   ~$50/month
ElastiCache t3.micro: ~$12/month
ALB:                ~$20/month
CloudFront:         ~$50/month (with traffic)
ECS Fargate:        Variable based on usage
---
Full Stack:         ~$326/month + compute
```

### Cost Thresholds
- **<$50/month**: Auto-approve for dev
- **$50-$200/month**: Requires approval
- **>$200/month**: Requires VP approval + business justification

## Monitoring & Alerts

### Budget Alerts (Already Configured)
- 50% of budget: Warning email
- 80% of budget: Alert + review required
- 100% of budget: Critical alert + auto-stop non-essential resources
- 120% of budget: Emergency escalation

### Resource Tagging
All resources must have:
```hcl
tags = {
  Environment = "dev|staging|demo|production"
  Project     = "virons-ai"
  ManagedBy   = "terraform"
  CostCenter  = "engineering"
  Owner       = "team-name"
}
```

## Emergency Cost Controls

If budget exceeded:

### Immediate Actions (Auto-Execute)
1. Stop non-essential ECS tasks
2. Scale down EKS node groups to minimum
3. Disable CloudFront distributions
4. Stop RDS instances (if running)
5. Alert engineering team

## Agent Cost Responsibilities

Agents must:
- Estimate cost before creating resources
- Use smallest instance types that meet requirements
- Prefer Spot instances for fault-tolerant workloads
- Enable auto-scaling with appropriate limits
- Set resource quotas and limits
- Document cost justification in PR
- Never exceed environment budget without approval
