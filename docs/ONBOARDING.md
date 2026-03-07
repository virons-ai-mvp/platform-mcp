# Developer Onboarding Guide

## Welcome to Virons MCP Platform! 👋

This guide will get you productive in 30 minutes.

## Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Git
- curl & jq (for testing)

## Quick Start (5 minutes)

```bash
# 1. Clone and navigate
cd platform-mcp

# 2. Install git hooks
./scripts/install-hooks.sh

# 3. Start all services
docker-compose up -d

# 4. Verify services
curl http://localhost:9000/tools | jq '{total: (.tools | length)}'
# Expected: {"total": 90}

# 5. Check health
docker-compose ps
# All services should show "Up"
```

## Architecture Overview (10 minutes)

### Service Topology

```
Gateway (:9000)
├── Infrastructure MCP (:9100) - 78 tools
├── Security MCP (:9500) - 4 tools
├── Operations MCP (:9510) - 4 tools
└── Monitoring MCP (:9520) - 4 tools
```

### DDD Structure

Every service follows Domain-Driven Design:

```
virons/[service]_mcp_server/
├── application/      # Use cases & orchestration
│   └── README.md     # What: Business workflows
├── domain/           # Business logic & entities
│   └── README.md     # Why: Core business rules
├── infrastructure/   # External integrations
│   └── README.md     # How: Technical implementations
└── server.py         # Entry point
```

**Read this first:** Each layer's README explains its purpose and patterns.

### Key Concepts

1. **Gateway Pattern** - All services expose:
   - `GET /tools` - List available tools
   - `GET /health` - Liveness check
   - `GET /ready` - Readiness with dependencies
   - `GET /metrics` - Prometheus metrics
   - `POST /tools/{tool_name}` - Execute tool

2. **Correlation IDs** - Every request gets `x-correlation-id` for tracing

3. **Tool Discovery** - Gateway discovers tools from backends on startup

## Your First Task (15 minutes)

### Option A: Add a New Tool

1. **Choose a service** (start with Security - smallest)
   ```bash
   cd src/virons-security-mcp-server
   cat README.md  # Read service overview
   ```

2. **Understand the structure**
   ```bash
   cat virons/security_mcp_server/application/README.md
   cat virons/security_mcp_server/domain/README.md
   cat virons/security_mcp_server/infrastructure/README.md
   ```

3. **Add tool to server.py**
   ```python
   @mcp.tool()
   async def my_new_tool(param: str) -> str:
       """Tool description for MCP clients."""
       # Implementation
       return result
   ```

4. **Test locally**
   ```bash
   # Start service
   python -m virons.security_mcp_server.server
   
   # In another terminal
   curl http://localhost:9500/tools | jq '.tools[] | select(.name=="my_new_tool")'
   ```

5. **Run validation**
   ```bash
   .git/hooks/pre-push
   # Should pass all checks
   ```

### Option B: Fix Documentation

1. **Find a service with warnings**
   ```bash
   ./scripts/verify-docs.sh
   ```

2. **Fix the issue** (e.g., add missing section)

3. **Verify fix**
   ```bash
   ./scripts/verify-docs.sh
   # Should show fewer warnings
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "docs: fix missing section in X"
   # Pre-push hook runs automatically
   ```

## Development Workflow

### Daily Workflow

```bash
# 1. Pull latest
git pull origin main

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Make changes
# ... edit files ...

# 4. Run tests
pytest tests/

# 5. Verify documentation
./scripts/verify-docs.sh

# 6. Test examples
./scripts/test-examples.sh

# 7. Commit (hook runs automatically)
git add .
git commit -m "feat: add new feature"

# 8. Push (hook runs again)
git push origin feature/my-feature
```

### Pre-Push Hook

Automatically validates:
1. ✅ DDD structure (application/domain/infrastructure)
2. ✅ TDD compliance (tests exist)
3. ✅ Documentation quality (READMEs complete)
4. ⚠️ Forensic compliance (calculation_audit, ML gate)
5. ⚠️ ML compliance (MODEL_CARD.md for EU AI Act)
6. ✅ Code quality (syntax, anti-patterns)
7. ✅ Port namespaces (correct ports)

**Blocks push if:** Critical errors (missing DDD layers, syntax errors)  
**Warns if:** Best practices violated (missing tests, placeholders)

Bypass (emergency only): `git push --no-verify`

## Common Tasks

### Add a New MCP Server

1. **Create structure**
   ```bash
   mkdir -p src/virons-newservice-mcp-server/virons/newservice_mcp_server/{application,domain,infrastructure}
   mkdir -p src/virons-newservice-mcp-server/tests/{application,domain,infrastructure}
   mkdir -p src/virons-newservice-mcp-server/scripts/{development,operations}
   ```

2. **Copy template**
   ```bash
   cp src/virons-security-mcp-server/virons/security_mcp_server/server.py \
      src/virons-newservice-mcp-server/virons/newservice_mcp_server/server.py
   ```

3. **Update port** (use next available in range)
   - Infrastructure: 9100-9199
   - Security: 9500-9509
   - Operations: 9510-9519
   - Monitoring: 9520-9529
   - Forensic: 9300-9415
   - ML: 9420-9424

4. **Add to docker-compose.yml**

5. **Create READMEs** (use existing as template)

6. **Register with gateway** (update services.json)

### Debug a Service

```bash
# View logs
docker-compose logs -f virons-security-mcp

# Restart service
docker-compose restart virons-security-mcp

# Check health
curl http://localhost:9500/health

# Check tools
curl http://localhost:9500/tools | jq

# Execute tool
curl -X POST http://localhost:9500/tools/scan_secrets \
  -H "Content-Type: application/json" \
  -d '{"repo_path": "/tmp/test"}'
```

### Run Tests

```bash
# All tests
pytest

# Specific service
pytest src/virons-security-mcp-server/tests/

# With coverage
pytest --cov=virons --cov-report=html

# Watch mode
pytest-watch
```

## Documentation Standards

### README Structure

Every README must have:
1. `## Overview` - Purpose and audience
2. `## Architecture` or `## Structure` - Organization
3. `## Usage` or `## Tools` - How to use
4. `## Navigation` - Links to parent/child

### Code Comments

```python
# Good: Explains WHY
# Use nonlinear fusion to prevent score saturation
score = 1 - prod(1 - s_i)

# Bad: Explains WHAT (code already shows this)
# Calculate score
score = 1 - prod(1 - s_i)
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat(security): add secret scanning tool
fix(gateway): handle timeout errors
docs(operations): update deployment guide
test(monitoring): add dashboard tests
chore(deps): update prometheus-client
```

## Forensic & ML Services (Advanced)

If working on forensic (:9300-9415) or ML (:9420-9424) services:

### Forensic Rules

1. **Always** call `calculation_audit()` before `forensic_flags`
   ```python
   calculation_audit(transaction)
   forensic_flags = detect_anomalies(transaction)
   ```

2. **ML Gate** - Only use ML if deterministic flags exist
   ```python
   gated_ml = ml_score if len(deterministic_flags) >= 1 else 0.0
   ```

3. **Write Audit** - Call on every write path
   ```python
   def create_transaction(data):
       result = db.insert(data)
       write_audit()  # Required!
       return result
   ```

### ML Compliance (EU AI Act)

High-risk AI systems require:

1. **MODEL_CARD.md** - Document model details
   ```markdown
   # Model Card: Anomaly Detector
   
   ## Model Details
   - Type: Isolation Forest
   - Version: 1.0.0
   - Training Data: 100k transactions
   
   ## Intended Use
   - Detect fraudulent transactions
   
   ## Limitations
   - May have false positives on edge cases
   
   ## Ethical Considerations
   - No PII used in training
   ```

2. **Nonlinear Fusion** - Combine scores properly
   ```python
   # Correct: Prevents score saturation
   combined_score = 1 - prod(1 - s_i for s_i in scores)
   
   # Wrong: Linear combination saturates
   combined_score = sum(scores) / len(scores)
   ```

## Resources

### Documentation
- [Complete Docs Index](../docs/INDEX.md)
- [Architecture Guidelines](../docs/architecture/design-guidelines.md)
- [MCP Server Standard](../docs/architecture/mcp-server-standard.md)
- [Coding Tips](../docs/development/coding-tips.md)

### Scripts
- [Git Hooks](../scripts/hooks/README.md)
- [Verification](../scripts/verify-docs.sh)
- [Testing](../scripts/test-examples.sh)

### External
- [MCP Protocol](https://modelcontextprotocol.io/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Prometheus](https://prometheus.io/docs/)

## Getting Help

1. **Read the README** - Every layer has documentation
2. **Check examples** - Look at existing tools
3. **Run verification** - `./scripts/verify-docs.sh`
4. **Ask the team** - We're here to help!

## Next Steps

After completing this guide:

1. ✅ Read your assigned service's README
2. ✅ Complete "Your First Task" above
3. ✅ Review [Architecture Guidelines](../docs/architecture/design-guidelines.md)
4. ✅ Join team standup
5. ✅ Pick your first real ticket

Welcome to the team! 🚀

## Navigation

← [Platform README](../README.md)  
→ [Architecture](../docs/architecture/)  
→ [Development Guide](../docs/development/developer-guide.md)
