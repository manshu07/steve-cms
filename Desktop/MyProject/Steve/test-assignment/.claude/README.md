# Claude Code Skills System

Complete guide to the skills, agents, commands, and hooks system in this project.

## Table of Contents
- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Skills System](#skills-system)
- [Agents vs Skills](#agents-vs-skills)
- [Hooks System](#hooks-system)
- [Commands](#commands)
- [Quick Start](#quick-start)

---

## Overview

This project uses Claude Code's extensibility system to provide:
- **Skills**: Auto-activating guidance for specific domains (pricing, error tracking, etc.)
- **Agents**: Specialized AI agents for complex tasks (auth testing, code review, etc.)
- **Commands**: Reusable workflows for common operations
- **Hooks**: Automated checks and reminders throughout the development cycle

---

## Directory Structure

```
.claude/
├── agents/                  # Task-specific AI agents
│   ├── auth-route-debugger.md
│   ├── auto-error-resolver.md
│   ├── code-refactor-master.md
│   └── ...
├── commands/                # Reusable command workflows
│   ├── browser-test.md
│   ├── dev-docs.md
│   └── route-research-for-testing.md
├── hooks/                   # Automated triggers
│   ├── skill-activation-prompt.ts    # Suggests skills before work
│   ├── error-handling-reminder.ts    # Post-response error reminders
│   ├── tsc-check.sh                  # TypeScript validation
│   └── ...
├── skills/                  # Domain expertise and guardrails
│   ├── pricing-master/      # SaaS pricing strategies
│   ├── error-tracking/      # Sentry integration
│   ├── route-tester/        # API testing patterns
│   ├── backend-dev-guidelines/
│   ├── frontend-dev-guidelines/
│   └── ...
├── settings.json            # Main configuration
├── settings.local.json      # Local overrides (gitignored)
├── skill-rules.json         # Skill trigger configuration
└── .gitignore              # What to ignore in .claude/
```

---

## Skills System

### What Are Skills?

Skills are auto-activating domain experts that provide guidance when you're working on specific topics. They can:
- **Suggest** best practices (domain skills)
- **Block** dangerous operations (guardrail skills)
- **Provide** detailed examples and patterns

### Available Skills

#### Development Skills

| Skill | Purpose | When Activates |
|-------|---------|----------------|
| `backend-dev-guidelines` | Node.js/Express/TypeScript patterns | Creating routes, controllers, services |
| `frontend-dev-guidelines` | React/TypeScript/MUI v7 patterns | Creating components, pages, UI |
| `python-dev-guidelines` | Python development patterns | Working with Python code |
| `django-dev-guidelines` | Django web applications | Creating Django models, views, APIs |
| `fastapi-dev-guidelines` | FastAPI high-performance APIs | Creating FastAPI routes, dependencies |

#### Domain Skills

| Skill | Purpose | When Activates |
|-------|---------|----------------|
| `pricing-master` | SaaS pricing strategy | Designing pricing, monetization |
| `error-tracking` | Sentry v8 integration | Adding error handling, instrumentation |
| `route-tester` | Authenticated API testing | Testing endpoints, debugging auth |
| `browser-automation` | Playwright/Puppeteer | Automating browsers, scraping, E2E tests |
| `shadcn-ui-guidelines` | shadcn-ui + Tailwind CSS | Creating UI components, styling |

#### Leadership Skills

| Skill | Purpose | When Activates |
|-------|---------|----------------|
| `pm-guidelines` | Product management | Writing PRDs, planning sprints, roadmaps |
| `cto-guidelines` | Technical leadership | Architecture decisions, team management |

#### Meta Skills

| Skill | Purpose | When Activates |
|-------|---------|----------------|
| `skill-developer` | Creating/managing skills | Working with skill system, triggers |

### Skill Architecture

**Progressive Disclosure Pattern:**
```
SKILL.md (Quick Reference)
├── Under 500 lines
├── Core concepts
├── Quick start examples
└── Links to detailed resources

resources/ (Deep Dives)
├── code-patterns.md     - Detailed examples
├── configuration.md     - Setup guides
├── testing-patterns.md  - Test scenarios
└── reference.md         - Reference tables
```

### Skill Triggering

Skills activate automatically based on:
1. **Keywords** in your prompt ("pricing", "route", "error handling")
2. **Intent patterns** ("create a route", "fix the bug")
3. **File paths** you're editing (`src/routes/*.ts`)
4. **Content patterns** in files (PrismaService., useState)

**Example:**
```bash
# This activates pricing-master skill
"Help me design pricing for my SaaS product"

# This activates error-tracking skill
"Add error handling to this controller"

# This activates route-tester skill
"Test the /api/users endpoint"
```

---

## Agents vs Skills

### When to Use Skills

**Skills are for:**
- Learning best practices
- Understanding patterns
- Quick reference during coding
- Domain-specific guidance
- Guardrails against mistakes

**Example:**
```
User: "How should I structure this Express route?"
→ Skill activates: backend-dev-guidelines
→ Provides pattern and example
```

### When to Use Agents

**Agents are for:**
- Complex multi-step tasks
- Autonomous research
- End-to-end workflows
- Testing and validation
- Code refactoring

**Available Agents:**

| Agent | Purpose | Example |
|-------|---------|---------|
| `auth-route-debugger` | Debug authenticated routes | Test and fix auth issues |
| `auth-route-tester` | Test API authentication | Verify route security |
| `auto-error-resolver` | Fix TypeScript errors | Auto-fix compilation errors |
| `browser-automation` | Browser tasks | Scrape websites, take screenshots |
| `code-refactor-master` | Refactor code | Improve code structure |
| `documentation-architect` | Write docs | Generate documentation |
| `python-code-reviewer` | Review Python code | Analyze Python code quality |
| `web-research-specialist` | Research online | Find information, docs |

**Example:**
```
User: "Test all the authenticated routes in the blog-api service"
→ Agent launches: auth-route-tester
→ Tests all routes automatically
→ Returns comprehensive report
```

### Quick Decision Guide

```
Need guidance? → Use Skill
Need work done? → Use Agent

Learning something? → Skill
Automating something? → Agent

Quick reference? → Skill (instant)
Complex task? → Agent (takes time)
```

---

## Hooks System

Hooks automate checks and reminders at key points in your workflow.

### Hook Types

**1. UserPromptSubmit (Before Work)**
- **File:** `skill-activation-prompt.ts`
- **Purpose:** Suggest relevant skills based on your prompt
- **Example:** You mention "pricing" → suggests pricing-master skill

**2. PreToolUse (Before Tool Execution)**
- **File:** `auto-code-review.sh`
- **Purpose:** Review code before editing
- **Example:** Before editing a file, checks for issues

**3. PostToolUse (After Tool Execution)**
- **File:** `post-tool-use-tracker.sh`
- **Purpose:** Track what files were edited
- **Example:** Logs edited files for later review

**4. Stop (After Response)**
- **Files:**
  - `tsc-check.sh` - Validate TypeScript
  - `error-handling-reminder.ts` - Remind about error handling
  - `stop-build-check-enhanced.sh` - Check build status
  - `trigger-build-resolver.sh` - Auto-resolve build errors
- **Purpose:** Quality checks, reminders, auto-fixes
- **Example:** After writing code, reminds to add Sentry error handling

### Hook Flow

```
1. You type a prompt
   ↓
2. UserPromptSubmit hook runs
   → Suggests relevant skills
   ↓
3. Claude sees prompt + skill suggestions
   ↓
4. Claude uses tools (Edit, Write, Bash, etc.)
   ↓
5. PreToolUse hook runs (before each tool)
   → Validates the operation
   ↓
6. Tool executes
   ↓
7. PostToolUse hook runs
   → Tracks changes
   ↓
8. Claude responds to you
   ↓
9. Stop hook runs
   → Quality checks
   → Reminders
   → Auto-fixes
```

---

## Commands

Commands are reusable workflows for common operations.

### Available Commands

| Command | Purpose | Usage |
|---------|---------|-------|
| `browser-test` | Run browser automation tests | `/browser-test` |
| `dev-docs` | Create development docs | `/dev-docs` |
| `dev-docs-update` | Update existing docs | `/dev-docs-update` |
| `route-research-for-testing` | Find routes to test | `/route-research-for-testing` |

### Using Commands

Commands are invoked with `/` followed by the command name:

```bash
# Example: Run browser tests
You: /browser-test

→ Agent launches browser-automation
→ Runs all tests
→ Returns results
```

---

## Configuration Files

### settings.json

Main Claude Code configuration:

```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["mysql", "sequential-thinking", "playwright"],
  "permissions": {
    "allow": ["Edit:*", "Write:*", "Bash:*"]
  },
  "hooks": {
    "UserPromptSubmit": [...],
    "Stop": [...]
  }
}
```

### settings.local.json

Local overrides (gitignored):

```json
{
  "permissions": {
    "allow": ["Bash(mkdir:*)", "Bash(grep:*)"]
  }
}
```

### skill-rules.json

Defines skill triggers and behavior:

```json
{
  "skills": {
    "pricing-master": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "high",
      "promptTriggers": {
        "keywords": ["pricing", "monetization"],
        "intentPatterns": ["(design|create).*?pricing"]
      }
    }
  }
}
```

---

## Quick Start

### For New Developers

1. **Understand the Skills System**
   - Skills auto-activate based on your work
   - Read the suggestions they provide
   - Follow their patterns and best practices

2. **Learn the Available Skills**
   - Browse `.claude/skills/*/SKILL.md`
   - Each skill has a "When to Use" section
   - Skills link to detailed resources

3. **Use Agents for Complex Tasks**
   - Agents handle end-to-end workflows
   - Browse `.claude/agents/` for available agents
   - Invoke by name or describe the task

4. **Trust the Hooks**
   - Hooks protect you from mistakes
   - They suggest skills at the right time
   - They remind you about best practices

### Common Workflows

**Creating a New Route:**
```
1. You: "Create a route for user profile"
2. UserPromptSubmit hook suggests backend-dev-guidelines
3. Claude follows the patterns
4. Stop hook reminds about error tracking
5. Result: Properly structured route with Sentry
```

**Designing Pricing:**
```
1. You: "Help me price my SaaS product"
2. UserPromptSubmit hook suggests pricing-master
3. Pricing-master walks through 10-step framework
4. Result: Complete pricing strategy with tiers
```

**Testing Authenticated Routes:**
```
1. You: "Test all the protected endpoints"
2. Agent launches: auth-route-tester
3. Tests each route with authentication
4. Returns comprehensive test report
```

---

## MCP Servers

This project uses Model Context Protocol (MCP) servers:

### Enabled MCP Servers

| Server | Purpose | Usage in Skills |
|--------|---------|-----------------|
| `mysql` | Database queries | Database verification, testing |
| `sequential-thinking` | Complex reasoning | Architecture decisions, planning |
| `playwright` | Browser automation | Testing, screenshots, scraping |

Skills can leverage MCP tools when activated.

---

## Best Practices

### When Working with Skills

1. **Read the skill suggestions** - They're contextually relevant
2. **Follow the patterns** - Skills provide proven approaches
3. **Check the resources** - Detailed examples in `resources/` folders
4. **Ask questions** - Skills are interactive guides

### When Working with Agents

1. **Be specific** - Clear objectives = better results
2. **Provide context** - Agents need background information
3. **Review results** - Agents make mistakes too
4. **Iterate** - Refine based on agent output

### Customization

**Add a new skill:**
1. Create `.claude/skills/your-skill/SKILL.md`
2. Add entry to `skill-rules.json`
3. Test triggers with sample prompts
4. Create `resources/` folder if needed

**Add a new agent:**
1. Create `.claude/agents/your-agent.md`
2. Define capabilities and tools
3. Test with various scenarios

**Modify hooks:**
1. Edit hook scripts in `.claude/hooks/`
2. Update `settings.json` to register
3. Test with actual operations

---

## Troubleshooting

### Skill Not Activating

1. Check trigger keywords match your prompt
2. Verify skill-rules.json syntax: `jq . skill-rules.json`
3. Test hook: `echo '{"prompt":"test"}' | npx tsx skill-activation-prompt.ts`

### Hook Not Running

1. Check registered in `settings.json`
2. Verify hook file is executable
3. Check hook logs for errors
4. Test hook manually

### Agent Misbehaving

1. Provide clearer instructions
2. Break task into smaller steps
3. Review agent output for issues
4. Report agent problems if persistent

---

## Documentation

**Skill-specific documentation:**
- Each skill has its own `SKILL.md`
- Detailed guides in `resources/` folders
- Examples and patterns throughout

**System documentation:**
- This README - System overview
- `.claude/hooks/CONFIG.md` - Hook configuration
- `.claude/hooks/README.md` - Hook details
- `.claude/agents/README.md` - Agent catalog

---

## Support

For issues or questions:
1. Check relevant skill documentation
2. Review this README
3. Check hook/agent README files
4. Examine existing examples in codebase
