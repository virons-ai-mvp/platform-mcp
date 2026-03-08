# AWS Labs MCP Integration - Action Plan

**Status**: Ready for execution
**Timeline**: 4-6 hours
**Approach**: Pragmatic integration using existing infrastructure patterns

---

## Problem Analysis

**Current State**:
- ✅ 4 Virons MCP servers running (gateway, infrastructure, security, operations, monitoring)
- ✅ All 90 tools have valid schemas and HTTP endpoints
- ⚠️ AWS Labs servers use STDIO transport (not HTTP)
- ⚠️ 10 upstream services missing

**Key Insight**: AWS Labs servers are designed for STDIO (Model Context Protocol standard). Our Virons servers already have MCP client infrastructure that supports STDIO. We don't need HTTP wrappers - we need proper STDIO integration.

---

## Phase 1: Simplify Architecture (30 min)

### Action 1.1: Remove HTTP Wrapper Attempts
```bash
# Clean up failed HTTP wrapper attempts
rm -rf src/awslabs-http-gateway/
rm docker/aws-iac-http.Dockerfile
```

### Action 1.2: Revert docker-compose.yml
```bash
# Remove AWS Labs entries from docker-compose.yml
# We'll run them as subprocess services, not Docker containers
```

**Rationale**: AWS Labs servers are Python packages, not containerized services. Running them as subprocesses via STDIO is the MCP-native approach.

---

## Phase 2: Install AWS Labs Servers as Python Packages (45 min)

### Action 2.1: Create Unified AWS Labs Requirements
```bash
# File: requirements-awslabs.txt
awslabs.aws-iac-mcp-server>=1.0.13
awslabs.cloudtrail-mcp-server>=1.0.0
awslabs.iam-mcp-server>=1.0.0
awslabs.well-architected-security-mcp-server>=1.0.0
awslabs.cloudwatch-mcp-server>=1.0.0
```

### Action 2.2: Update Virons Server Dockerfiles
Add AWS Labs packages to each Virons server that needs upstream connectivity:

**infrastructure-mcp-server/Dockerfile**:
```dockerfile
# Add after main dependencies
COPY requirements-awslabs.txt ./
RUN uv pip install --system -r requirements-awslabs.txt
```

### Action 2.3: Test Installation
```bash
# Verify packages are installable
cd src/awslabs/aws-iac-mcp-server
uv pip install -e .
python -m awslabs.aws_iac_mcp_server --help
```

---

## Phase 3: Update MCP Client for Subprocess STDIO (60 min)

### Action 3.1: Enhance MCPClient to Support Module Execution

**File**: `src/virons-infrastructure-mcp-server/virons/infrastructure_mcp_server/domain/mcp_client.py`

```python
class MCPClient:
    def __init__(
        self,
        command: str,  # e.g., "python" or full path
        args: list[str],  # e.g., ["-m", "awslabs.aws_iac_mcp_server"]
        server_name: str,
        max_retries: int = 3,
    ):
        self.command = command
        self.args = args
        self.server_name = server_name
        self.max_retries = max_retries
        self._session: Optional[ClientSession] = None
        self._connected = False

    async def connect(self) -> None:
        """Establish STDIO connection to subprocess MCP server."""
        try:
            server_params = StdioServerParameters(
                command=self.command,
                args=self.args,
                env=None
            )

            read, write = await stdio_client(server_params)
            self._session = ClientSession(read, write)
            await self._session.__aenter__()
            await self._session.initialize()
            self._connected = True
            logger.info(f"Connected to MCP server: {self.server_name}")
        except Exception as e:
            logger.error(f"Failed to connect to {self.server_name}: {e}")
            raise MCPConnectionError(f"Connection failed: {e}")
```

### Action 3.2: Update UpstreamRegistry Configuration Format

**File**: `src/virons-infrastructure-mcp-server/virons/infrastructure_mcp_server/domain/upstream_registry.py`

```python
class UpstreamRegistry:
    """Registry for managing upstream MCP server connections."""

    def __init__(self, config: Dict[str, Dict[str, Any]]):
        """
        Config format:
        {
            "iac": {
                "command": "python",
                "args": ["-m", "awslabs.aws_iac_mcp_server"],
                "description": "AWS IaC MCP Server"
            }
        }
        """
        self.servers = config
        self._clients: Dict[str, MCPClient] = {}

    async def get_client(self, server_name: str) -> MCPClient:
        """Get or create a connected client for the specified server."""
        if server_name not in self.servers:
            raise UnknownServerError(f"Unknown server: {server_name}")

        if server_name in self._clients:
            return self._clients[server_name]

        config = self.servers[server_name]
        client = MCPClient(
            command=config["command"],
            args=config["args"],
            server_name=server_name,
        )

        await client.connect()
        self._clients[server_name] = client
        logger.info(f"Created and cached client for {server_name}")

        return client
```

---

## Phase 4: Configure Upstream Connections (30 min)

### Action 4.1: Update Infrastructure MCP Server Configuration

**File**: `src/virons-infrastructure-mcp-server/virons/infrastructure_mcp_server/server.py`

```python
# Replace old UPSTREAM_CONFIG (lines 59-66)
UPSTREAM_CONFIG = {
    "iac": {
        "command": "python",
        "args": ["-m", "awslabs.aws_iac_mcp_server"],
        "description": "AWS IaC MCP Server (CDK, CloudFormation, Terraform)"
    }
}
```

### Action 4.2: Update Security MCP Server Configuration

**File**: `src/virons-security-mcp-server/virons/security_mcp_server/server.py`

```python
UPSTREAM_CONFIG = {
    "cloudtrail": {
        "command": "python",
        "args": ["-m", "awslabs.cloudtrail_mcp_server"],
        "description": "AWS CloudTrail MCP Server"
    },
    "iam": {
        "command": "python",
        "args": ["-m", "awslabs.iam_mcp_server"],
        "description": "AWS IAM MCP Server"
    },
    "well_architected": {
        "command": "python",
        "args": ["-m", "awslabs.well_architected_security_mcp_server"],
        "description": "AWS Well-Architected Security MCP Server"
    }
}
```

### Action 4.3: Update Monitoring MCP Server Configuration

**File**: `src/virons-monitoring-mcp-server/virons/monitoring_mcp_server/server.py`

```python
UPSTREAM_CONFIG = {
    "cloudwatch": {
        "command": "python",
        "args": ["-m", "awslabs.cloudwatch_mcp_server"],
        "description": "AWS CloudWatch MCP Server"
    }
}
```

---

## Phase 5: Write Tests (TDD) (60 min)

### Action 5.1: Unit Tests for MCPClient

**File**: `tests/domain/test_mcp_client_subprocess.py`

```python
"""Test MCP client subprocess STDIO connections."""
import pytest
from virons.infrastructure_mcp_server.domain.mcp_client import MCPClient


@pytest.mark.asyncio
async def test_mcp_client_connects_to_subprocess():
    """Test client can connect to subprocess MCP server."""
    client = MCPClient(
        command="python",
        args=["-m", "awslabs.aws_iac_mcp_server"],
        server_name="test-iac"
    )

    await client.connect()
    assert client.is_connected()

    await client.disconnect()
    assert not client.is_connected()


@pytest.mark.asyncio
async def test_mcp_client_lists_tools():
    """Test client can list tools from subprocess server."""
    client = MCPClient(
        command="python",
        args=["-m", "awslabs.aws_iac_mcp_server"],
        server_name="test-iac"
    )

    await client.connect()
    tools = await client.list_tools()

    assert len(tools) > 0
    assert any("cloudformation" in t["name"].lower() for t in tools)

    await client.disconnect()
```

### Action 5.2: Integration Tests

**File**: `tests/integration/test_awslabs_integration.py`

```python
"""Integration tests for AWS Labs upstream servers."""
import pytest
from virons.infrastructure_mcp_server.domain.upstream_registry import UpstreamRegistry


@pytest.mark.asyncio
async def test_infrastructure_connects_to_iac_upstream():
    """Test infrastructure-mcp connects to AWS IaC upstream."""
    config = {
        "iac": {
            "command": "python",
            "args": ["-m", "awslabs.aws_iac_mcp_server"],
            "description": "AWS IaC"
        }
    }

    registry = UpstreamRegistry(config)
    client = await registry.get_client("iac")

    assert client.is_connected()

    tools = await client.list_tools()
    assert len(tools) > 0

    await registry.close_all()


@pytest.mark.asyncio
async def test_security_connects_to_cloudtrail_upstream():
    """Test security-mcp connects to CloudTrail upstream."""
    config = {
        "cloudtrail": {
            "command": "python",
            "args": ["-m", "awslabs.cloudtrail_mcp_server"],
            "description": "AWS CloudTrail"
        }
    }

    registry = UpstreamRegistry(config)
    client = await registry.get_client("cloudtrail")

    assert client.is_connected()
    await registry.close_all()
```

---

## Phase 6: Build and Deploy (45 min)

### Action 6.1: Update Dockerfiles

**infrastructure-mcp-server/Dockerfile**:
```dockerfile
# Add AWS Labs packages
COPY --from=uv /app/.venv /app/.venv

# Install AWS Labs servers
RUN /app/.venv/bin/pip install \
    awslabs.aws-iac-mcp-server>=1.0.13

# Rest of Dockerfile unchanged
```

### Action 6.2: Build Images
```bash
# Build infrastructure-mcp with AWS Labs packages
docker-compose build virons-infrastructure-mcp

# Build security-mcp with AWS Labs packages
docker-compose build virons-security-mcp

# Build monitoring-mcp with AWS Labs packages
docker-compose build virons-monitoring-mcp
```

### Action 6.3: Start Services
```bash
# Start all services
docker-compose up -d

# Wait for health checks
sleep 30

# Verify all services healthy
docker-compose ps
```

---

## Phase 7: Validation (30 min)

### Action 7.1: Run Integration Tests
```bash
# Run AWS Labs integration tests
pytest tests/integration/test_awslabs_integration.py -v

# Run full test suite
pytest tests/ -v --cov
```

### Action 7.2: Manual Verification
```bash
# Test infrastructure-mcp tools
curl -X POST http://localhost:9100/tools/list_stacks \
  -H "Content-Type: application/json" \
  -d '{}'

# Test security-mcp tools
curl -X POST http://localhost:9500/tools/audit_cloudtrail \
  -H "Content-Type: application/json" \
  -d '{}'

# Test monitoring-mcp tools
curl -X POST http://localhost:9520/tools/get_metrics \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Action 7.3: Platform Status Check
```bash
# Run comprehensive platform check
python3 scripts/platform-status.py

# Expected output:
# ✅ All 90 tools callable
# ✅ All upstream services connected
# ✅ Platform 100% operational
```

---

## Phase 8: Documentation (30 min)

### Action 8.1: Update Documentation

**Files to update**:
- `README.md` - Update status badges
- `docs/operations/UPSTREAM-SERVICES.md` - Mark services as deployed
- `docs/domain/tools/TOOL_CATALOG.md` - Update tool availability
- `docs/architecture/UPSTREAM-INTEGRATION.md` - Document STDIO approach

### Action 8.2: Create Troubleshooting Guide

**File**: `docs/operations/AWSLABS-TROUBLESHOOTING.md`

```markdown
# AWS Labs MCP Servers - Troubleshooting

## Common Issues

### Subprocess Connection Fails
**Symptom**: `MCPConnectionError: Connection failed`
**Solution**: Verify AWS Labs package is installed in container
```bash
docker exec virons-infrastructure-mcp python -m awslabs.aws_iac_mcp_server --help
```

### Tools Not Available
**Symptom**: Upstream tools not listed
**Solution**: Check subprocess is running
```bash
docker logs virons-infrastructure-mcp | grep "Connected to MCP server"
```

### AWS Credentials Missing
**Symptom**: AWS API calls fail
**Solution**: Mount AWS credentials in docker-compose.yml
```yaml
volumes:
  - ~/.aws:/root/.aws:ro
```
```

---

## Success Criteria

### Phase 1-4 Complete
- [ ] HTTP wrapper code removed
- [ ] MCPClient supports subprocess STDIO
- [ ] UpstreamRegistry uses new config format
- [ ] All 3 Virons servers configured with upstreams

### Phase 5-6 Complete
- [ ] Unit tests pass (95%+ coverage)
- [ ] Integration tests pass
- [ ] Docker images build successfully
- [ ] All services start and pass health checks

### Phase 7-8 Complete
- [ ] All 90 tools callable via HTTP
- [ ] All upstream connections established
- [ ] Platform status shows 100% operational
- [ ] Documentation updated

---

## Rollback Plan

If integration fails at any phase:

```bash
# Stop all services
docker-compose down

# Revert code changes
git checkout HEAD -- src/virons-*-mcp-server/

# Rebuild original images
docker-compose build

# Restart platform
docker-compose up -d
```

---

## Timeline Summary

| Phase | Duration | Cumulative |
|-------|----------|------------|
| 1. Simplify Architecture | 30 min | 0:30 |
| 2. Install AWS Labs Packages | 45 min | 1:15 |
| 3. Update MCP Client | 60 min | 2:15 |
| 4. Configure Upstreams | 30 min | 2:45 |
| 5. Write Tests (TDD) | 60 min | 3:45 |
| 6. Build and Deploy | 45 min | 4:30 |
| 7. Validation | 30 min | 5:00 |
| 8. Documentation | 30 min | 5:30 |

**Total**: 5.5 hours (with buffer: 6 hours)

---

## Next Steps

1. **Review and approve plan** ✓
2. **Execute Phase 1** - Clean up failed attempts
3. **Execute Phase 2** - Install AWS Labs packages
4. **Execute Phase 3** - Update MCP client
5. **Execute Phase 4** - Configure upstreams
6. **Execute Phase 5** - Write and run tests
7. **Execute Phase 6** - Build and deploy
8. **Execute Phase 7** - Validate integration
9. **Execute Phase 8** - Update documentation

**Ready to begin Phase 1?**
