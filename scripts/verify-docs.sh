#!/bin/bash
# TDD-driven documentation verification
# Tests: links, formatting, examples, completeness

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

echo "🧪 Documentation Verification (TDD)"
echo "=================================="
echo

# Test 1: All expected READMEs exist
test_readme_existence() {
    echo "Test 1: README existence..."
    local missing=0
    
    for server in security operations monitoring; do
        for path in \
            "src/virons-${server}-mcp-server/README.md" \
            "src/virons-${server}-mcp-server/virons/${server}_mcp_server/README.md" \
            "src/virons-${server}-mcp-server/virons/${server}_mcp_server/application/README.md" \
            "src/virons-${server}-mcp-server/virons/${server}_mcp_server/domain/README.md" \
            "src/virons-${server}-mcp-server/virons/${server}_mcp_server/infrastructure/README.md" \
            "src/virons-${server}-mcp-server/tests/README.md" \
            "src/virons-${server}-mcp-server/scripts/README.md"; do
            
            if [[ ! -f "$path" ]]; then
                echo -e "${RED}✗${NC} Missing: $path"
                ((missing++))
            fi
        done
    done
    
    for path in \
        "src/virons-mcp-gateway/README.md" \
        "src/virons-mcp-gateway/virons/mcp_gateway/README.md" \
        "src/virons-mcp-gateway/virons/mcp_gateway/application/README.md" \
        "src/virons-mcp-gateway/virons/mcp_gateway/domain/README.md" \
        "src/virons-mcp-gateway/virons/mcp_gateway/infrastructure/README.md" \
        "src/virons-mcp-gateway/tests/README.md"; do
        
        if [[ ! -f "$path" ]]; then
            echo -e "${RED}✗${NC} Missing: $path"
            ((missing++))
        fi
    done
    
    if [[ $missing -eq 0 ]]; then
        echo -e "${GREEN}✓${NC} All expected READMEs exist"
    else
        echo -e "${RED}✗${NC} $missing READMEs missing"
        ((ERRORS+=missing))
    fi
    echo
}

# Test 2: No placeholder text
test_no_placeholders() {
    echo "Test 2: No placeholder text..."
    local found=0
    
    while IFS= read -r file; do
        if grep -q "TODO\|FIXME\|XXX\|PLACEHOLDER" "$file" 2>/dev/null; then
            echo -e "${YELLOW}⚠${NC} Placeholder in: $file"
            grep -n "TODO\|FIXME\|XXX\|PLACEHOLDER" "$file" | head -3
            ((found++))
        fi
    done < <(find src/virons-*-mcp-* -name "README.md" -type f)
    
    if [[ $found -eq 0 ]]; then
        echo -e "${GREEN}✓${NC} No placeholders found"
    else
        echo -e "${YELLOW}⚠${NC} $found files with placeholders"
        ((WARNINGS+=found))
    fi
    echo
}

# Test 3: Navigation links exist
test_navigation_links() {
    echo "Test 3: Navigation links..."
    local missing=0
    
    while IFS= read -r file; do
        if ! grep -q "## Navigation" "$file" 2>/dev/null; then
            echo -e "${YELLOW}⚠${NC} No navigation: $file"
            ((missing++))
        fi
    done < <(find src/virons-*-mcp-* -name "README.md" -type f | grep -v "/docs/")
    
    if [[ $missing -eq 0 ]]; then
        echo -e "${GREEN}✓${NC} All READMEs have navigation"
    else
        echo -e "${YELLOW}⚠${NC} $missing READMEs missing navigation"
        ((WARNINGS+=missing))
    fi
    echo
}

# Test 4: Required sections present
test_required_sections() {
    echo "Test 4: Required sections in root READMEs..."
    local missing=0
    
    for server in security operations monitoring; do
        file="src/virons-${server}-mcp-server/README.md"
        for section in "## Overview" "## Architecture" "## Tools" "## Usage"; do
            if ! grep -q "^$section" "$file" 2>/dev/null; then
                echo -e "${RED}✗${NC} Missing section '$section' in $file"
                ((missing++))
            fi
        done
    done
    
    file="src/virons-mcp-gateway/README.md"
    for section in "## Overview" "## Architecture" "## Key Features" "## Usage"; do
        if ! grep -q "^$section" "$file" 2>/dev/null; then
            echo -e "${RED}✗${NC} Missing section '$section' in $file"
            ((missing++))
        fi
    done
    
    if [[ $missing -eq 0 ]]; then
        echo -e "${GREEN}✓${NC} All required sections present"
    else
        echo -e "${RED}✗${NC} $missing sections missing"
        ((ERRORS+=missing))
    fi
    echo
}

# Test 5: Mermaid diagrams present
test_mermaid_diagrams() {
    echo "Test 5: Mermaid diagrams in root READMEs..."
    local missing=0
    
    for server in security operations monitoring; do
        file="src/virons-${server}-mcp-server/README.md"
        if ! grep -q '```mermaid' "$file" 2>/dev/null; then
            echo -e "${YELLOW}⚠${NC} No mermaid diagram in $file"
            ((missing++))
        fi
    done
    
    file="src/virons-mcp-gateway/README.md"
    if ! grep -q '```mermaid' "$file" 2>/dev/null; then
        echo -e "${YELLOW}⚠${NC} No mermaid diagram in $file"
        ((missing++))
    fi
    
    if [[ $missing -eq 0 ]]; then
        echo -e "${GREEN}✓${NC} All root READMEs have diagrams"
    else
        echo -e "${YELLOW}⚠${NC} $missing READMEs missing diagrams"
        ((WARNINGS+=missing))
    fi
    echo
}

# Test 6: Port numbers documented
test_port_numbers() {
    echo "Test 6: Port numbers documented..."
    local missing=0
    
    if ! grep -q "9500" "src/virons-security-mcp-server/README.md"; then
        echo -e "${RED}✗${NC} Port 9500 not in security README"
        ((missing++))
    fi
    
    if ! grep -q "9510" "src/virons-operations-mcp-server/README.md"; then
        echo -e "${RED}✗${NC} Port 9510 not in operations README"
        ((missing++))
    fi
    
    if ! grep -q "9520" "src/virons-monitoring-mcp-server/README.md"; then
        echo -e "${RED}✗${NC} Port 9520 not in monitoring README"
        ((missing++))
    fi
    
    if ! grep -q "9000" "src/virons-mcp-gateway/README.md"; then
        echo -e "${RED}✗${NC} Port 9000 not in gateway README"
        ((missing++))
    fi
    
    if [[ $missing -eq 0 ]]; then
        echo -e "${GREEN}✓${NC} All ports documented"
    else
        echo -e "${RED}✗${NC} $missing ports missing"
        ((ERRORS+=missing))
    fi
    echo
}

# Test 7: Code examples present
test_code_examples() {
    echo "Test 7: Code examples in root READMEs..."
    local missing=0
    
    for server in security operations monitoring; do
        file="src/virons-${server}-mcp-server/README.md"
        if ! grep -q '```bash' "$file" 2>/dev/null; then
            echo -e "${YELLOW}⚠${NC} No bash examples in $file"
            ((missing++))
        fi
    done
    
    if [[ $missing -eq 0 ]]; then
        echo -e "${GREEN}✓${NC} All READMEs have code examples"
    else
        echo -e "${YELLOW}⚠${NC} $missing READMEs missing examples"
        ((WARNINGS+=missing))
    fi
    echo
}

# Run all tests
test_readme_existence
test_no_placeholders
test_navigation_links
test_required_sections
test_mermaid_diagrams
test_port_numbers
test_code_examples

# Summary
echo "=================================="
echo "Summary:"
echo -e "Errors:   ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo

if [[ $ERRORS -eq 0 ]]; then
    echo -e "${GREEN}✓ All critical tests passed${NC}"
    exit 0
else
    echo -e "${RED}✗ $ERRORS critical issues found${NC}"
    exit 1
fi
