# MCP Architecture - Correct Implementation

## Problem Identified

**MCP servers use stdio protocol, not HTTP**. They cannot run as standalone HTTP containers.

## Correct Architecture

```
HTTP Client
    ↓
virons-mcp-gateway (HTTP → MCP stdio)
    ↓ (invokes via subprocess/stdio)
virons-infrastructure-mcp (MCP stdio server)
    ↓ (invokes via subprocess/stdio)
eks-mcp-server (MCP stdio server)
```

## Implementation Options

### Option 1: Gateway Invokes Orchestrators via Subprocess ✅ RECOMMENDED
- Gateway is HTTP server
- Gateway spawns orchestrator processes and communicates via stdio
- Orchestrators spawn awslabs processes and communicate via stdio
- **Deploy**: 1 container (gateway only)

### Option 2: Orchestrators as HTTP Wrappers
- Each orchestrator wraps MCP stdio with HTTP endpoint
- Orchestrators spawn awslabs processes via stdio
- **Deploy**: 10 containers (1 gateway + 9 orchestrators)

### Option 3: All-in-One Gateway
- Gateway directly invokes awslabs servers
- No separate orchestrator layer
- **Deploy**: 1 container (gateway only)

## Recommended: Option 1

**Why**: Simplest deployment, follows MCP protocol correctly, gateway already handles HTTP → stdio conversion.

**Implementation**:
1. Gateway config lists 9 orchestrators with their stdio commands
2. Gateway spawns orchestrator subprocess when tool is called
3. Orchestrator spawns awslabs subprocess when needed
4. All communication via stdio pipes

## Next Steps

1. Update gateway to spawn orchestrators as subprocesses
2. Test gateway → orchestrator → awslabs flow
3. Deploy single gateway container
4. Remove docker-compose.orchestrators.yml (not needed)

## Files to Update

1. `virons-mcp-gateway/virons/mcp_gateway/config/services.json` - Add stdio commands
2. `virons-mcp-gateway/virons/mcp_gateway/domain/gateway.py` - Add subprocess invocation
3. Test with: `curl -X POST http://localhost:9000/tools/call -d '{"name": "list_kubernetes_clusters", "arguments": {}}'`
