# MCP Server README Population Plan

## Strategy: Server-by-Server, Layer-by-Layer

### Priority Order
1. **Security MCP** (smallest: 4 tools) - Template validation
2. **Operations MCP** (small: 4 tools) - Pattern replication
3. **Monitoring MCP** (small: 4 tools) - Pattern replication
4. **Gateway** (aggregator: 90 tools) - Integration point
5. **Infrastructure MCP** (largest: 78 tools) - Already complete, verify only

## Phase 1: Security MCP (Validation Phase)

### Files to Create/Update
```
src/virons-security-mcp-server/
├── README.md                                    [UPDATE] Root entry point
├── virons/security_mcp_server/
│   ├── README.md                                [UPDATE] Core implementation
│   ├── application/README.md                    [CREATE] Use cases layer
│   ├── domain/README.md                         [CREATE] Business logic layer
│   └── infrastructure/README.md                 [CREATE] External integrations
├── tests/
│   ├── README.md                                [UPDATE] Test suite overview
│   ├── application/README.md                    [CREATE] Application tests
│   ├── domain/README.md                         [CREATE] Domain tests
│   └── infrastructure/README.md                 [CREATE] Infrastructure tests
└── scripts/
    ├── README.md                                [UPDATE] Scripts overview
    ├── development/README.md                    [CREATE] Dev scripts
    └── operations/README.md                     [CREATE] Ops scripts
```

### Content Sources
- **Port**: 9500
- **Tools**: 4 (scan_secrets, audit_cloudtrail, check_iam_policy, run_compliance_gate)
- **Upstreams**: cloudtrail, iam, well-architected, gitleaks, compliance-gate
- **Tool metadata**: `virons/security_mcp_server/tool_metadata.py`
- **Server code**: `virons/security_mcp_server/server.py`

### Automation Script
```bash
./scripts/populate-security-readmes.sh
```

## Phase 2: Operations MCP (Pattern Replication)

### Files (Same structure as Security)
```
src/virons-operations-mcp-server/
├── README.md                                    [UPDATE]
├── virons/operations_mcp_server/
│   ├── README.md                                [UPDATE]
│   ├── application/README.md                    [CREATE]
│   ├── domain/README.md                         [CREATE]
│   └── infrastructure/README.md                 [CREATE]
├── tests/
│   ├── README.md                                [UPDATE]
│   ├── application/README.md                    [CREATE]
│   ├── domain/README.md                         [CREATE]
│   └── infrastructure/README.md                 [CREATE]
└── scripts/
    ├── README.md                                [UPDATE]
    ├── development/README.md                    [CREATE]
    └── operations/README.md                     [CREATE]
```

### Content Sources
- **Port**: 9510
- **Tools**: 4 (deploy_service, rollback_deployment, scale_service, check_deployment_status)
- **Upstreams**: eks, lambda, ecs, stepfunctions
- **Tool metadata**: `virons/operations_mcp_server/tool_metadata.py`

## Phase 3: Monitoring MCP (Pattern Replication)

### Files (Same structure)
```
src/virons-monitoring-mcp-server/
├── README.md                                    [UPDATE]
├── virons/monitoring_mcp_server/
│   ├── README.md                                [UPDATE]
│   ├── application/README.md                    [CREATE]
│   ├── domain/README.md                         [CREATE]
│   └── infrastructure/README.md                 [CREATE]
├── tests/
│   ├── README.md                                [UPDATE]
│   ├── application/README.md                    [CREATE]
│   ├── domain/README.md                         [CREATE]
│   └── infrastructure/README.md                 [CREATE]
└── scripts/
    ├── README.md                                [UPDATE]
    ├── development/README.md                    [CREATE]
    └── operations/README.md                     [CREATE]
```

### Content Sources
- **Port**: 9520
- **Tools**: 4 (query_metrics, create_dashboard, set_alert, check_system_health)
- **Upstreams**: cloudwatch, prometheus, grafana, elasticsearch
- **Tool metadata**: `virons/monitoring_mcp_server/tool_metadata.py`

## Phase 4: Gateway (Integration Point)

### Files
```
src/virons-mcp-gateway/
├── README.md                                    [UPDATE]
├── virons/mcp_gateway/
│   ├── README.md                                [CREATE]
│   ├── application/README.md                    [CREATE]
│   ├── domain/README.md                         [CREATE]
│   └── infrastructure/README.md                 [CREATE]
└── tests/
    └── README.md                                [CREATE]
```

### Content Sources
- **Port**: 9000
- **Tools**: 90 (aggregated from all backends)
- **Backends**: infrastructure:9100, security:9500, operations:9510, monitoring:9520
- **Code**: `virons/mcp_gateway/server.py`, `domain/gateway.py`, `domain/registry.py`

## Phase 5: Infrastructure MCP (Verification Only)

### Action
- Verify all existing READMEs are complete
- Update if missing sections
- Already has full DDD structure

## Automation Strategy

### 1. Data Extraction Script
```bash
./scripts/extract-server-metadata.sh [server-name]
```
Extracts:
- Tool list from tool_metadata.py
- Upstream servers from server.py
- Port from Dockerfile/docker-compose.yml
- Dependencies from pyproject.toml

### 2. README Generation Script
```bash
./scripts/populate-readme.sh [server-name] [layer] [file-path]
```
Generates README with:
- Extracted metadata
- Template structure
- Navigation links

### 3. Validation Script
```bash
./scripts/validate-readmes.sh [server-name]
```
Checks:
- All required files exist
- All sections populated
- Navigation links valid
- Code examples work

## Execution Plan

### Day 1: Security MCP (2-3 hours)
1. Extract metadata → 15 min
2. Generate 13 READMEs → 30 min
3. Populate content → 60 min
4. Validate & test → 30 min
5. Commit → 15 min

### Day 2: Operations + Monitoring (3-4 hours)
1. Operations MCP → 90 min (pattern replication)
2. Monitoring MCP → 90 min (pattern replication)
3. Validate both → 30 min
4. Commit → 15 min

### Day 3: Gateway (2 hours)
1. Extract metadata → 15 min
2. Generate 6 READMEs → 20 min
3. Populate content → 60 min
4. Validate → 15 min
5. Commit → 10 min

### Day 4: Infrastructure Verification (1 hour)
1. Review existing READMEs → 30 min
2. Update missing sections → 20 min
3. Final validation → 10 min

## Success Criteria

- [ ] All 63 README.md files exist
- [ ] All sections populated with real content
- [ ] All navigation links work
- [ ] All code examples tested
- [ ] All diagrams render correctly
- [ ] Consistent formatting across servers
- [ ] No placeholder text (TODO, FIXME, etc.)

## Commit Strategy

One commit per server:
1. `docs(security-mcp): populate all DDD layer READMEs`
2. `docs(operations-mcp): populate all DDD layer READMEs`
3. `docs(monitoring-mcp): populate all DDD layer READMEs`
4. `docs(gateway): populate all layer READMEs`
5. `docs(infrastructure-mcp): verify and update READMEs`

## Next Action

Start with Security MCP Phase 1:
```bash
./scripts/populate-security-readmes.sh
```
