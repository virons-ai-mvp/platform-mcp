# Architecture Documentation

System architecture, design patterns, and technical decisions for the Virons Infrastructure MCP Server.

## Contents

- [Model Architecture](model-architecture.md) - Reference architecture for all MCP servers
- [Comprehensive Review](comprehensive-review.md) - Complete server review
- [Diagrams](diagrams/) - Architecture diagrams
- [Decisions](decisions/) - Architecture Decision Records (ADRs)

## Overview

The Virons Infrastructure MCP Server follows a clean 4-layer architecture:

```
API Layer (FastAPI)
    ↓
Application Layer (Services)
    ↓
Domain Layer (Models)
    ↓
Infrastructure Layer (Technical)
```

## Key Patterns

- **Multi-protocol support**: MCP (stdio), HTTP (health), REST API (Swagger)
- **Domain-Driven Design**: Clear separation of concerns
- **Dependency Injection**: Services injected into API layer
- **Repository Pattern**: Upstream registry abstraction

## Documentation

- [Model Architecture](model-architecture.md) - Complete reference
- [Comprehensive Review](comprehensive-review.md) - Implementation review
