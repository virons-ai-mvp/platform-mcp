# Kiro Auto-Load Configuration

## Always Loaded (~10KB total)

**CRITICAL - Load First**:
- `.kiro/steering/TDD-FIRST.md` (1KB) — TDD workflow, MUST read before any code changes

**Core Context**:
- `.ai/context/repository.json` (3KB) — machine-readable: all 42 services, ports, namespaces, critical rules
- `.kiro/steering/project.md` (3KB) — service catalog, compliance coordinates, quick commands
- `.kiro/steering/agents.md` (2KB) — agent selection matrix, coordination patterns
- `.kiro/steering/compliance.md` (2KB) — TDD methodology, regulatory requirements
- `README.md` (1KB) — repo overview
- `.ai/rules/repository-guidelines.md` (1KB) — TDD, commit format, security requirements
- `.ai/rules/orchestration/agent-coordinator.md` (1KB) — agent selection and coordination
- `.ai/rules/orchestration/safety-protocol.md` (1KB) — risk assessment, approval gates

## Load On-Demand

**Workflows** (load when task requires it, ~1KB each):
- `.ai/rules/workflows/testing-workflows.md`
- `.ai/rules/workflows/security-workflows.md`
- `.ai/rules/workflows/deployment-workflows.md`
- `.ai/rules/workflows/monitoring-workflows.md`
- `.ai/rules/workflows/documentation-workflows.md`
- `.ai/rules/workflows/service-development-workflow.md`
- `.ai/rules/workflows/inter-service-communication-workflow.md`
- `.ai/rules/workflows/database-migration-workflow.md`
- `.ai/rules/workflows/pre-execution-checklist.md`

**Specialized Agents** (load when working in that domain):
- `.ai/rules/02-services/go-backend-engineer.agent.md`
- `.ai/rules/02-services/python-backend-engineer.agent.md`
- `.ai/rules/02-services/ml-engineer.agent.md`
- `.ai/rules/02-services/compliance-validator.agent.md`
- `.ai/rules/02-services/api-engineer.agent.md`

**Guardrails** (load when making changes):
- `.ai/rules/agent-restrictions.md`
- `.ai/rules/cost-guards.md`
- `.ai/rules/GUARDRAILS-README.md`

## Context Budget

- Auto-load target: ≤10KB
- Remaining for task context: ~190KB
- Namespace CLAUDE.md files load lazily (only when editing files in that namespace)
- Per-namespace skills load lazily (only when editing files in that namespace)
