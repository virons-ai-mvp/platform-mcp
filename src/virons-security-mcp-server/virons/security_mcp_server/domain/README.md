# Security MCP Server - Domain Layer

## Overview

Business logic and domain entities for security operations. Currently minimal - domain logic embedded in tools.

## Future Structure

```
domain/
├── __init__.py
├── entities/
│   ├── secret.py           # Secret detection entity
│   ├── audit_event.py      # CloudTrail event entity
│   ├── iam_policy.py       # IAM policy entity
│   └── compliance_result.py # Compliance check result
├── rules/
│   ├── secret_rules.py     # Secret detection rules
│   ├── iam_rules.py        # IAM best practices
│   └── compliance_rules.py # Compliance requirements
└── services/
    └── security_analyzer.py # Core security analysis logic
```

## Responsibilities

- Define security domain entities (Secret, AuditEvent, Policy)
- Implement security rules and policies
- Validate security configurations
- Calculate risk scores

## Example Entities

```python
@dataclass
class Secret:
    type: str  # api_key, password, token
    location: str  # file:line
    severity: str  # high, medium, low
    confidence: float
    
@dataclass
class IAMPolicy:
    document: dict
    resource_type: str  # user, role, group
    violations: list[str]
    risk_score: int
```

## Navigation

← [Core Implementation](../)
