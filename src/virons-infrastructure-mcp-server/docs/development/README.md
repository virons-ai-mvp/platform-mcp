# Development Documentation

Development guides, implementation notes, and contribution guidelines.

## Contents

- [Implementation](implementation.md) - Implementation details
- [Implementation Progress](implementation-progress.md) - Progress tracking
- [Project Complete](project-complete.md) - Project status
- [Enhancement Summary](enhancement-summary.md) - Recent changes
- [Contributing](contributing/) - Contribution guidelines
- [Testing](testing/) - Testing guides

## Getting Started

```bash
# Clone and setup
git clone <repo>
cd virons-infrastructure-mcp-server
uv sync

# Run tests
uv run pytest

# Start development server
./scripts/development/start-api.sh
```

## Architecture

- **API Layer**: FastAPI with Swagger UI
- **Application Layer**: Service classes (deploy, list, destroy)
- **Domain Layer**: Business models and logic
- **Infrastructure Layer**: Health, metrics, compliance

## Testing

- Unit tests: `tests/`
- Integration tests: `tests/integration/`
- Coverage: 88% (43/49 tests passing)

## Contributing

See [Contributing](contributing/) for guidelines.
