#!/bin/bash
# Generate D2 and Mermaid diagram files from documentation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DIAGRAMS_DIR="$PROJECT_ROOT/docs/diagrams"

# Create diagrams directory
mkdir -p "$DIAGRAMS_DIR"/{d2,mermaid}

echo "🎨 Generating diagram files..."

# System Overview - Mermaid
cat > "$DIAGRAMS_DIR/mermaid/system-overview.mmd" << 'EOF'
graph TB
  MCP[MCP Client<br/>stdio] --> Server[FastMCP Server<br/>Multi-protocol]
  REST[REST API<br/>:8000] --> Server
  Server --> Domain[Domain Layer<br/>MCP Client + Registry]
  Domain --> App[Application Layer<br/>Deploy/Destroy/List]
  App --> Infra[Infrastructure Layer<br/>Health + Metrics]
EOF

# System Overview - D2
cat > "$DIAGRAMS_DIR/d2/system-overview.d2" << 'EOF'
MCP Client\nstdio -> FastMCP Server\nMulti-protocol
REST API\n:8000 -> FastMCP Server\nMulti-protocol
FastMCP Server\nMulti-protocol -> Domain Layer\nMCP Client + Registry
Domain Layer\nMCP Client + Registry -> Application Layer\nDeploy/Destroy/List
Application Layer\nDeploy/Destroy/List -> Infrastructure Layer\nHealth + Metrics
EOF

# Domain Layer - Mermaid
cat > "$DIAGRAMS_DIR/mermaid/domain-layer.mmd" << 'EOF'
graph TB
  App[Application Layer] --> Domain[Domain Layer]
  Domain --> MCP[MCPClient<br/>Protocol logic]
  Domain --> Registry[UpstreamRegistry<br/>Server registry]
EOF

# Domain Layer - D2
cat > "$DIAGRAMS_DIR/d2/domain-layer.d2" << 'EOF'
Application Layer -> Domain Layer
Domain Layer -> MCPClient\nProtocol logic
Domain Layer -> UpstreamRegistry\nServer registry
EOF

# Application Layer - Mermaid
cat > "$DIAGRAMS_DIR/mermaid/application-layer.mmd" << 'EOF'
graph TB
  API[API/Server] --> Deploy[DeployService<br/>Deploy use case]
  API --> Destroy[DestroyService<br/>Destroy use case]
  API --> List[ListService<br/>List use case]
  Deploy --> Domain[Domain Layer]
  Destroy --> Domain
  List --> Domain
  Deploy --> Compliance[ComplianceLogger<br/>Audit trail]
  Destroy --> Compliance
EOF

# Application Layer - D2
cat > "$DIAGRAMS_DIR/d2/application-layer.d2" << 'EOF'
API/Server -> DeployService\nDeploy use case
API/Server -> DestroyService\nDestroy use case
API/Server -> ListService\nList use case
DeployService\nDeploy use case -> Domain Layer
DestroyService\nDestroy use case -> Domain Layer
ListService\nList use case -> Domain Layer
DeployService\nDeploy use case -> ComplianceLogger\nAudit trail
DestroyService\nDestroy use case -> ComplianceLogger\nAudit trail
EOF

# Infrastructure Layer - Mermaid
cat > "$DIAGRAMS_DIR/mermaid/infrastructure-layer.mmd" << 'EOF'
graph TB
  App[Application Layer] --> Infra[Infrastructure Layer]
  Infra --> Health[health.py<br/>Health checks]
  Infra --> Server[health_server.py<br/>HTTP server]
  Infra --> Metrics[metrics.py<br/>Prometheus]
  Metrics --> Prom[Prometheus<br/>Scraper]
  Server --> HTTP[HTTP :8080<br/>/health /metrics]
EOF

# Infrastructure Layer - D2
cat > "$DIAGRAMS_DIR/d2/infrastructure-layer.d2" << 'EOF'
Application Layer -> Infrastructure Layer
Infrastructure Layer -> health.py\nHealth checks
Infrastructure Layer -> health_server.py\nHTTP server
Infrastructure Layer -> metrics.py\nPrometheus
metrics.py\nPrometheus -> Prometheus\nScraper
health_server.py\nHTTP server -> HTTP :8080\n/health /metrics
EOF

# Deployment Verification - Mermaid
cat > "$DIAGRAMS_DIR/mermaid/deployment-verification.mmd" << 'EOF'
graph TB
  Script[verify-deployment.sh] --> Deploy[Check Deployment<br/>kubectl get deploy]
  Deploy --> Pods[Verify Pods<br/>kubectl get pods]
  Pods --> Health[Test Health<br/>curl /health]
  Health --> Success[Exit 0]
  Deploy --> Fail[Exit 1]
  Pods --> Fail
  Health --> Fail
EOF

# Deployment Verification - D2
cat > "$DIAGRAMS_DIR/d2/deployment-verification.d2" << 'EOF'
verify-deployment.sh -> Check Deployment\nkubectl get deploy
Check Deployment\nkubectl get deploy -> Verify Pods\nkubectl get pods
Verify Pods\nkubectl get pods -> Test Health\ncurl /health
Test Health\ncurl /health -> Exit 0
Check Deployment\nkubectl get deploy -> Exit 1
Verify Pods\nkubectl get pods -> Exit 1
Test Health\ncurl /health -> Exit 1
EOF

# Test Architecture - Mermaid
cat > "$DIAGRAMS_DIR/mermaid/test-architecture.mmd" << 'EOF'
graph TB
  E2E[integration/<br/>E2E tests] --> App[application/<br/>Service tests]
  E2E --> Domain[domain/<br/>Domain tests]
  E2E --> Infra[infrastructure/<br/>Infrastructure tests]
  App --> Domain
  Infra --> Domain
EOF

# Test Architecture - D2
cat > "$DIAGRAMS_DIR/d2/test-architecture.d2" << 'EOF'
integration/\nE2E tests -> application/\nService tests
integration/\nE2E tests -> domain/\nDomain tests
integration/\nE2E tests -> infrastructure/\nInfrastructure tests
application/\nService tests -> domain/\nDomain tests
infrastructure/\nInfrastructure tests -> domain/\nDomain tests
EOF

echo "✅ Generated diagram files:"
echo "   📁 $DIAGRAMS_DIR/mermaid/ (7 .mmd files)"
echo "   📁 $DIAGRAMS_DIR/d2/ (7 .d2 files)"
echo ""
echo "📊 Mermaid diagrams can be rendered in:"
echo "   - GitHub/GitLab markdown"
echo "   - Mermaid Live Editor: https://mermaid.live"
echo ""
echo "📊 D2 diagrams can be rendered with:"
echo "   - d2 CLI: d2 file.d2 output.svg"
echo "   - D2 Playground: https://play.d2lang.com"
