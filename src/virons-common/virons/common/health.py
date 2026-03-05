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
"""DORA Art 11 compliant health monitoring.

Provides liveness and readiness checks for ICT service continuity.

Regulatory Reference:
    DORA (Digital Operational Resilience Act) Article 11 - Testing of ICT tools and systems
    https://eur-lex.europa.eu/eli/reg/2022/2554/oj

    Article 11(1) requires financial entities to establish, maintain and review a sound and
    comprehensive digital operational resilience testing programme as an integral part of the
    ICT risk-management framework.
"""

from typing import Callable


class HealthCheck:
    """Health check manager for DORA Art 11 compliance.

    Provides liveness (service running) and readiness (service ready to accept traffic) checks.
    """

    def __init__(self):
        """Initialize health check manager."""
        self._readiness_checks: dict[str, Callable[[], bool]] = {}

    def liveness(self) -> dict[str, str]:
        """Return liveness status.

        Returns:
            dict with status "ok" if service is running.
        """
        return {"status": "ok"}

    def readiness(self) -> dict[str, str | dict[str, bool]]:
        """Return readiness status by executing all registered checks.

        Returns:
            dict with status "ok" or "degraded" and individual check results.
        """
        checks = {name: check() for name, check in self._readiness_checks.items()}
        status = "ok" if all(checks.values()) else "degraded"
        return {"status": status, "checks": checks}

    def add_readiness_check(self, name: str, check: Callable[[], bool]) -> None:
        """Register a readiness check.

        Args:
            name: Unique name for the check.
            check: Callable that returns True if ready, False otherwise.
        """
        self._readiness_checks[name] = check
