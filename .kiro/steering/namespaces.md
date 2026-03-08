# Namespace-Specific Skills

Skills are organized by namespace and auto-loaded when working in that namespace's directory.

## ingestion/ (Go 1.23, ports 9101-9117)

**Skills**: `.kiro/skills/ingestion/`
- `ingestion-patterns.md` — SHA-256 hashing, EventBridge, idempotency

**Key Rule**: Every artifact MUST be SHA-256 hashed before storage

## forensic/ (Python 3.12, ports 9300-9415)

**Skills**: `.kiro/skills/forensic/`
- `calculation-audit-pattern.md` — BaFin AT 8.1 compliance
- `beneish-formulas.md` — BEN_001–BEN_008
- `altman-formulas.md` — ALT_001–ALT_003

**Critical Rule**: `write_audit()` MUST be called BEFORE `forensic_flags` write

## ml/ (Python 3.12, ports 9420-9424)

**Skills**: `.kiro/skills/ml/`
- `iforest-ensemble.md` — k=5 IsolationForest
- `eu-ai-act-compliance.md` — Model cards, human oversight

**Key Rules**:
- ML gate: `gated_ml = ml_score if len(deterministic_flags) >= 1 else 0.0`
- Model cards required for high-risk AI systems

## blockchain/ (Go 1.23, ports 9430-9432)

**Skills**: `.kiro/skills/blockchain/`
- `merkle-chain.md` — SHA-256 chain, async writes

**Critical Rule**: Async write only — NEVER block forensic engine

## api/ (Go 1.23 + Next.js 15, ports 6001-8002)

**Skills**: `.kiro/skills/api/`
- `api-patterns.md` — JWT auth, rate limiting, RFC 7807, audit logging

**Key Rule**: 100% request audit logging (GDPR/DORA)
