# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-03-07

### Added - Phase 1 Expansion (20 new tools)

**Stack Management (6 tools)**:
- `get_stack_info` - Get detailed stack information
- `get_stack_outputs` - Get stack outputs only
- `get_stack_resources` - List all resources in stack
- `get_stack_events` - Get stack deployment events
- `validate_template` - Validate IaC template
- `update_stack` - Update existing stack

**Resource Management (2 tools)**:
- `list_resources` - List all resources across stacks
- `tag_resource` - Add/update resource tags

**Monitoring & Observability (3 tools)**:
- `get_health_status` - Get infrastructure health
- `get_metrics` - Get infrastructure metrics
- `get_alarms` - Get CloudWatch alarms

**Security & Compliance (3 tools)**:
- `scan_security` - Security scan (IAM, encryption, public access)
- `detect_drift` - Detect configuration drift
- `get_audit_logs` - Get infrastructure audit logs

**Backup & Recovery (2 tools)**:
- `create_backup` - Create infrastructure backup
- `list_backups` - List available backups

**Cost Management (1 tool)**:
- `get_cost_breakdown` - Get cost by service/stack

**Infrastructure Queries (3 tools)**:
- `list_vpcs` - List VPCs
- `list_databases` - List RDS/DynamoDB instances
- `list_instances` - List EC2/ECS/Lambda instances

**New Services**:
- `application/stack_info_service.py`
- `application/resource_service.py`
- `application/monitoring_service.py`
- `application/security_service.py`
- `application/infrastructure_services.py`

**Documentation**:
- `docs/TOOL_INVENTORY.md` - 78 tools planned
- `docs/reference/api-reference-v2.md`
- `docs/diagrams/` - D2 and Mermaid diagrams
- Updated all READMEs with Virons template

### Changed
- Expanded from 3 to 23 tools (667% increase)
- Enhanced DDD architecture
- Updated API documentation

---

## [0.1.0] - 2026-03-04

### Added
- Initial scaffold with compliance baseline
- BaFin MaRisk AT 8.1 audit integration
- GDPR Art 25, 32 compliance hooks
- DORA Art 11 health checks
