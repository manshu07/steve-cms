   # Agents

Specialized agents for complex, multi-step tasks.

---

## What Are Agents?

Agents are autonomous Claude instances that handle specific complex tasks. Unlike skills (which provide inline guidance), agents:
- Run as separate sub-tasks
- Work autonomously with minimal supervision
- Have specialized tool access
- Return comprehensive reports when complete

**Key advantage:** Agents are **standalone** - just copy the `.md` file and use immediately!

---

## Available Agents (17)

### code-architecture-reviewer
**Purpose:** Review code for architectural consistency and best practices

**When to use:**
- After implementing a new feature
- Before merging significant changes
- When refactoring code
- To validate architectural decisions

**Integration:** ✅ Copy as-is

---

### code-refactor-master
**Purpose:** Plan and execute comprehensive refactoring

**When to use:**
- Reorganizing file structures
- Breaking down large components
- Updating import paths after moves
- Improving code maintainability

**Integration:** ✅ Copy as-is

---

### documentation-architect
**Purpose:** Create comprehensive documentation

**When to use:**
- Documenting new features
- Creating API documentation
- Writing developer guides
- Generating architectural overviews

**Integration:** ✅ Copy as-is

---

### frontend-error-fixer
**Purpose:** Debug and fix frontend errors

**When to use:**
- Browser console errors
- TypeScript compilation errors in frontend
- React errors
- Build failures

**Integration:** ⚠️ May reference screenshot paths - update if needed

---

### plan-reviewer
**Purpose:** Review development plans before implementation

**When to use:**
- Before starting complex features
- Validating architectural plans
- Identifying potential issues early
- Getting second opinion on approach

**Integration:** ✅ Copy as-is

---

### refactor-planner
**Purpose:** Create comprehensive refactoring strategies

**When to use:**
- Planning code reorganization
- Modernizing legacy code
- Breaking down large files
- Improving code structure

**Integration:** ✅ Copy as-is

---

### web-research-specialist
**Purpose:** Research technical issues online

**When to use:**
- Debugging obscure errors
- Finding solutions to problems
- Researching best practices
- Comparing implementation approaches

**Integration:** ✅ Copy as-is

---

### auth-route-tester
**Purpose:** Test authenticated API endpoints

**When to use:**
- Testing routes with JWT cookie auth
- Validating endpoint functionality
- Debugging authentication issues

**Integration:** ⚠️ Requires JWT cookie-based auth

---

### auth-route-debugger
**Purpose:** Debug authentication issues

**When to use:**
- Auth failures
- Token issues
- Cookie problems
- Permission errors

**Integration:** ⚠️ Requires JWT cookie-based auth

---

### auto-error-resolver
**Purpose:** Automatically fix TypeScript compilation errors

**When to use:**
- Build failures with TypeScript errors
- After refactoring that breaks types
- Systematic error resolution needed

**Integration:** ⚠️ May need path updates

---

### prd-writer
**Purpose:** Generate comprehensive Product Requirements Documents

**When to use:**
- Converting feature requests to formal PRDs
- Creating documentation for new features
- Standardizing requirements across teams

**Integration:** ✅ Copy as-is

---

### tech-debt-analyzer
**Purpose:** Analyze codebase for technical debt and create remediation plans

**When to use:**
- Quarterly tech debt reviews
- Before major refactoring initiatives
- Planning sprint capacity for debt reduction

**Integration:** ✅ Copy as-is

---

### python-code-reviewer
**Purpose:** Review Python code for best practices and type safety

**When to use:**
- Before merging Python code changes
- After implementing new Python features
- During code review process

**Integration:** ✅ Copy as-is

---

### yolo-fixer
**Purpose:** Automatically fix all issues without asking for confirmation

**When to use:**
- When you want things fixed automatically
- Quick cleanup tasks
- Non-technical users who want things "just work"

**Integration:** ✅ Copy as-is

---

### ux-writer
**Purpose:** Expert-level UX writing for interfaces, microcopy, and user flows

**When to use:**
- Writing button labels and CTAs
- Creating error messages and validation text
- Designing empty states and onboarding copy
- Writing form labels and help text

**Integration:** ✅ Copy as-is

---

### browser-automation
**Purpose:** Automate browser interactions with Playwright/Puppeteer

**When to use:**
- Web scraping and data extraction
- E2E testing
- Automated screenshots
- Form automation
- Browser-based workflows

**Integration:** ✅ Copy as-is

---

## How to Integrate an Agent

### Standard Integration (Most Agents)

**Step 1: Copy the file**
```bash
cp claude-skill/.claude/agents/agent-name.md \\
   your-project/.claude/agents/
```

**Step 2: Verify (optional)**
```bash
# Check for hardcoded paths
grep -n "~/git/\|/root/git/\|/Users/" your-project/.claude/agents/agent-name.md
```

**Step 3: Use it**
Ask Claude: "Use the [agent-name] agent to [task]"

That's it! Agents work immediately.

---

### Agents Requiring Customization

**frontend-error-fixer:**
- May reference screenshot paths
- Ask user: "Where should screenshots be saved?"
- Update paths in agent file

**auth-route-tester / auth-route-debugger:**
- Require JWT cookie authentication
- Update service URLs from examples
- Customize for user's auth setup

**auto-error-resolver:**
- May have hardcoded project paths
- Update to use `$CLAUDE_PROJECT_DIR` or relative paths

---

## When to Use Agents vs Skills

| Use Agents When... | Use Skills When... |
|-------------------|-------------------|
| Task requires multiple steps | Need inline guidance |
| Complex analysis needed | Checking best practices |
| Autonomous work preferred | Want to maintain control |
| Task has clear end goal | Ongoing development work |
| Example: "Review all controllers" | Example: "Creating a new route" |

**Both can work together:**
- Skill provides patterns during development
- Agent reviews the result when complete

---

## Agent Quick Reference

| Agent | Complexity | Customization | Auth Required |
|-------|-----------|---------------|---------------|
| code-architecture-reviewer | Medium | ✅ None | No |
| code-refactor-master | High | ✅ None | No |
| documentation-architect | Medium | ✅ None | No |
| frontend-error-fixer | Medium | ⚠️ Screenshot paths | No |
| plan-reviewer | Low | ✅ None | No |
| refactor-planner | Medium | ✅ None | No |
| web-research-specialist | Low | ✅ None | No |
| auth-route-tester | Medium | ⚠️ Auth setup | JWT cookies |
| auth-route-debugger | Medium | ⚠️ Auth setup | JWT cookies |
| auto-error-resolver | Low | ⚠️ Paths | No |
| prd-writer | Medium | ✅ None | No |
| tech-debt-analyzer | High | ✅ None | No |
| python-code-reviewer | Medium | ✅ None | No |

---

## For Claude Code

**When integrating agents for a user:**

1. **Read [CLAUDE_INTEGRATION_GUIDE.md](../../CLAUDE_INTEGRATION_GUIDE.md)**
2. **Just copy the .md file** - agents are standalone
3. **Check for hardcoded paths:**
   ```bash
   grep "~/git/\|/root/" agent-name.md
   ```
4. **Update paths if found** to `$CLAUDE_PROJECT_DIR` or `.`
5. **For auth agents:** Ask if they use JWT cookie auth first

**That's it!** Agents are the easiest components to integrate.

---

## Creating Your Own Agents

Agents are markdown files with optional YAML frontmatter:

```markdown
# Agent Name

## Purpose
What this agent does

## Instructions
Step-by-step instructions for autonomous execution

## Tools Available
List of tools this agent can use

## Expected Output
What format to return results in
```

**Tips:**
- Be very specific in instructions
- Break complex tasks into numbered steps
- Specify exactly what to return
- Include examples of good output
- List available tools explicitly

---

## Troubleshooting

### Agent not found

**Check:**
```bash
# Is agent file present?
ls -la .claude/agents/[agent-name].md
```

### Agent fails with path errors

**Check for hardcoded paths:**
```bash
grep "~/\|/root/\|/Users/" .claude/agents/[agent-name].md
```

**Fix:**
```bash
sed -i 's|~/git/.*project|$CLAUDE_PROJECT_DIR|g' .claude/agents/[agent-name].md
```

---

## Next Steps

1. **Browse agents above** - Find ones useful for your work
2. **Copy what you need** - Just the .md file
3. **Ask Claude to use them** - "Use [agent] to [task]"
4. **Create your own** - Follow the pattern for your specific needs

**Questions?** See [CLAUDE_INTEGRATION_GUIDE.md](../../CLAUDE_INTEGRATION_GUIDE.md)
