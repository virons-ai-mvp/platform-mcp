# API Reference v2.0

**Version**: 2.0.0 (Phase 1)
**Last Updated**: 2026-03-07
**Total Tools**: 23

## MCP Tools (23)

### Core Operations (3)

**deploy_infrastructure** - Deploy infrastructure stack
**list_stacks** - List deployed stacks
**destroy_infrastructure** - Destroy stack

### Stack Management (6)

**get_stack_info** - Get detailed stack information
**get_stack_outputs** - Get stack outputs
**get_stack_resources** - List stack resources
**get_stack_events** - Get stack events
**validate_template** - Validate template
**update_stack** - Update existing stack

### Resource Management (2)

**list_resources** - List all resources
**tag_resource** - Tag resource

### Monitoring (3)

**get_health_status** - Get health status
**get_metrics** - Get metrics
**get_alarms** - Get alarms

### Security (3)

**scan_security** - Security scan
**detect_drift** - Detect drift
**get_audit_logs** - Get audit logs

### Backup (2)

**create_backup** - Create backup
**list_backups** - List backups

### Cost (1)

**get_cost_breakdown** - Get cost breakdown

### Infrastructure (3)

**list_vpcs** - List VPCs
**list_databases** - List databases
**list_instances** - List instances

## Tool Details

All tools accept `tool` parameter: `cdk|cfn|terraform|iac`

See full documentation: [docs/reference/api-reference-full.md](./api-reference-full.md)

## REST API

- `POST /api/deploy` - Deploy stack
- `GET /api/stacks` - List stacks
- `POST /api/destroy` - Destroy stack
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /api/docs` - Swagger UI

## Compliance

- BaFin MaRisk AT 8.1 (10-year audit)
- GDPR Article 32 (encryption)
- DORA Article 11 (ICT risk)
- EU AI Act Article 9 (high-risk AI)
