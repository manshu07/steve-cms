# TypeScript Hooks Build Guide

## Overview

This guide explains how TypeScript hooks are built and executed in Claude Code. The hooks system uses TypeScript for type safety and better development experience, with `tsx` for direct execution without compilation.

## Architecture

### Hook Types

Claude Code supports hooks at these points:
- **UserPromptSubmit** - Before Claude sees user's prompt
- **PreToolUse** - Before tool execution (for validation/guardrails)
- **PostToolUse** - After tool completes (for tracking)
- **Stop** - When session ends (for cleanup/validation)

### TypeScript vs Bash Hooks

This project uses **both TypeScript and Bash hooks**:

| Hook Type | Language | When to Use | Example |
|-----------|----------|-------------|---------|
| TypeScript | `.ts` files | Complex logic, JSON parsing, type safety | `skill-activation-prompt.ts` |
| Bash | `.sh` files | Simple operations, file operations | `post-tool-use-tracker.sh` |

**Why TypeScript?**
- Type safety with interfaces
- Better JSON handling
- Easier to maintain complex logic
- IDE support and autocomplete

**Why Bash?**
- Simple file operations
- No dependencies needed
- Faster execution for simple tasks
- Portable across systems

## Build Process

### Key Insight: No Build Required!

The hooks use **`tsx`** (TypeScript Execute) which runs TypeScript files directly without compilation:

```bash
# This works directly - no build step needed!
npx tsx skill-activation-prompt.ts < input.json
```

**How it works:**
1. `tsx` reads TypeScript files
2. Transpiles in-memory using `esbuild`
3. Executes immediately
4. No `dist/` directory needed
5. No build step in CI/CD

### Package.json Scripts

```json
{
  "scripts": {
    "check": "tsc --noEmit",      // Type-check only (no output)
    "test": "tsx skill-activation-prompt.ts < test-input.json"
  }
}
```

**Note:** The `check` script validates types without generating output files.

## Setup Instructions

### 1. Install Dependencies

```bash
cd .claude/hooks
npm install
```

**Dependencies:**
- `typescript` - TypeScript compiler
- `tsx` - TypeScript executor
- `@types/node` - Node.js type definitions

### 2. Configure TypeScript

**File:** `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "resolveJsonModule": true,
    "types": ["node"]
  }
}
```

### 3. Create Hook Interface

**Example:** `skill-activation-prompt.ts`

```typescript
#!/usr/bin/env node
import { readFileSync } from 'fs';
import { join } from 'path';

// Define input interface
interface HookInput {
    session_id: string;
    transcript_path: string;
    cwd: string;
    permission_mode: string;
    prompt: string;
}

// Read stdin
const input = readFileSync(0, 'utf-8');
const data: HookInput = JSON.parse(input);

// Your hook logic here
console.log('Output to Claude');
```

### 4. Make Executable

```bash
chmod +x skill-activation-prompt.ts
```

### 5. Register in settings.json

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "npx tsx $CLAUDE_PROJECT_DIR/.claude/hooks/skill-activation-prompt.ts"
          }
        ]
      }
    ]
  }
}
```

## Execution Flow

### How Hooks Execute

```
User Action
    ↓
Claude Code triggers hook
    ↓
settings.json defines which command to run
    ↓
Command executes (either .sh or npx tsx .ts)
    ↓
Hook writes to stdout (Claude's input) or stderr (errors)
    ↓
Exit code determines behavior:
    - 0: Success, continue
    - 1: Warning, continue with message
    - 2: Error, BLOCK action (for PreToolUse guardrails)
```

### TypeScript Hook Execution

```
Claude Code
    ↓
Calls: npx tsx hook.ts < input.json
    ↓
tsx transpiles TypeScript in-memory
    ↓
Executes JavaScript
    ↓
Hook writes to stdout/stderr
    ↓
Exit code returned to Claude Code
```

## Development Workflow

### 1. Create Hook

```bash
# Create new TypeScript hook
touch .claude/hooks/my-hook.ts
chmod +x .claude/hooks/my-hook.ts
```

### 2. Develop with Types

```typescript
#!/usr/bin/env node
import { readFileSync } from 'fs';

interface MyHookInput {
    session_id: string;
    // ... your fields
}

const input: MyHookInput = JSON.parse(readFileSync(0, 'utf-8'));
// ... your logic
```

### 3. Test Locally

```bash
# Type check
npm run check

# Test with sample input
echo '{"prompt":"test"}' | npx tsx my-hook.ts
```

### 4. Register in settings.json

Add hook configuration to `.claude/settings.json` or `.claude/settings.local.json`

### 5. Restart Claude Code

Hooks load when Claude Code starts.

## Troubleshooting

### Hook Not Executing

**Check:**
```bash
# Is file executable?
ls -la .claude/hooks/my-hook.ts

# Make executable
chmod +x .claude/hooks/my-hook.ts
```

### TypeScript Errors

**Check:**
```bash
# Type check
npm run check

# Fix errors in IDE or with tsc output
npm run check 2>&1 | head -20
```

### Dependencies Missing

**Check:**
```bash
# Are node_modules present?
ls -la .claude/hooks/node_modules/

# Reinstall
cd .claude/hooks
npm install
```

### Hook Not in settings.json

**Check:**
```bash
# Is hook registered?
grep -r "my-hook" .claude/settings*.json

# Add to settings.json
```

### Permission Issues

**Check:**
```bash
# Can the script run?
npx tsx .claude/hooks/my-hook.ts < test-input.json

# Check exit code
echo $?  # Should be 0, 1, or 2
```

## Best Practices

### 1. Use TypeScript for Complex Logic

**Good for TypeScript:**
- JSON parsing and validation
- Complex string matching
- Data transformation
- Multi-step logic

**Example:**
```typescript
// Complex pattern matching
const intentPatterns = [
    /(create|add|make).*?skill/,
    /(new|custom).*?guidelines/
];

const hasMatch = intentPatterns.some(pattern =>
    pattern.test(prompt)
);
```

### 2. Use Bash for Simple Operations

**Good for Bash:**
- File existence checks
- Simple text processing
- Git operations
- File permissions

**Example:**
```bash
#!/usr/bin/env bash
# Simple file check
if [ -f "package.json" ]; then
    echo "Node.js project detected"
fi
```

### 3. Handle Errors Gracefully

```typescript
try {
    const input = JSON.parse(readFileSync(0, 'utf-8'));
    // Process input
} catch (error) {
    console.error('Error:', error);
    process.exit(1); // Warning, don't block
}
```

### 4. Use Exit Codes Correctly

```typescript
// Exit codes matter!
process.exit(0);  // Success, continue
process.exit(1);  // Warning, show message
process.exit(2);  // Error, BLOCK (PreToolUse only)
```

### 5. Write Type-Safe Code

```typescript
// Good: Type-safe
interface SkillRule {
    type: 'guardrail' | 'domain';
    enforcement: 'block' | 'suggest';
}

const rule: SkillRule = JSON.parse(data);

// Bad: No types
const rule = JSON.parse(data); // any type
```

## Testing

### Manual Testing

```bash
# Test hook directly
echo '{"prompt":"create a skill"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

### Automated Testing

Create `test-input.json`:
```json
{
  "session_id": "test-session",
  "prompt": "create a new skill",
  "cwd": "/project"
}
```

Run test:
```bash
npm test
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Type-check hooks
  run: |
    cd .claude/hooks
    npm install
    npm run check
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
cd .claude/hooks
npm run check || exit 1
```

## Summary

| Aspect | Details |
|--------|---------|
| **Build Required** | No - uses `tsx` for direct execution |
| **Dependencies** | `typescript`, `tsx`, `@types/node` |
| **Type Checking** | `npm run check` (no output) |
| **Execution** | `npx tsx hook.ts < input.json` |
| **Exit Codes** | 0 (success), 1 (warning), 2 (block) |
| **When to Use TS** | Complex logic, JSON, type safety needed |
| **When to Use Bash** | Simple operations, file tasks |

---

**Last Updated:** 2025-03-09
**Tested With:** TypeScript 5.3.3, tsx 4.7.0, Node.js 20+
