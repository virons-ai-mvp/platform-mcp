# Virons MCP Gateway

**Single entry point for all Virons MCP servers**

## Overview

The MCP Gateway acts as a unified interface to communicate with all Virons MCP servers:
- Infrastructure MCP Server (port 9100)
- Security MCP Server (port 9200)
- Operations MCP Server (port 9300)
- Monitoring MCP Server (port 9400)

## Architecture

```
Client → MCP Gateway (9000) → Infrastructure Server (9100)
                            → Security Server (9200)
                            → Operations Server (9300)
                            → Monitoring Server (9400)
```

## Tools

### Core Gateway Tools
- `route_tool` - Route any tool call to appropriate server
- `list_servers` - List all available MCP servers
- `health_check` - Check health of specific server

### Convenience Tools
- `infrastructure_deploy` - Route to infrastructure server
- `security_scan` - Route to security server
- `operations_execute` - Route to operations server
- `monitoring_query` - Route to monitoring server

## Usage

### Install
```bash
uv pip install -e .
```

### Run
```bash
virons-mcp-gateway
```

### Example
```python
# Route to infrastructure server
result = await route_tool(
    server_name="infrastructure",
    tool_name="deploy_infrastructure",
    tool="cdk",
    stack_name="my-stack"
)

# Check server health
health = await health_check(server_name="infrastructure")

# List all servers
servers = await list_servers()
```

## Configuration

Edit `virons/mcp_gateway/config.py` to configure server endpoints:

```python
GATEWAY_CONFIG = {
    "infrastructure": ServerConfig(
        name="infrastructure",
        url="http://localhost:9100",
        enabled=True,
    ),
    # ... more servers
}
```

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Format code
ruff format .

# Type check
pyright
```

## License

Apache-2.0
