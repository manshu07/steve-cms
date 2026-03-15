# Agent-Skill Orchestration Patterns

Guide for orchestrating agents and skills together for complex workflows.

---

## Overview

Agents and skills can work together in powerful ways:
- **Agents** execute complex multi-step tasks
- **Skills** provide domain-specific guidance
- **Orchestration** coordinates their interactions

---

## Orchestration Patterns

### Pattern 1: Skill Guides, Agent Executes

**Use When:** You need to learn a pattern, then apply it at scale

```
1. SKILL teaches you the approach
2. YOU implement the initial version
3. AGENT applies it to remaining codebase
```

**Example: Adding Error Tracking**

```bash
# Step 1: Learn from skill
You: "How do I add Sentry to this controller?"
→ error-tracking skill activates
→ Provides: Pattern with BaseController, captureException

# Step 2: Implement with guidance
You: Add error handling to one controller
→ Skill guides the implementation

# Step 3: Scale with agent
You: "Add Sentry error tracking to all remaining controllers"
→ auto-error-resolver agent launches
→ Agent: Applies pattern to all controllers
→ Returns: Report of files modified
```

### Pattern 2: Agent Discovers, Skill Explains

**Use When:** Agent finds issues, skill provides solutions

```
1. AGENT scans codebase
2. AGENT identifies issues
3. SKILL explains root causes and patterns
4. YOU implement fixes
```

**Example: Performance Issues**

```bash
# Step 1: Agent discovery
You: "Find performance issues in the codebase"
→ Agent: Could use specialized agent
→ Agent: Identifies N+1 queries, missing indexes

# Step 2: Skill explanation
You: "How do I fix N+1 queries?"
→ performance-optimization skill activates
→ Provides: Explanation, solutions, code examples

# Step 3: You implement
You: Apply the pattern with skill guidance
```

### Pattern 3: Skill Validates, Agent Executes

**Use When:** Validation before expensive operations

```
1. SKILL validates approach
2. AGENT executes the work
3. SKELL verifies results
```

**Example: Database Migration**

```bash
# Step 1: Skill validation
You: "I want to add a new column to the users table"
→ database-verification skill (hypothetical)
→ Validates: Column name, type, migration safety

# Step 2: Agent execution
You: "Create and run the migration"
→ database-migration agent (hypothetical)
→ Executes: Migration with rollback plan

# Step 3: Skill verification
You: "Verify the migration worked"
→ skill: Provides verification queries
```

### Pattern 4: Agent-Skill-Agent Pipeline

**Use When:** Multi-stage workflow

```
1. AGENT: Discovery and analysis
2. SKILL: Guidance for solution design
3. AGENT: Implementation
4. AGENT: Testing and verification
```

**Example: Complete Feature Development**

```bash
# Stage 1: Discovery
Agent: code-architecture-reviewer
→ Analyzes: Current codebase structure
→ Returns: Recommendations

# Stage 2: Design
Skill: backend-dev-guidelines (or cto-guidelines)
→ Provides: Architecture patterns
→ You: Design the approach

# Stage 3: Implementation
Agent: code-refactor-master
→ Implements: The refactoring
→ Returns: Modified files

# Stage 4: Testing
Agent: auth-route-tester
→ Tests: All affected routes
→ Returns: Test results
```

---

## Complex Workflow Examples

### Workflow 1: Security Audit

**Objective:** Audit codebase for security vulnerabilities

```
Step 1: Agent Discovery
├── Agent: security-scanner (hypothetical)
└── Output: List of files with potential issues

Step 2: Skill Analysis
├── Skill: security-guidelines
└── Action: Review each issue, get remediation patterns

Step 3: Implementation
├── You: Implement fixes with skill guidance
└── Agent: auto-error-resolver (if applicable)

Step 4: Verification
├── Agent: Run security tests
└── Output: Final security report
```

### Workflow 2: API Development

**Objective:** Create a new API endpoint

```
Step 1: Design
├── Skill: backend-dev-guidelines
└── Output: Controller pattern, validation approach

Step 2: Implementation
├── You: Implement the route
└── Skill: error-tracking
└── Action: Add error handling

Step 3: Testing
├── Agent: route-tester
└── Output: Test results

Step 4: Documentation
├── Agent: documentation-architect
└── Output: API documentation
```

### Workflow 3: Performance Optimization

**Objective:** Optimize slow application

```
Step 1: Profiling
├── Tool: Performance profiler
└── Output: Bottleneck identification

Step 2: Analysis
├── Skill: performance-optimization
└── Output: Optimization strategies

Step 3: Implementation
├── You: Apply optimizations
└── Skill: Continues to guide

Step 4: Verification
├── Tool: Benchmark comparison
└── Output: Performance improvement report
```

---

## When to Orchestrate

### Single Agent or Skill?

**Use Just One:**
- Simple, single-step tasks
- Straightforward questions
- Quick reference needed

**Orchestrate:**
- Multi-step workflows
- Learning + applying at scale
- Validation + execution
- Discovery + implementation

### Decision Guide

```
Can one tool do it?
├── Yes → Use single tool
└── No → Orchestrate multiple tools

Need to learn first?
├── Yes → Skill → You → Agent
└── No → Agent directly

Need validation?
├── Yes → Skill validates → Agent executes
└── No → Agent executes directly

Complex workflow?
├── Yes → Multi-stage orchestration
└── No → Single tool
```

---

## Orchestration Tips

### 1. Start with Skills

**Why:** Skills are faster and interactive

```
Good:
1. Ask skill for pattern
2. Implement yourself
3. Use agent to scale

Bad:
1. Jump straight to agent
2. Waste time on simple tasks
```

### 2. Validate Before Scaling

**Why:** Agents make mistakes at scale

```
Good:
1. Implement with skill guidance
2. Test manually
3. Then use agent for rest

Bad:
1. Let agent loose on entire codebase
2. Fix hundreds of mistakes
```

### 3. Use Agents for Repetition

**Why:** Agents excel at repetitive tasks

```
Good:
Agent applies pattern to 50 files

Bad:
You manually update 50 files
```

### 4. Verify Agent Output

**Why:** Agents aren't perfect

```
Always:
- Review agent changes
- Test affected code
- Check for errors
- Use git to review diffs
```

---

## Common Orchestrations

### Backend Development

```
Task: Add new API endpoint

1. backend-dev-guidelines (pattern)
2. YOU implement (one endpoint)
3. error-tracking (add error handling)
4. route-tester (test endpoint)
5. Scale: Apply to multiple endpoints
```

### Frontend Development

```
Task: Add new component

1. shadcn-ui-guidelines (pattern)
2. frontend-dev-guidelines (React patterns)
3. YOU implement (one component)
4. Scale: Apply to similar components
```

### Database Changes

```
Task: Add new table/column

1. database-verification (verify schema)
2. security-guidelines (PII considerations)
3. YOU write migration
4. Agent: Run migration safely
5. Agent: Test queries work
```

### Security Hardening

```
Task: Fix security vulnerabilities

1. Agent: Scan for vulnerabilities
2. security-guidelines (explain fixes)
3. YOU implement critical fixes
4. Agent: Apply pattern to remaining code
5. Agent: Re-scan to verify
```

### Performance Tuning

```
Task: Optimize slow queries

1. Tool: Identify slow queries
2. performance-optimization (strategies)
3. YOU optimize one query
4. Verify improvement
5. Apply pattern to other queries
```

---

## Error Recovery

### When Agent Fails

```
1. Check agent output for errors
2. Use skill to understand the issue
3. Fix the specific problem
4. Retry agent with corrected approach
```

### When Skill Guidance Conflicts

```
1. Compare with official documentation
2. Test pattern in isolation
3. Use sequential-thinking for decision
4. Choose best approach for your context
```

### When Orchestration Breaks

```
1. Simplify: Use single tool
2. Manual: Do it yourself
3. Iterate: Try different orchestration
4. Learn: Document what works
```

---

## Best Practices

### DO

✅ Start with skills for learning
✅ Use agents for scaling
✅ Validate before automation
✅ Review agent output
✅ Test orchestrations
✅ Document successful patterns
✅ Use git for safety
✅ Handle errors gracefully

### DON'T

❌ Skip to agent without understanding
❌ Trust agent output blindly
❌ Orchestrate unnecessarily
❌ Use agent for one-off tasks
❌ Skip validation steps
❌ Forget to test agent results
❌ Orchestrate without rollback plan

---

## Quick Reference

### Common Orchestrations

| Task | First | Then | Finally |
|------|-------|------|----------|
| New API | backend skill | You implement | route-tester |
| Security fix | security skill | You fix | Agent scale |
| Performance | profile | perf skill | Apply pattern |
| Error handling | error-tracking | You add | Auto-resolver |

### Tool Selection

| Need | Use |
|------|-----|
| Learn pattern | Skill |
| Quick answer | Skill |
| Apply to many | Agent |
| Test comprehensively | Agent |
| Complex decision | Sequential-thinking + Skill |

---

## Summary

**Orchestration combines strengths:**
- **Skills** teach you best practices
- **Agents** apply patterns at scale
- **You** provide oversight and validation

**Successful orchestration:**
1. Learn from skill
2. Implement yourself
3. Validate it works
4. Use agent to scale
5. Review results

**Remember:** Agents accelerate work, but skills ensure quality.
