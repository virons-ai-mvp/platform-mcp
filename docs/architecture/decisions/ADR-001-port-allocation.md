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
| **Security** | 9100-9109 | 10 servers | 2 (gitleaks, compliance-gate) |
| **Governance** | 9110-9119 | 10 servers | 2 (org-governance, workflow-governance) |
| **Operations** | 9120-9129 | 10 servers | 1 (secrets-rotation) |
| **Compliance** | 9130-9139 | 10 servers | 1 (compliance-checklist) |
| **Reserved** | 9140-9199 | 60 servers | Future contexts |

### Port Registry

```yaml
# Security Context
9100: gitleaks
9101: compliance-gate
9102-9109: reserved

# Governance Context
9110: org-governance
9111: workflow-governance
9112-9119: reserved

# Operations Context
9120: secrets-rotation
9121-9129: reserved

# Compliance Context
9130: compliance-checklist
9131-9139: reserved
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
