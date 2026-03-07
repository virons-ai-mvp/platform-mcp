"""Domain entities for dashboards - DDD approach."""
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Panel:
    """Panel value object."""
    title: str
    query: str
    type: str  # graph, stat, table
    datasource: str = "prometheus"
    
    def __post_init__(self):
        if not self.title:
            raise ValueError("Panel title required")
        if self.type not in ["graph", "stat", "table"]:
            raise ValueError(f"Invalid panel type: {self.type}")


@dataclass
class Dashboard:
    """Dashboard entity - core domain object."""
    name: str
    panels: List[Panel]
    tags: List[str] = None
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Dashboard name required")
        if not self.panels:
            raise ValueError("At least one panel required")
        if self.tags is None:
            self.tags = []
    
    def add_panel(self, panel: Panel):
        """Add panel to dashboard."""
        self.panels.append(panel)
    
    def panel_count(self) -> int:
        """Get panel count."""
        return len(self.panels)
