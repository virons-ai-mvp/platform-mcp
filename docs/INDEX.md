# Virons MCP Platform Documentation

Complete documentation index for the multi-service MCP platform.

## 📖 Quick Links

- **[Getting Started](getting-started/README.md)** - Quick start guide and onboarding
- **[README](README.md)** - Platform overview
- **[Onboarding](ONBOARDING.md)** - Developer onboarding guide

## 🏗️ Architecture (DDD Structure)

### Domain Layer
- **[Tools](domain/tools/)** - Tool catalog, standards, and documentation
  - [Tool Catalog](domain/tools/TOOL_CATALOG.md) - All 90 tools with comprehensive docs
  - [Documentation Standard](domain/tools/TOOL_DOCUMENTATION_STANDARD.md) - Tool doc guidelines
  - [Documentation Improvements](domain/tools/TOOL_DOCUMENTATION_IMPROVEMENTS.md) - Enhancement summary

- **[Integration](domain/integration/)** - Integration patterns and upstream services
  - [AWS Labs Integration](domain/integration/AWSLABS_INTEGRATION.md)
  - [AWS Labs Deployment Plan](domain/integration/AWSLABS_DEPLOYMENT_PLAN.md)
  - [AWS Labs Quick Reference](domain/integration/AWSLABS_QUICK_REFERENCE.md)
  - [Upstream Integration](domain/integration/UPSTREAM_INTEGRATION.md)
  - [MCP Expansion Plan](domain/integration/MCP_EXPANSION_PLAN.md)
  - [MCP Server Orchestrator Mapping](domain/integration/MCP-SERVER-ORCHESTRATOR-MAPPING.md)

- **[DDD Patterns](architecture/ddd/)** - Domain-Driven Design documentation
  - [Context Map](architecture/ddd/CONTEXT-MAP.md)
  - [DDD Overview](architecture/ddd/README.md)

### Application Layer
- **[Workflows](application/workflows/)** - Business workflows and processes
  - [Workflow Compliance Comparison](application/workflows/WORKFLOW-COMPLIANCE-COMPARISON.md)
  - [Workflow Implementation Summary](application/workflows/WORKFLOW-IMPLEMENTATION-SUMMARY.md)
  - [Repo Workflow Comparison](application/workflows/3-REPO-WORKFLOW-COMPARISON.md)

### Infrastructure Layer
- **[Deployment](infrastructure/deployment/)** - Deployment guides and migration plans
  - [AWS Deployment](infrastructure/deployment/aws-deployment.md)
  - [Gateway Migration Plan](infrastructure/deployment/gateway-migration-plan.md)

- **[AWS Infrastructure](infrastructure/aws/)** - AWS-specific infrastructure
- **[EKS](infrastructure/eks/)** - Kubernetes infrastructure
- **[Foundation](infrastructure/foundation/)** - Base infrastructure
- **[Modules](infrastructure/modules/)** - Reusable infrastructure modules

## 🎯 Core Documentation

### Architecture
- **[Overview](architecture/README.md)** - Architecture documentation index
- **[Design Guidelines](architecture/design-guidelines.md)** - Design principles and patterns
- **[MCP Server Standard](architecture/mcp-server-standard.md)** - Standard for all MCP servers
- **[MCP Servers Overview](architecture/mcp-servers-overview.md)** - All MCP servers catalog
- **[MCP Server Script Implementation](architecture/mcp-server-script-implementation.md)**
- **[Agentic AI Plan](architecture/agentic-ai-plan.md)** - AI agent integration strategy

### Architecture Decisions
- **[ADR Index](architecture/decisions/README.md)** - Architecture Decision Records
- [ADR-001: Port Allocation](architecture/decisions/ADR-001-port-allocation.md)
- [ADR-002: AWS MCP Integration](architecture/decisions/ADR-002-aws-mcp-integration.md)

### AWS MCP Audit
- [Context Mapping](architecture/aws-mcp-audit/CONTEXT-MAPPING.md)
- [Implementation Checklist](architecture/aws-mcp-audit/IMPLEMENTATION-CHECKLIST.md)
- [Integration Backlog](architecture/aws-mcp-audit/INTEGRATION-BACKLOG.md)
- [Platform vs Business Classification](architecture/aws-mcp-audit/PLATFORM-VS-BUSINESS-CLASSIFICATION.md)
- [Scoring Framework](architecture/aws-mcp-audit/SCORING-FRAMEWORK.md)
- [Server Catalog](architecture/aws-mcp-audit/SERVER-CATALOG.md)
- [Server Scores](architecture/aws-mcp-audit/SERVER-SCORES.md)

## 👨‍💻 Development

- **[Developer Guide](development/developer-guide.md)** - Complete development guide
- **[Contributing](development/contributing.md)** - Contribution guidelines
- **[Coding Tips](development/coding-tips.md)** - Best practices and tips
- **[Git Hooks Activation](development/GIT-HOOKS-ACTIVATION.md)** - Pre-push validation setup
- **[Testing](development/testing/)** - Testing guidelines
- **[TDD](development/tdd/)** - Test-Driven Development practices

## 🚀 Operations

- **[Deployment](operations/deployment.md)** - Deployment procedures
- **[Docker Optimization](operations/docker-optimization.md)** - Docker best practices
- **[Runbooks](operations/runbooks/)** - Operational runbooks
  - [MCP Server Outage](operations/runbooks/MCP-SERVER-OUTAGE.md)
  - [Secret Rotation Failure](operations/runbooks/SECRET-ROTATION-FAILURE.md)
- **[Procedures](operations/procedures/)** - Standard operating procedures
- **[Process](operations/process/)** - Process documentation

## 🔒 Security

- **[Security Overview](security/README.md)** - Security documentation index
- **[MCP Security Policies](security/MCP-SECURITY-POLICIES.md)** - Security policies and controls

## ✅ Compliance

- **[Compliance Overview](compliance/README.md)** - Compliance documentation index
- **[BaFin](compliance/bafin/)** - BaFin regulatory compliance
  - [BaFin AT 8.1](compliance/bafin/BAFIN-AT-8.1.md)
- **[DORA](compliance/dora/)** - Digital Operational Resilience Act
  - [DORA Article 11](compliance/dora/DORA-ART-11.md)
- **[GDPR](compliance/gdpr/)** - General Data Protection Regulation
  - [GDPR Articles 25-32](compliance/gdpr/GDPR-ART-25-32.md)
- **[Audits](compliance/audits/)** - Audit reports and evidence
- **[Evidence](compliance/evidence/)** - Compliance evidence
- **[Policies](compliance/policies/)** - Compliance policies
- **[Reports](compliance/reports/)** - Compliance reports

## 📚 Reference

- **[Reference Index](reference/README.md)** - Reference documentation
- **[AWS MCP Audit Summary](reference/aws-mcp-audit-summary.md)**
- **[AWS MCP](reference/aws-mcp/)** - AWS MCP reference
- **[Style Guides](reference/style-guides/)** - Documentation style guides
- **[README Checklist](reference/readme-checklist.md)**
- **[README Completion Report](reference/readme-completion-report.md)**
- **[README Population Plan](reference/readme-population-plan.md)**
- **[Docs Mirror Checklist](reference/docs-mirror-checklist.md)**

## 🏛️ Governance

- **[Governance Overview](governance/README.md)** - Governance documentation
- **[Code of Conduct](governance/code-of-conduct.md)** - Community guidelines

## 🎨 Diagrams

- **[Architecture Diagrams](architecture/diagrams/)** - Visual architecture documentation

## 📝 Document Organization

This documentation follows Domain-Driven Design (DDD) principles:

### Domain Layer (`domain/`)
Core business concepts and rules:
- **tools/** - Tool definitions, catalog, and standards
- **integration/** - Integration patterns and upstream services

### Application Layer (`application/`)
Use cases and workflows:
- **workflows/** - Business workflows and process documentation

### Infrastructure Layer (`infrastructure/`)
Technical implementation details:
- **deployment/** - Deployment guides and procedures
- **aws/** - AWS-specific infrastructure
- **eks/** - Kubernetes infrastructure
- **foundation/** - Base infrastructure components

### Cross-Cutting Concerns
- **architecture/** - System-wide architectural decisions
- **security/** - Security policies and controls
- **compliance/** - Regulatory compliance documentation
- **operations/** - Operational procedures and runbooks
- **development/** - Development guidelines and practices

## 🔍 Finding Documentation

### By Role
- **Developers**: Start with [Developer Guide](development/developer-guide.md)
- **Operators**: See [Operations](operations/README.md)
- **Architects**: Review [Architecture](architecture/README.md)
- **Compliance**: Check [Compliance](compliance/README.md)

### By Task
- **Deploy services**: [Deployment](operations/deployment.md)
- **Add new tool**: [Tool Documentation Standard](domain/tools/TOOL_DOCUMENTATION_STANDARD.md)
- **Integrate upstream**: [Integration](domain/integration/)
- **Troubleshoot**: [Runbooks](operations/runbooks/)

## 📊 Documentation Status

- ✅ Architecture: Complete
- ✅ Development: Complete
- ✅ Operations: Complete
- ✅ Compliance: Complete
- ✅ Tool Documentation: Complete (90/90 tools)
- ✅ DDD Structure: Implemented

## 🤝 Contributing

See [Contributing Guide](development/contributing.md) for documentation contribution guidelines.
