# Cost Guards

**Budget Limits**: Dev $400 | Staging $900 | Demo $1,200 | Production $2,500

## High-Cost Resources (Require Approval)

### Compute
- EKS node groups: Justify >2 nodes
- `ng-general`: m6i.large Spot ($31/month Spot)
- `ng-inference`: m6i.xlarge On-Demand ($124/month) — ML workloads only
- Any instance >xlarge requires written justification

### Database
- RDS: db.t3.medium max for dev/staging
- Multi-AZ: +100% cost, requires justification
- ElastiCache: cache.t3.micro for dev

### Networking
- NAT Gateway: $32/month + data transfer — do not add AZs without approval
- Data transfer: Monitor cross-AZ egress

## Auto-Reject

- Instance types >xlarge without justification
- GPU instances (p3, g4) without approval
- Resources outside eu-central-1
- SageMaker / EMR without approval (use Bedrock instead)
- Unattached EBS volumes
- RDS snapshots >30 days without lifecycle policy

## Cost Thresholds

- <$50/month: Auto-approve for dev
- $50–$200/month: Requires approval
- >$200/month: Requires VP approval + business justification

## Bedrock Costs

- `amazon.nova-pro-v1:0`: ~$0.0008/1K input tokens, ~$0.0032/1K output tokens
- Always use streaming for long responses
- Cache repeated prompts where possible
- Alert if Bedrock spend >$100/month

## Resource Tagging (Mandatory)

```yaml
labels:
  app: {service-name}
  version: {version}
  namespace: virons-{namespace}
  managed-by: kustomize
```

## Budget Alerts

- 50%: Warning
- 80%: Alert + review required
- 100%: Critical + auto-scale down non-essential
- 120%: Emergency escalation
