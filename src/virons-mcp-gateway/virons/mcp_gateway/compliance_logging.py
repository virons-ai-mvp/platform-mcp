# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""BaFin-compliant logging templates for virons-infrastructure-mcp-server."""

import json
from datetime import UTC, datetime
from typing import Any, Dict, Optional

from loguru import logger


def log_calculation_audit(
    correlation_id: str,
    operation: str,
    inputs: Dict[str, Any],
    calculation_steps: list[Dict[str, Any]],
    result: Any,
    user_id: str = "system",
) -> None:
    """Log calculation audit BEFORE forensic flags (BaFin MaRisk AT 8.1)."""
    audit = {
        "event_type": "calculation_audit",
        "correlation_id": correlation_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "operation": operation,
        "user_id": user_id,
        "inputs": inputs,
        "calculation_steps": calculation_steps,
        "result": result,
        "compliance": "BaFin_MaRisk_AT_8.1",
    }
    logger.info(f"AUDIT_CALCULATION: {json.dumps(audit)}")


def log_forensic_flags(
    correlation_id: str,
    deterministic_flags: list[str],
    ml_score: float,
    gated_ml: float,
    final_score: float,
) -> None:
    """Log forensic analysis with ML gate (virons-services :9300-:9415)."""
    audit = {
        "event_type": "forensic_flags",
        "correlation_id": correlation_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "deterministic_flags": deterministic_flags,
        "ml_score": ml_score,
        "gated_ml": gated_ml,
        "final_score": final_score,
        "ml_gate_applied": len(deterministic_flags) >= 1,
        "compliance": "virons_forensic",
    }
    logger.info(f"AUDIT_FORENSIC: {json.dumps(audit)}")


def log_write_audit(
    correlation_id: str,
    operation: str,
    entity_type: str,
    entity_id: str,
    changes: Dict[str, Any],
    user_id: str = "system",
) -> None:
    """Log write operation (BaFin: 10-year retention)."""
    audit = {
        "event_type": "write_audit",
        "correlation_id": correlation_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "operation": operation,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "changes": changes,
        "user_id": user_id,
        "retention_years": 10,
        "compliance": "BaFin_MaRisk_AT_8.1",
        "immutable": True,
    }
    logger.info(f"AUDIT_WRITE: {json.dumps(audit)}")


def log_tool_call_start(
    correlation_id: str, tool_name: str, parameters: Dict[str, Any], user_id: str = "system"
) -> None:
    """Log MCP tool call start."""
    logger.info(
        f"TOOL_START: {
            json.dumps(
                {
                    'correlation_id': correlation_id,
                    'timestamp': datetime.now(UTC).isoformat(),
                    'tool_name': tool_name,
                    'parameters': parameters,
                    'user_id': user_id,
                }
            )
        }"
    )


def log_tool_call_end(
    correlation_id: str,
    tool_name: str,
    status: str,
    duration_ms: float,
    result: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
) -> None:
    """Log MCP tool call completion."""
    logger.info(
        f"TOOL_END: {
            json.dumps(
                {
                    'correlation_id': correlation_id,
                    'timestamp': datetime.now(UTC).isoformat(),
                    'tool_name': tool_name,
                    'status': status,
                    'duration_ms': duration_ms,
                    'result': result,
                    'error': error,
                }
            )
        }"
    )
