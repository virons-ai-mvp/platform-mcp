# DDD Documentation Structure

## Overview

Documentation is organized following Domain-Driven Design (DDD) principles with clear separation of concerns across layers.

## Layer Structure

```
docs/
├── domain/                 # Domain Layer - Core business concepts
│   ├── tools/             # Tool definitions and standards
│   └── integration/       # Integration patterns and contracts
├── application/           # Application Layer - Use cases and workflows
│   └── workflows/         # Business workflow documentation
├── infrastructure/        # Infrastructure Layer - Technical implementation
│   ├── deployment/        # Deployment guides
│   ├── aws/              # AWS infrastructure
│   ├── eks/              # Kubernetes infrastructure
│   └── foundation/       # Base infrastructure
├── architecture/          # Cross-cutting architectural concerns
├── security/             # Security policies and controls
├── compliance/           # Regulatory compliance
├── operations/           # Operational procedures
└── development/          # Development guidelines
```

## Domain Layer (`domain/`)

**Purpose**: Core business concepts independent of technical implementation

### Tools Domain (`domain/tools/`)
- Tool catalog (90 tools)
- Documentation standards
- Tool improvements and enhancements

### Integration Domain (`domain/integration/`)
- AWS Labs integration
- Upstream service patterns
- MCP expansion plans
- Server orchestration

**Key Principle**: Ubiquitous language - consistent terminology across all docs

## Application Layer (`application/`)

**Purpose**: Orchestrate domain concepts into business workflows

### Workflows (`application/workflows/`)
- Compliance workflows
- Implementation patterns
- Repository workflows

**Key Principle**: Thin orchestration over domain logic

## Infrastructure Layer (`infrastructure/`)

**Purpose**: Technical implementation details

### Deployment (`infrastructure/deployment/`)
- AWS deployment guides
- Gateway migration plans

### Infrastructure Components
- AWS-specific infrastructure
- EKS/Kubernetes setup
- Foundation modules

**Key Principle**: Separate technical concerns from business logic

## Cross-Cutting Concerns

### Architecture (`architecture/`)
- System-wide patterns
- Design guidelines
- MCP server standards
- Architecture decisions (ADRs)
- DDD patterns and context maps

### Security (`security/`)
- Security policies
- MCP security controls

### Compliance (`compliance/`)
- BaFin regulations
- DORA requirements
- GDPR compliance
- Audit evidence

### Operations (`operations/`)
- Deployment procedures
- Docker optimization
- Runbooks
- Standard operating procedures

### Development (`development/`)
- Developer guide
- Contributing guidelines
- Coding tips
- Testing practices
- Git hooks

## Navigation

Each layer has:
- **README.md** - Layer overview and index
- **Subdirectories** - Organized by bounded context
- **Cross-references** - Links to related docs in other layers

## DDD Principles Applied

| Principle | Implementation |
|-----------|----------------|
| **Ubiquitous Language** | Consistent terminology (tool, stack, deployment) |
| **Bounded Contexts** | Clear boundaries: tools, integration, workflows |
| **Layered Architecture** | Domain → Application → Infrastructure |
| **Separation of Concerns** | Business logic separate from technical details |
| **Context Mapping** | Documented in `architecture/ddd/CONTEXT-MAP.md` |

## Finding Documentation

### By Layer
- **Domain concepts**: `domain/`
- **Business workflows**: `application/`
- **Technical details**: `infrastructure/`
- **System design**: `architecture/`

### By Role
- **Developers**: `development/` → `domain/` → `application/`
- **Operators**: `operations/` → `infrastructure/`
- **Architects**: `architecture/` → `domain/`
- **Compliance**: `compliance/` → `application/workflows/`

### By Task
- **Add new tool**: `domain/tools/TOOL_DOCUMENTATION_STANDARD.md`
- **Implement workflow**: `application/workflows/`
- **Deploy service**: `infrastructure/deployment/`
- **Integrate upstream**: `domain/integration/`

## Maintenance

When adding documentation:

1. **Identify the layer**: Domain, Application, or Infrastructure?
2. **Find the bounded context**: Tools, Integration, Workflows, etc.
3. **Follow the template**: Use `docs/reference/virons-readme-template copy.md`
4. **Update indexes**: Add links to layer README and INDEX.md
5. **Cross-reference**: Link to related docs in other layers

## Benefits

- **Clear organization**: Easy to find relevant documentation
- **Separation of concerns**: Business logic separate from technical details
- **Maintainability**: Changes in one layer don't affect others
- **Scalability**: Easy to add new bounded contexts
- **Consistency**: Standard structure across all documentation

## References

- [DDD Context Map](architecture/ddd/CONTEXT-MAP.md)
- [Architecture Guidelines](architecture/design-guidelines.md)
- [Documentation Index](INDEX.md)
