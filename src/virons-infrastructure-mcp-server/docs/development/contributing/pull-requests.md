# Pull Request Guidelines

**Version**: 1.0
**Last Updated**: 2026-03-07

## Overview

Guidelines for creating and reviewing pull requests for the Virons Infrastructure MCP Server.

## Before Creating a PR

### 1. Create an Issue
- Describe the problem or feature
- Get approval from maintainers
- Reference issue in PR

### 2. Create a Branch
```bash
# Feature branch
git checkout -b feature/add-new-tool

# Bug fix branch
git checkout -b fix/deployment-timeout

# Documentation branch
git checkout -b docs/update-readme
```

**Branch Naming**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test improvements

### 3. Make Changes
```bash
# Make your changes
vim virons/infrastructure_mcp_server/service.py

# Run tests
pytest tests/

# Format code
black virons/ tests/
isort virons/ tests/

# Type check
mypy virons/

# Lint
ruff check virons/ tests/
```

### 4. Commit Changes
```bash
# Atomic commits with clear messages
git add virons/infrastructure_mcp_server/service.py
git commit -m "feat: add support for Pulumi deployments"

git add tests/test_service.py
git commit -m "test: add tests for Pulumi integration"

git add docs/README.md
git commit -m "docs: document Pulumi support"
```

**Commit Message Format**:
```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `chore:` - Maintenance

**Example**:
```
feat: add Pulumi deployment support

Add support for deploying infrastructure using Pulumi.
Includes integration with pulumi-mcp-server and compliance
logging for all Pulumi operations.

Closes #123
```

## Creating a PR

### 1. Push Branch
```bash
git push origin feature/add-new-tool
```

### 2. Open PR on GitHub
- Use descriptive title
- Fill out PR template
- Link related issues
- Add labels
- Request reviewers

### 3. PR Template
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Changes Made
- Added Pulumi support
- Updated documentation
- Added tests

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Compliance logging added (if applicable)
- [ ] No breaking changes (or documented)
- [ ] Reviewed own code
```

## PR Requirements

### Code Quality
- ✅ All tests pass (88%+ coverage)
- ✅ Black formatted
- ✅ isort sorted
- ✅ mypy passes (strict mode)
- ✅ ruff passes (no warnings)
- ✅ No merge conflicts

### Documentation
- ✅ Docstrings for new functions
- ✅ README updated (if needed)
- ✅ CHANGELOG updated
- ✅ Architecture docs updated (if needed)

### Testing
- ✅ Unit tests for new code
- ✅ Integration tests (if applicable)
- ✅ Edge cases covered
- ✅ Error handling tested

### Compliance
- ✅ Compliance logging added (if infrastructure change)
- ✅ Audit trail verified
- ✅ Security reviewed
- ✅ No secrets in code

## PR Size Guidelines

### Small PR (Preferred)
- **Lines**: <200
- **Files**: <5
- **Review Time**: <30 minutes
- **Merge Time**: Same day

### Medium PR
- **Lines**: 200-500
- **Files**: 5-10
- **Review Time**: 1-2 hours
- **Merge Time**: 1-2 days

### Large PR (Avoid)
- **Lines**: >500
- **Files**: >10
- **Review Time**: >2 hours
- **Merge Time**: >2 days

**Tip**: Break large PRs into smaller ones.

## Review Process

### 1. Self-Review
Before requesting review:
- [ ] Read your own code
- [ ] Check for typos
- [ ] Verify tests pass
- [ ] Run linters
- [ ] Test manually

### 2. Automated Checks
CI/CD runs automatically:
- Unit tests
- Integration tests
- Code formatting (Black, isort)
- Type checking (mypy)
- Linting (ruff)
- Security scanning

### 3. Peer Review
**Reviewers check**:
- Code correctness
- Test coverage
- Documentation
- Security
- Performance
- Maintainability

**Review Turnaround**:
- Small PR: <24 hours
- Medium PR: <48 hours
- Large PR: <72 hours

### 4. Address Feedback
```bash
# Make requested changes
vim virons/infrastructure_mcp_server/service.py

# Commit changes
git add .
git commit -m "fix: address review feedback"

# Push updates
git push origin feature/add-new-tool
```

### 5. Approval
- Requires 1 approval (small changes)
- Requires 2 approvals (large changes, breaking changes)
- Platform lead approval (architecture changes)

## Reviewer Guidelines

### What to Look For

**Correctness**:
- Logic is correct
- Edge cases handled
- Error handling appropriate

**Testing**:
- Tests cover new code
- Tests are meaningful
- Edge cases tested

**Code Quality**:
- Follows style guide
- Clear and readable
- Well-documented
- No code smells

**Security**:
- No hardcoded secrets
- Input validation
- Proper error handling
- Compliance logging

**Performance**:
- No obvious bottlenecks
- Efficient algorithms
- Appropriate data structures

### How to Review

**1. Understand Context**:
- Read issue/description
- Understand the problem
- Review related code

**2. Review Code**:
```bash
# Checkout PR branch
git fetch origin
git checkout feature/add-new-tool

# Run tests
pytest tests/

# Test manually
python -m virons.infrastructure_mcp_server.server --transport stdio
```

**3. Leave Feedback**:
- Be constructive
- Explain reasoning
- Suggest improvements
- Approve or request changes

**4. Types of Comments**:
- **Blocking**: Must be fixed before merge
- **Non-blocking**: Nice to have
- **Question**: Seeking clarification
- **Praise**: Acknowledge good work

**Example Comments**:
```
Blocking: This function needs input validation to prevent injection attacks.

Non-blocking: Consider extracting this logic into a separate function for reusability.

Question: Why did you choose this approach over X?

Praise: Great test coverage! 👍
```

## Merging

### Merge Requirements
- ✅ All checks pass
- ✅ Required approvals received
- ✅ No merge conflicts
- ✅ Up to date with main branch

### Merge Strategy
```bash
# Squash and merge (preferred for feature branches)
git checkout main
git merge --squash feature/add-new-tool
git commit -m "feat: add Pulumi deployment support (#123)"

# Rebase and merge (for clean history)
git checkout feature/add-new-tool
git rebase main
git checkout main
git merge --ff-only feature/add-new-tool
```

**GitHub**: Use "Squash and merge" button

### After Merge
```bash
# Delete branch
git branch -d feature/add-new-tool
git push origin --delete feature/add-new-tool

# Update CHANGELOG
vim docs/reference/changelog.md
git add docs/reference/changelog.md
git commit -m "docs: update changelog for v1.1.0"
```

## Common Issues

### Merge Conflicts
```bash
# Update branch with main
git checkout feature/add-new-tool
git fetch origin
git rebase origin/main

# Resolve conflicts
vim <conflicted-file>
git add <conflicted-file>
git rebase --continue

# Force push (if already pushed)
git push --force-with-lease origin feature/add-new-tool
```

### Failed CI Checks
```bash
# Run checks locally
pytest tests/
black --check virons/ tests/
isort --check-only virons/ tests/
mypy virons/
ruff check virons/ tests/

# Fix issues
black virons/ tests/
isort virons/ tests/
ruff check --fix virons/ tests/

# Commit and push
git add .
git commit -m "fix: resolve CI issues"
git push origin feature/add-new-tool
```

### Stale Branch
```bash
# Update with main
git checkout feature/add-new-tool
git fetch origin
git merge origin/main

# Or rebase
git rebase origin/main

# Push updates
git push origin feature/add-new-tool
```

## PR Labels

| Label | Description |
|-------|-------------|
| `bug` | Bug fix |
| `feature` | New feature |
| `documentation` | Documentation update |
| `breaking-change` | Breaking change |
| `security` | Security fix |
| `performance` | Performance improvement |
| `needs-review` | Awaiting review |
| `work-in-progress` | Not ready for review |
| `blocked` | Blocked by other work |

## Examples

### Good PR
```
Title: feat: add Pulumi deployment support

Description:
Adds support for deploying infrastructure using Pulumi.

Changes:
- Add PulumiClient in infrastructure layer
- Update InfrastructureService to support Pulumi
- Add compliance logging for Pulumi operations
- Add unit and integration tests
- Update documentation

Testing:
- Unit tests: 95% coverage
- Integration tests: Pass
- Manual testing: Deployed test stack successfully

Closes #123
```

### Bad PR
```
Title: Updates

Description:
Made some changes.

Changes:
- Various updates
- Fixed stuff
- Added things

Testing:
- Tested locally
```

## Tips

✅ **Do**:
- Keep PRs small and focused
- Write clear descriptions
- Add tests
- Update documentation
- Respond to feedback promptly
- Be respectful in reviews

❌ **Don't**:
- Mix unrelated changes
- Skip tests
- Ignore review feedback
- Force push without warning
- Merge without approval
- Leave commented-out code

## Contact

- **Questions**: #development on Slack
- **PR Help**: platform@virons.ai
- **Urgent**: @platform-lead on Slack

## References

- [Code Style Guide](./code-style.md)
- [Testing Guide](../testing/unit-tests.md)
- [Architecture Documentation](../../architecture/)

---

**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
