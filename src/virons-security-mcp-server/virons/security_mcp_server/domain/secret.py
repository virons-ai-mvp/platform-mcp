"""Domain entities for secret scanning."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SecretFinding:
    """A secret found in code."""
    type: str
    file: str
    line: int
    secret: str
    commit: Optional[str] = None

    def __post_init__(self):
        if not self.type:
            raise ValueError("Secret type is required")
        if not self.file:
            raise ValueError("File path is required")


@dataclass
class ScanRequest:
    """Request to scan repository for secrets."""
    repository_path: str
    scan_history: bool = False

    def __post_init__(self):
        if not self.repository_path:
            raise ValueError("Repository path is required")
