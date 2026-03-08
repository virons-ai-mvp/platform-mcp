# Architecture Documentation

MCP server architecture, decisions, and governance.

- `ddd/`: Domain-Driven Design
- `decisions/`: ADRs
  - [ADR-001: Port Allocation](decisions/ADR-001-port-allocation.md)
  - [ADR-002: AWS MCP Integration](decisions/ADR-002-aws-mcp-integration.md) ⭐ NEW
- `diagrams/`: System diagrams
- `governance/`: Architecture governance
- `implementation/`: Implementation docs
- `aws-mcp-audit/`: AWS MCP Server Integration Audit ⭐ NEW
  - [Server Catalog](aws-mcp-audit/SERVER-CATALOG.md) - 67 AWS MCP servers
  - [Scoring Framework](aws-mcp-audit/SCORING-FRAMEWORK.md) - Integration prioritization
  - [Server Scores](aws-mcp-audit/SERVER-SCORES.md) - Tier 1/2/3 assignments (33/25/8)
  - [Context Mapping](aws-mcp-audit/CONTEXT-MAPPING.md) - 10 bounded contexts, port allocation
  - [Integration Backlog](aws-mcp-audit/INTEGRATION-BACKLOG.md) - Phase 2/3 roadmap
  - [Implementation Checklist](aws-mcp-audit/IMPLEMENTATION-CHECKLIST.md) - Execution plan
