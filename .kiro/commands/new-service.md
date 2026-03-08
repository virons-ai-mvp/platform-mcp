# New Service Command

**Description**: Scaffold a new microservice from template with full compliance structure.

**Usage**: `/new-service [name] [namespace] [language]`

**Model**: claude-sonnet-4-5

## Behavior

Invoke the `virons-service-scaffolder` agent to create a new microservice.

The scaffolder will:
1. Check port availability in `.ai/context/repository.json`
2. Copy the appropriate template (Go: `ingestion/corporate-filings/`, Python: `forensic/beneish-calculator/`)
3. Replace all placeholders with the new service name and port
4. Create K8s manifests in `infra/k8s/{namespace}/{service-name}/`
5. Add compliance stubs appropriate for the namespace
6. Update `.ai/context/repository.json` with the new service entry
7. Run compliance-check to verify the scaffold is valid

After scaffolding, implement business logic in `{namespace}/{service-name}/services/`.

## Example

```bash
/new-service transaction-monitor forensic python
```

This creates:
- `forensic/transaction-monitor/` with FastAPI template
- K8s manifests in `infra/k8s/forensic/transaction-monitor/`
- Compliance stubs with `write_audit()` calls
- Entry in `.ai/context/repository.json`
