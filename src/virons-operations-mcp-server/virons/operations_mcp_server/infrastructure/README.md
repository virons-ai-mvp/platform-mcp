# Operations MCP Server - Infrastructure Layer

## Overview

External integrations and technical implementations. Currently minimal - upstream calls are TODO in server.py.

## Future Structure

```
infrastructure/
├── __init__.py
├── clients/
│   ├── eks_client.py           # EKS MCP client
│   ├── lambda_client.py        # Lambda MCP client
│   ├── ecs_client.py           # ECS MCP client
│   └── stepfunctions_client.py # Step Functions MCP client
├── repositories/
│   └── deployment_repository.py # Deployment history persistence
└── adapters/
    └── mcp_adapter.py          # MCP protocol adapter
```

## Responsibilities

- Connect to upstream MCP servers
- Handle MCP protocol communication
- Retry logic and circuit breakers
- Deployment history persistence

## Example Client

```python
class EKSClient:
    def __init__(self, host: str, port: int):
        self.base_url = f"http://{host}:{port}"
    
    async def deploy(self, service: str, image: str, replicas: int):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tools/deploy",
                json={"service": service, "image": image, "replicas": replicas}
            )
            return response.json()
    
    async def get_status(self, service: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/tools/status/{service}")
            return response.json()
```

## Upstreams

| Service | Port | Purpose |
|---------|------|---------|
| eks | 9105 | Kubernetes deployments |
| lambda | 9106 | Serverless functions |
| ecs | 9107 | Container orchestration |
| stepfunctions | 9108 | Workflow orchestration |

## Navigation

← [Core Implementation](../)
