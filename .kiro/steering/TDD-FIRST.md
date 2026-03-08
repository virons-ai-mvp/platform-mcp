# TDD-FIRST — Critical Development Rule

**ALWAYS LOADED FIRST — READ THIS BEFORE ANY CODE CHANGES**

## The Golden Rule

```
🔴 WRITE TEST FIRST → 🟢 WRITE CODE TO PASS → 🔵 REFACTOR
```

## TDD Workflow (MANDATORY)

1. **Write failing test** — define expected behavior
2. **Run test** — verify it fails (red)
3. **Write minimal code** — make test pass (green)
4. **Run test** — verify it passes
5. **Refactor** — improve code while keeping tests green
6. **Repeat** — for each new feature or bug fix

## Coverage Requirements

- **Minimum**: 95% coverage
- **Unit tests**: isolated components with mocks
- **Integration tests**: service interactions with testcontainers
- **Comprehensive tests**: edge cases, error scenarios, end-to-end

## Quick Commands

```bash
make test                    # run all tests
make test-unit              # unit tests only
make test-integration       # integration tests only
make test-coverage          # coverage report
```

## Reference Documentation

- `docs/TESTING-STRATEGY.md` — comprehensive testing patterns
- `docs/TESTING-QUICKSTART.md` — quick start guide
- `docs/TDD-FINAL-SUMMARY.md` — TDD implementation summary

## Before Writing ANY Code

1. ✅ Do tests exist for this feature/fix?
2. ✅ If no → write tests FIRST
3. ✅ If yes → run tests to verify current behavior
4. ✅ Write minimal code to pass tests
5. ✅ Refactor while keeping tests green

**NO EXCEPTIONS — TDD IS NON-NEGOTIABLE**
