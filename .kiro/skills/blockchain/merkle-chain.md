# Merkle Chain Pattern

**Name**: merkle-chain
**Description**: SHA-256 Merkle chain for forensic ledger. Async write only.
**Namespace**: blockchain
**User-invocable**: false

## Chain Hash Function

```go
package ledger

import (
    "crypto/sha256"
    "encoding/hex"
    "fmt"
)

func ChainHash(payloadHash, prevHash string) string {
    combined := fmt.Sprintf("%s%s", payloadHash, prevHash)
    h := sha256.Sum256([]byte(combined))
    return hex.EncodeToString(h[:])
}

func PayloadHash(payload []byte) string {
    h := sha256.Sum256(payload)
    return hex.EncodeToString(h[:])
}
```

## Record Evidence (Async Only)

```go
func (l *Ledger) RecordEvidence(ctx context.Context, e Evidence) error {
    var prevHash string
    err := l.db.QueryRowContext(ctx,
        `SELECT chain_hash FROM evidence_chain ORDER BY created_at DESC LIMIT 1`,
    ).Scan(&prevHash)
    if err == sql.ErrNoRows {
        prevHash = "genesis"
    } else if err != nil {
        return fmt.Errorf("get prev hash: %w", err)
    }

    payload, _ := json.Marshal(e)
    ph := PayloadHash(payload)
    ch := ChainHash(ph, prevHash)

    _, err = l.db.ExecContext(ctx, `
        INSERT INTO evidence_chain (evidence_id, payload_hash, prev_hash, chain_hash)
        VALUES ($1, $2, $3, $4)
    `, e.ID, ph, prevHash, ch)
    return err
}
```

## Caller Pattern (Never Block)

```go
// Fire and forget
go func() {
    if err := ledger.RecordEvidence(context.Background(), evidence); err != nil {
        log.Error().Err(err).Str("evidence_id", evidence.ID.String()).Msg("ledger write failed")
    }
}()
```
