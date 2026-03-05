# Compliance Reference — virons.common

Regulatory traceability for the Virons AI shared compliance package.

## Regulatory Sources

| Regulation | Official Document | Key Articles | Module |
|---|---|---|---|
| BaFin MaRisk | [MaRisk (BA) 09/2017](https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Rundschreiben/2017/rs_1709_marisk_ba.html) | AT 8.1 (IT risk management), AT 7.2 (audit trail) | `audit.py` |
| GDPR | [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Art 25 (data protection by design), Art 32 (security of processing), Art 35 (DPIA) | `residency.py`, `correlation.py` |
| DORA | [Regulation (EU) 2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554/oj) | Art 6 (ICT risk management), Art 11 (response & recovery), Art 15 (incident management) | `health.py` |
| EU AI Act | [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Art 9 (risk management), Art 11 (technical documentation), Art 14 (human oversight), Art 17 (quality management) | `audit.py` (model card checks in downstream servers) |

## Module → Regulation Mapping

### `audit.py` — BaFin MaRisk AT 8.1

- `write_audit()` implements the immutable audit trail required by AT 8.1
- Calculation audit MUST complete before forensic flags are set (AT 7.2 ordering)
- Structured logging with SHA-256 traceable fields

### `health.py` — DORA Art 11

- Liveness and readiness probes for ICT continuity (Art 11.1)
- Readiness checks validate dependency availability (Art 11.3)

### `correlation.py` — GDPR Art 32

- Correlation ID threading enables full request traceability (Art 32.1.d)
- Context propagation supports audit trail reconstruction

### `residency.py` — GDPR Art 25, Art 32

- Data residency enforcement to `eu-central-1` (Art 25 — data protection by design)
- Rejects processing outside approved regions (Art 32 — security of processing)
