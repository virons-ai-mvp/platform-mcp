# Kiro Auto-Load Configuration

## Always Loaded (~10KB total)

**Core Context**:
- `.kiro/steering/project.md` (3KB) — MCP server catalog, tool counts, compliance coordinates, quick commands
- `README.md` (1KB) — repo overview
- `docs/INDEX.md` (2KB) — documentation index
- `docs/DDD-STRUCTURE.md` (2KB) — DDD architecture guide
- `docs/domain/README.md` (1KB) — domain layer overview
- `docs/application/README.md` (1KB) — application layer overview

## Load On-Demand

**Documentation** (load when task requires it):
- `docs/domain/tools/TOOL_CATALOG.md` — Complete tool catalog
- `docs/domain/tools/TOOL_DOCUMENTATION_STANDARD.md` — Tool documentation standard
- `docs/domain/tools/TOOL_DOCUMENTATION_IMPROVEMENTS.md` — Tool documentation improvements
- `docs/domain/integration/UPSTREAM_INTEGRATION.md` — AWS Labs integration
- `docs/domain/integration/MCP_EXPANSION_PLAN.md` — MCP expansion plan
- `docs/application/workflows/WORKFLOW-*.md` — Workflow documentation
- `docs/infrastructure/deployment/aws-deployment.md` — AWS deployment guide
- `docs/infrastructure/deployment/gateway-migration-plan.md` — Gateway migration plan

**Development** (load when making changes):
- `docs/development/GIT-HOOKS-ACTIVATION.md` — Git hooks setup
- `scripts/validate-tool-docs.sh` — Tool documentation validation
- `scripts/generate-tool-docs.py` — Tool documentation generation
- `scripts/enhance-tool-descriptions.py` — Tool description enhancement
- `scripts/update-docstrings.py` — Docstring updates

**Compliance** (load when validating):
- `.kiro/steering/compliance.md` — Regulatory requirements
- `docs/compliance/BAFIN-COMPLIANCE.md` — BaFin requirements
- `docs/compliance/GDPR-COMPLIANCE.md` — GDPR requirements
- `docs/compliance/DORA-COMPLIANCE.md` — DORA requirements

**Testing** (load when writing tests):
- `docs/development/TESTING-STRATEGY.md` — Testing strategy
- `src/virons-infrastructure-mcp-server/tests/` — Test examples

**Server-Specific** (load when working on specific server):
- `src/virons-infrastructure-mcp-server/README.md` — Infrastructure server docs
- `src/virons-security-mcp-server/README.md` — Security server docs
- `src/virons-operations-mcp-server/README.md` — Operations server docs
- `src/virons-monitoring-mcp-server/README.md` — Monitoring server docs
- `src/virons-mcp-gateway/README.md` — Gateway docs

## Context Budget

- Auto-load target: ≤10KB
- Remaining for task context: ~190KB
- Server-specific docs load lazily (only when editing files in that server)
- Tool documentation loads on-demand (only when working with specific tools)

## File Patterns

**Auto-load when editing**:
- `src/virons-*-mcp-server/virons/*/server.py` → Load server README + tool catalog
- `src/virons-*-mcp-server/tests/` → Load testing strategy
- `docs/**/*.md` → Load DDD structure guide
- `scripts/*.py` → Load development docs

**Never auto-load** (too large):
- `uv.lock`
- `*.pyc`, `__pycache__/`
- `.venv/`, `node_modules/`
- `.pytest_cache/`, `.ruff_cache/`
