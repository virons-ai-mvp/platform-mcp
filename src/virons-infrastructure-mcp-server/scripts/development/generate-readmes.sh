#!/bin/bash
# Generate README files in all DDD directories

set -e

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$BASE_DIR/docs/reference/virons-readme-template.md"

# DDD directories that need README files
DIRS=(
    "docs/architecture"
    "docs/architecture/diagrams"
    "docs/architecture/decisions"
    "docs/compliance"
    "docs/compliance/policies"
    "docs/compliance/audits"
    "docs/compliance/evidence"
    "docs/operations"
    "docs/operations/runbooks"
    "docs/development"
    "docs/development/contributing"
    "docs/development/testing"
    "docs/getting-started"
    "docs/reference"
    "scripts/operations"
    "scripts/development"
    "scripts/docker"
    "virons/infrastructure_mcp_server"
    "virons/infrastructure_mcp_server/application"
    "virons/infrastructure_mcp_server/domain"
    "virons/infrastructure_mcp_server/infrastructure"
    "tests"
    "tests/application"
    "tests/domain"
    "tests/infrastructure"
    "tests/integration"
)

echo "📝 Generating README files from template..."
echo ""

for dir in "${DIRS[@]}"; do
    target="$BASE_DIR/$dir/README.md"

    # Skip if README already exists and is not empty
    if [ -f "$target" ] && [ -s "$target" ]; then
        echo "⏭️  Skipping $dir (README exists)"
        continue
    fi

    # Create directory if it doesn't exist
    mkdir -p "$BASE_DIR/$dir"

    # Copy template
    cp "$TEMPLATE" "$target"

    echo "✅ Created $dir/README.md"
done

echo ""
echo "✅ README generation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Review generated README files"
echo "2. Customize each README for its domain"
echo "3. Run: ./scripts/development/populate-docs.sh"
