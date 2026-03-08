#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Check for BaFin MaRisk AT 8.1 audit trail patterns."""

import sys


REQUIRED_PATTERNS = [
    r'log_calculation_audit',
    r'log_forensic_flags',
    r'write_audit',
]


def check_file(filepath):
    """Check if file contains required audit patterns."""
    if 'forensic' in filepath or 'ml' in filepath:
        with open(filepath, 'r') as f:
            content = f.read()
            if 'def ' in content or 'async def ' in content:
                for pattern in REQUIRED_PATTERNS:
                    if pattern not in content:
                        return False
    return True


if __name__ == '__main__':
    files = sys.argv[1:]
    failed = []
    for f in files:
        if not check_file(f):
            failed.append(f)

    if failed:
        print(f'❌ BaFin audit pattern missing in: {", ".join(failed)}')
        sys.exit(1)
    sys.exit(0)
