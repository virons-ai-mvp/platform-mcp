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

"""Test tool schema validation across all MCP servers."""

import httpx
import pytest


@pytest.mark.asyncio
async def test_all_tools_have_valid_schemas():
    """Verify all 90 tools have proper input schemas (regression test for snake_case bug)."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:9000/tools", timeout=5.0)
        assert response.status_code == 200

        data = response.json()
        tools = data.get("tools", [])

        assert len(tools) == 90, f"Expected 90 tools, got {len(tools)}"

        errors = []
        for tool in tools:
            name = tool.get("name")
            service = tool.get("service")

            # Check required fields
            if not name:
                errors.append("Tool missing name")
                continue

            if not tool.get("description"):
                errors.append(f"{name}: Missing description")

            # Accept both camelCase and snake_case
            schema = tool.get("inputSchema") or tool.get("input_schema")
            if not schema or schema == {}:
                errors.append(f"{name} ({service}): Empty or missing input schema")
            elif schema.get("type") != "object":
                errors.append(f"{name}: Schema type must be 'object', got '{schema.get('type')}'")

        assert not errors, "Schema validation failed:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_security_mcp_tools_have_schemas():
    """Verify security-mcp tools have proper schemas (regression test)."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:9000/tools", timeout=5.0)
        data = response.json()

        security_tools = [t for t in data["tools"] if t["service"] == "security-mcp"]
        assert len(security_tools) == 4

        for tool in security_tools:
            schema = tool.get("inputSchema") or tool.get("input_schema")
            assert schema, f"{tool['name']}: Missing schema"
            assert schema != {}, f"{tool['name']}: Empty schema"
            assert schema.get("type") == "object", f"{tool['name']}: Invalid schema type"
            assert "properties" in schema, f"{tool['name']}: Missing properties"


@pytest.mark.asyncio
async def test_operations_mcp_tools_have_schemas():
    """Verify operations-mcp tools have proper schemas (regression test)."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:9000/tools", timeout=5.0)
        data = response.json()

        ops_tools = [t for t in data["tools"] if t["service"] == "operations-mcp"]
        assert len(ops_tools) == 4

        for tool in ops_tools:
            schema = tool.get("inputSchema") or tool.get("input_schema")
            assert schema and schema != {}, f"{tool['name']}: Missing or empty schema"


@pytest.mark.asyncio
async def test_monitoring_mcp_tools_have_schemas():
    """Verify monitoring-mcp tools have proper schemas (regression test)."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:9000/tools", timeout=5.0)
        data = response.json()

        mon_tools = [t for t in data["tools"] if t["service"] == "monitoring-mcp"]
        assert len(mon_tools) == 4

        for tool in mon_tools:
            schema = tool.get("inputSchema") or tool.get("input_schema")
            assert schema and schema != {}, f"{tool['name']}: Missing or empty schema"
