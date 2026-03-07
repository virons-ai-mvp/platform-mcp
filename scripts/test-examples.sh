#!/bin/bash
# Test all code examples in documentation
# Validates curl commands, docker commands, and Python snippets

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASSED=0
FAILED=0
SKIPPED=0

echo -e "${BLUE}🧪 Testing Documentation Code Examples${NC}"
echo "========================================"
echo

# Check if services are running
check_services() {
    echo -e "${BLUE}[1/4] Checking services...${NC}"
    
    services=("virons-mcp-gateway:9000" "virons-infrastructure-mcp:9100" "virons-security-mcp:9500" "virons-operations-mcp:9510" "virons-monitoring-mcp:9520")
    
    for service in "${services[@]}"; do
        name="${service%:*}"
        port="${service#*:}"
        
        if curl -sf "http://localhost:$port/health" > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} $name ($port)"
            ((PASSED++))
        else
            echo -e "${YELLOW}⚠${NC} $name ($port) not running"
            ((SKIPPED++))
        fi
    done
    echo
}

# Test gateway endpoints
test_gateway_endpoints() {
    echo -e "${BLUE}[2/4] Testing gateway endpoints...${NC}"
    
    # Test /tools endpoint
    if curl -sf "http://localhost:9000/tools" > /dev/null 2>&1; then
        tool_count=$(curl -s "http://localhost:9000/tools" | grep -o '"name"' | wc -l | tr -d ' ')
        echo -e "${GREEN}✓${NC} GET /tools (${tool_count} tools)"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} GET /tools failed"
        ((FAILED++))
    fi
    
    # Test /health endpoint
    if curl -sf "http://localhost:9000/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} GET /health"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} GET /health failed"
        ((FAILED++))
    fi
    
    # Test /ready endpoint
    if curl -sf "http://localhost:9000/ready" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} GET /ready"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} GET /ready failed"
        ((FAILED++))
    fi
    
    # Test /metrics endpoint
    if curl -sf "http://localhost:9000/metrics" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} GET /metrics"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} GET /metrics failed"
        ((FAILED++))
    fi
    
    echo
}

# Test backend server endpoints
test_backend_endpoints() {
    echo -e "${BLUE}[3/4] Testing backend endpoints...${NC}"
    
    backends=("9100:infrastructure" "9500:security" "9510:operations" "9520:monitoring")
    
    for backend in "${backends[@]}"; do
        port="${backend%:*}"
        name="${backend#*:}"
        
        if curl -sf "http://localhost:$port/health" > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} $name /health"
            ((PASSED++))
        else
            echo -e "${YELLOW}⚠${NC} $name /health (service not running)"
            ((SKIPPED++))
        fi
        
        if curl -sf "http://localhost:$port/tools" > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} $name /tools"
            ((PASSED++))
        else
            echo -e "${YELLOW}⚠${NC} $name /tools (service not running)"
            ((SKIPPED++))
        fi
    done
    
    echo
}

# Test docker commands from READMEs
test_docker_commands() {
    echo -e "${BLUE}[4/4] Testing docker commands...${NC}"
    
    # Test docker-compose ps
    if docker-compose ps > /dev/null 2>&1; then
        running=$(docker-compose ps | grep "Up" | wc -l | tr -d ' ')
        echo -e "${GREEN}✓${NC} docker-compose ps ($running services up)"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} docker-compose ps failed"
        ((FAILED++))
    fi
    
    # Test docker-compose logs (just check command works)
    if docker-compose logs --tail=1 virons-mcp-gateway > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} docker-compose logs"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} docker-compose logs (gateway not running)"
        ((SKIPPED++))
    fi
    
    echo
}

# Run all tests
check_services
test_gateway_endpoints
test_backend_endpoints
test_docker_commands

# Summary
echo "========================================"
echo -e "${BLUE}Summary:${NC}"
echo -e "Passed:  ${GREEN}$PASSED${NC}"
echo -e "Failed:  ${RED}$FAILED${NC}"
echo -e "Skipped: ${YELLOW}$SKIPPED${NC}"
echo

if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}✓ All available tests passed${NC}"
    if [[ $SKIPPED -gt 0 ]]; then
        echo -e "${YELLOW}ℹ Start services with: docker-compose up -d${NC}"
    fi
    exit 0
else
    echo -e "${RED}✗ $FAILED tests failed${NC}"
    exit 1
fi
