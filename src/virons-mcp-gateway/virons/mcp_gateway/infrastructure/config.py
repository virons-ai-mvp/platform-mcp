# Copyright Virons Fintech. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    services = []
    for s in raw["services"]:
        # Support both URL (HTTP) and command (stdio) modes
        if "url" in s:
            url = _substitute_env_vars(s["url"])
            services.append(MCPService(name=s["name"], url=url, tools=s.get("tools", [])))
        elif "command" in s:
            # Store command as URL with stdio:// scheme
            url = f"stdio://{s['name']}"
            service = MCPService(name=s["name"], url=url, tools=s.get("tools", []))
            service.command = s["command"]
            service.cwd = s.get("cwd", "/app")
            services.append(service)

    return GatewayConfig(services=services)
