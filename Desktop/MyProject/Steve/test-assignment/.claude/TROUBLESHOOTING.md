# Claude Code Infrastructure - Troubleshooting Guide

Comprehensive troubleshooting guide for the Claude Code skills, agents, commands, and hooks system.

---

## Table of Contents

1. [Skills](#skills)
2. [Agents](#agents)
3. [Commands](#commands)
4. [Hooks](#hooks)
5. [General Issues](#general-issues)
6. [Validation](#validation)
7. [Performance](#performance)

---

## Skills

### Skill Not Activating

**Symptoms:**
- Skill doesn't appear in context
- No skill suggestions shown
- Skill doesn't trigger on relevant topics

**Diagnosis:**
```bash
# 1. Check if skill exists
ls -la .claude/skills/your-skill/

# 2. Verify SKILL.md structure
head -20 .claude/skills/your-skill/SKILL.md

# 3. Check skill-rules.json
grep -A 10 "your-skill" .claude/skills/skill-rules.json

# 4. Test hook manually
echo '{"prompt":"your trigger words"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

**Solutions:**

1. **Skill missing from skill-rules.json**
   ```json
   // Add to .claude/skills/skill-rules.json
   {
     "your-skill": {
       "type": "domain",
       "enforcement": "suggest",
       "priority": "medium",
       "promptTriggers": {
         "keywords": ["keyword1", "keyword2"]
       }
     }
   }
   ```

2. **YAML frontmatter incomplete**
   ```yaml
   # Ensure SKILL.md has this at the top:
   ---
   name: your-skill
   description: Description with trigger keywords
   ---
   ```

3. **Keywords not matching**
   - Check if your prompt contains trigger keywords
   - Use exact phrases from description
   - Try more general terms

4. **Hook not registered**
   ```json
   // .claude/settings.json or .claude/settings.local.json
   {
     "hooks": {
       "UserPromptSubmit": [
         {
           "hooks": [{
             "type": "command",
             "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/skill-activation-prompt.sh"
           }]
         }
       ]
     }
   }
   ```

### Skill Exceeds 500 Lines

**Symptoms:**
- Warning about 500-line rule
- SKILL.md is very long

**Solution:**
```bash
# Check line count
wc -l .claude/skills/your-skill/SKILL.md

# Use progressive disclosure
mkdir -p .claude/skills/your-skill/resources

# Move detailed content to resources
# Keep main points in SKILL.md
```

**Example structure:**
```
your-skill/
├── SKILL.md          # Main guidelines (under 500 lines)
└── resources/
    ├── detailed-guide.md
    ├── examples.md
    └── patterns.md
```

### Missing SKILL.md

**Symptoms:**
- Validation fails
- Skill not recognized

**Solution:**
```bash
# Create SKILL.md
cat > .claude/skills/your-skill/SKILL.md << 'EOF'
---
name: your-skill
description: Brief description
---

# Your Skill

## Purpose
What this skill does
EOF
```

---

## Agents

### Agent Not Found

**Symptoms:**
- "Agent not found" error
- Can't invoke agent

**Diagnosis:**
```bash
# Check if agent file exists
ls -la .claude/agents/your-agent.md

# Check filename (case-sensitive)
ls .claude/agents/ | grep -i your-agent
```

**Solutions:**

1. **Agent file missing**
   ```bash
   # Copy from source
   cp source/your-agent.md .claude/agents/
   ```

2. **Wrong filename**
   ```bash
   # Rename to match
   mv .claude/agents/Your-Agent.md .claude/agents/your-agent.md
   ```

3. **File not readable**
   ```bash
   # Check permissions
   chmod 644 .claude/agents/your-agent.md
   ```

### Agent Has Hardcoded Paths

**Symptoms:**
- Agent fails with path errors
- References non-existent directories

**Diagnosis:**
```bash
# Find hardcoded paths
grep -n "~/\|/root/\|/Users/" .claude/agents/your-agent.md
```

**Solution:**
```bash
# Replace with project-relative paths
sed -i 's|~/git/your-project|$CLAUDE_PROJECT_DIR|g' \
  .claude/agents/your-agent.md

# Or use relative paths
sed -i 's|/absolute/path/here|.|g' \
  .claude/agents/your-agent.md
```

### Agent Not Completing

**Symptoms:**
- Agent starts but doesn't finish
- No output from agent

**Diagnosis:**
```bash
# Check agent instructions
grep -A 5 "## Expected Output" .claude/agents/your-agent.md

# Check if agent has clear steps
grep -E "^#{1,3} " .claude/agents/your-agent.md
```

**Solution:**
- Ensure agent has clear "Expected Output" section
- Specify exactly what agent should return
- Add examples of good output
- Check agent instructions are complete

---

## Commands

### Command Not Found

**Symptoms:**
- `/command-name` doesn't work
- Command not recognized

**Diagnosis:**
```bash
# Check if command file exists
ls -la .claude/commands/your-command.md

# Check command name in file
head -5 .claude/commands/your-command.md
```

**Solution:**
```bash
# Ensure YAML frontmatter has name
cat > .claude/commands/your-command.md << 'EOF'
---
name: your-command
description: What this command does
---

# Command Name

## What This Command Does
...
EOF
```

### Command Not Invoking Agent

**Symptoms:**
- Command should use agent but doesn't
- Agent not called

**Diagnosis:**
```bash
# Check if command references agent
grep -i "agent" .claude/commands/your-command.md
```

**Solution:**
```markdown
# In your command.md, explicitly invoke agent

Use the **agent-name** agent to:
1. Do task A
2. Do task B
3. Return results
```

---

## Hooks

### Hook Not Executing

**Symptoms:**
- Hook never runs
- No output from hook
- Skills not activating

**Diagnosis:**
```bash
# 1. Check if hook is registered
grep -r "skill-activation-prompt" .claude/settings*.json

# 2. Check if hook file exists
ls -la .claude/hooks/skill-activation-prompt.*

# 3. Check if hook is executable
ls -la .claude/hooks/*.sh

# 4. Check permissions
stat .claude/hooks/skill-activation-prompt.sh
```

**Solutions:**

1. **Hook not in settings.json**
   ```json
   // Add to .claude/settings.json
   {
     "hooks": {
       "UserPromptSubmit": [{
         "hooks": [{
           "type": "command",
           "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/skill-activation-prompt.sh"
         }]
       }]
     }
   }
   ```

2. **Hook not executable**
   ```bash
   chmod +x .claude/hooks/*.sh
   chmod +x .claude/hooks/*.ts
   ```

3. **Wrong path in settings.json**
   ```bash
   # Use environment variable
   $CLAUDE_PROJECT_DIR/.claude/hooks/hook-name.sh

   # Or absolute path (not recommended)
   /absolute/path/to/.claude/hooks/hook-name.sh
   ```

### TypeScript Hook Failing

**Symptoms:**
- TypeScript errors
- Hook exits with error
- No output

**Diagnosis:**
```bash
# 1. Check TypeScript installation
cd .claude/hooks
npm list typescript tsx

# 2. Type check
npm run check

# 3. Test hook manually
echo '{"prompt":"test"}' | npx tsx skill-activation-prompt.ts
```

**Solutions:**

1. **Missing dependencies**
   ```bash
   cd .claude/hooks
   npm install
   ```

2. **TypeScript errors**
   ```bash
   # Fix type errors
   npm run check 2>&1 | head -20

   # Common fixes:
   # - Add proper types
   # - Import missing modules
   # - Fix interface definitions
   ```

3. **Execution error**
   ```bash
   # Check shebang
   head -1 .claude/hooks/hook.ts
   # Should be: #!/usr/bin/env node

   # Add if missing
   sed -i '1s|^|#!/usr/bin/env node\n|' .claude/hooks/hook.ts
   ```

### Hook Blocking When It Shouldn't

**Symptoms:**
- Operations blocked unexpectedly
- "Hook blocked operation" error

**Diagnosis:**
```bash
# Check hook exit codes
echo '{"test":"data"}' | npx tsx hook.ts; echo "Exit code: $?"

# Exit code 2 = BLOCK (for PreToolUse hooks)
```

**Solution:**
```typescript
// Change exit code from 2 to 0 or 1
process.exit(0);  // Success, continue
process.exit(1);  // Warning, continue with message
process.exit(2);  // Error, BLOCK (use carefully!)
```

---

## General Issues

### Files Not Tracked by Git

**Symptoms:**
- `git status` shows many untracked files
- Changes not saved

**Diagnosis:**
```bash
# Check untracked files
git status --porcelain | grep "^??"

# Count untracked files
git status --porcelain | grep "^??" | wc -l
```

**Solution:**
```bash
# Add all .claude files
git add .claude/

# Or selectively
git add .claude/agents/*.md
git add .claude/commands/*.md
git add .claude/skills/*/

# Commit
git commit -m "feat: Add skills, agents, and commands"
```

### Broken References in Documentation

**Symptoms:**
- Links don't work
- References to non-existent files
- `showcase/` or `claude-code-infrastructure-showcase/` paths

**Diagnosis:**
```bash
# Find broken references
grep -r "showcase/" .claude/
grep -r "claude-code-infrastructure-showcase/" .claude/

# Find all relative links
grep -r "\[.*\](" .claude/README*.md | grep "^\.\./\|../../"
```

**Solution:**
```bash
# Update to use current project name
sed -i 's|showcase/|claude-skill/|g' .claude/README*.md
sed -i 's|claude-code-infrastructure-showcase/|claude-skill/|g' .claude/README*.md

# Or use relative paths from doc location
# From .claude/agents/README.md to root: ../../
```

### Permission Errors

**Symptoms:**
- "Permission denied" errors
- Hooks not executing
- Scripts not running

**Diagnosis:**
```bash
# Check file permissions
ls -la .claude/hooks/*.sh
ls -la .claude/scripts/*.sh

# Should show rwxr-xr-x (755)
```

**Solution:**
```bash
# Make scripts executable
chmod +x .claude/hooks/*.sh
chmod +x .claude/scripts/*.sh
chmod +x .claude/hooks/*.ts

# Or recursively
find .claude -name "*.sh" -exec chmod +x {} \;
find .claude -name "*.ts" -exec chmod +x {} \;
```

---

## Validation

### Run Skill Validation

**Validate all skills:**
```bash
bash .claude/scripts/validate-skill.sh
```

**Validate specific skill:**
```bash
bash .claude/scripts/validate-skill.sh skill-name
```

**Expected output:**
```
=== Validating: skill-name ===
✓ SKILL.md exists
  ✓ name: skill-name
  ✓ description: Description...
✓ VALID

=== Validation Summary ===
Total skills:     36
Valid skills:     36
Invalid skills:   0
Total warnings:  7

✓ All skills are valid!
```

### Validate Agent Structure

```bash
# Check for required YAML frontmatter
for file in .claude/agents/*.md; do
  if ! grep -q "^name:" "$file"; then
    echo "Missing name: $file"
  fi
  if ! grep -q "^description:" "$file"; then
    echo "Missing description: $file"
  fi
done
```

### Validate Command Structure

```bash
# Check all commands have proper frontmatter
for file in .claude/commands/*.md; do
  echo "Checking: $file"
  head -10 "$file" | grep -E "^name:|^description:"
done
```

---

## Performance

### Hooks Are Slow

**Symptoms:**
- Delayed responses
- Hooks taking long to execute

**Diagnosis:**
```bash
# Time hook execution
time echo '{"prompt":"test"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts

# Should be < 100ms for simple hooks
# < 200ms for complex hooks
```

**Solutions:**

1. **Cache results**
   ```bash
   # Hook should cache expensive operations
   # Use .claude/hooks/cache/ directory
   ```

2. **Optimize patterns**
   ```typescript
   // Use simpler regex patterns
   // Avoid complex nested loops
   // Cache skill-rules.json parsing
   ```

3. **Reduce file reads**
   ```typescript
   // Read files once, not in loops
   // Use process.cwd() caching
   // Avoid fs.existsSync() in hot paths
   ```

### Too Many Skill Suggestions

**Symptoms:**
- Long list of skills on every prompt
- Irrelevant skills suggested

**Diagnosis:**
```bash
# Check skill triggers
grep -A 5 "promptTriggers" .claude/skills/skill-rules.json
```

**Solution:**
```json
// Make triggers more specific
{
  "your-skill": {
    "promptTriggers": {
      "keywords": ["very", "specific", "keyword"],
      "intentPatterns": ["(create|make).*?very specific thing"]
    }
  }
}
```

---

## Getting Help

### Collect Diagnostic Information

```bash
# Create diagnostic bundle
cat > diagnostic-info.txt << 'EOF'
=== System Information ===
OS: $(uname -a)
Node: $(node --version)
NPM: $(npm --version)

=== Git Status ===
$(git status --short)

=== File Counts ===
Skills: $(find .claude/skills -name SKILL.md | wc -l)
Agents: $(find .claude/agents -name "*.md" | wc -l)
Commands: $(find .claude/commands -name "*.md" | wc -l)
Hooks: $(find .claude/hooks -name "*.sh" -o -name "*.ts" | wc -l)

=== Validation ===
$(bash .claude/scripts/validate-skill.sh 2>&1 | tail -20)

=== Hook Test ===
$(echo '{"prompt":"test"}' | npx tsx .claude/hooks/skill-activation-prompt.ts 2>&1 | head -10)
EOF

cat diagnostic-info.txt
```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Agent not found` | Agent file missing | Create agent file in `.claude/agents/` |
| `Skill not found` | SKILL.md missing or invalid | Run validation script |
| `Hook exited with code 2` | Guardrail blocked operation | Fix the issue or use skip marker |
| `Permission denied` | Script not executable | Run `chmod +x` on script |
| `Cannot find module` | Missing dependencies | Run `npm install` in hooks directory |
| `Unexpected token` | TypeScript syntax error | Run `npm run check` to find errors |

---

**Last Updated:** 2025-03-09
**Version:** 1.0.0

For more help, see:
- [Skill Structure Standards](.claude/SKILL_STRUCTURE_STANDARDS.md)
- [TypeScript Build Guide](.claude/hooks/TYPESCRIPT_BUILD_GUIDE.md)
- [CLAUDE_INTEGRATION_GUIDE.md](CLAUDE_INTEGRATION_GUIDE.md)
