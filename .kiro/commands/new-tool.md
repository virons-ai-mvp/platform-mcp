# /new-tool - Create New MCP Tool

Scaffold a new MCP tool with proper structure, documentation, and tests.

## Usage

```
/new-tool [server] [tool-name] [category]
```

## Arguments

- `server` - MCP server name (infrastructure, security, operations, monitoring)
- `tool-name` - Tool name in snake_case (e.g., `list_ec2_instances`)
- `category` - Tool category (e.g., EC2, Lambda, S3, IAM, Monitoring)

## Example

```
/new-tool infrastructure list_ecs_tasks ECS
```

## What It Does

1. **Creates tool function** in `src/virons-{server}-mcp-server/virons/{server}_mcp_server/server.py`
   - Proper async function signature
   - Comprehensive docstring with Args section
   - Error handling
   - Type hints

2. **Creates test file** in `src/virons-{server}-mcp-server/tests/test_{tool_name}.py`
   - Unit tests
   - Integration tests
   - Mock AWS responses
   - 95% coverage target

3. **Updates documentation**
   - Adds tool to `docs/domain/tools/TOOL_CATALOG.md`
   - Updates server README
   - Adds example usage

4. **Validates**
   - Runs `./scripts/validate-tool-docs.sh`
   - Runs `ruff check` and `ruff format`
   - Runs `pytest` for new tests

## Template

```python
@server.call_tool()
async def {tool_name}(
    arguments: dict[str, Any]
) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """
    {Tool description}

    Args:
        param1 (str): Description of param1
        param2 (str, optional): Description of param2. Defaults to None.

    Returns:
        List of TextContent with tool results

    Example:
        ```python
        result = await {tool_name}({{"param1": "value"}})
        ```
    """
    try:
        # Implementation
        pass
    except Exception as e:
        logger.error(f"Error in {tool_name}: {{e}}")
        raise
```

## Checklist

- [ ] Tool function created with comprehensive docstring
- [ ] Args section matches function parameters
- [ ] Test file created with unit and integration tests
- [ ] Documentation updated (TOOL_CATALOG.md, server README)
- [ ] Validation passes (`./scripts/validate-tool-docs.sh`)
- [ ] Linting passes (`ruff check`)
- [ ] Tests pass (`pytest`)
- [ ] Pre-commit hooks pass

## Related

- Tool Documentation Standard: `docs/domain/tools/TOOL_DOCUMENTATION_STANDARD.md`
- Tool Catalog: `docs/domain/tools/TOOL_CATALOG.md`
- Testing Strategy: `docs/development/TESTING-STRATEGY.md`
