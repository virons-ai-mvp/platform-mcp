# Compliance Reference — virons-security-mcp-server

Regulatory traceability for the Virons AI security MCP server.

## Regulatory Sources

| Regulation | Official Document | Key Articles | Implementation |
|---|---|---|---|
| BaFin MaRisk | [MaRisk (BA) 09/2017](https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Rundschreiben/2017/rs_1709_marisk_ba.html) | AT 8.1, AT 7.2 | `compliance.py` → `virons.common.audit` |
| GDPR | [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Art 25, Art 32, Art 35 | `compliance.py` → `virons.common.residency`, `correlation` |
| DORA | [Regulation (EU) 2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554/oj) | Art 6, Art 11, Art 15 | `compliance.py` → `virons.common.health` |
| EU AI Act | [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Art 9, Art 11, Art 14, Art 17 | Model card validation (if high-risk) |

## Compliance Hooks

### BaFin MaRisk AT 8.1 — Audit Trail

Every write operation MUST call `virons.common.write_audit()` before returning:

```python
from virons.common import write_audit

audit_id = await write_audit(
    service_name='virons-security-mcp-server',
    calculation_type='operation_name',
    entity_id=entity_id,
    input_data={'key': 'value'},
    output_data={'result': 'value'},
)
```

### GDPR Art 25, 32 — Data Protection

- **Residency**: All data MUST reside in `eu-central-1` (enforced by `virons.common.enforce_region()`)
- **Correlation**: All requests MUST have correlation IDs (via `virons.common.CorrelationContext`)

### DORA Art 11 — Health Monitoring

- **Liveness**: `/health/live` endpoint via `virons.common.HealthCheck().liveness()`
- **Readiness**: `/health/ready` endpoint via `virons.common.HealthCheck().readiness()`

### EU AI Act — High-Risk Systems

If this server is classified as high-risk (Art 6), ensure:
- Model cards exist in `models/` directory
- Technical documentation per Art 11
- Human oversight mechanisms per Art 14
