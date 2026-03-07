# MCP Tool Development Workflow

Complete workflow for developing new MCP tools following TDD and DDD principles.

## Phase 1: Planning

1. **Define tool requirements**
   - Tool name and category
   - Input parameters
   - Expected output
   - Error cases
   - AWS API calls needed

2. **Check existing tools**
   - Review `docs/domain/tools/TOOL_CATALOG.md`
   - Avoid duplication
   - Identify reusable patterns

3. **Select target server**
   - Infrastructure (9100) - AWS resource management
   - Security (9500) - Security scanning and compliance
   - Operations (9510) - Deployment and operations
   - Monitoring (9520) - Metrics and logging

## Phase 2: Test-Driven Development

### 2.1 Write Tests First (TDD)

```python
# tests/test_new_tool.py
import pytest
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_new_tool_success():
    """Test successful tool execution"""
    # Arrange
    mock_client = Mock()
    mock_client.describe_instances.return_value = {...}

    # Act
    result = await new_tool({"param": "value"})

    # Assert
    assert len(result) == 1
    assert "success" in result[0].text

@pytest.mark.asyncio
async def test_new_tool_error_handling():
    """Test error handling"""
    # Test error cases
    pass

@pytest.mark.asyncio
async def test_new_tool_validation():
    """Test parameter validation"""
    # Test validation
    pass
```

### 2.2 Run Tests (Should Fail)

```bash
pytest tests/test_new_tool.py -v
# Expected: FAILED (tool not implemented yet)
```

### 2.3 Implement Tool

```python
# server.py
@server.call_tool()
async def new_tool(
    arguments: dict[str, Any]
) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """
    Tool description

    Args:
        param1 (str): Description of param1
        param2 (str, optional): Description of param2. Defaults to None.

    Returns:
        List of TextContent with tool results

    Example:
        ```python
        result = await new_tool({"param1": "value"})
        ```
    """
    try:
        # Extract parameters
        param1 = arguments.get("param1")
        if not param1:
            raise ValueError("param1 is required")

        # Call AWS API
        client = get_aws_client("service-name")
        response = client.api_call(Param=param1)

        # Format response
        return [TextContent(
            type="text",
            text=json.dumps(response, indent=2)
        )]

    except Exception as e:
        logger.error(f"Error in new_tool: {e}")
        raise
```

### 2.4 Run Tests (Should Pass)

```bash
pytest tests/test_new_tool.py -v
# Expected: PASSED
```

### 2.5 Check Coverage

```bash
pytest tests/test_new_tool.py --cov=virons.infrastructure_mcp_server --cov-report=term-missing
# Target: 95% coverage
```

## Phase 3: Documentation

### 3.1 Update Tool Catalog

Add to `docs/domain/tools/TOOL_CATALOG.md`:

```markdown
### new_tool

**Category**: EC2
**Server**: Infrastructure (9100)
**Status**: ✅ Implemented

Description of what the tool does.

**Parameters**:
- `param1` (str, required): Description
- `param2` (str, optional): Description

**Returns**: JSON with tool results

**Example**:
```json
{
  "param1": "value"
}
```
```

### 3.2 Update Server README

Add tool to server's README.md tool list.

### 3.3 Validate Documentation

```bash
./scripts/validate-tool-docs.sh
# Expected: All checks passed
```

## Phase 4: Quality Checks

### 4.1 Linting

```bash
ruff check src/virons-infrastructure-mcp-server/
ruff format src/virons-infrastructure-mcp-server/
```

### 4.2 Type Checking

```bash
mypy src/virons-infrastructure-mcp-server/
```

### 4.3 Security Scanning

```bash
# Pre-commit hook runs TruffleHog
git add .
git commit -m "feat(infrastructure): add new_tool"
```

## Phase 5: Integration Testing

### 5.1 Rebuild Docker Image

```bash
docker-compose build virons-infrastructure-mcp
```

### 5.2 Restart Services

```bash
docker-compose up -d
```

### 5.3 Test via Gateway

```bash
# Check tool is available
curl http://localhost:9000/tools | jq '.tools[] | select(.name=="new_tool")'

# Test tool execution
curl -X POST http://localhost:9000/call-tool \
  -H "Content-Type: application/json" \
  -d '{
    "server": "infrastructure",
    "tool": "new_tool",
    "arguments": {"param1": "value"}
  }'
```

## Phase 6: Commit and Push

### 6.1 Commit Changes

```bash
git add .
git commit -m "feat(infrastructure): add new_tool for EC2 management

- Implement new_tool with comprehensive error handling
- Add unit and integration tests (95% coverage)
- Update tool catalog and documentation
- Validate with pre-commit hooks"
```

### 6.2 Pre-Push Validation

```bash
# Runs automatically on push
git push origin feature/new-tool
```

Pre-push checks:
- DDD structure validation
- TDD compliance
- Documentation quality
- Forensic services compliance
- ML services compliance
- Code quality
- Port namespace validation

## Checklist

- [ ] Tests written first (TDD)
- [ ] Tests pass with 95% coverage
- [ ] Tool implemented with comprehensive docstring
- [ ] Args section matches function parameters
- [ ] Error handling implemented
- [ ] Tool catalog updated
- [ ] Server README updated
- [ ] Documentation validation passes
- [ ] Linting passes (ruff)
- [ ] Type checking passes (mypy)
- [ ] Security scanning passes (TruffleHog)
- [ ] Docker image rebuilt
- [ ] Integration tests pass
- [ ] Gateway exposes tool
- [ ] Pre-commit hooks pass
- [ ] Pre-push validation passes

## Related Documents

- Tool Documentation Standard: `docs/domain/tools/TOOL_DOCUMENTATION_STANDARD.md`
- Tool Catalog: `docs/domain/tools/TOOL_CATALOG.md`
- Testing Strategy: `docs/development/TESTING-STRATEGY.md`
- DDD Structure: `docs/DDD-STRUCTURE.md`
- Git Hooks: `docs/development/GIT-HOOKS-ACTIVATION.md`
