# Ingestion Patterns Skill

**Name**: ingestion-patterns
**Description**: SHA-256 artifact hashing, EventBridge publishing, and idempotency patterns for ingestion services.
**Namespace**: ingestion
**User-invocable**: false

## SHA-256 Artifact Hashing (Mandatory)

Every ingested artifact MUST be hashed before storage.

```go
package ingestion

import (
    "crypto/sha256"
    "encoding/hex"
    "io"
)

func HashArtifact(r io.Reader) (string, []byte, error) {
    h := sha256.New()
    data, err := io.ReadAll(io.TeeReader(r, h))
    if err != nil {
        return "", nil, err
    }
    return hex.EncodeToString(h.Sum(nil)), data, nil
}
```

## Idempotency Pattern

```go
func (s *Service) IngestArtifact(ctx context.Context, artifact Artifact) error {
    hash, data, err := HashArtifact(artifact.Body)
    if err != nil {
        return err
    }

    var existing string
    err = s.db.QueryRowContext(ctx,
        `SELECT id FROM ingestion_log WHERE artifact_hash = $1`, hash,
    ).Scan(&existing)
    if err == nil {
        return nil
    }

    s3Key := fmt.Sprintf("raw/%s/%s/%s", artifact.Source, artifact.EntityID, hash)
    if err := s.s3.PutObject(ctx, s3Key, data); err != nil {
        return fmt.Errorf("s3 put: %w", err)
    }

    _, err = s.db.ExecContext(ctx, `
        INSERT INTO ingestion_log (source, entity_id, artifact_type, artifact_hash, s3_key)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (artifact_hash) DO NOTHING
    `, artifact.Source, artifact.EntityID, artifact.Type, hash, s3Key)

    return s.publishEvent(ctx, hash, artifact)
}
```
