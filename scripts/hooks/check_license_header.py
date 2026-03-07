#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Check for Virons license headers."""

import sys


REQUIRED_HEADER = [
    '# Copyright Virons Fintech. All Rights Reserved.',
    '# SPDX-License-Identifier: Apache-2.0',
]


def check_file(filepath):
    """Check if file has required license header."""
    if not filepath.endswith('.py'):
        return True

    with open(filepath, 'r') as f:
        lines = f.readlines()
        if len(lines) < 2:
            return False
        return lines[0].strip() == REQUIRED_HEADER[0] and lines[1].strip() == REQUIRED_HEADER[1]


if __name__ == '__main__':
    files = sys.argv[1:]
    failed = []
    for f in files:
        if not check_file(f):
            failed.append(f)

    if failed:
        print(f'❌ Missing license header: {", ".join(failed)}')
        sys.exit(1)
    sys.exit(0)
