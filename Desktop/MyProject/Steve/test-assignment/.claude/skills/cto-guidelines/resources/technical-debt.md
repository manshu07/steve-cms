# Technical Debt Management

## What is Technical Debt?

Technical debt is the implied cost of additional rework caused by choosing an easy solution now instead of a better approach that would take longer.

## Types of Technical Debt

| Type | Description | Example |
|------|-------------|---------|
| Deliberate | Intentional shortcut | Skip tests to meet deadline |
| Accidental | Unintentional poor design | Learned better way later |
| Bit rot | Gradual decay | Dependencies outdated |
| Infrastructure | Tooling/deployment debt | Manual deployments |

## Tracking Technical Debt

### Debt Register
```markdown
# Technical Debt Register

| ID | Description | Impact | Effort | Priority | Status |
|----|-------------|--------|--------|----------|--------|
| TD-001 | No API tests | High | 2 weeks | P1 | In Progress |
| TD-002 | Legacy auth system | Medium | 4 weeks | P2 | Planned |
| TD-003 | Hardcoded configs | Low | 1 week | P3 | Backlog |
```

### Debt Score Formula
```
Debt Score = Impact × Urgency

Impact: 1-5 (Low to Critical)
Urgency: 1-5 (Not urgent to Blocking)
```

## Paying Down Debt

### Strategies

1. **The Scout Rule:** Leave code better than you found it
2. **Debt Sprints:** Dedicate sprints to debt reduction
3. **20% Time:** Allocate 20% of each sprint to debt
4. **New Feature Refactor:** Refactor related debt when adding features

### Debt Reduction Plan
```markdown
## Debt Item: TD-001 - No API Tests

### Current State
- 0% API test coverage
- Manual testing required for each release
- Frequent regressions

### Target State
- 80% API test coverage
- Automated CI/CD pipeline
- Regression testing automated

### Plan
| Week | Task | Owner |
|------|------|-------|
| 1 | Set up test framework | Team A |
| 2-3 | Write critical path tests | Team A |
| 4 | CI integration | DevOps |

### Investment
- Effort: 2 weeks
- ROI: Reduced bugs, faster releases
```

## Preventing Debt

### Code Review Checklist
- [ ] Tests included
- [ ] Documentation updated
- [ ] No hardcoded values
- [ ] Error handling complete
- [ ] Security reviewed

### Definition of Done
```markdown
## Definition of Done

- [ ] Code reviewed and approved
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] No critical debt introduced
- [ ] Deployed to staging
- [ ] QA verified
```

## Debt Review Process

### Monthly Debt Review
1. Review debt register
2. Update priorities
3. Assign owners
4. Plan debt sprints

### Metrics to Track
- Debt items count (trend)
- Debt resolution velocity
- New debt introduced per sprint
- % of time spent on debt