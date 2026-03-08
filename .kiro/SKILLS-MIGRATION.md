# Skills Migration: .claude → .kiro

All namespace-specific skills have been migrated from `.claude` to `.kiro` format.

## Migration Summary

### ✅ Completed

**ingestion/** (1 skill)
- ✅ ingestion-patterns.md — SHA-256 hashing, EventBridge, idempotency

**forensic/** (3 skills)
- ✅ calculation-audit-pattern.md — BaFin AT 8.1 compliance
- ✅ beneish-formulas.md — BEN_001–BEN_008 formulas
- ✅ altman-formulas.md — ALT_001–ALT_003 Z-Score variants

**ml/** (2 skills)
- ✅ iforest-ensemble.md — k=5 IsolationForest ensemble
- ✅ eu-ai-act-compliance.md — Model cards, human oversight

**blockchain/** (1 skill)
- ✅ merkle-chain.md — SHA-256 Merkle chain, async writes

**api/** (1 skill)
- ✅ api-patterns.md — JWT auth, rate limiting, RFC 7807, audit logging

**Total**: 8 namespace skills migrated

## Key Differences: .claude vs .kiro

| Aspect | .claude | .kiro |
|---|---|---|
| Location | `{namespace}/.claude/skills/` | `.kiro/skills/{namespace}/` |
| Format | `SKILL.md` in subdirectory | `{skill-name}.md` directly |
| Loading | Auto-load when in namespace | Auto-load when in namespace |
| Structure | Nested directories | Flat per namespace |

## Verification

```bash
# List all Kiro skills
find .kiro/skills -name "*.md" -type f | sort

# Expected output:
# .kiro/skills/api/api-patterns.md
# .kiro/skills/blockchain/merkle-chain.md
# .kiro/skills/compliance-check/SKILL.md
# .kiro/skills/forensic/altman-formulas.md
# .kiro/skills/forensic/beneish-formulas.md
# .kiro/skills/forensic/calculation-audit-pattern.md
# .kiro/skills/ingestion/ingestion-patterns.md
# .kiro/skills/ml/eu-ai-act-compliance.md
# .kiro/skills/ml/iforest-ensemble.md
# .kiro/skills/service-generator/SKILL.md
```

## Next Steps

1. ✅ Skills migrated to `.kiro/skills/`
2. ✅ Namespace documentation updated in `.kiro/steering/namespaces.md`
3. ✅ README created at `.kiro/skills/README.md`
4. ⏳ Test skills load correctly when working in each namespace
5. ⏳ Optional: Remove old `.claude` folders after verification

## Testing

Work in each namespace and verify skills are available:

```bash
cd ingestion/corporate-filings/
# Kiro should load ingestion-patterns.md

cd ../../forensic/beneish-calculator/
# Kiro should load calculation-audit-pattern.md, beneish-formulas.md, altman-formulas.md

cd ../../ml/
# Kiro should load iforest-ensemble.md, eu-ai-act-compliance.md
```
