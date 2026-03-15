# MCP Server Integration Patterns

Guide for leveraging Model Context Protocol (MCP) servers in skills and agents.

---

## Overview

This project has the following MCP servers enabled:
- **mysql** - Database queries and operations
- **sequential-thinking** - Complex reasoning and planning
- **playwright** - Browser automation and testing

These servers provide tools that skills can reference and agents can use.

---

## Configuration

MCP servers are configured in `.claude/settings.json`:

```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": [
    "mysql",
    "sequential-thinking",
    "playwright"
  ]
}
```

---

## MySQL MCP Server

### Available Tools

- `query` - Execute SQL queries
- `schema` - Get database schema information
- `tables` - List all tables
- `describe` - Describe table structure

### Usage in Skills

**When to Reference:**
- Database verification before queries
- Understanding database structure
- Writing Prisma queries
- Debugging database issues

**Example: Database Verification Skill**

```markdown
## MySQL Integration

This skill leverages the MySQL MCP server for database operations:

### Before Writing Queries

Use the MySQL MCP server to verify structure:
1. Get table schema: `schema` tool
2. Check column names: `describe` tool
3. List available tables: `tables` tool

### Query Verification

Test queries with the `query` tool before:
- Using in application code
- Creating complex JOINs
- Optimizing slow queries
```

### Usage in Agents

**Example: Auto-Database Verifier Agent**

```
When user wants to query database:

1. Use `schema` tool to get table structure
2. Verify column names and types
3. Use `query` tool to test the SQL
4. Return verified query to user
```

### Common Patterns

**Schema Verification:**
```typescript
// Skill suggests using MCP to verify
// Before writing:
const user = await prisma.user.findUnique({ where: { email } });

// First verify with MCP:
// 1. Get schema for 'users' table
// 2. Confirm 'email' column exists and is indexed
// 3. Write confident query
```

---

## Sequential Thinking MCP Server

### Available Tools

- `think` - Chain multiple reasoning steps
- `plan` - Create structured plans
- `analyze` - Deep analysis of problems

### Usage in Skills

**When to Reference:**
- Complex decision-making
- Architecture decisions
- Breaking down large tasks
- Analyzing trade-offs

**Example: CTO Guidelines Skill**

```markdown
## Sequential Thinking Integration

For complex architectural decisions, use the sequential-thinking MCP server:

### When Planning Architecture

Use the `plan` tool to:
1. Break down requirements into components
2. Identify dependencies between services
3. Plan migration strategies
4. Consider scalability requirements

### When Making Trade-offs

Use the `analyze` tool to:
1. List pros and cons of approaches
2. Consider technical debt implications
3. Evaluate team skills and learning curve
4. Assess time and resource constraints
```

### Usage in Agents

**Example: Architecture Planner Agent**

```
When designing system architecture:

1. Gather requirements from user
2. Use `plan` tool to create structured architecture plan
3. Use `analyze` tool to evaluate technology choices
4. Return comprehensive architecture document
```

### Common Patterns

**Decision Framework:**
```markdown
// Skill suggests using sequential-thinking
// For major decisions:

Step 1: Use `think` tool to chain reasoning
Step 2: Consider business requirements
Step 3: Evaluate technical constraints
Step 4: Assess team capabilities
Step 5: Make recommendation with rationale
```

---

## Playwright MCP Server

### Available Tools

- `browse` - Navigate to URLs
- `click` - Click elements
- `fill` - Fill form fields
- `screenshot` - Capture screenshots
- `evaluate` - Execute JavaScript in browser
- `test` - Run browser tests

### Usage in Skills

**When to Reference:**
- Browser automation tasks
- Web scraping
- E2E testing
- Taking screenshots
- Testing user flows

**Example: Browser Automation Skill**

```markdown
## Playwright Integration

This skill works with the Playwright MCP server for browser automation:

### Common Automation Tasks

**Taking Screenshots:**
1. Use `browse` tool to navigate to URL
2. Use `screenshot` tool to capture page
3. Return screenshot to user

**Form Testing:**
1. Use `browse` to load form
2. Use `fill` to input test data
3. Use `click` to submit
4. Use `screenshot` to verify result

### Web Scraping

1. Use `browse` to load page
2. Use `evaluate` to extract data
3. Return structured data
```

### Usage in Agents

**Example: Browser Automation Agent**

```
When user requests browser automation:

1. Get URL and task from user
2. Use `browse` tool to navigate
3. Use appropriate tools (click, fill, screenshot)
4. Return results/data to user
```

### Common Patterns

**E2E Test Pattern:**
```markdown
// Skill suggests using Playwright MCP
// For testing user flows:

1. Navigate: `browse` tool
2. Interact: `fill` and `click` tools
3. Verify: `screenshot` or `evaluate` tool
4. Report: Return test results
```

---

## Integration Best Practices

### In Skills

**1. Reference MCP Tools in Guidance:**

```markdown
## Database Operations

For database queries, leverage the MySQL MCP server:

1. **Verify Schema First**
   - Use `schema` tool to understand tables
   - Use `describe` tool to check columns

2. **Test Queries**
   - Use `query` tool before using in code
   - Verify query returns expected results

3. **Optimize**
   - Check query performance
   - Add indexes if needed
```

**2. Provide MCP Tool Examples:**

```markdown
### Example: Query Verification with MCP

Before using this query in your code:

**Step 1:** Verify table structure
```
Use MCP `describe` tool on 'users' table
→ Returns: id, email, name, created_at columns
```

**Step 2:** Test query
```
Use MCP `query` tool with: SELECT id, email FROM users LIMIT 5
→ Returns: 5 sample rows
```

**Step 3:** Use in Prisma
```typescript
const users = await prisma.user.findMany({
  select: { id: true, email: true },
  take: 5
});
```
```

### In Agents

**1. Document MCP Tool Usage:**

```markdown
# Database Migration Agent

This agent uses the MySQL MCP server for safe migrations.

## Workflow

1. **Backup Schema**
   - Use `schema` tool to get current state
   - Save for rollback if needed

2. **Verify Changes**
   - Use `describe` on affected tables
   - Confirm columns exist

3. **Run Migration**
   - Execute migration SQL with `query` tool
   - Verify success

4. **Validate**
   - Query sample data with `query` tool
   - Return validation results
```

**2. Error Handling with MCP:**

```markdown
## Error Recovery

If MCP tool fails:

1. **MySQL Query Fails**
   - Check syntax with `schema` tool
   - Verify table exists with `tables` tool
   - Retry with corrected query

2. **Browser Action Fails**
   - Use `screenshot` to see current state
   - Check if element exists with `evaluate`
   - Wait for page load if needed
```

---

## MCP Tools Reference

### MySQL Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `query` | Execute SQL | `SELECT * FROM users LIMIT 10` |
| `schema` | Get DB schema | Get all tables and relationships |
| `tables` | List tables | `SHOW TABLES` |
| `describe` | Table structure | `DESCRIBE users` |

### Sequential Thinking Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `think` | Chain reasoning | Multi-step logic |
| `plan` | Structure plans | Break down complex tasks |
| `analyze` | Deep analysis | Evaluate trade-offs |

### Playwright Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `browse` | Navigate | Go to URL |
| `click` | Click element | Click button by selector |
| `fill` | Fill form | Input text in fields |
| `screenshot` | Capture | Get page image |
| `evaluate` | Run JS | Execute JavaScript |
| `test` | Run tests | Execute test suite |

---

## Quick Integration Checklist

When creating/updating skills:

- [ ] Identify relevant MCP servers
- [ ] Add MCP tool references to skill documentation
- [ ] Provide examples of MCP tool usage
- [ ] Document error handling with MCP tools
- [ ] Include MCP tool patterns in resources

---

## Examples in Current Skills

**error-tracking:**
```markdown
This skill works with the MySQL MCP server to:
- Verify database schema before adding tracking
- Test performance queries before deployment
```

**route-tester:**
```markdown
This skill leverages the Playwright MCP server to:
- Automate browser-based authentication tests
- Capture screenshots of test failures
```

**performance-optimization:**
```markdown
This skill uses the MySQL MCP server to:
- Analyze slow queries with EXPLAIN
- Verify indexes before optimization
```

---

## Best Practices

1. **Verify Before Execute** - Use MCP tools to verify structure
2. **Test Before Deploy** - Use MCP to test queries/interactions
3. **Document Tool Usage** - Show examples in skill docs
4. **Handle Errors** - Document MCP error recovery
5. **Leverage Strengths** - Use each MCP server for its purpose

---

## Summary

MCP servers extend Claude Code capabilities:
- **MySQL** → Database operations
- **Sequential Thinking** → Complex reasoning
- **Playwright** → Browser automation

Skills should reference these tools in their documentation.
Agents should use these tools in their workflows.

For more information on MCP, see: https://modelcontextprotocol.io/
