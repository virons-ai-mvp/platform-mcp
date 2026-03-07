# MCP Server README.md Checklist

## Template Source
`platform-mcp/src/virons-infrastructure-mcp-server/docs/reference/virons-readme-template.md`

## Required README.md Locations

### Per MCP Server (4 servers × 11 locations = 44 files)

#### Root Level
- [ ] `src/virons-infrastructure-mcp-server/README.md`
- [ ] `src/virons-security-mcp-server/README.md`
- [ ] `src/virons-operations-mcp-server/README.md`
- [ ] `src/virons-monitoring-mcp-server/README.md`

#### DDD Layers (virons/)
- [ ] `src/virons-infrastructure-mcp-server/virons/infrastructure_mcp_server/README.md`
- [ ] `src/virons-infrastructure-mcp-server/virons/infrastructure_mcp_server/application/README.md` ✅
- [ ] `src/virons-infrastructure-mcp-server/virons/infrastructure_mcp_server/domain/README.md` ✅
- [ ] `src/virons-infrastructure-mcp-server/virons/infrastructure_mcp_server/infrastructure/README.md` ✅
- [ ] `src/virons-security-mcp-server/virons/security_mcp_server/README.md`
- [ ] `src/virons-operations-mcp-server/virons/operations_mcp_server/README.md`
- [ ] `src/virons-monitoring-mcp-server/virons/monitoring_mcp_server/README.md`

#### Tests
- [ ] `src/virons-infrastructure-mcp-server/tests/README.md` ✅
- [ ] `src/virons-infrastructure-mcp-server/tests/application/README.md` ✅
- [ ] `src/virons-infrastructure-mcp-server/tests/domain/README.md` ✅
- [ ] `src/virons-infrastructure-mcp-server/tests/infrastructure/README.md` ✅
- [ ] `src/virons-infrastructure-mcp-server/tests/integration/README.md` ✅
- [ ] `src/virons-security-mcp-server/tests/README.md`
- [ ] `src/virons-operations-mcp-server/tests/README.md`
- [ ] `src/virons-monitoring-mcp-server/tests/README.md`

#### Scripts
- [ ] `src/virons-infrastructure-mcp-server/scripts/README.md` ✅
- [ ] `src/virons-infrastructure-mcp-server/scripts/development/README.md` ✅
- [ ] `src/virons-infrastructure-mcp-server/scripts/docker/README.md` ✅
- [ ] `src/virons-infrastructure-mcp-server/scripts/operations/README.md` ✅
- [ ] `src/virons-security-mcp-server/scripts/README.md`
- [ ] `src/virons-operations-mcp-server/scripts/README.md`
- [ ] `src/virons-monitoring-mcp-server/scripts/README.md`

#### Docs (already exist, verify completeness)
- [x] `src/virons-infrastructure-mcp-server/docs/README.md` ✅
- [x] `src/virons-security-mcp-server/docs/README.md` ✅
- [x] `src/virons-operations-mcp-server/docs/README.md` ✅
- [x] `src/virons-monitoring-mcp-server/docs/README.md` ✅

### Gateway
- [ ] `src/virons-mcp-gateway/README.md`
- [ ] `src/virons-mcp-gateway/virons/mcp_gateway/README.md`
- [ ] `src/virons-mcp-gateway/virons/mcp_gateway/application/README.md`
- [ ] `src/virons-mcp-gateway/virons/mcp_gateway/domain/README.md`
- [ ] `src/virons-mcp-gateway/virons/mcp_gateway/infrastructure/README.md`
- [ ] `src/virons-mcp-gateway/tests/README.md`

## Template Sections to Populate

For each README.md, customize these sections:

### 1. Overview
- [ ] Service name (infrastructure/security/operations/monitoring)
- [ ] Purpose (what problem it solves)
- [ ] Audience (who uses it)
- [ ] Status (production/development)
- [ ] Port number
- [ ] Tool count

### 2. Architecture
- [ ] Mermaid diagram showing:
  - API endpoints
  - Upstream MCP servers
  - Data flow
  - Health checks

### 3. Contents
- [ ] Directory structure
- [ ] Key files
- [ ] DDD layers (if applicable)

### 4. Key Features
- [ ] List of tools (link to tool_metadata.py)
- [ ] Gateway pattern compliance
- [ ] Middleware (correlation ID, metrics)
- [ ] Health endpoints

### 5. Usage
- [ ] Docker commands
- [ ] API examples (curl)
- [ ] Tool execution examples

### 6. Dependencies
- [ ] Upstream MCP servers
- [ ] Python packages
- [ ] External services

### 7. Testing
- [ ] Test commands
- [ ] Coverage requirements
- [ ] Test structure

### 8. Metrics & Monitoring
- [ ] Prometheus metrics
- [ ] Health check endpoints
- [ ] Logging configuration

### 9. Security & Compliance
- [ ] EU AI Act (if applicable)
- [ ] BaFin/DORA requirements
- [ ] GDPR compliance
- [ ] Audit logging

### 10. Navigation
- [ ] Links to parent README
- [ ] Links to related docs

## Priority Order

1. **Root READMEs** (4 servers + gateway) - Entry points
2. **virons/ layer READMEs** (5 servers) - Core implementation
3. **tests/ READMEs** (5 servers) - Testing documentation
4. **scripts/ READMEs** (4 servers) - Operational scripts
5. **DDD sublayer READMEs** (application/domain/infrastructure) - Deep dive

## Automation Script

```bash
# Generate all missing READMEs from template
./scripts/generate-readmes.sh

# Verify all READMEs exist
./scripts/verify-readmes.sh
```

## Status Summary

- Infrastructure: 13/24 ✅ (54%)
- Security: 0/11 ❌ (0%)
- Operations: 0/11 ❌ (0%)
- Monitoring: 0/11 ❌ (0%)
- Gateway: 0/6 ❌ (0%)

**Total: 13/63 (21%)**
