# Skill Developer Reference Library

Supplementary reference materials for creating and managing Claude Code skills.

## Table of Contents
- [Trigger Pattern Examples](#trigger-pattern-examples)
- [Skill Configuration Templates](#skill-configuration-templates)
- [Hook Implementation Details](#hook-implementation-details)
- [Testing & Debugging](#testing--debugging)

---

## Trigger Pattern Examples

### Keyword Triggers

**Best Practices:**
- Use specific, actionable terms
- Include variations (singular, plural, synonyms)
- Max 1024 characters in description

**Examples:**

```json
{
  "keywords": [
    "pricing",
    "pricing strategy",
    "saas pricing",
    "monetization",
    "subscription pricing",
    "freemium"
  ]
}
```

**Anti-Patterns to Avoid:**
- Too generic: `"code"`, `"help"`, `"make"`
- Too many: >30 keywords reduces precision
- Overlapping with other skills

### Intent Pattern Examples

**Syntax:** Regex pattern matching user intent

**Creating New Routes:**
```json
{
  "intentPatterns": [
    "(create|add|implement|build).*?(route|endpoint|API)",
    "(add.*?new.*?(route|endpoint))",
    "(create.*?API)"
  ]
}
```

**Debugging:**
```json
{
  "intentPatterns": [
    "(fix|resolve|debug).*?(error|issue|bug)",
    "(troubleshoot|diagnose).*?(problem|failure)",
    "(why.*?(not working|failing|broken))"
  ]
}
```

**Database Operations:**
```json
{
  "intentPatterns": [
    "(query|fetch|get).*?(from|database)",
    "(insert|create|add).*?(record|row|data)",
    "(update|modify|change).*?(record|data)"
  ]
}
```

### File Path Pattern Examples

**Syntax:** Glob patterns for file paths

**TypeScript/React:**
```json
{
  "pathPatterns": [
    "src/**/*.tsx",
    "src/**/*.ts",
    "components/**/*.{ts,tsx}"
  ]
}
```

**Backend Routes:**
```json
{
  "pathPatterns": [
    "src/routes/**/*.ts",
    "src/api/**/*.ts",
    "**/*routes*.ts"
  ]
}
```

**Configuration Files:**
```json
{
  "pathPatterns": [
    "*.config.js",
    "*.config.ts",
    "config/**/*",
    ".env*"
  ]
}
```

### Content Pattern Examples

**Syntax:** Regex for file content detection

**Prisma Usage:**
```json
{
  "contentPatterns": [
    "PrismaService\\.main\\.",
    "prisma\\.",
    "@prisma/client"
  ]
}
```

**Express Routes:**
```json
{
  "contentPatterns": [
    "router\\.(get|post|put|delete)\\(",
    "app\\.(use|get|post)\\(",
    "express\\.(Router|application)"
  ]
}
```

**React Hooks:**
```json
{
  "contentPatterns": [
    "useEffect\\(",
    "useState\\(",
    "useQuery\\(",
    "from ['\"]react['\"]"
  ]
}
```

---

## Skill Configuration Templates

### Basic Domain Skill Template

```json
{
  "skill-name": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "description": "Brief description including trigger keywords",
    "promptTriggers": {
      "keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
      ],
      "intentPatterns": [
        "(action|verb).*?(target|context)",
        "(create|add).*?(something)"
      ]
    }
  }
}
```

### Guardrail Skill Template

```json
{
  "guardrail-skill": {
    "type": "guardrail",
    "enforcement": "block",
    "priority": "critical",
    "description": "Critical validation skill",
    "promptTriggers": {
      "pathPatterns": ["**/*.ts"],
      "contentPatterns": ["risky\\.pattern"]
    },
    "blockMessage": "⚠️ Validation required - use 'guardrail-skill' skill first",
    "skipConditions": {
      "sessionSkillUsed": true,
      "fileMarkers": ["@skip-validation"],
      "envOverride": "SKIP_GUARDRAIL_SKILL"
    }
  }
}
```

### Advanced Multi-Trigger Skill

```json
{
  "advanced-skill": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "description": "Comprehensive skill with multiple trigger types",
    "promptTriggers": {
      "keywords": [
        "feature",
        "feature x",
        "specific term"
      ],
      "intentPatterns": [
        "(do|perform).*?specific action",
        "(create|make).*?something"
      ],
      "pathPatterns": [
        "src/feature/**/*.ts",
        "features/**/*.{ts,tsx}"
      ],
      "contentPatterns": [
        "specificPattern",
        "anotherPattern"
      ]
    }
  }
}
```

---

## Hook Implementation Details

### UserPromptSubmit Hook Structure

**File:** `.claude/hooks/skill-activation-prompt.ts`

```typescript
interface HookInput {
  session_id: string;
  prompt: string;
}

interface HookOutput {
  stdout: string;  // Injected as context
}

async function main(input: HookInput): Promise<HookOutput> {
  // 1. Load skill-rules.json
  // 2. Match prompt against all skills
  // 3. Return formatted suggestions
}
```

**Output Format:**

```
**Consider using these skills:**
- skill-name: [Brief description why it's relevant]
- another-skill: [Brief description why it's relevant]
```

### Stop Hook Structure

**File:** `.claude/hooks/error-handling-reminder.ts`

```typescript
interface StopHookInput {
  edited_files: string[];
}

async function main(input: StopHookInput): Promise<void> {
  // 1. Analyze edited files
  // 2. Check for risky patterns
  // 3. Display reminder if needed
}
```

**Trigger Conditions:**
- Files edited contain specific patterns
- Risky operations performed
- No error handling detected

**Output Format:**

```
⚠️ Reminder: Did you handle errors properly?
- Consider adding try/catch blocks
- Use Sentry.captureException for errors
- Check database operations for proper error handling
```

---

## Testing & Debugging

### Testing Skill Activation

**Manual Test:**

```bash
echo '{"session_id":"test","prompt":"your test prompt here"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

**Test Cases:**

1. **Keyword Match:**
   ```bash
   echo '{"session_id":"test","prompt":"help me design pricing"}' | npx tsx .claude/hooks/skill-activation-prompt.ts
   ```

2. **Intent Pattern Match:**
   ```bash
   echo '{"session_id":"test","prompt":"create a new route for user profile"}' | npx tsx .claude/hooks/skill-activation-prompt.ts
   ```

3. **No Match:**
   ```bash
   echo '{"session_id":"test","prompt":"what is the weather"}' | npx tsx .claude/hooks/skill-activation-prompt.ts
   ```

### Debugging Skill Not Triggering

**Checklist:**

1. **Verify skill-rules.json Syntax:**
   ```bash
   cat .claude/skills/skill-rules.json | jq .
   ```

2. **Test Keywords Directly:**
   - Does prompt contain exact keyword?
   - Check for typos in keywords
   - Case insensitive (usually)

3. **Test Intent Patterns:**
   - Regex must match prompt
   - Test regex at: https://regex101.com/
   - Escape special characters properly

4. **Check File Paths:**
   - Glob pattern correct?
   - File exists at path?
   - Relative to project root?

5. **Check Content Patterns:**
   - Regex matches file content?
   - Content loaded correctly?
   - Special characters escaped?

### Common Issues & Solutions

**Issue:** Skill not triggering
- **Cause:** JSON syntax error
- **Fix:** `jq . skill-rules.json` to validate

**Issue:** Too many false positives
- **Cause:** Keywords too generic
- **Fix:** Use more specific keywords, add intent patterns

**Issue:** Hook not executing
- **Cause:** Not registered in settings.json
- **Fix:** Add to `hooks.UserPromptSubmit` or `hooks.Stop`

**Issue:** Performance slow
- **Cause:** Too many patterns, complex regex
- **Fix:** Reduce patterns, simplify regex, add caching

---

## Progressive Disclosure Examples

### When to Create Resources

**Create resource file when:**
- SKILL.md approaches 400+ lines
- Content can be logically separated
- Detailed examples vs quick reference
- Reference tables and lists

**Resource File Types:**
- `code-patterns.md` - Detailed code examples
- `configuration.md` - Setup and config guides
- `examples.md` - Real-world examples
- `reference.md` - Reference tables and lists

### Resource Linking in SKILL.md

```markdown
## Quick Reference

[Brief overview here]

## Resources

📚 **Detailed Guides:**
- [code-patterns.md](resources/code-patterns.md) - Detailed examples
- [configuration.md](resources/configuration.md) - Setup guide
```

### Resource File Structure

```markdown
# Resource Title

## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)

---

## Section 1

[Detailed content]

---

## Section 2

[More detailed content]
```

---

## Quick Reference

### Priority Levels

| Priority | When to Use | Example |
|----------|-------------|---------|
| `critical` | Security, data loss | `database-verification` |
| `high` | Common operations | `backend-dev-guidelines` |
| `medium` | Specific domains | `pricing-master` |
| `low` | Rare situations | (rarely used) |

### Enforcement Types

| Type | Behavior | Use Case |
|------|----------|----------|
| `block` | Prevents action | Guardrails, critical checks |
| `suggest` | Shows suggestion | Domain guidance, best practices |
| `warn` | Warning message | (rarely used) |

### Trigger Types Summary

| Type | Best For | Example |
|------|----------|---------|
| `keywords` | Explicit mentions | "pricing", "database" |
| `intentPatterns` | Actions & intent | "create route", "fix error" |
| `pathPatterns` | File locations | `**/*.tsx`, `src/routes/**` |
| `contentPatterns` | Technology detection | "PrismaService.", "useState(" |

---

## Best Practices Checklist

Creating a new skill:

- [ ] Created `.claude/skills/{name}/SKILL.md`
- [ ] Added YAML frontmatter with name and description
- [ ] Added entry to `skill-rules.json`
- [ ] Description includes all trigger keywords
- [ ] Tested with 3+ real prompts
- [ ] SKILL.md under 500 lines
- [ ] Created resources/ folder if needed
- [ ] Linked resources in SKILL.md
- [ ] Tested trigger patterns
- [ ] Verified JSON syntax
- [ ] Checked for false positives
- [ ] Documented when to use skill
