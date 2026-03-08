# Git Hooks Documentation

## Overview

Automated validation hooks ensuring code quality, DDD structure, TDD compliance, and documentation standards.

## Installation

```bash
# Install all hooks
./scripts/install-hooks.sh

# Manual installation
cp scripts/hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

## Pre-Push Hook

Runs 7 validation checks before allowing push:

### 1. DDD Structure Validation ✅

Ensures all MCP servers follow Domain-Driven Design:

```
virons/[server]_mcp_server/
├── application/     # Use cases & orchestration
├── domain/          # Business logic & entities
└── infrastructure/  # External integrations
```

**Blocks push if:** DDD directories missing

### 2. TDD Compliance ✅

Validates test-driven development practices:

- Tests directory exists for each server
- Test files present (test_*.py)
- pytest configuration exists

**Blocks push if:** Tests directory missing  
**Warns if:** No test files found

### 3. Documentation Quality ✅

Checks README completeness:

- All servers have root README.md
- Required sections present:
  - ## Overview
  - ## Architecture
  - ## Tools
  - ## Usage
- No placeholder text (TODO, FIXME, XXX)

**Blocks push if:** Missing READMEs or required sections  
**Warns if:** Placeholders found

### 4. Forensic Services Compliance ⚠️

Validates forensic services (ports 9300-9415):

**Rule 1:** `calculation_audit()` before `forensic_flags`
```python
# ✓ Correct
calculation_audit(transaction)
forensic_flags = detect_anomalies(transaction)

# ✗ Wrong
forensic_flags = detect_anomalies(transaction)
calculation_audit(transaction)
```

**Rule 2:** ML gate pattern
```python
# ✓ Correct
gated_ml = ml_score if len(deterministic_flags) >= 1 else 0.0
```

**Rule 3:** `write_audit()` on all write paths
```python
# ✓ Correct
def create_transaction(data):
    result = db.insert(data)
    write_audit()
    return result
```

**Warns if:** Patterns not found

### 5. ML Services Compliance 🤖

Validates ML services (ports 9420-9424) for EU AI Act:

**High-risk AI systems require:**
- MODEL_CARD.md documentation
- Nonlinear fusion pattern: `S' = 1 - prod(1 - s_i)`

**Services checked:**
- anomaly-detector
- grandmaster-service

**Blocks push if:** MODEL_CARD.md missing for high-risk AI  
**Warns if:** Fusion pattern not found

### 6. Code Quality ✅

Validates Python code:

- Syntax errors (py_compile)
- Anti-patterns:
  - `print()` statements (use logging)
  - Hardcoded credentials
  - SQL injection risks

**Blocks push if:** Syntax errors  
**Warns if:** Anti-patterns found

### 7. Port Namespace Validation 🔌

Validates port assignments:

| Service | Port Range |
|---------|------------|
| Infrastructure | 9100 |
| Security | 9500 |
| Operations | 9510 |
| Monitoring | 9520 |
| Forensic | 9300-9415 |
| ML | 9420-9424 |

**Warns if:** Port not found in config

## Exit Codes

- **0**: All validations passed
- **1**: Critical errors (push blocked)
- **2**: Script error

## Bypassing Hook

```bash
# Not recommended - only for emergencies
git push --no-verify
```

## Thresholds

- **Errors > 0**: Push blocked
- **Warnings > 5**: Push allowed with warning
- **Warnings ≤ 5**: Push allowed silently

## Example Output

```
🔍 Pre-Push Validation
======================

[1/7] DDD Structure...
✓ DDD structure valid

[2/7] TDD Compliance...
✓ TDD structure valid

[3/7] Documentation Quality...
⚠ 2 READMEs with placeholders
✓ Documentation valid

[4/7] Forensic Services Compliance...
✓ Forensic compliance checked

[5/7] ML Services Compliance...
✓ ML compliance valid

[6/7] Code Quality...
✓ Code quality valid

[7/7] Port Namespace Validation...
✓ Port namespaces checked

======================
Summary:
Errors:   0
Warnings: 1

✓ All validations passed
```

## Maintenance

### Adding New Checks

Edit `scripts/hooks/pre-push`:

```bash
validate_new_check() {
    echo -e "${BLUE}[8/8] New Check...${NC}"
    local issues=0
    
    # Your validation logic
    
    if [[ $issues -eq 0 ]]; then
        echo -e "${GREEN}✓${NC} Check passed"
    else
        echo -e "${RED}✗${NC} $issues issues"
        ((ERRORS+=issues))
    fi
    echo
}

# Add to execution
validate_new_check
```

### Updating Thresholds

```bash
# Change warning threshold
if [[ $WARNINGS -gt 5 ]]; then  # Change 5 to desired value
```

## Related Scripts

- `scripts/verify-docs.sh` - Standalone documentation verification
- `scripts/install-hooks.sh` - Hook installer
- `scripts/extract-server-metadata.sh` - Server metadata extraction

## Troubleshooting

**Hook not running:**
```bash
# Check hook is executable
ls -la .git/hooks/pre-push

# Reinstall
./scripts/install-hooks.sh
```

**False positives:**
```bash
# Check specific validation
.git/hooks/pre-push | grep "Test X"

# Review validation logic
cat scripts/hooks/pre-push | grep -A20 "validate_X"
```

**Performance issues:**
```bash
# Time each validation
time .git/hooks/pre-push
```

## Best Practices

1. **Run locally before push:**
   ```bash
   .git/hooks/pre-push
   ```

2. **Fix errors immediately** - Don't accumulate technical debt

3. **Keep warnings low** - Aim for 0 warnings

4. **Update hook regularly** - Pull latest from main branch

5. **Document exceptions** - Use comments for legitimate bypasses

## Navigation

← [Scripts](../)  
→ [Verification Script](../verify-docs.sh)  
→ [Installation Script](../install-hooks.sh)
