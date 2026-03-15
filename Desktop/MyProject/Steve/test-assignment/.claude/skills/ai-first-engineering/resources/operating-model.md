# AI-First Engineering Operating Model

## Principles

### 1. AI Generates, Humans Curate

```
Traditional: Human writes code, AI reviews
AI-First: AI generates code, humans curate and refine
```

### 2. Small Human Inputs, Large AI Outputs

```
Human: "Build a REST API for user management with CRUD operations"
AI: Generates (500+ lines):
  - Express routes
  - Middleware
  - Validation schemas
  - Error handling
  - Tests
  - Documentation
```

### 3. Iterative Refinement

```
Iteration 1: Generate basic implementation
Iteration 2: Add error handling
Iteration 3: Optimize performance
Iteration 4: Add edge cases
Iteration 5: Human review and polish
```

## Team Structure

### AI-First Team Roles

| Role | Human Responsibilities | AI Responsibilities |
|------|---------------------|-------------------|
| **Product Owner** | Define requirements, review outputs | Generate user stories, create specs |
| **AI Architect** | Design system architecture, validate decisions | Generate code, implement features |
| **Quality Curator** | Review code, test outputs, refine prompts | Generate tests, fix bugs, optimize |
| **Prompt Engineer** | Craft and optimize prompts | Execute prompts, generate variations |

### Workflow

```
1. Product Owner defines requirement
2. Prompt Engineer creates prompt template
3. AI Architect generates initial implementation
4. Quality Curator reviews and refines
5. Iterate until satisfied
```

## Prompt Templates

### Feature Development

```markdown
You are an AI-first engineer. Generate a complete implementation of:

Feature: [Description]

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Tech Stack:
- [Language/Framework]
- [Database]
- [Testing framework]

Output:
1. Implementation plan
2. Complete code
3. Tests
4. Documentation
5. Example usage

Constraints:
- Follow project coding standards
- Include error handling
- Write tests for all edge cases
- Add comments for complex logic
```

### Bug Fixing

```markdown
You are an AI-first engineer. Fix the following bug:

Error: [Error message]

Context:
- Code snippet: [code]
- Expected behavior: [description]
- Actual behavior: [description]

Output:
1. Root cause analysis
2. Fix implementation
3. Test to verify fix
4. Regression tests
```

### Refactoring

```markdown
You are an AI-first engineer. Refactor this code for:

Goals:
- [Goal 1: e.g., better performance]
- [Goal 2: e.g., improved readability]
- [Goal 3: e.g., reduced complexity]

Current Code:
[code]

Output:
1. Refactored code
2. Explanation of changes
3. Before/after comparison
4. Migration guide if breaking changes
```

## Quality Gates

### Human Review Points

1. **Requirements Review** (Before AI generation)
   - [ ] Requirements are clear
   - [ ] Acceptance criteria defined
   - [ ] Tech stack specified

2. **Output Review** (After AI generation)
   - [ ] Code meets requirements
   - [ ] Follows standards
   - [ ] Tests comprehensive
   - [ ] Documentation complete

3. **Integration Review** (Before commit)
   - [ ] Code reviewed by human
   - [ ] Tests passing
   - [ ] No breaking changes
   - [ ] Documentation updated

## Metrics

### Team Productivity

| Metric | Traditional | AI-First | Improvement |
|--------|-----------|----------|-------------|
| Features per week | 2-3 | 5-8 | 2-3x |
| Lines of code per day | 200-500 | 2000-5000 | 10x |
| Test coverage | 60-80% | 85-95% | +15-30% |
| Time to first draft | 1-2 days | 10-30 minutes | 50-100x |

### Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Bug rate | <5% post-review | Bugs found in production |
| Refactor needed | <20% | Code requiring human rewrite |
| Test pass rate | >95% | Automated tests passing |
| Human review time | <30 min/feature | Time spent in review |

## Best Practices

### 1. Start Small

```markdown
❌ Bad: "Build entire e-commerce platform"
✅ Good: "Build user registration endpoint"
```

### 2. Provide Context

```markdown
❌ Bad: "Add authentication"
✅ Good: "Add JWT authentication with email/password,
       store users in PostgreSQL, hash passwords with bcrypt"
```

### 3. Iterate

```markdown
Iteration 1: Basic implementation
Iteration 2: Add error handling
Iteration 3: Add logging
Iteration 4: Optimize performance
Iteration 5: Add documentation
```

### 4. Review Thoroughly

```markdown
Human review checklist:
- Security vulnerabilities
- Edge cases
- Error handling
- Performance issues
- Code style consistency
- Test coverage
- Documentation completeness
```

## Anti-Patterns

### ❌ Accept AI Output Without Review

```markdown
Bad: Generate code → Commit to production
Good: Generate code → Human review → Test → Deploy
```

### ❌ Unclear Requirements

```markdown
Bad: "Make it faster"
Good: "Optimize database queries to reduce API response
       time from 500ms to under 200ms"
```

### ❌ Over-Relying on AI for Architecture

```markdown
Bad: Let AI design entire system architecture
Good: Human designs architecture, AI implements components
```

## Transition Guide

### Moving from Traditional to AI-First

**Phase 1: Experimentation (Week 1-2)**
- Use AI for simple tasks (boilerplate, tests)
- Measure output quality
- Identify best practices

**Phase 2: Integration (Week 3-4)**
- Use AI for feature development
- Establish review process
- Create prompt templates

**Phase 3: Optimization (Week 5-6)**
- Refine prompts based on feedback
- Build prompt library
- Optimize human review process

**Phase 4: Full AI-First (Week 7+)**
- AI generates most code
- Humans focus on curation and architecture
- Continuous improvement of prompts

## Tooling

### Prompt Management

```markdown
# prompts/library/
feature-development.md
bug-fixing.md
refactoring.md
testing.md
documentation.md
```

### Version Control

```markdown
# AI-generated commits
git commit -m "feat: user authentication (AI-generated)

- AI generated: 90%
- Human reviewed and refined
- Prompt: prompts/library/feature-development.md
- Reviewed by: @human"
```

### Code Review Checklist

```markdown
## AI-Generated Code Review

- [ ] Requirements met
- [ ] Code follows standards
- [ ] Security review passed
- [ ] Tests comprehensive
- [ ] Documentation complete
- [ ] Performance acceptable
- [ ] No hardcoded values
- [ ] Error handling robust
- [ ] Edge cases covered

Reviewer: @human
Date: 2025-03-08
```

---

This resources file provides a comprehensive operating model for AI-first engineering teams.
