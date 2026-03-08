# Shared Compliance Utilities

## Overview

Core compliance modules shared by all virons MCP servers.

- `audit.py` — BaFin MaRisk AT 8.1 immutable audit trail
- `health.py` — DORA Art 11 liveness/readiness checks
- `correlation.py` — GDPR Art 32 request traceability
- `residency.py` — GDPR Art 25 data residency guard

## Contents

```
├── audit.py
├── correlation.py
├── health.py
└── residency.py
```

## Context

| Key | Value |
|-----|-------|
| **Domain** | `virons.virons.common` |
| **Parent** | [virons](../) |
| **Bounded Context** | Compliance Domain |

## Navigation

← [virons README](../)

---

**Last Updated**: 2026-03-04

**Maintained By**: compliance@virons.ai
