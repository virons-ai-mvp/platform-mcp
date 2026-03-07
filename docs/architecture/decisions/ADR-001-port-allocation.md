<link rel="stylesheet" href="../../../../platform-resources/styles/virons-markdown.css">

# ADR-001: MCP Server Port Allocation

**Status**: ✅ Accepted
**Date**: 2026-03-05
**Contexts**: Security, Governance, Operations, Compliance
**Compliance**: BaFin AT 8.1, DORA Art 11

## Context

***

Virons platform requires clear port allocation for MCP servers to:
1. Avoid conflicts with virons-services (9300-9424)
2. Enable context-based network segmentation
3. Support compliance audit trails
4. Allow predictable scaling

## Decision

***

Allocate MCP server ports in the **9100-9199 range** with context-based segmentation:

| Context | Port Range | Capacity | Current Usage |
|---------|------------|----------|---------------|
| **Security** | 9100-9109 | 10 servers | 5 (gitleaks, compliance-gate, cloudtrail, iam, well-architected-security) |
| **Governance** | 9110-9119 | 10 servers | 2 (org-governance, workflow-governance) |
| **Operations** | 9120-9129 | 10 servers | 5 (secrets-rotation, eks, lambda, ecs, stepfunctions) |
| **Compliance** | 9130-9139 | 10 servers | 3 (compliance-checklist, cost-explorer, billing) |
| **Infrastructure** | 9140-9149 | 10 servers | 5 (cdk, cfn, terraform, iac, network) |
| **Data-Relational** | 9150-9159 | 10 servers | 4 (postgres, mysql, aurora-dsql, redshift) |
| **AI-ML** | 9160-9169 | 10 servers | 3 (sagemaker, bedrock-kb, kendra) |
| **Messaging** | 9170-9179 | 10 servers | 2 (sns-sqs, msk) |
| **Data-NoSQL** | 9180-9189 | 10 servers | 6 (dynamodb, documentdb, keyspaces, neptune, elasticache, s3-tables) |
| **Monitoring** | 9190-9199 | 10 servers | 4 (cloudwatch, prometheus, appsignals, applicationsignals) |

**Total Allocated**: 39 servers (6 existing + 33 AWS MCP Tier 1)
**Total Reserved**: 61 ports for future expansion

### Port Registry

```yaml
# Security Context (9100-9109)
9100: gitleaks
9101: compliance-gate
9102: cloudtrail-mcp-server
9103: iam-mcp-server
9104: well-architected-security-mcp-server
9105-9109: reserved

# Governance Context (9110-9119)
9110: org-governance
9111: workflow-governance
9112-9119: reserved

# Operations Context (9120-9129)
9120: secrets-rotation
9121: eks-mcp-server
9122: lambda-tool-mcp-server
9123: ecs-mcp-server
9124: stepfunctions-tool-mcp-server
9125-9129: reserved

# Compliance Context (9130-9139)
9130: compliance-checklist
9131: cost-explorer-mcp-server
9132: billing-cost-management-mcp-server
9133-9139: reserved

# Infrastructure Context (9140-9149)
9140: cdk-mcp-server
9141: cfn-mcp-server
9142: terraform-mcp-server
9143: aws-iac-mcp-server
9144: aws-network-mcp-server
9145-9149: reserved

# Data-Relational Context (9150-9159)
9150: postgres-mcp-server
9151: mysql-mcp-server
9152: aurora-dsql-mcp-server
9153: redshift-mcp-server
9154-9159: reserved

# AI-ML Context (9160-9169)
9160: sagemaker-ai-mcp-server
9161: bedrock-kb-retrieval-mcp-server
9162: amazon-kendra-index-mcp-server
9163-9169: reserved

# Messaging Context (9170-9179)
9170: amazon-sns-sqs-mcp-server
9171: aws-msk-mcp-server
9172-9179: reserved

# Data-NoSQL Context (9180-9189)
9180: dynamodb-mcp-server
9181: documentdb-mcp-server
9182: amazon-keyspaces-mcp-server
9183: amazon-neptune-mcp-server
9184: elasticache-mcp-server
9185: s3-tables-mcp-server
9186-9189: reserved

# Monitoring Context (9190-9199)
9190: cloudwatch-mcp-server
9191: prometheus-mcp-server
9192: cloudwatch-appsignals-mcp-server
9193: cloudwatch-applicationsignals-mcp-server
9194-9199: reserved
```

## Rationale

***

### 1. Isolation from virons-services

- **virons-services**: 9300-9424 (forensic: 9300-9415, ml: 9420-9424)
- **platform-mcp**: 9100-9199
- Clear separation prevents port conflicts

### 2. Context-Based Segmentation

- Each bounded context gets 10-port range
- Easy to identify server context by port
- Supports network policies per context

### 3. Compliance Audit Trail

- Port allocation documented (BaFin AT 8.1)
- Network segmentation for resilience (DORA Art 11)
- Clear ownership per context

### 4. Scalability

- 10 servers per context (sufficient for MVP)
- 60 reserved ports for future contexts
- Total capacity: 100 MCP servers

## Consequences

***

### Positive

✅ No port conflicts with platform-services
✅ Predictable port allocation by context
✅ Easy to configure firewall rules (9100-9199)
✅ Clear audit trail for compliance
✅ Room for growth (60 reserved ports)

### Negative

⚠️ Must maintain port registry documentation
⚠️ Firewall rules need updating for 9100-9199
⚠️ Port exhaustion if >10 servers per context (unlikely)

### Neutral

- Port allocation must be coordinated with platform team
- Documentation must be updated when adding servers

## Implementation

***

### Helm Chart

```yaml
# charts/virons-mcp/values.yaml
servers:
  gitleaks:
    port: 9100
    context: security
  compliance-gate:
    port: 9101
    context: security
  org-governance:
    port: 9110
    context: governance
  # ...
```

### Network Policy

```yaml
# Allow traffic to Security Context
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mcp-security-context
spec:
  podSelector:
    matchLabels:
      context: security
  ingress:
  - from:
    - podSelector: {}
    ports:
    - protocol: TCP
      port: 9100
    - protocol: TCP
      port: 9101
```

### Firewall Rules (AWS Security Group)

```hcl
# Allow MCP server traffic
resource "aws_security_group_rule" "mcp_servers" {
  type              = "ingress"
  from_port         = 9100
  to_port           = 9199
  protocol          = "tcp"
  cidr_blocks       = [var.vpc_cidr]
  security_group_id = aws_security_group.eks_nodes.id
}
```

## Compliance

***

| Regulation | Requirement | Implementation |
|------------|-------------|----------------|
| **BaFin AT 8.1** | Documented change control | Port registry in ADR-001 |
| **DORA Art 11** | Network segmentation | Context-based port ranges |
| **GDPR Art 32** | Security of processing | Firewall rules per context |

## Alternatives Considered

***

### Alternative 1: Dynamic Port Allocation

- **Pros**: Flexible, no port exhaustion
- **Cons**: Hard to audit, firewall complexity
- **Rejected**: Compliance requires predictability

### Alternative 2: Single Port with Path Routing

- **Pros**: Simple firewall rules
- **Cons**: Single point of failure, no context isolation
- **Rejected**: DORA Art 11 requires segmentation

### Alternative 3: Random High Ports (30000+)

- **Pros**: No conflicts
- **Cons**: Hard to remember, no semantic meaning
- **Rejected**: Poor developer experience

## References

***

- [Platform Services Port Allocation](../../../platform-services/docs/architecture/decisions/ADR-XXX-port-allocation.md)
- [DORA Art 11: ICT Risk Management](../../compliance/dora/DORA-ART-11.md)
- [BaFin AT 8.1: Audit Trail](../../compliance/bafin/BAFIN-AT-8.1.md)

## Navigation
← [ADRs Home](README.md)

***

**Last Updated**: 2026-03-05
**Author**: platform@virons.ai
**Reviewers**: security@virons.ai, compliance@virons.ai
