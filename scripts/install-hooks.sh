#!/bin/bash
# Install git hooks for the project

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GIT_HOOKS_DIR="$(git rev-parse --git-dir)/hooks"

echo "Installing git hooks..."

# Install pre-push hook
if [[ -f "$SCRIPT_DIR/hooks/pre-push" ]]; then
    cp "$SCRIPT_DIR/hooks/pre-push" "$GIT_HOOKS_DIR/pre-push"
    chmod +x "$GIT_HOOKS_DIR/pre-push"
    echo "✓ Installed pre-push hook"
else
    echo "✗ pre-push hook not found"
    exit 1
fi

echo
echo "Git hooks installed successfully!"
echo
echo "The pre-push hook will validate:"
echo "  1. DDD structure (application/domain/infrastructure)"
echo "  2. TDD compliance (test files exist)"
echo "  3. Documentation quality (READMEs, sections)"
echo "  4. Forensic services compliance (calculation_audit, ML gate)"
echo "  5. ML services compliance (MODEL_CARD.md for EU AI Act)"
echo "  6. Code quality (syntax, anti-patterns)"
echo "  7. Port namespace validation"
echo
echo "To bypass hook (not recommended): git push --no-verify"
