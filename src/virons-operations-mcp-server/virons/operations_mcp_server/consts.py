# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Constants for virons-operations-mcp-server."""

SERVER_NAME = "virons.operations-mcp-server"
SERVER_PORT = 9121

SERVER_INSTRUCTIONS = """
Virons Operations MCP Server

This server is compliance-first and follows:
- BaFin MaRisk AT 8.1 (audit trail on all writes)
- GDPR Art 25, 32 (data residency, correlation IDs)
- DORA Art 11 (health monitoring)
- EU AI Act (model card validation if high-risk)

All write operations are audited. Data resides in eu-central-1 only.

## Tool Naming Convention

Tool names must follow MCP naming rules:
- Maximum 64 characters
- Start with a letter
- Use only lowercase letters and hyphens (-)
- No special characters or numbers at start

Valid examples: data-cleaner, csv-uploader, pdf-generator
Invalid examples: 123tool, tool!@#$, name-that-is-way-too-long...
"""

SERVER_DEPENDENCIES = [
    "mcp[cli]>=1.23.0",
    "loguru>=0.7.0",
    "pydantic>=2.10.6",
    "virons.common>=0.1.0",
]
