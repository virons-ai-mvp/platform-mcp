#!/bin/bash
# Quick start script for API mode with Swagger UI

set -e

echo "🚀 Starting Virons Infrastructure MCP Server in API mode..."
echo ""
echo "📚 Documentation will be available at:"
echo "   - Swagger UI: http://localhost:8080/api/docs"
echo "   - ReDoc:      http://localhost:8080/api/redoc"
echo "   - OpenAPI:    http://localhost:8080/api/openapi.json"
echo ""
echo "🏥 Health endpoints:"
echo "   - Liveness:   http://localhost:8080/health/live"
echo "   - Readiness:  http://localhost:8080/health/ready"
echo ""
echo "📊 Metrics:"
echo "   - Prometheus: http://localhost:8080/metrics"
echo ""
echo "🔧 API endpoints:"
echo "   - POST /api/v1/deploy   - Deploy infrastructure"
echo "   - POST /api/v1/destroy  - Destroy infrastructure"
echo "   - GET  /api/v1/stacks   - List stacks"
echo "   - GET  /api/v1/info     - Server info"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
uv run virons-infrastructure-mcp-server --transport api --port 8080
