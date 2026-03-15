# Agents vs Skills - When to Use Which

Quick decision guide for choosing between agents and skills in Claude Code.

---

## Quick Decision Flow

```
Need guidance? → Use SKILL
Need work done? → Use AGENT

Learning something? → SKILL
Automating something? → AGENT

Quick reference? → SKILL (instant)
Complex task? → AGENT (takes time)

Interactive? → SKILL
Autonomous? → AGENT
```

---

## Skills (Domain Guidance)

**What They Do:**
- Provide best practices and patterns
- Answer questions and give examples
- Suggest approaches to problems
- Teach domain knowledge
- Guide implementation decisions

**When to Use:**
```
✅ "How should I structure this Express route?"
✅ "What's the best way to handle errors?"
✅ "Show me examples of React hooks"
✅ "What are the security considerations?"
✅ "Explain pricing strategy"
```

**Characteristics:**
- **Instant**: Activates immediately
- **Interactive**: You're in control
- **Suggestive**: Provides options
- **Contextual**: Activates based on your work
- **Lightweight**: Quick guidance

**Examples:**
- backend-dev-guidelines - Patterns for routes, controllers
- frontend-dev-guidelines - React component patterns
- security-guidelines - OWASP compliance
- pricing-master - Pricing strategy framework

---

## Agents (Task Automation)

**What They Do:**
- Execute complex multi-step tasks
- Perform autonomous research
- Run end-to-end workflows
- Test and validate code
- Refactor and optimize

**When to Use:**
```
✅ "Test all the authenticated routes in blog-api"
✅ "Refactor this module to use async/await"
✅ "Write comprehensive documentation for this API"
✅ "Fix all TypeScript errors in this file"
✅ "Review this code for security issues"
```

**Characteristics:**
- **Autonomous**: Works independently
- **Time-consuming**: Takes minutes to complete
- **Comprehensive**: Deep analysis and action
- **Specialized**: Each agent has specific capabilities
- **Output-focused**: Returns completed work

**Examples:**
- auth-route-tester - Tests all routes with authentication
- auto-error-resolver - Auto-fixes TypeScript errors
- code-refactor-master - Refactors code structure
- documentation-architect - Writes documentation

---

## Comparison Table

| Aspect | Skills | Agents |
|--------|--------|--------|
| **Purpose** | Guidance & education | Task execution |
| **Speed** | Instant (seconds) | Slow (minutes) |
| **Control** | You drive | Agent drives |
| **Output** | Suggestions | Completed work |
| **Best For** | Learning, patterns | Automation, testing |
| **Interaction** | Conversation | Launch and wait |
| **Activation** | Automatic (keywords) | Manual invoke |

---

## Usage Examples

### Example 1: Creating a New Feature

**Step 1: Use Skill (Learning Phase)**
```
You: "I want to add user authentication"
→ Skill: security-guidelines activates
→ Provides: JWT patterns, best practices, security checklist
→ You: Learn the approach
```

**Step 2: Implement with Skill Guidance**
```
You: "Create the login route"
→ Skill: backend-dev-guidelines activates
→ You: Write code following patterns
→ Skill: Suggests error tracking
```

**Step 3: Test with Agent**
```
You: "Test all the authentication routes"
→ Agent: auth-route-tester launches
→ Agent: Tests every route, returns report
→ You: Review results and fix issues
```

### Example 2: Fixing Performance Issues

**Step 1: Use Skill (Diagnosis)**
```
You: "My API is slow, how do I optimize it?"
→ Skill: performance-optimization activates
→ Provides: Caching strategies, query optimization tips
→ You: Learn the patterns
```

**Step 2: Implement Fixes**
```
You: Implements caching based on skill guidance
→ Skill: Continues to guide implementation
```

**Step 3: Verify with Agent**
```
You: "Profile the database queries and find slow ones"
→ Agent: Could use specialized agent (if available)
→ Agent: Analyzes, returns optimization suggestions
```

### Example 3: Pricing Strategy

**Step 1: Use Skill**
```
You: "Help me design pricing for my SaaS product"
→ Skill: pricing-master activates
→ Provides: 10-step framework, value-based pricing
→ You: Work through the framework interactively
→ Result: Complete pricing strategy
```

**No Agent Needed**
- Pricing is creative/strategic work
- Requires your input and decisions
- Skill provides better interactive guidance

---

## Common Patterns

### Pattern 1: Learn → Implement → Test

```
1. SKILL teaches you the pattern
2. YOU implement the feature
3. AGENT tests what you built
```

**Example:**
- Skill: security-guidelines (teach auth patterns)
- You: Implement authentication
- Agent: auth-route-tester (verify auth works)

### Pattern 2: Design → Build → Verify

```
1. SKILL helps design the approach
2. YOU build with skill guidance
3. AGENT verifies and tests
```

**Example:**
- Skill: pricing-master (design pricing tiers)
- You: Implement pricing page
- (No agent - pricing is front-end, manual test)

### Pattern 3: Debug → Understand → Fix

```
1. AGENT identifies the problem
2. SKILL explains the root cause
3. YOU implement the fix
```

**Example:**
- Agent: auto-error-resolver (finds TS errors)
- Skill: backend-dev-guidelines (explains pattern)
- You: Fix the errors

---

## Decision Checklist

### Use a Skill When:

- [ ] You're learning something new
- [ ] You need quick reference
- [ ] You want best practices
- [ ] You're designing a solution
- [ ] You need examples
- [ ] You want interactive guidance

### Use an Agent When:

- [ ] You have a complex multi-step task
- [ ] You need comprehensive testing
- [ ] You want autonomous analysis
- [ ] You're refactoring large codebases
- [ ] You need end-to-end automation
- [ ] You can wait for completion

---

## Quick Reference

### For Common Tasks

| Task | Use | Example |
|------|-----|---------|
| **Create API endpoint** | Skill | backend-dev-guidelines |
| **Test all endpoints** | Agent | auth-route-tester |
| **Design pricing** | Skill | pricing-master |
| **Fix TypeScript errors** | Agent | auto-error-resolver |
| **Add authentication** | Skill | security-guidelines |
| **Refactor code** | Agent | code-refactor-master |
| **Optimize performance** | Skill | performance-optimization |
| **Write documentation** | Agent | documentation-architect |
| **Setup CI/CD** | Skill | devops-guidelines |
| **Debug route issues** | Agent | auth-route-debugger |

---

## Summary

**Skills** are like **consultants** - they advise and guide you.

**Agents** are like **contractors** - they do the work for you.

**Rule of Thumb:**
- If you want to **learn** → Use a Skill
- If you want to **delegate** → Use an Agent

---

## Available Resources

- **All Skills:** `.claude/skills/*/SKILL.md`
- **All Agents:** `.claude/agents/*.md`
- **System Overview:** `.claude/README.md`
