# Inter-Service Communication

## Synchronous (HTTP/gRPC)

Use HTTP for service-to-service calls within a namespace.

```go
// Go — use context with timeout
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

resp, err := http.NewRequestWithContext(ctx, "POST",
    "http://risk-scorer:9409/score", body)
```

```python
# Python — use httpx async
async with httpx.AsyncClient(timeout=5.0) as client:
    resp = await client.post("http://risk-scorer:9409/score", json=payload)
```

## Asynchronous (EventBridge)

Use EventBridge for cross-namespace events.

### Event Bus
`virons-ingestion-events` — ingestion → forensic

### Event Schema
```json
{
  "source": "virons.ingestion.{source-name}",
  "detail-type": "ArtifactIngested",
  "detail": {
    "artifact_hash": "sha256:...",
    "entity_id": "...",
    "artifact_type": "10-K",
    "s3_key": "raw/..."
  }
}
```

## Service Discovery

Within K8s: `{service-name}.virons-{namespace}.svc.cluster.local:{port}`

Short form (same namespace): `{service-name}:{port}`

## Circuit Breaker

For calls to external services (Bedrock, SEC EDGAR):

```go
import "github.com/sony/gobreaker"

cb := gobreaker.NewCircuitBreaker(gobreaker.Settings{
    MaxRequests: 3,
    Interval:    10 * time.Second,
    Timeout:     30 * time.Second,
})
```

## Blockchain Writes — Always Async

```go
// Never block forensic engine for blockchain writes
go func() {
    if err := ledger.RecordEvidence(context.Background(), evidence); err != nil {
        log.Error().Err(err).Msg("ledger write failed")
    }
}()
```

## Challenge Mode SLA

End-to-end pipeline (ingestion → forensic → ml → blockchain) must complete in <90s.
Monitor with `challenge_mode_duration_seconds` Prometheus metric.
