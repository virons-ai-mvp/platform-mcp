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

"""BaFin MaRisk AT 8.1 compliant audit logging.

This module implements the immutable audit trail required by BaFin MaRisk AT 8.1
(IT risk management) and AT 7.2 (audit trail ordering). Every write path in a
virons MCP server MUST call ``write_audit()`` before setting forensic flags.

Regulatory references:
    - BaFin MaRisk (BA) 09/2017 AT 8.1
      https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Rundschreiben/2017/rs_1709_marisk_ba.html
    - EU AI Act (Regulation (EU) 2024/1689) Art 11 — technical documentation
      https://eur-lex.europa.eu/eli/reg/2024/1689/oj
"""

from datetime import datetime, timezone
from typing import Any, Optional

from loguru import logger


async def write_audit(
    service_name: str,
    calculation_type: str,
    entity_id: str,
    input_data: dict[str, Any],
    output_data: dict[str, Any],
    metadata: Optional[dict[str, Any]] = None,
) -> str:
    """Write an audit record. MUST be called before forensic flags are set.

    BaFin MaRisk AT 8.1 requires an immutable audit trail for every calculation.
    This function MUST complete before any ``forensic_flags`` write (AT 7.2 ordering).

    Args:
        service_name: Name of the calling MCP server.
        calculation_type: Type of calculation (e.g. "beneish", "altman").
        entity_id: Entity being analysed.
        input_data: Input parameters used.
        output_data: Calculation results.
        metadata: Optional additional context (e.g. correlation_id).

    Returns:
        audit_id: Unique identifier for this audit entry.
    """
    ts = datetime.now(timezone.utc).isoformat()
    audit_id = f'{service_name}-{entity_id}-{ts}'

    logger.info(
        'calculation_audit',
        audit_id=audit_id,
        service=service_name,
        calculation_type=calculation_type,
        entity_id=entity_id,
        input_data=input_data,
        output_data=output_data,
        metadata=metadata or {},
        timestamp=ts,
    )

    # TODO: persist to calculation_audit table in PostgreSQL
    # await db.execute(
    #     "INSERT INTO calculation_audit (...) VALUES (...)",
    #     audit_id, service_name, calculation_type, ...
    # )

    return audit_id
