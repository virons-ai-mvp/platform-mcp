# virons.common

Virons AI shared compliance utilities for MCP servers.

Every virons MCP server depends on this package for regulatory-compliant audit logging, health checks, correlation ID threading, and data residency enforcement.

## Compliance

| Regulation | Status | Module | Official Reference |
|---|---|---|---|
| BaFin MaRisk AT 8.1 | ✅ | `audit.py` | [MaRisk (BA) 09/2017](https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Rundschreiben/2017/rs_1709_marisk_ba.html) |
| GDPR Art 32 | ✅ | `residency.py`, `correlation.py` | [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj) |
| DORA Art 11 | ✅ | `health.py` | [Regulation (EU) 2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554/oj) |
| EU AI Act | ✅ | `audit.py` | [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) |

See [COMPLIANCE.md](COMPLIANCE.md) for detailed regulatory traceability.

## Install

```bash
uv add virons.common
```

## Usage

```python
from virons.common.audit import write_audit

audit_id = await write_audit(
    service_name='forensic',
    calculation_type='beneish',
    entity_id='entity-001',
    input_data={'score': 1.0},
    output_data={'flag': True},
)
```

## Development

```bash
cd src/virons-common
uv sync
uv run pytest
```

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
