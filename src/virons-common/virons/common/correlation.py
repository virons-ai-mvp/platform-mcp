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
"""GDPR Art 32 compliant correlation ID threading.

Provides correlation ID generation and context propagation for audit trails.

Regulatory Reference:
    GDPR (General Data Protection Regulation) Article 32 - Security of processing
    https://eur-lex.europa.eu/eli/reg/2016/679/oj

    Article 32(1)(d) requires a process for regularly testing, assessing and evaluating
    the effectiveness of technical and organisational measures for ensuring the security
    of the processing. Correlation IDs enable traceability across distributed systems.
"""

import uuid
from contextvars import ContextVar


def generate_correlation_id() -> str:
    """Generate a UUID4 correlation ID.

    Returns:
        String representation of a UUID4.
    """
    return str(uuid.uuid4())


class CorrelationContext:
    """Context manager for correlation ID propagation using contextvars.

    Enables thread-safe correlation ID propagation across async boundaries.
    """

    def __init__(self):
        """Initialize correlation context."""
        self._context: ContextVar[str | None] = ContextVar("correlation_id", default=None)

    def get(self) -> str | None:
        """Get current correlation ID from context.

        Returns:
            Current correlation ID or None if not set.
        """
        return self._context.get()

    def set(self, correlation_id: str) -> None:
        """Set correlation ID in context.

        Args:
            correlation_id: Correlation ID to set.
        """
        self._context.set(correlation_id)

    def reset(self) -> None:
        """Reset correlation ID to None."""
        self._context.set(None)
