# Kiro Specs — virons-services

Each feature gets its own subdirectory with three files following the Kiro spec workflow:

```
specs/
  <feature-name>/
    requirements.md   ← WHAT: user stories, acceptance criteria
    design.md         ← HOW: architecture, data flow, API contracts
    tasks.md          ← WORK: ordered implementation checklist
```

## Workflow

1. Start with `requirements.md` — define the feature in user story format
2. Write `design.md` — technical design, sequence diagrams, schema changes
3. Break down into `tasks.md` — atomic tasks an agent can execute one at a time

## Compliance Note

Every spec for forensic or ML features MUST include in `requirements.md`:
- BaFin AT 8.1 ordering requirement (calculation_audit → forensic_flags)
- EU AI Act classification (high-risk or not)
- GDPR data classification of any new fields

## Active Specs

_(add entries here as specs are created)_
