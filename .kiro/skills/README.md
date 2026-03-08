# Kiro Skills — virons-services

Skills provide domain-specific knowledge and patterns that Kiro loads contextually.

## Structure

```
.kiro/skills/
├── ingestion/           # Go ingestion services (ports 9101-9117)
│   └── ingestion-patterns.md
├── forensic/            # Python forensic services (ports 9300-9415)
│   ├── calculation-audit-pattern.md
│   ├── beneish-formulas.md
│   └── altman-formulas.md
├── ml/                  # Python ML services (ports 9420-9424)
│   ├── iforest-ensemble.md
│   └── eu-ai-act-compliance.md
├── blockchain/          # Go blockchain services (ports 9430-9432)
│   └── merkle-chain.md
├── api/                 # Go/Next.js API services (ports 6001-8002)
│   └── api-patterns.md
├── compliance-check/    # Global compliance validation
│   └── SKILL.md
└── service-generator/   # Global service scaffolding
    └── SKILL.md
```

## Namespace Skills

Namespace skills are automatically loaded when working in that namespace's directory:

- **ingestion/** → loads `.kiro/skills/ingestion/*`
- **forensic/** → loads `.kiro/skills/forensic/*`
- **ml/** → loads `.kiro/skills/ml/*`
- **blockchain/** → loads `.kiro/skills/blockchain/*`
- **api/** → loads `.kiro/skills/api/*`

## Global Skills

Global skills (compliance-check, service-generator) are available everywhere.

## Skill Format

Each skill file contains:
- **Name**: Skill identifier
- **Description**: What the skill provides
- **Namespace**: Which namespace it belongs to
- **User-invocable**: Whether users can call it directly
- **Content**: Patterns, formulas, code examples

## Usage

Kiro automatically loads relevant skills based on:
1. Current working directory (namespace detection)
2. File being edited (namespace inference)
3. Explicit skill invocation (for global skills)

No manual loading required — skills are context-aware.
