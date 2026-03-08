#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Check EU AI Act model cards for high-risk systems."""

import os
import sys


HIGH_RISK_SERVERS = ['anomaly-detector', 'grandmaster']


def check_model_cards():
    """Check if model cards exist for high-risk servers."""
    for server in HIGH_RISK_SERVERS:
        model_card_path = f'src/virons-{server}-mcp-server/docs/model-card.md'
        if not os.path.exists(model_card_path):
            print(f'❌ EU AI Act: Missing model card for {server}')
            return False
    return True


if __name__ == '__main__':
    if not check_model_cards():
        sys.exit(1)
    sys.exit(0)
