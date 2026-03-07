# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Config loader with env var substitution."""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

from ..domain.registry import MCPService


@dataclass
class GatewayConfig:
    """Gateway configuration."""

    services: list[MCPService]


def _substitute_env_vars(value: str) -> str:
    """Replace ${VAR:default} with env value or default."""
    return re.sub(
        r"\$\{([^:}]+):([^}]+)\}",
        lambda m: os.environ.get(m.group(1), m.group(2)),
        value,
    )


def load_config(config_path: str) -> GatewayConfig:
    """Load gateway config from JSON file."""
    p = Path(config_path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    raw = json.loads(p.read_text())
    services = [
        MCPService(
            name=s["name"],
            url=_substitute_env_vars(s["url"]),
            tools=s.get("tools", []),  # Optional: tools will be discovered dynamically
        )
        for s in raw["services"]
    ]
    return GatewayConfig(services=services)
