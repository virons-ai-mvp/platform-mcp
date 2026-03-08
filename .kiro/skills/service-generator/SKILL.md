# Service Generator Skill

**Name**: service-generator
**Description**: Generate a new microservice from template — Go or Python, with full compliance structure including health endpoints, metrics, Dockerfile, K8s manifests, and namespace-appropriate compliance stubs.
**Arguments**: `[service-name] [namespace] [language] [port]`
**User-invocable**: true

## Steps

1. **Check port availability**
   - Read `.ai/context/repository.json`
   - Verify port is not already assigned
   - Suggest next available port if conflict

2. **Copy template**
   - Go → `ingestion/corporate-filings/` as base
   - Python → `forensic/beneish-calculator/` as base

3. **Replace placeholders**
   - Service name throughout all files
   - Port number in configs, manifests, Dockerfile
   - Module paths and imports

4. **Create K8s manifests**
   - `infra/k8s/{namespace}/{service-name}/deployment.yaml`
   - `infra/k8s/{namespace}/{service-name}/service.yaml`
   - `infra/k8s/{namespace}/{service-name}/hpa.yaml`
   - `infra/k8s/{namespace}/{service-name}/pdb.yaml`

5. **Add compliance stubs**
   - `forensic/` → add `write_audit()` import and stub call
   - `ml/` → create `ml/model-cards/{service-name}.md`
   - All → health endpoints at `/health/live`, `/health/ready`, `/metrics`

6. **Update repository.json**
   - Add service entry with name, port, language, namespace
   - Set status: "scaffolded"

7. **Verify scaffold**
   - Run basic linting
   - Check all required files present

## Output

```
✅ Service scaffolded: {service-name}
   Port: {port}
   Namespace: {namespace}
   Language: {language}
   Files created: {count}

Next steps:
1. Implement business logic in {namespace}/{service-name}/services/
2. Run: make test SERVICE={service-name}
3. Run: /compliance-audit {namespace}/{service-name}
```

## Example

```bash
service-generator transaction-monitor forensic python 9408
```
