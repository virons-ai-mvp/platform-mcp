"""Domain entities for compliance gates."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ComplianceResult:
    """Result of compliance gate check."""
    status: str
    gate_type: str
    artifact: str
    checks_passed: int = 0
    checks_failed: int = 0

    def __post_init__(self):
        if not self.status:
            raise ValueError("Status is required")
        if self.status not in ["passed", "failed", "warning"]:
            raise ValueError("Status must be passed, failed, or warning")


@dataclass
class GateCheck:
    """Compliance gate check request."""
    gate_type: str
    artifact_path: str

    def __post_init__(self):
        if not self.gate_type:
            raise ValueError("Gate type is required")
        if self.gate_type not in ["pre-commit", "pre-deploy", "post-deploy"]:
            raise ValueError("Gate type must be pre-commit, pre-deploy, or post-deploy")
