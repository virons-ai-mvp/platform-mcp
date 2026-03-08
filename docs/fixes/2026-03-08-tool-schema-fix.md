# Tool Schema Fix - 2026-03-08

## Issue
All 12 tools from security-mcp, operations-mcp, and monitoring-mcp were returning empty `input_schema: {}` through the gateway, making them unusable by AI agents.

## Root Cause
**Case sensitivity mismatch**: Backend MCP servers return `input_schema` (snake_case) but the gateway was only checking for `inputSchema` (camelCase).

```python
# Before (gateway/domain/registry.py:63)
input_schema=tool.get("inputSchema", {})  # ❌ Returns {} for snake_case keys
```

## Fix
Updated gateway to accept both naming conventions:

```python
# After (gateway/domain/registry.py:63-64)
input_schema = tool.get("inputSchema") or tool.get("input_schema", {})  # ✅ Handles both
```

## Verification

### Before Fix
```bash
$ python3 scripts/sanity-check-tools.py
❌ FAILED - 12 critical issues found
- security-mcp: 4/4 tools broken
- operations-mcp: 4/4 tools broken
- monitoring-mcp: 4/4 tools broken
```

### After Fix
```bash
$ python3 scripts/sanity-check-tools.py
✅ PASSED - All tools valid
- infrastructure-mcp: 78 tools ✅
- security-mcp: 4 tools ✅
- operations-mcp: 4 tools ✅
- monitoring-mcp: 4 tools ✅
```

## Regression Prevention

Added comprehensive test suite in `src/virons-mcp-gateway/tests/test_tool_schemas.py`:
- `test_all_tools_have_valid_schemas()` - Validates all 90 tools
- `test_security_mcp_tools_have_schemas()` - Security-specific validation
- `test_operations_mcp_tools_have_schemas()` - Operations-specific validation
- `test_monitoring_mcp_tools_have_schemas()` - Monitoring-specific validation

All tests pass ✅

## Files Changed
1. `src/virons-mcp-gateway/virons/mcp_gateway/domain/registry.py` - Fixed schema lookup
2. `src/virons-mcp-gateway/tests/test_tool_schemas.py` - Added regression tests
3. `scripts/sanity-check-tools.py` - Created validation script

## Impact
- **Before**: 12 tools (13.3%) unusable
- **After**: 90 tools (100%) functional
- **Zero breaking changes**: Backward compatible with both naming conventions
