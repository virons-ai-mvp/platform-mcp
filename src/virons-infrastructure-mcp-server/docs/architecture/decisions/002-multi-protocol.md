# ADR 002: Multi-Protocol Transport Support

**Status**: Accepted
**Date**: 2026-03-07
**Deciders**: Platform Team
**Context**: Need to support multiple transport protocols

## Context and Problem Statement

Different use cases require different transport protocols:
- AI agents need MCP protocol (stdio)
- Kubernetes needs HTTP health checks
- Human operators need REST API with Swagger UI
- External systems need REST API integration

How do we support all these protocols in a single server?

## Decision Drivers

- Support AI agents (MCP stdio)
- Support Kubernetes (HTTP health)
- Support human operators (REST API)
- Maintain single codebase
- Follow DDD architecture
- Enable easy protocol selection

## Considered Options

1. **Single server with mode selection** - CLI flag to choose protocol
2. **Separate servers** - Different binaries for each protocol
3. **Always run all protocols** - Listen on multiple ports
4. **Protocol auto-detection** - Detect protocol from request

## Decision Outcome

Chosen option: **Single server with mode selection**

### Rationale

- Single codebase, easier maintenance
- Clear protocol selection via CLI
- Efficient resource usage (only run what's needed)
- Flexible deployment options

### Implementation

```python
parser.add_argument(
    "--transport",
    choices=["stdio", "http", "api"],
    default="stdio",
    help="Transport protocol"
)

if args.transport == "api":
    # Full REST API with Swagger
    uvicorn.run(app, host="0.0.0.0", port=args.port)
elif args.transport == "http":
    # Health checks only (K8s)
    HTTPServer(("0.0.0.0", args.port), HealthHandler)
elif args.transport == "stdio":
    # MCP protocol
    mcp.run()
```

## Positive Consequences

- ✅ Single binary, multiple modes
- ✅ Clear protocol selection
- ✅ Efficient resource usage
- ✅ Easy to test each mode
- ✅ Flexible deployment
- ✅ Shared business logic

## Negative Consequences

- ➖ Need to test all modes
- ➖ CLI complexity
- ➖ Documentation overhead

## Protocol Details

### stdio Mode (MCP)
**Use Case**: AI agents, CLI clients
**Port**: stdin/stdout
**Format**: JSON-RPC
**Features**: Full MCP tools

```bash
virons-infrastructure-mcp-server --transport stdio
```

### http Mode (Health)
**Use Case**: Kubernetes probes
**Port**: 8080 (configurable)
**Format**: HTTP/JSON
**Features**: Health checks, metrics only

```bash
virons-infrastructure-mcp-server --transport http --port 8080
```

### api Mode (REST)
**Use Case**: Human operators, external systems
**Port**: 8080 (configurable)
**Format**: HTTP/JSON
**Features**: Full REST API, Swagger UI, health, metrics

```bash
virons-infrastructure-mcp-server --transport api --port 8080
```

## Deployment Patterns

### Kubernetes (http mode)
```yaml
containers:
- name: virons-infrastructure
  args: ["--transport", "http", "--port", "8080"]
  ports:
  - containerPort: 8080
  livenessProbe:
    httpGet:
      path: /health/live
      port: 8080
```

### Development (api mode)
```bash
./scripts/development/start-api.sh
# Opens Swagger UI at http://localhost:8080/api/docs
```

### AI Agent (stdio mode)
```json
{
  "mcpServers": {
    "virons-infrastructure": {
      "command": "virons-infrastructure-mcp-server",
      "args": ["--transport", "stdio"]
    }
  }
}
```

## Pros and Cons of the Options

### Single server with mode selection ✅
- ✅ Single codebase
- ✅ Shared logic
- ✅ Easy maintenance
- ✅ Flexible deployment
- ➖ Need to test all modes

### Separate servers
- ✅ Clear separation
- ✅ Independent deployment
- ➖ Code duplication
- ➖ Maintenance overhead
- ➖ Multiple binaries

### Always run all protocols
- ✅ Always available
- ➖ Resource waste
- ➖ Port conflicts
- ➖ Security concerns

### Protocol auto-detection
- ✅ Automatic
- ➖ Complex logic
- ➖ Error-prone
- ➖ Hard to debug

## Migration Path

Existing deployments can migrate gradually:
1. Update to new version
2. Add `--transport` flag to deployment
3. Test each mode independently
4. Roll out to production

## Links

- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Kubernetes Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
