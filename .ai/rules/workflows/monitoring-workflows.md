# Monitoring Workflows

## Metrics — Prometheus

All services expose `/metrics` on their service port.

### Required Metrics (Go)
```go
import "github.com/prometheus/client_golang/prometheus"

var (
    requestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{Name: "http_request_duration_seconds"},
        []string{"method", "path", "status"},
    )
    requestTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{Name: "http_requests_total"},
        []string{"method", "path", "status"},
    )
)
```

### Required Metrics (Python)
```python
from prometheus_client import Counter, Histogram

REQUEST_DURATION = Histogram("http_request_duration_seconds", "...",
                             labelnames=["method", "path", "status"])
REQUEST_TOTAL = Counter("http_requests_total", "...",
                        labelnames=["method", "path", "status"])
```

## Alerts

### Challenge Mode SLA
- Alert if pipeline duration > 90s (DORA Art 11)

### Forensic Audit Gap
- Alert if `forensic_flags` written without preceding `calculation_audit`

### ML Gate Bypass
- Alert if ML score > 0 with zero deterministic flags

### API Audit Gap
- Alert if request not logged to audit table

## Logging

All services use structured JSON logging:

```go
// Go — zerolog
log.Info().
    Str("service", "beneish-calculator").
    Str("entity_id", entityID).
    Float64("m_score", mScore).
    Bool("flag_triggered", flagTriggered).
    Msg("calculation complete")
```

```python
# Python — structlog
log.info("calculation_complete",
         service="beneish-calculator",
         entity_id=entity_id,
         m_score=m_score,
         flag_triggered=flag_triggered)
```

**No PII in logs** — use entity_id, not company name or person name.
