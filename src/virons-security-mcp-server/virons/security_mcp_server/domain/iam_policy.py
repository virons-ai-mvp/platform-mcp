"""Domain entities for IAM policies."""
from dataclasses import dataclass


@dataclass
class IAMPolicy:
    """IAM policy document."""
    policy_document: dict
    resource_type: str

    def __post_init__(self):
        if not self.policy_document:
            raise ValueError("Policy document is required")
        if self.resource_type not in ["user", "role", "group"]:
            raise ValueError("Resource type must be user, role, or group")


@dataclass
class PolicyIssue:
    """Security issue in IAM policy."""
    severity: str
    message: str
    rule: str

    def __post_init__(self):
        if not self.severity:
            raise ValueError("Severity is required")
        if self.severity not in ["low", "medium", "high", "critical"]:
            raise ValueError("Severity must be low, medium, high, or critical")
