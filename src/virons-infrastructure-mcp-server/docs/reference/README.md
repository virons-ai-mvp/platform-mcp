# Reference Documentation

API reference, changelog, and templates.

## Contents

- [Changelog](changelog.md) - Version history
- [Virons README Template](virons-readme-template.md) - Documentation template

## API Reference

### REST API
- Swagger UI: http://localhost:8080/api/docs
- ReDoc: http://localhost:8080/api/redoc
- OpenAPI: http://localhost:8080/api/openapi.json

### Endpoints

#### Infrastructure
- `POST /api/v1/deploy` - Deploy infrastructure
- `POST /api/v1/destroy` - Destroy infrastructure
- `GET /api/v1/stacks` - List stacks
- `GET /api/v1/info` - Server information

#### Health & Monitoring
- `GET /health/live` - Liveness probe
- `GET /health/ready` - Readiness probe
- `GET /metrics` - Prometheus metrics

## MCP Tools

- `deploy_infrastructure` - Deploy using CDK/CFN/Terraform/IaC
- `destroy_infrastructure` - Destroy infrastructure stack
- `list_stacks` - List deployed stacks

## Version History

See [Changelog](changelog.md) for version history.
