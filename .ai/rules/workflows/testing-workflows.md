# Testing Workflows

## Unit Testing

### Go Services
```bash
go test ./... -race -coverprofile=coverage.out
go tool cover -func=coverage.out  # must be ≥ 80%
```

### Python Services
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

## Integration Testing

Use `testcontainers` (Go) or `testcontainers-python` for:
- Postgres integration tests
- Redis integration tests
- EventBridge mock tests

```go
// Go example
container, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
    ContainerRequest: testcontainers.ContainerRequest{
        Image:        "postgres:16",
        ExposedPorts: []string{"5432/tcp"},
        WaitingFor:   wait.ForListeningPort("5432/tcp"),
    },
    Started: true,
})
```

## Compliance Tests (Mandatory for Forensic Services)

```python
async def test_audit_before_flag(db):
    """BaFin AT 8.1: audit record must precede forensic flag."""
    await calculate_beneish(inputs, db)
    audit = await get_audit_record(db, rule_id="BEN_001")
    flag = await get_forensic_flag(db, rule_id="BEN_001")
    assert audit is not None
    assert audit.created_at <= flag.created_at
```

## ML Gate Tests (Mandatory for ML Services)

```python
def test_ml_gate_zero_without_deterministic_flags():
    score = apply_ml_gate(ml_score=0.9, deterministic_flags=[])
    assert score == 0.0

def test_ml_gate_passes_with_flags():
    score = apply_ml_gate(ml_score=0.9, deterministic_flags=["BEN_001"])
    assert score == 0.9
```

## Code Quality

- `golangci-lint run` (Go)
- `ruff check src/` + `mypy src/` (Python)
- Fix all linting errors before commit
