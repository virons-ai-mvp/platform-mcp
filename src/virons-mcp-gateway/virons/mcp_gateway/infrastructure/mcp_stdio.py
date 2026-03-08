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

"""MCP stdio client - invoke MCP servers via subprocess."""

import asyncio
import json
from typing import Any


async def invoke_mcp_stdio(
    command: list[str], cwd: str, method: str, params: dict[str, Any]
) -> dict[str, Any]:
    """Invoke MCP server via stdio subprocess."""
    from loguru import logger

    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "virons-gateway", "version": "1.0.0"},
        },
    }

    method_request = {"jsonrpc": "2.0", "id": 2, "method": method, "params": params}

    proc = await asyncio.create_subprocess_exec(
        *command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
    )

    input_data = json.dumps(init_request) + "\n" + json.dumps(method_request) + "\n"
    stdout, stderr = await proc.communicate(input_data.encode())

    logger.debug(f"MCP stdio call: {command} method={method} returncode={proc.returncode}")
    logger.debug(f"stdout: {stdout.decode()[:500]}")
    if stderr:
        logger.debug(f"stderr: {stderr.decode()[:500]}")

    if proc.returncode != 0:
        return {"error": f"Process failed: {stderr.decode()}", "returncode": proc.returncode}

    lines = stdout.decode().strip().split("\n")
    for line in lines:
        try:
            response = json.loads(line)
            if response.get("id") == 2:
                logger.debug(f"Found response for id=2: {response.get('result', {})}")
                return response.get("result", {})
        except json.JSONDecodeError:
            continue

    logger.warning(f"No valid response found in {len(lines)} lines")
    return {"error": "No valid response", "stdout": stdout.decode()}
