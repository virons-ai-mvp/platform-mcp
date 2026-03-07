# Architecture Diagrams

This directory contains architecture diagrams in multiple formats.

## Formats

### Mermaid (.mmd)
- Renders in GitHub/GitLab markdown
- View/edit: https://mermaid.live
- Embedded in documentation READMEs

### D2 (.d2)
- Modern declarative diagram language
- Render: `d2 file.d2 output.svg`
- Playground: https://play.d2lang.com

## Diagrams

### System Architecture
- `system-overview` - Overall system architecture
- `domain-layer` - Domain layer (DDD)
- `application-layer` - Application layer (DDD)
- `infrastructure-layer` - Infrastructure layer (DDD)

### Operations
- `deployment-verification` - Deployment verification workflow

### Testing
- `test-architecture` - Test suite organization

## Generation

Diagrams are auto-generated from:
```bash
./scripts/development/generate-diagrams.sh
```

## Usage

### Mermaid
```markdown
```mermaid
graph TB
  A --> B
```
```

### D2
```bash
# Render to SVG
d2 docs/diagrams/d2/system-overview.d2 output.svg

# Render to PNG
d2 docs/diagrams/d2/system-overview.d2 output.png
```
