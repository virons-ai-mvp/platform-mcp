#!/bin/bash
# Validate tool documentation quality

set -e

echo "🔍 Validating Tool Documentation..."
echo

# Check if gateway is running
if ! curl -s http://localhost:9000/health > /dev/null 2>&1; then
    echo "❌ Gateway is not running. Start services with: docker-compose up -d"
    exit 1
fi

# Fetch tools
TOOLS_JSON=$(curl -s http://localhost:9000/tools)
TOTAL_TOOLS=$(echo "$TOOLS_JSON" | jq '.tools | length')

echo "📊 Total tools: $TOTAL_TOOLS"
echo

# Check for tools with minimal descriptions
echo "🔎 Checking for tools with minimal descriptions..."
MINIMAL_DESC=$(echo "$TOOLS_JSON" | jq -r '.tools[] | select(.description | length < 30) | .name')
MINIMAL_COUNT=$(echo "$MINIMAL_DESC" | grep -c . || true)

if [ "$MINIMAL_COUNT" -gt 0 ]; then
    echo "⚠️  Found $MINIMAL_COUNT tools with minimal descriptions:"
    echo "$MINIMAL_DESC" | sed 's/^/  - /'
    echo
else
    echo "✅ All tools have adequate descriptions"
    echo
fi

# Check for tools missing Args section
echo "🔎 Checking for tools missing Args documentation..."
MISSING_ARGS=$(echo "$TOOLS_JSON" | jq -r '.tools[] | select(.input_schema.properties | length > 0) | select(.description | contains("Args:") | not) | .name')
MISSING_COUNT=$(echo "$MISSING_ARGS" | grep -c . || true)

if [ "$MISSING_COUNT" -gt 0 ]; then
    echo "⚠️  Found $MISSING_COUNT tools missing Args section:"
    echo "$MISSING_ARGS" | sed 's/^/  - /'
    echo
else
    echo "✅ All tools with parameters have Args documentation"
    echo
fi

# Check for tools with examples
echo "🔎 Checking for tools with examples..."
WITH_EXAMPLES=$(echo "$TOOLS_JSON" | jq -r '.tools[] | select(.examples | length > 0) | .name' | wc -l)
echo "✅ $WITH_EXAMPLES/$TOTAL_TOOLS tools have examples"
echo

# Summary
echo "📋 Summary:"
echo "  Total tools: $TOTAL_TOOLS"
echo "  With examples: $WITH_EXAMPLES"
echo "  Minimal descriptions: $MINIMAL_COUNT"
echo "  Missing Args: $MISSING_COUNT"
echo

if [ "$MINIMAL_COUNT" -eq 0 ] && [ "$MISSING_COUNT" -eq 0 ]; then
    echo "✅ All tool documentation meets quality standards!"
    exit 0
else
    echo "⚠️  Some tools need documentation improvements"
    echo "📖 See docs/TOOL_DOCUMENTATION_STANDARD.md for guidelines"
    exit 1
fi
