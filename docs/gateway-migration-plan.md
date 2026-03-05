# Gateway Migration Plan

## Current State (platform-services)

Location: `/platform-services/src/interfaces/gateway`

**Architecture**:
- FastAPI HTTP server on port 3000
- Service registry with JSON config
- Middleware: rate limiting, correlation IDs, metrics
- Circuit breaker for resilience
- Health/readiness checks
- Tool routing to backend services

**Files**:
```
gateway/
├── virons/gateway/
│   ├── server.py              # FastAPI app
│   ├── domain/
│   │   ├── gateway.py         # GatewayRouter
│   │   └── registry.py        # ServiceRegistry
│   ├── infrastructure/
│   │   ├── config.py          # Config loader
│   │   ├── metrics.py         # Prometheus metrics
│   │   └── circuit_breaker.py # Circuit breaker
│   └── orchestrator/          # Tool orchestration
├── config/services.json       # Service definitions
└── tests/                     # Full test suite
```

## Target State (platform-mcp)

Location: `/platform-mcp/src/virons-gateway-mcp-server`

**Architecture**:
- FastMCP server (MCP protocol, not HTTP)
- Aggregates other virons MCP servers
- Compliance middleware layer
- Audit trail for all operations (BaFin AT 8.1)
- Data residency enforcement (GDPR Art 25)
- Correlation ID propagation (GDPR Art 32)
- Health monitoring (DORA Art 11)

**Migration Steps**:

### 1. Scaffold Gateway MCP Server
```bash
python3 scripts/scaffold_virons_server.py \
  --name gateway \
  --description "Gateway MCP server that aggregates other MCP servers with compliance middleware" \
  --port 9420 \
  --deps "httpx,mcp-client" \
  --output-dir src
```

### 2. Port Core Components

**From platform-services → platform-mcp**:

- `ServiceRegistry` → `MCPServerRegistry`
  - Change from HTTP services to MCP server connections
  - Use MCP client library instead of httpx
  
- `GatewayRouter` → `MCPGatewayRouter`
  - Route to MCP servers instead of HTTP endpoints
  - Wrap with compliance middleware
  
- Circuit breaker → Keep pattern, adapt for MCP
- Rate limiting → Keep, add per-server limits
- Metrics → Keep Prometheus, add MCP-specific metrics

### 3. Add Compliance Layer

**New components**:

```python
# virons/gateway_mcp_server/compliance_middleware.py
class ComplianceMiddleware:
    """Wraps MCP tool calls with compliance checks."""
    
    async def before_tool_call(self, tool_name: str, params: dict):
        # 1. Generate correlation ID (GDPR Art 32)
        # 2. Enforce data residency (GDPR Art 25)
        # 3. Check authorization
        pass
    
    async def after_tool_call(self, tool_name: str, result: dict):
        # 1. Audit trail (BaFin AT 8.1)
        # 2. Log metrics
        pass
```

### 4. MCP Server Aggregation

**Config format** (replace services.json):

```yaml
# config/mcp-servers.yaml
servers:
  - name: infrastructure
    port: 9300
    namespace: forensic
    tools:
      - list_resources
      - get_resource
  
  - name: development
    port: 9301
    namespace: forensic
    tools:
      - create_environment
      - deploy_service
  
  - name: anomaly-detector
    port: 9420
    namespace: ml
    high_risk: true  # EU AI Act
    model_cards_required: true
```

### 5. Testing Strategy

- Port existing gateway tests
- Add MCP protocol tests
- Add compliance middleware tests
- Integration tests with mock MCP servers

## Benefits of Migration

1. **Protocol Alignment**: Native MCP instead of HTTP translation
2. **Compliance First**: Built-in audit, residency, correlation
3. **Unified Stack**: All servers use same MCP infrastructure
4. **Better Observability**: MCP-native metrics and tracing
5. **Type Safety**: MCP schema validation

## Timeline

- **Phase 1**: Scaffold + port registry (1 day)
- **Phase 2**: Port router + middleware (1 day)
- **Phase 3**: Add compliance layer (1 day)
- **Phase 4**: Testing + integration (1 day)
- **Phase 5**: Documentation + deployment (1 day)

## Decision

**Recommendation**: Migrate gateway to platform-mcp as `virons-gateway-mcp-server`

**Rationale**:
- Gateway is the entry point for all MCP operations
- Compliance must be enforced at the gateway level
- MCP-native protocol is more efficient than HTTP translation
- Aligns with "born compliant" philosophy

## Next Steps

1. Create `virons-gateway-mcp-server` using scaffold
2. Port ServiceRegistry → MCPServerRegistry
3. Port GatewayRouter → MCPGatewayRouter with compliance
4. Add MCP server aggregation logic
5. Write tests
6. Deploy to Kind cluster
