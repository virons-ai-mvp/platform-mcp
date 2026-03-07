# Operations MCP Server - Application Layer

## Overview

Use cases and orchestration logic for deployment operations. Currently minimal - tools are registered directly in server.py.

## Future Structure

```
application/
├── __init__.py
├── deploy_service.py        # Deployment orchestration
├── rollback_service.py      # Rollback orchestration
├── scale_service.py         # Scaling orchestration
└── status_service.py        # Status aggregation
```

## Responsibilities

- Coordinate deployments across multiple platforms
- Implement deployment strategies (blue-green, canary, rolling)
- Aggregate status from different platforms
- Handle rollback logic and version management

## Example Pattern

```python
class DeployService:
    def __init__(self, eks_client, ecs_client, lambda_client):
        self.eks = eks_client
        self.ecs = ecs_client
        self.lambda_client = lambda_client
    
    async def deploy(self, platform: str, service: str, image: str) -> DeployResult:
        # 1. Select platform client
        client = self._get_client(platform)
        
        # 2. Execute deployment
        result = await client.deploy(service, image)
        
        # 3. Wait for health checks
        await self._wait_for_healthy(client, service)
        
        return result
```

## Navigation

← [Core Implementation](../)
