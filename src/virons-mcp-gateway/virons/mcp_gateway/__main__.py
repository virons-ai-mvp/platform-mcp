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

"""MCP Gateway CLI entry point."""

import argparse

from .mcp_server import MCPGateway


def main():
    """Run MCP gateway in stdio mode."""
    parser = argparse.ArgumentParser(description="Virons MCP Gateway")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport type (default: stdio)",
    )
    args = parser.parse_args()

    # Backend configurations
    backend_configs = {
        "infrastructure": {
            "command": "uv",
            "args": ["run", "virons-infrastructure-mcp-server", "--transport", "stdio"],
        },
        "security": {
            "command": "uv",
            "args": ["run", "virons-security-mcp-server", "--transport", "stdio"],
        },
        "operations": {
            "command": "uv",
            "args": ["run", "virons-operations-mcp-server", "--transport", "stdio"],
        },
        "monitoring": {
            "command": "uv",
            "args": ["run", "virons-monitoring-mcp-server", "--transport", "stdio"],
        },
    }

    gateway = MCPGateway(backend_configs)
    gateway.run(transport=args.transport)


if __name__ == "__main__":
    main()
