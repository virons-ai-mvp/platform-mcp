# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""MCP Gateway configuration."""

from typing import Dict

from pydantic import BaseModel


class ServerConfig(BaseModel):
    """Configuration for an MCP server."""

    name: str
    url: str
    enabled: bool = True
    timeout: int = 30


GATEWAY_CONFIG: Dict[str, ServerConfig] = {
    "infrastructure": ServerConfig(
        name="infrastructure",
        url="http://localhost:9100",
        enabled=True,
    ),
    "security": ServerConfig(
        name="security",
        url="http://localhost:9200",
        enabled=True,
    ),
    "operations": ServerConfig(
        name="operations",
        url="http://localhost:9300",
        enabled=True,
    ),
    "monitoring": ServerConfig(
        name="monitoring",
        url="http://localhost:9400",
        enabled=True,
    ),
}

GATEWAY_PORT = 9000
