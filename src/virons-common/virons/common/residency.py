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
"""GDPR Art 25 compliant data residency enforcement.

Enforces EU data residency requirements for GDPR compliance.

Regulatory Reference:
    GDPR (General Data Protection Regulation) Article 25 - Data protection by design and by default
    https://eur-lex.europa.eu/eli/reg/2016/679/oj

    Article 25(1) requires the controller to implement appropriate technical and organisational
    measures designed to implement data-protection principles in an effective manner. Data
    residency enforcement ensures data remains within EU jurisdiction.
"""


class DataResidencyError(Exception):
    """Raised when data residency requirements are violated."""

    pass


def enforce_region(region: str | None) -> None:
    """Enforce EU data residency by validating region.

    Args:
        region: AWS region identifier.

    Raises:
        DataResidencyError: If region is not eu-central-1.
    """
    if region != "eu-central-1":
        raise DataResidencyError(f"Data must reside in eu-central-1, got: {region}")
