# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Compliance hooks for virons-security-mcp-server.

Integrates virons.common compliance utilities:
- BaFin MaRisk AT 8.1: write_audit()
- GDPR Art 25: enforce_region()
- DORA Art 11: HealthCheck
"""

from loguru import logger
from mcp.server.fastmcp import FastMCP

from virons.common import (
    HealthCheck,
    enforce_region,
    write_audit,
)

# Global instances
health_check = HealthCheck()


def setup_compliance_hooks(server: FastMCP) -> None:
    """Register compliance hooks with the FastMCP server.

    Args:
        server: FastMCP server instance
    """
    # Enforce EU data residency (GDPR Art 25)
    enforce_region("eu-central-1")
    logger.info("Data residency enforced: eu-central-1")
    logger.info("Compliance hooks initialized")


async def audit_write_operation(
    operation_name: str,
    entity_id: str,
    input_data: dict,
    output_data: dict,
) -> str:
    """Audit a write operation per BaFin MaRisk AT 8.1.

    Args:
        operation_name: Name of the operation
        entity_id: Entity identifier
        input_data: Input parameters
        output_data: Operation results

    Returns:
        Audit trail ID
    """
    audit_id = await write_audit(
        service_name="virons-security-mcp-server",
        calculation_type=operation_name,
        entity_id=entity_id,
        input_data=input_data,
        output_data=output_data,
    )
    logger.info(f"Audit trail created: {audit_id}")
    return audit_id
