# Verification Loop Procedures and Templates

## Complete Verification Workflow

### Pre-Verification Checklist

Before running the verification loop, ensure:

- [ ] All changes are staged or committed
- [ ] Dependencies are installed (`npm install` or `pnpm install`)
- [ ] Environment variables are set (if needed for tests)
- [ ] Database/services are running (if needed for tests)
- [ ] No uncommitted changes in config files

---

## Phase 1: Build Verification

### Frontend Build (Next.js)

```bash
# Check build output
npm run build 2>&1 | tee build-output.log

# Check last 30 lines for errors
npm run build 2>&1 | tail -30

# Check for specific error patterns
npm run build 2>&1 | grep -i "error" | head -20

# Check build time (should be < 2min for small projects)
time npm run build
```

**What to Look For:**
- TypeScript compilation errors
- Module resolution failures
- Bundle size warnings
- Static generation failures
- Environment variable missing errors

**Common Issues:**

❌ **Error: "Cannot find module"**
```bash
# Fix: Install missing dependency
npm install missing-package
```

❌ **Error: "Type X is not assignable to type Y"**
```bash
# Fix: Run type check to see full error
npx tsc --noEmit
```

❌ **Error: "Environment variable not defined"**
```bash
# Fix: Add to .env.local
echo "VARIABLE_NAME=value" >> .env.local
```

### Backend Build (Node.js/Express)

```bash
# Check if TypeScript compiles
npx tsc 2>&1 | head -30

# Check if dist folder is created
ls -la dist/ | head -10

# Verify build output
node -e "require('./dist/index.js')"
```

### Monorepo Build

```bash
# Build all packages
npm run build 2>&1 | tee build.log

# Check specific package
cd apps/web && npm run build

# Check build status of all workspaces
npm run build -- --workspaces 2>&1 | grep -E "(✓|✗)"
```

---

## Phase 2: Type Check

### TypeScript Full Check

```bash
# Full type check
npx tsc --noEmit 2>&1 | tee typecheck.log

# Show first 30 errors
npx tsc --noEmit 2>&1 | head -30

# Count total errors
npx tsc --noEmit 2>&1 | grep "error TS" | wc -l

# Filter by severity
npx tsc --noEmit 2>&1 | grep "error TS" | grep -i "strict" # Strict mode errors
npx tsc --noEmit 2>&1 | grep "error TS" | grep -i "implicit" # Implicit any errors
```

**Common TypeScript Errors:**

| Error | Fix |
|-------|-----|
| `TS2307: Cannot find module` | Install missing dependency or check import path |
| `TS2345: Argument of type X is not assignable to Y` | Type mismatch - check types or add type assertion |
| `TS2532: Object is possibly 'undefined'` | Add null check or use non-null assertion |
| `TS2339: Property 'x' does not exist on type Y` | Add property to type or use interface |

### Project-Specific Type Checks

```bash
# Check specific file
npx tsc --noEmit src/components/Button.tsx

# Check specific directory
npx tsc --noEmit apps/web/**/*.tsx 2>&1 | head -20

# Exclude test files
npx tsc --noEmit --skipLibCheck 2>&1 | grep -v ".test." | head -30
```

---

## Phase 3: Lint Check

### ESLint

```bash
# Run ESLint
npm run lint 2>&1 | tee lint.log

# Show errors only (ignore warnings)
npm run lint 2>&1 | grep "error"

# Count errors and warnings
npm run lint 2>&1 | grep -E "✖ ([0-9]+):" | wc -l

# Check specific file
npx eslint src/components/Button.tsx

# Fix auto-fixable issues
npm run lint:fix
```

**Common ESLint Errors:**

| Error | Fix |
|-------|-----|
| `no-unused-vars` | Remove unused variable or prefix with `_` |
| `no-console` | Remove console.log or use logger |
| `react-hooks/exhaustive-deps` | Add missing dependencies to useEffect |
| `@typescript-eslint/no-explicit-any` | Replace `any` with specific type |

### Prettier Check

```bash
# Check formatting
npx prettier --check "src/**/*.{ts,tsx}" 2>&1 | head -20

# Auto-fix formatting
npx prettier --write "src/**/*.{ts,tsx}"

# Check specific file
npx prettier --check src/App.tsx
```

### Python Linting (ruff)

```bash
# Run ruff
ruff check . 2>&1 | tee ruff.log

# Auto-fix issues
ruff check --fix .

# Check specific file
ruff check src/main.py
```

---

## Phase 4: Test Suite

### Unit Tests

```bash
# Run all tests
npm test 2>&1 | tee test-output.log

# Run with coverage
npm run test:coverage 2>&1 | tee coverage.log

# Run specific test file
npm test Button.test.tsx

# Run tests matching pattern
npm test -- --testNamePattern="Button"

# Run in watch mode
npm test -- --watch
```

### Parse Test Output

```bash
# Extract summary
npm test 2>&1 | grep -A 5 "Test Suites:"
npm test 2>&1 | grep -E "(Tests:|Snapshots:|Time:)"

# Check for failed tests
npm test 2>&1 | grep -B 5 "FAIL"

# Count tests
npm test 2>&1 | grep "✓" | wc -l  # Passed
npm test 2>&1 | grep "✕" | wc -l  # Failed
```

### Coverage Report

```bash
# Show coverage summary
npm run test:coverage 2>&1 | grep -A 10 "Coverage summary"

# Check if 80% threshold met
npm run test:coverage 2>&1 | grep -E "All files[^|]*\|" | awk '{print $6}' | sed 's/%//' | awk '{if($1<80) print "FAIL"; else print "PASS"}'

# Generate HTML report
npm run test:coverage -- --coverageReporters=html
open coverage/index.html  # macOS
xdg-open coverage/index.html  # Linux
```

**Coverage Thresholds:**

| Metric | Target | Command |
|--------|--------|---------|
| Statements | 80% | `coverage report --include="**/*.{ts,tsx}"` |
| Branches | 80% | `npx jest --coverage --coverageThreshold='{"global":{"branches":80}}'` |
| Functions | 80% | Check coverage report |
| Lines | 80% | Check coverage report |

### Integration Tests

```bash
# Run integration tests only
npm test -- --testPathPattern=".integration."

# Run with test database
TEST_DB=test_db npm test

# Run API tests
npm test apps/api/src/**/*.test.ts
```

### E2E Tests

```bash
# Run all E2E tests
npm run test:e2e 2>&1 | tee e2e-output.log

# Run specific test file
npx playwright test e2e/trading-flow.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed

# Debug mode
npx playwright test --debug

# Run specific test
npx playwright test --grep "trading workflow"
```

---

## Phase 5: Security Scan

### Secret Scanning

```bash
# Check for API keys
grep -rn "sk-" --include="*.ts" --include="*.js" --include="*.tsx" . 2>/dev/null | grep -v "node_modules" | grep -v ".git"

# Check for API key patterns
grep -rn "api_key\|API_KEY\|apikey" --include="*.ts" --include="*.js" . 2>/dev/null | grep -v "node_modules"

# Check for tokens
grep -rn "token\|Token\|TOKEN" --include="*.ts" --include="*.js" . 2>/dev/null | grep -v "node_modules"

# Check for passwords
grep -rn "password\|Password\|PASSWORD" --include="*.ts" --include="*.js" . 2>/dev/null | grep -v "node_modules"

# Check for secret strings
grep -rn "secret\|Secret\|SECRET" --include="*.ts" --include="*.js" . 2>/dev/null | grep -v "node_modules"
```

### Debug Code Check

```bash
# Check for console.log
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | wc -l

# Show all console.log locations
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null

# Check for debugger statements
grep -rn "debugger" --include="*.ts" --include="*.js" . 2>/dev/null | grep -v "node_modules"

# Check for TODO comments
grep -rn "TODO\|FIXME\|XXX\|HACK" --include="*.ts" --include="*.tsx" src/ 2>/dev/null
```

### Dependency Vulnerability Scan

```bash
# Check for vulnerabilities
npm audit 2>&1 | tee audit.log

# Check for high/critical vulnerabilities
npm audit --audit-level=high

# Auto-fix vulnerabilities
npm audit fix

# Check production dependencies only
npm audit --production
```

### Additional Security Checks

```bash
# Check for eval() usage (dangerous)
grep -rn "eval(" --include="*.ts" --include="*.js" src/ 2>/dev/null

# Check for innerHTML (XSS risk)
grep -rn "innerHTML" --include="*.ts" --include="*.tsx" src/ 2>/dev/null

# Check for dangerous imports
grep -rn "dangerouslySetInnerHTML" --include="*.tsx" src/ 2>/dev/null

# Check for hardcoded credentials
grep -rnE "(mongodb://|postgres://|mysql://|redis://)" --include="*.ts" --include="*.js" src/ 2>/dev/null
```

---

## Phase 6: Diff Review

### Git Diff Commands

```bash
# Show summary of changes
git diff --stat

# Show files changed
git diff --name-only

# Show files changed with status
git diff --name-status

# Show detailed diff
git diff

# Show diff of specific file
git diff src/components/Button.tsx

# Show staged changes
git diff --staged

# Show last commit diff
git diff HEAD~1
```

### Diff Analysis

```bash
# Count lines added/removed
git diff --shortstat

# Show most changed files
git diff --stat | sort -k2 -nr | head -10

# Check for large files (>100 lines changed)
git diff --stat | awk '$4 > 100 {print $0}'

# Show deleted files
git diff --diff-filter=D --name-only

# Show new files
git diff --diff-filter=A --name-only
```

### Review Checklist

For each changed file, verify:

**Code Quality:**
- [ ] No unused imports
- [ ] No commented-out code
- [ ] No console.log or debug statements
- [ ] Consistent code style with rest of file
- [ ] Proper error handling
- [ ] Edge cases handled

**Type Safety:**
- [ ] No `any` types (unless documented)
- [ ] Proper type definitions for functions
- [ ] Null checks where needed
- [ ] Interface exports are stable

**Testing:**
- [ ] Tests added for new features
- [ ] Tests updated for changed behavior
- [ ] No skipped or disabled tests
- [ ] Test coverage not decreased

**Security:**
- [ ] No hardcoded secrets
- [ ] No dangerous patterns (eval, innerHTML)
- [ ] Proper input validation
- [ ] SQL injection prevention (no string concatenation in queries)

**Performance:**
- [ ] No unnecessary re-renders (React)
- [ ] No memory leaks (cleanup in useEffect)
- [ ] Efficient data fetching (caching, debouncing)
- [ ] No large bundle size increases

---

## Complete Verification Script

### Automated Verification Script

Create `verify.sh`:

```bash
#!/bin/bash

echo "🔍 VERIFICATION REPORT"
echo "====================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
ALL_PASS=true

# Phase 1: Build
echo -n "Build: "
if npm run build > /dev/null 2>&1; then
  echo -e "${GREEN}PASS${NC}"
  BUILD_STATUS="PASS"
else
  echo -e "${RED}FAIL${NC}"
  BUILD_STATUS="FAIL"
  ALL_PASS=false
fi

# Phase 2: Type Check
echo -n "Types: "
TYPE_ERRORS=$(npx tsc --noEmit 2>&1 | grep "error TS" | wc -l | tr -d ' ')
if [ "$TYPE_ERRORS" -eq 0 ]; then
  echo -e "${GREEN}PASS${NC} (0 errors)"
  TYPE_STATUS="PASS"
else
  echo -e "${RED}FAIL${NC} ($TYPE_ERRORS errors)"
  TYPE_STATUS="FAIL"
  ALL_PASS=false
fi

# Phase 3: Lint
echo -n "Lint: "
LINT_ERRORS=$(npm run lint 2>&1 | grep "error" | wc -l | tr -d ' ')
if [ "$LINT_ERRORS" -eq 0 ]; then
  echo -e "${GREEN}PASS${NC} (0 errors)"
  LINT_STATUS="PASS"
else
  echo -e "${YELLOW}WARN${NC} ($LINT_ERRORS errors)"
  LINT_STATUS="WARN"
fi

# Phase 4: Tests
echo -n "Tests: "
TEST_OUTPUT=$(npm test -- --passWithNoTests 2>&1)
if echo "$TEST_OUTPUT" | grep -q "0 failures"; then
  TESTS_PASSED=$(echo "$TEST_OUTPUT" | grep -oP '\d+(?= passed)' | head -1)
  COVERAGE=$(npm run test:coverage 2>&1 | grep -oP '\d+(?=%)' | head -1)
  echo -e "${GREEN}PASS${NC} ($TESTS_PASSED passed, ${COVERAGE}% coverage)"
  TEST_STATUS="PASS"
else
  echo -e "${RED}FAIL${NC}"
  TEST_STATUS="FAIL"
  ALL_PASS=false
fi

# Phase 5: Security
echo -n "Security: "
SECRETS=$(grep -rn "sk-\|api_key\|API_KEY" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | wc -l | tr -d ' ')
if [ "$SECRETS" -eq 0 ]; then
  echo -e "${GREEN}PASS${NC} (0 secrets found)"
  SECURITY_STATUS="PASS"
else
  echo -e "${RED}FAIL${NC} ($SECRETS potential secrets)"
  SECURITY_STATUS="FAIL"
  ALL_PASS=false
fi

# Phase 6: Diff
echo -n "Diff: "
FILES_CHANGED=$(git diff --name-only | wc -l | tr -d ' ')
echo "$FILES_CHANGED files changed"

# Overall Status
echo ""
if [ "$ALL_PASS" = true ]; then
  echo -e "Overall: ${GREEN}READY${NC} for PR ✅"
  exit 0
else
  echo -e "Overall: ${RED}NOT READY${NC} for PR ❌"
  echo ""
  echo "Issues to Fix:"
  [ "$BUILD_STATUS" = "FAIL" ] && echo "  - Build is failing"
  [ "$TYPE_STATUS" = "FAIL" ] && echo "  - Type errors detected"
  [ "$TEST_STATUS" = "FAIL" ] && echo "  - Tests are failing"
  [ "$SECURITY_STATUS" = "FAIL" ] && echo "  - Security issues found"
  exit 1
fi
```

**Usage:**

```bash
# Make script executable
chmod +x verify.sh

# Run verification
./verify.sh
```

---

## Verification Report Templates

### Minimal Report

```
VERIFICATION REPORT
==================

Build:     PASS
Types:     PASS (0 errors)
Lint:      PASS (3 warnings - auto-fixable)
Tests:     PASS (42/42 passed, 85% coverage)
Security:  PASS (0 issues)
Diff:      3 files changed

Overall:   READY for PR ✅

Changed Files:
- src/components/Button.tsx (added loading state)
- src/components/Button.test.tsx (added tests)
- src/hooks/useButton.ts (refactored)
```

### Detailed Report

```
🔍 VERIFICATION REPORT
=====================

Phase 1: Build
─────────────────────────────────────────────
Status: ✅ PASS
Duration: 45s
Bundle size: 145KB (gzip: 42KB)

Phase 2: Type Check
─────────────────────────────────────────────
Status: ✅ PASS
Errors: 0
Files checked: 142

Phase 3: Lint
─────────────────────────────────────────────
Status: ⚠️  WARN
Errors: 0
Warnings: 3
  - src/App.tsx:15:25 - Unused variable 'data' (fixable)
  - src/utils/format.ts:42:10 - Missing return type (fixable)
  - src/components/Header.tsx:8:5 - Prefer const (fixable)

Fix: npm run lint:fix

Phase 4: Tests
─────────────────────────────────────────────
Status: ✅ PASS
Total: 47 tests
Passed: 47
Failed: 0
Skipped: 0
Coverage: 87.3%

Coverage by Type:
  - Statements: 89.2%
  - Branches: 82.1%
  - Functions: 91.5%
  - Lines: 87.3%

Phase 5: Security
─────────────────────────────────────────────
Status: ✅ PASS
Secrets found: 0
Console.log: 0
Dangerous patterns: 0
Vulnerabilities: 0 (npm audit)

Phase 6: Diff Review
─────────────────────────────────────────────
Files changed: 5
Lines added: 127
Lines removed: 43

Changes:
  M src/components/Button.tsx (+45, -12)
    Added loading state
    Added error boundary
    Improved type safety

  M src/components/Button.test.tsx (+38, -5)
    Added loading state tests
    Added error handling tests
    Coverage increased to 92%

  M src/hooks/useButton.ts (+28, -18)
    Refactored for better performance
    Fixed memory leak
    Added cleanup

  M package-lock.json (+2, -2)
    Updated dependencies

  M README.md (+14, -6)
    Updated documentation

Quality Assessment:
  ✅ No unused imports
  ✅ No commented code
  ✅ No console.log
  ✅ Proper error handling
  ✅ Edge cases covered
  ✅ Tests added
  ✅ No security issues
  ✅ Performance improved

─────────────────────────────────────────────
OVERALL STATUS: ✅ READY FOR PR

Recommendations:
1. Run `npm run lint:fix` to auto-fix 3 lint warnings
2. Consider adding E2E test for Button loading state
3. Package update is safe (no breaking changes)

Confidence Level: HIGH
```

### Failure Report

```
🔍 VERIFICATION REPORT
=====================

Phase 1: Build
─────────────────────────────────────────────
Status: ❌ FAIL
Error: Module not found: Error: Can't resolve './missing-module'

Location: src/components/Header.tsx:12

Fix: Install missing dependency or correct import path

Phase 2: Type Check
─────────────────────────────────────────────
Status: ❌ FAIL
Errors: 5

src/components/Button.tsx:23:5
  Type 'string' is not assignable to type 'number'

src/utils/format.ts:45:10
  Property 'toISOString' does not exist on type 'undefined'

[3 more errors]

Phase 3: Lint
─────────────────────────────────────────────
Status: ⚠️  WARN
Errors: 2
Warnings: 7

Critical:
  - src/api/auth.ts:18:12 - Unhandled promise rejection
  - src/hooks/useData.ts:34:8 - Missing error handling

Phase 4: Tests
─────────────────────────────────────────────
Status: ❌ FAIL
Total: 47 tests
Passed: 42
Failed: 5
Coverage: 74.3%

Failed Tests:
  ❌ Button Component › should handle loading state
  ❌ Button Component › should call onClick when clicked
  ❌ API › POST /api/users should return 201
  ❌ Auth › login should validate credentials
  ❌ Utils › formatDate should handle null input

Phase 5: Security
─────────────────────────────────────────────
Status: ❌ FAIL
Issues: 3

Secrets found:
  - src/config/api.ts:8 - Hardcoded API key
  - .env.local - Committed file (should be in .gitignore)

Console.log:
  - src/components/Header.tsx:15 - console.log user object
  - src/utils/logger.ts:23 - console.debug in production

Phase 6: Diff Review
─────────────────────────────────────────────
Files changed: 8
Lines added: 234
Lines removed: 89

Concerns:
  - Large refactor in single commit (consider splitting)
  - Missing tests for new feature
  - Breaking change in API (not documented)

─────────────────────────────────────────────
OVERALL STATUS: ❌ NOT READY FOR PR

Critical Issues (Must Fix):
1. ❌ Build failure - missing module import
2. ❌ 5 TypeScript errors
3. ❌ 5 failing tests
4. ❌ Hardcoded API key (security risk)
5. ❌ Coverage below 80% threshold

Recommended Actions:
1. Fix import error in Header.tsx
2. Resolve all TypeScript errors
3. Fix failing tests
4. Remove API key, use environment variable
5. Add tests for new code to reach 80% coverage
6. Remove console.log statements
7. Add .env.local to .gitignore
8. Consider splitting large refactor into smaller commits

Confidence Level: LOW
Do not merge until critical issues are resolved.
```

---

## Integration with CI/CD

### GitHub Actions Workflow

```yaml
# .github/workflows/verify.yml
name: Verification

on:
  pull_request:
    branches: [main]

jobs:
  verify:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Type Check
        run: npx tsc --noEmit

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm run test:coverage

      - name: Security Scan
        run: |
          if grep -rn "sk-\|api_key" --include="*.ts" src/; then
            echo "Secrets found!"
            exit 1
          fi

      - name: Coverage Check
        run: |
          COVERAGE=$(npm run test:coverage 2>&1 | grep -oP '\d+(?=%)' | head -1)
          if [ "$COVERAGE" -lt 80 ]; then
            echo "Coverage ${COVERAGE}% is below 80% threshold"
            exit 1
          fi

      - name: Post Status
        if: always()
        uses: actions/github-script@v6
        with:
          script: |
            const status = '${{ job.status }}'
            const comment = `Verification: ${status === 'success' ? '✅ PASS' : '❌ FAIL'}`
            // Post comment on PR
```

### Pre-Commit Hook

```bash
#!/bin/bash
# .husky/pre-commit

echo "Running verification..."

# Quick checks before commit
npm run lint:fix || echo "⚠️  Lint issues (auto-fixed where possible)"
npx tsc --noEmit || { echo "❌ Type errors detected"; exit 1; }
npm test -- --passWithNoTests || { echo "❌ Tests failing"; exit 1; }

# Quick secret scan
if grep -rn "sk-\|api_key" --include="*.ts" src/ 2>/dev/null; then
  echo "❌ Potential secrets detected"
  exit 1
fi

echo "✅ Verification passed"
```

---

This procedures file provides comprehensive verification workflows with scripts, templates, and CI/CD integration for the verification-loop skill.
