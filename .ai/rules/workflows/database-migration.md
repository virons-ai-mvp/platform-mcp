# Database Migration Workflow

## Tool: golang-migrate (Go) / Alembic (Python)

### Go Services
```bash
# Create migration
migrate create -ext sql -dir migrations -seq {description}

# Apply
migrate -path migrations -database "${DATABASE_URL}" up

# Rollback
migrate -path migrations -database "${DATABASE_URL}" down 1
```

### Python Services
```bash
# Create migration
alembic revision --autogenerate -m "{description}"

# Apply
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Migration Rules

1. **Always backwards-compatible** — never drop columns in the same migration that removes code
2. **Additive first** — add column → deploy code → remove old column (separate PR)
3. **Test migrations** — run up + down in CI
4. **No data migrations in schema migrations** — separate scripts for data backfills

## BaFin AT 8.1 — Audit Tables

`calculation_audit` and `ingestion_log` are **immutable audit tables**:
- No UPDATE or DELETE allowed
- No schema changes that remove columns
- Retention: minimum 7 years

```sql
-- Protect audit tables with RLS
ALTER TABLE calculation_audit ENABLE ROW LEVEL SECURITY;
CREATE POLICY audit_insert_only ON calculation_audit FOR INSERT WITH CHECK (true);
-- No SELECT policy needed — service account has SELECT
-- No UPDATE/DELETE policy — blocked by default
```

## Migration Approval

- Dev: Apply after tests pass
- Staging/Production: Requires human approval + rollback script documented

## Rollback Script

Every migration PR must include a rollback script in the PR description:
```sql
-- Rollback for migration {version}
ALTER TABLE ... DROP COLUMN ...;
```
