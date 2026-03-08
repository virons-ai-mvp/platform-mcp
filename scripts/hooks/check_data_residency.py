#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Check GDPR Art 25 data residency compliance."""

import sys


FORBIDDEN_REGIONS = ['us-east-1', 'us-west-1', 'us-west-2']


def check_file(filepath):
    """Check for forbidden AWS regions."""
    with open(filepath, 'r') as f:
        content = f.read()
        for region in FORBIDDEN_REGIONS:
            if region in content:
                return False
    return True


if __name__ == '__main__':
    files = sys.argv[1:]
    failed = []
    for f in files:
        if not check_file(f):
            failed.append(f)

    if failed:
        print(f'❌ GDPR: US regions found in: {", ".join(failed)}')
        sys.exit(1)
    sys.exit(0)
