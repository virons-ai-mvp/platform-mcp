# MCP Servers Expansion Plan

## Current State

| Server | Current Tools | Should Have | Gap |
|--------|--------------|-------------|-----|
| Monitoring | 4 | 15 | 11 missing |
| Security | 4 | 18 | 14 missing |
| Operations | 4 | 25 | 21 missing |
| **Total** | **12** | **58** | **46 missing** |

## Problem

We only implemented 4 "orchestrator" tools per server, but the upstream AWS MCP servers provide 50+ tools. We're not exposing the full AWS API surface.

## Solution Options

### Option 1: Expand Each MCP Server (Recommended)

Add all missing tools to properly expose upstream capabilities.

**Pros:**
- Complete AWS API coverage
- Proper orchestration layer
- Maintains DDD architecture

**Cons:**
- 46 more tools to implement (~20-30 hours)
- Large codebase

### Option 2: Pass-Through Proxy Pattern

Create a generic proxy that forwards ALL upstream tools automatically.

**Pros:**
- Minimal code (~2 hours)
- Automatic coverage of all upstream tools
- Easy to maintain

**Cons:**
- Less control over orchestration
- Harder to add business logic per tool

### Option 3: Hybrid Approach (RECOMMENDED)

- **Core tools:** Implement with full DDD (current 12 tools)
- **Extended tools:** Use pass-through proxy for remaining tools
- **Add orchestration:** Only when business logic needed

**Pros:**
- Best of both worlds
- Fast implementation (~4-6 hours)
- Extensible

**Cons:**
- Mixed architecture (acceptable)

## Recommended: Option 3 - Hybrid Approach

### Phase 1: Add Pass-Through Proxy (2 hours)

Create generic proxy in each MCP server:

```python
# virons/monitoring_mcp_server/proxy.py
class UpstreamProxy:
    """Generic proxy for upstream tools."""
    
    async def call_upstream(self, upstream: str, tool: str, args: dict):
        """Forward call to upstream MCP server."""
        client = self._get_client(upstream)
        return await client.call_tool(tool, args)
```

Register all upstream tools dynamically:

```python
# Auto-discover and register all upstream tools
for upstream in ["cloudwatch", "prometheus", "grafana"]:
    tools = await discover_tools(upstream)
    for tool in tools:
        register_proxy_tool(tool, upstream)
```

### Phase 2: Expand Core Tools (4-6 hours)

Add high-value tools with business logic:

**Monitoring MCP (+8 tools):**
- put_metric_data
- list_metrics
- describe_alarms
- delete_alarms
- update_dashboard
- delete_dashboard
- create_log_group
- put_log_events

**Security MCP (+10 tools):**
- simulate_principal_policy
- list_policies
- create_policy
- attach_policy
- get_role
- create_role
- scan_uncommitted (gitleaks)
- get_trail_status
- start_logging
- stop_logging

**Operations MCP (+12 tools):**
- describe_instances
- start_instances
- stop_instances
- invoke_function
- list_functions
- list_buckets
- get_object
- put_object
- list_clusters
- describe_services
- update_service
- create_function

### Phase 3: Documentation (1 hour)

Update tool_metadata.py with all tools.

## Implementation Priority

1. **Immediate:** Add pass-through proxy (2 hours)
   - Gives instant access to all 58 tools
   - Minimal code

2. **Short-term:** Expand core tools (4-6 hours)
   - Add business logic where needed
   - Maintain DDD for important operations

3. **Long-term:** Migrate proxy tools to DDD
   - As business logic requirements emerge
   - Gradual improvement

## Estimated Time

- Option 1 (Full expansion): 20-30 hours
- Option 2 (Proxy only): 2 hours
- **Option 3 (Hybrid): 6-8 hours** ✅

## Decision

Proceed with **Option 3 (Hybrid)**?

This gives us:
- ✅ Immediate access to all 58 tools (via proxy)
- ✅ Proper DDD for core 12 tools (already done)
- ✅ Ability to add orchestration incrementally
- ✅ Fast implementation (6-8 hours total)
