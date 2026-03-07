# Security MCP - Implementation Plan

## Overview

Apply TDD + DDD pattern from Monitoring MCP to Security MCP.

**Status:** 0/4 tools implemented  
**Estimated Time:** 2-3 hours  
**Pattern:** Infrastructure → Domain → Application → Server

## Tools to Implement

1. **scan_secrets** - Scan repository for secrets (Gitleaks upstream)
2. **audit_cloudtrail** - Query CloudTrail audit logs (CloudTrail upstream)
3. **check_iam_policy** - Validate IAM policies (IAM upstream)
4. **run_compliance_gate** - Run compliance checks (Compliance-gate upstream)

## Upstream Servers

| Upstream | Port | Purpose |
|----------|------|---------|
| Gitleaks | 9100 | Secret scanning |
| Compliance-gate | 9101 | Compliance checks |
| CloudTrail | 9102 | Audit logs |
| IAM | 9103 | Policy validation |

## Implementation Approach

### 4 Iterations (TDD + DDD)

**Iteration 1: Secrets (45 min)**
- Domain: SecretFinding, ScanRequest
- Infrastructure: GitleaksClient
- Application: SecretScanService
- Server: Update scan_secrets()
- Tests: Domain + Application

**Iteration 2: CloudTrail (30 min)**
- Domain: AuditEvent, AuditQuery
- Infrastructure: CloudTrailClient
- Application: AuditService
- Server: Update audit_cloudtrail()
- Tests: Domain + Application

**Iteration 3: IAM (30 min)**
- Domain: IAMPolicy, PolicyIssue
- Infrastructure: IAMClient
- Application: PolicyValidationService
- Server: Update check_iam_policy()
- Tests: Domain + Application

**Iteration 4: Compliance (30 min)**
- Domain: ComplianceResult, GateCheck
- Infrastructure: ComplianceGateClient
- Application: ComplianceService
- Server: Update run_compliance_gate()
- Tests: Domain + Application

## Architecture (DDD Layers)

```
Server Layer (server.py)
    ↓
Application Layer (services)
    ↓
Domain Layer (entities + value objects)
    ↓
Infrastructure Layer (upstream clients)
```

## Success Criteria

- [ ] 4/4 tools implemented
- [ ] 0 TODO comments in server.py
- [ ] All tests passing (target: 40+ tests)
- [ ] Audit trails preserved
- [ ] Correlation IDs propagated
- [ ] Documentation updated

## Reusable Components

From Monitoring MCP:
- UpstreamClient base class (retry, circuit breaker)
- Test patterns
- Documentation structure

## Next Steps

1. Create CHECKLIST.md (detailed tasks)
2. Start Iteration 1 (Secrets)
3. Iterate through all 4 tools
4. Update documentation
5. Commit and verify

**Ready to start?**
