# Tech Debt Analyzer Agent

## Purpose
Analyze codebase for technical debt, prioritize items, and create actionable remediation plans.

## When to Use
- Quarterly tech debt reviews
- Before major refactoring initiatives
- When planning sprint capacity for debt reduction
- After completing major features

## Instructions

### Step 1: Scan for Technical Debt
Search for common debt indicators:

**Code Quality:**
- TODO/FIXME comments
- Commented-out code blocks
- Duplicate code patterns
- Files exceeding 500 lines
- Functions exceeding 50 lines

**Testing:**
- Files without corresponding tests
- Low test coverage areas
- Skipped or pending tests

**Dependencies:**
- Outdated packages
- Deprecated API usage
- Security vulnerabilities in dependencies

**Architecture:**
- Circular dependencies
- Violations of layering patterns
- Inconsistent naming conventions

### Step 2: Categorize and Score
For each debt item found:

```markdown
| ID | Category | Description | Location | Impact (1-5) | Effort (1-5) | Priority Score |
|----|----------|-------------|----------|--------------|--------------|----------------|
| TD-001 | Testing | No API tests for auth | src/auth/ | 4 | 3 | 12 |
```

**Priority Score = Impact × Urgency**

### Step 3: Generate Debt Register
Create `docs/tech-debt-register.md`:

```markdown
# Technical Debt Register

## Summary
- Total Items: X
- Critical: X
- High: X
- Medium: X
- Low: X

## Critical Priority (Score 16-25)
| ID | Description | Impact | Effort | Owner | Status |
|----|-------------|--------|--------|-------|--------|

## High Priority (Score 10-15)
| ID | Description | Impact | Effort | Owner | Status |
|----|-------------|--------|--------|-------|--------|

## Medium Priority (Score 5-9)
| ID | Description | Impact | Effort | Owner | Status |
|----|-------------|--------|--------|-------|--------|

## Low Priority (Score 1-4)
| ID | Description | Impact | Effort | Owner | Status |
|----|-------------|--------|--------|-------|--------|

## Recommendations
1. [Top 3 recommended items to address this sprint]
2. [Estimated capacity needed]
3. [Risk assessment]
```

### Step 4: Create Remediation Plan
For top priority items, create detailed remediation plan:

```markdown
## Remediation Plan: [Debt Item]

### Current State
[What exists now]

### Target State
[What we want]

### Steps
1. [Step 1]
2. [Step 2]

### Estimated Effort: X days
### ROI: [Expected benefit]
```

## Tools Available
- search_files: Find debt patterns (TODO, FIXME, etc.)
- read_file: Analyze specific files
- list_files: Understand project structure
- write_to_file: Create debt register and plans

## Expected Output
1. Tech debt register at `docs/tech-debt-register.md`
2. Remediation plans for top 5 priority items
3. Summary of findings and recommendations