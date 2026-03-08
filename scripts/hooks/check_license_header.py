#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Check and add Virons license headers."""

import sys


FULL_LICENSE_HEADER = """# Copyright Virons Fintech. All Rights Reserved.
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
"""


def check_and_fix_file(filepath):
    """Check if file has required license header, add if missing."""
    if not filepath.endswith('.py'):
        return True

    with open(filepath, 'r') as f:
        content = f.read()

    # Check if file already has the full license
    if content.startswith('# Copyright Virons Fintech. All Rights Reserved.\n#\n# Licensed under'):
        return True

    # Check if file has SPDX-only header (needs upgrade)
    if content.startswith(
        '# Copyright Virons Fintech. All Rights Reserved.\n# SPDX-License-Identifier:'
    ):
        # Remove SPDX header and add full license
        lines = content.split('\n')
        # Skip first 2 lines (SPDX header)
        remaining = '\n'.join(lines[2:]).lstrip('\n')
        new_content = FULL_LICENSE_HEADER + '\n' + remaining

        with open(filepath, 'w') as f:
            f.write(new_content)
        return True

    # No header at all - add it
    new_content = FULL_LICENSE_HEADER + '\n' + content
    with open(filepath, 'w') as f:
        f.write(new_content)
    return True


if __name__ == '__main__':
    files = sys.argv[1:]
    for f in files:
        check_and_fix_file(f)
    sys.exit(0)
