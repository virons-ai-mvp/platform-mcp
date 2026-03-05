#!/usr/bin/env python3
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
"""Inject README.md into every directory that lacks one.

Reads the virons README template and generates context-aware READMEs
based on directory role (DDD: domain, application, infrastructure, tests).

Usage:
    python3 scripts/inject-readme.py src/virons-common [--dry-run]
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path


YEAR = datetime.now(timezone.utc).year

# Lightweight README for subdirectories (not the full service template).
# The full template is for top-level service roots only.
SUBDIR_TEMPLATE = """\
# {title}

## Overview

{description}

## Contents

```
{tree}
```

## Context

| Key | Value |
|-----|-------|
| **Domain** | `{domain}` |
| **Parent** | [{parent}](../) |
| **Bounded Context** | {context} |

## Navigation

← [{parent} README](../)

---

**Last Updated**: {date}

**Maintained By**: compliance@virons.ai
"""


def dir_tree(path: Path, prefix: str = '', depth: int = 0, max_depth: int = 2) -> str:
    """Generate a simple directory tree string."""
    if depth > max_depth:
        return ''
    lines = []
    entries = sorted(
        [e for e in path.iterdir() if not e.name.startswith(('.', '__'))],
        key=lambda e: (e.is_file(), e.name),
    )
    for i, entry in enumerate(entries):
        connector = '└── ' if i == len(entries) - 1 else '├── '
        suffix = '/' if entry.is_dir() else ''
        lines.append(f'{prefix}{connector}{entry.name}{suffix}')
        if entry.is_dir() and depth < max_depth:
            extension = '    ' if i == len(entries) - 1 else '│   '
            sub = dir_tree(entry, prefix + extension, depth + 1, max_depth)
            if sub:
                lines.append(sub)
    return '\n'.join(lines)


# Map directory names to DDD descriptions
ROLE_MAP = {
    'tests': (
        'Test Suite',
        'TDD test suite. Tests are written FIRST per virons methodology.',
        'Testing',
    ),
    'virons': (
        'Virons Namespace Package',
        'PEP 420 namespace root for all `virons.*` packages. '
        'Enables multiple virons packages to coexist under one namespace.',
        'Namespace',
    ),
    'common': (
        'Shared Compliance Utilities',
        'Core compliance modules shared by all virons MCP servers.\n\n'
        '- `audit.py` — BaFin MaRisk AT 8.1 immutable audit trail\n'
        '- `health.py` — DORA Art 11 liveness/readiness (planned)\n'
        '- `correlation.py` — GDPR Art 32 request traceability (planned)\n'
        '- `residency.py` — GDPR Art 25 data residency guard (planned)',
        'Compliance Domain',
    ),
}


def infer_role(dirname: str, parent_path: Path) -> tuple[str, str, str]:
    """Infer title, description, and DDD context from directory name."""
    if dirname in ROLE_MAP:
        return ROLE_MAP[dirname]
    return (
        dirname.replace('_', ' ').replace('-', ' ').title(),
        f'Module: `{dirname}`',
        dirname,
    )


def inject(root: Path, dry_run: bool = False) -> list[Path]:
    """Walk root and inject README.md where missing. Returns list of created files."""
    created = []
    for dirpath in sorted(root.rglob('*')):
        if not dirpath.is_dir():
            continue
        if any(
            part.startswith(('.', '__'))
            for part in dirpath.relative_to(root).parts
        ):
            continue

        readme = dirpath / 'README.md'
        if readme.exists():
            continue

        dirname = dirpath.name
        title, description, context = infer_role(dirname, dirpath.parent)
        rel = dirpath.relative_to(root)
        raw_parts = list(rel.parts)
        if raw_parts == ['virons']:
            domain = 'virons'
        else:
            domain = f'virons.{".".join(raw_parts)}'
        parent = dirpath.parent.name or root.name
        tree = dir_tree(dirpath, max_depth=1)
        date = datetime.now(timezone.utc).strftime('%Y-%m-%d')

        content = SUBDIR_TEMPLATE.format(
            title=title,
            description=description,
            tree=tree,
            domain=domain,
            parent=parent,
            context=context,
            date=date,
        )

        if dry_run:
            print(f'  [dry-run] would create: {readme}')
        else:
            readme.write_text(content)
            print(f'  ✅ created: {readme}')
        created.append(readme)

    return created


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description='Inject README.md into directories')
    parser.add_argument('root', help='Root directory to scan')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f'Error: {root} is not a directory', file=sys.stderr)
        return 1

    print(f'Scanning {root} for directories missing README.md...')
    created = inject(root, dry_run=args.dry_run)

    if not created:
        print('All directories already have README.md ✓')
    else:
        action = 'Would create' if args.dry_run else 'Created'
        print(f'\n{action} {len(created)} README(s)')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
