# Documentation Workflows

## Service README

Every service must have `{namespace}/{service}/README.md`:

```markdown
# {service-name}

**Port**: {port} | **Namespace**: virons-{namespace} | **Language**: {language}

## Purpose
One sentence description.

## API Endpoints
| Method | Path | Description |
|---|---|---|
| GET | /health | Health check |
| POST | /... | ... |

## Configuration
| Env Var | Required | Description |
|---|---|---|
| DATABASE_URL | Yes | Postgres connection string |

## Compliance Notes
- {BaFin/GDPR/DORA/EU AI Act notes specific to this service}

## Running Locally
\`\`\`bash
go run cmd/main.go  # or: uvicorn main:app --reload
\`\`\`
```

## Model Cards (EU AI Act)

Required for `anomaly-detector` and `grandmaster-service`.
Template: `ml/.claude/skills/eu-ai-act-compliance/SKILL.md`
Location: `ml/model-cards/{service-name}.md`

## ADRs (Architecture Decision Records)

For significant decisions, create `docs/adr/{NNNN}-{title}.md`:

```markdown
# ADR-{NNNN}: {Title}

**Status**: Accepted | Superseded | Deprecated
**Date**: YYYY-MM-DD

## Context
Why this decision was needed.

## Decision
What was decided.

## Consequences
Trade-offs and implications.
```

## Changelog

Use conventional commits — changelog auto-generated from commit messages.
