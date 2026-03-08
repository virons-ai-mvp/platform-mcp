# Quick Start Guide - Virons MCP Gateway

## Installation Complete! ✅

The Virons MCP Gateway now supports MCP protocol and is configured in your Kiro CLI.

## Verify Installation

```bash
# Test the gateway command
cd /Users/amjadalissaalkhalaf/repos/virons-fintech/virons-ai-mvp/platform-mcp/src/virons-mcp-gateway
uv run virons-mcp-gateway --help

# Expected output:
# usage: virons-mcp-gateway [-h] [--port PORT] [--transport {http,stdio,sse,both}]
```

## Using with Kiro CLI

The gateway is already configured in `~/.kiro/settings/mcp.json`. Simply start Kiro CLI:

```bash
kiro-cli chat
```

### Example Commands

Once in Kiro CLI, you can use any of the 90+ tools:

```
You: List all available tools from the gateway

You: What infrastructure deployment tools are available?

You: Deploy a test stack using Terraform

You: Scan for security vulnerabilities

You: Check CloudTrail audit logs
```

## Manual Testing

### Test MCP stdio mode:
```bash
cd src/virons-mcp-gateway
uv run virons-mcp-gateway --transport stdio
# Server will start and wait for stdio input
# Press Ctrl+C to stop
```

### Test HTTP mode (REST API):
```bash
cd src/virons-mcp-gateway
uv run virons-mcp-gateway --transport http --port 9000
# Open http://localhost:9000/docs for Swagger UI
```

### Test dual mode:
```bash
cd src/virons-mcp-gateway
uv run virons-mcp-gateway --transport both --port 9000
# Both HTTP and MCP stdio available
```

## Troubleshooting

### Gateway won't start
```bash
# Check dependencies
cd src/virons-mcp-gateway
uv sync

# Verify virons-common is available
ls ../virons-common/
```

### Backend servers not connecting
```bash
# Verify backend servers are available
uv run virons-infrastructure-mcp-server --help
uv run virons-security-mcp-server --help
uv run virons-operations-mcp-server --help
uv run virons-monitoring-mcp-server --help
```

### Kiro CLI not finding tools
```bash
# Check MCP configuration
cat ~/.kiro/settings/mcp.json

# Verify working directory is correct
cd /Users/amjadalissaalkhalaf/repos/virons-fintech/virons-ai-mvp/platform-mcp/src/virons-mcp-gateway
pwd
```

## Architecture

```
Kiro CLI → Virons Gateway (MCP) → Backend MCP Servers
                                   ├─ Infrastructure (78 tools)
                                   ├─ Security (4 tools)
                                   ├─ Operations (4 tools)
                                   └─ Monitoring (4 tools)
```

## What's Next?

1. **Try it out**: Start Kiro CLI and explore the available tools
2. **Read the docs**: See `README.md` for detailed usage examples
3. **Check implementation**: See `MCP_IMPLEMENTATION.md` for technical details
4. **Run tests**: Execute `test_mcp_gateway.py` to verify functionality

## Support

- **Documentation**: `src/virons-mcp-gateway/README.md`
- **Implementation Details**: `src/virons-mcp-gateway/MCP_IMPLEMENTATION.md`
- **Configuration**: `src/virons-mcp-gateway/virons/mcp_gateway/config/services.json`

---

**Status**: ✅ Ready to use with Kiro CLI!
