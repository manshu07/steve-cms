# Strategic Compact Guide

## Understanding Context Compaction

### What is Context Compaction?

Context compaction (`/compact`) is a Claude Code feature that truncates conversation history to free up tokens while preserving essential information. It's like taking a snapshot of your work and clearing away the intermediate steps.

### Why Manual Compaction?

**Auto-compaction problems:**
- Triggers at arbitrary token counts (e.g., 150K tokens)
- No awareness of task phase boundaries
- Can compact mid-implementation, losing critical context
- May delete important reasoning or file contents you just read

**Strategic compaction benefits:**
- Control WHEN to compact (at logical boundaries)
- Preserve critical context for active work
- Clear bulky research/exploration before execution
- Start fresh for new phases

---

## Phase-Aware Compaction Strategy

### Phase 1: Exploration & Research

**Characteristics:**
- Lots of file reads
- Code exploration
- Analysis and reasoning
- Understanding architecture

**When to compact:**
✅ **After exploration is complete** - Before moving to planning
✅ **After research phase** - Before writing implementation plan
❌ **Mid-exploration** - While still discovering how code works

**What to save before compacting:**
```markdown
# Exploration Summary

## Key Findings
- Authentication handled in apps/api/src/middleware/auth.ts
- Database schema in apps/api/supabase/migrations/
- State management uses Zustand (apps/web/src/lib/store.ts)

## Architecture Notes
- API routes in apps/web/app/api/
- Supabase client in apps/api/src/lib/supabase.ts
- Redis for caching (apps/api/src/lib/redis.ts)

## Files Modified
- None yet (exploration only)
```

---

### Phase 2: Planning & Design

**Characteristics:**
- Creating task lists
- Designing solutions
- Writing specifications
- Making implementation decisions

**When to compact:**
✅ **After plan is finalized** - Before starting implementation
✅ **After TodoWrite is populated** - Plan is now in persistent storage
❌ **While actively planning** - Before decisions are finalized

**What to save before compacting:**
```markdown
# Implementation Plan

## Tasks (from TodoWrite)
1. Add authentication middleware
2. Create login page component
3. Implement session management
4. Add protected routes
5. Write tests

## Design Decisions
- Using JWT for session tokens
- Storing tokens in httpOnly cookies
- Middleware checks token on protected routes
- Login page: apps/web/app/login/page.tsx

## Files to Create
- apps/api/src/middleware/auth.ts
- apps/web/app/login/page.tsx
- apps/web/src/components/LoginForm.tsx
- apps/api/src/app/api/auth/login/route.ts
```

---

### Phase 3: Implementation

**Characteristics:**
- Writing code
- Creating new files
- Making incremental changes
- Referring back to recent decisions

**When to compact:**
✅ **After completing a major feature** - Before starting unrelated feature
✅ **After fixing major bug** - Before continuing development
❌ **Mid-implementation** - While actively coding related changes
❌ **While refactoring** - Context is critical for consistency

**What to save before compacting:**
```markdown
# Implementation Status

## Completed
✅ Authentication middleware (apps/api/src/middleware/auth.ts)
✅ Login page (apps/web/app/login/page.tsx)
✅ Login form component (apps/web/src/components/LoginForm.tsx)

## In Progress
- Session management (apps/api/src/lib/session.ts) - 80% done
- Protected routes (apps/web/src/middleware/protected.ts) - Started

## Next Steps
1. Finish session management
2. Complete protected routes
3. Add logout functionality
4. Write tests for auth flow

## Important Context
- Using JWT with 24hr expiration
- Token stored in httpOnly cookie
- Session data in Redis for quick lookups
```

---

### Phase 4: Testing & Debugging

**Characteristics:**
- Writing tests
- Running test suites
- Debugging failures
- Fixing bugs

**When to compact:**
✅ **After debugging session** - Before new feature work
✅ **After completing test suite** - Before refactoring
❌ **While actively debugging** - Error traces are important
❌ **Mid-fix** - Partial fixes need context

**What to save before compacting:**
```markdown
# Testing Summary

## Tests Written
✅ Unit tests for auth middleware (10 tests, 100% coverage)
✅ Integration tests for login flow (5 tests)
✅ E2E tests for protected routes (3 tests)

## Bugs Fixed
- Fixed token validation (incorrect header parsing)
- Fixed session expiration (wrong time calculation)
- Fixed redirect loop in protected routes

## Known Issues
- None remaining

## Coverage
- Overall: 87%
- Auth module: 95%
```

---

## Real-World Examples

### Example 1: Multi-Phase Feature Development

**Session flow:**

1. **Exploration** (50 tool calls)
   - Read 15 files to understand auth system
   - Explored database schema
   - Reviewed existing middleware

   ✅ **COMPACT HERE** - Save exploration summary, clear bulk

2. **Planning** (15 tool calls)
   - Created TodoWrite with 12 tasks
   - Designed new authentication flow
   - Decided on JWT + httpOnly cookies

   ✅ **COMPACT HERE** - Plan is in TodoWrite, free context for implementation

3. **Implementation** (75 tool calls)
   - Created 8 new files
   - Modified 5 existing files
   - Wrote code continuously

   ❌ **NO COMPACT** - Mid-implementation, need context
   - File names, variable names, recent changes are critical

4. **Testing** (30 tool calls)
   - Wrote 18 tests
   - Debugged 3 failures
   - Fixed 2 bugs

   ✅ **COMPACT HERE** - Testing done, before next feature

5. **Next Feature** (Starting now)
   - Fresh context
   - Reference test coverage if needed

---

### Example 2: Long Debugging Session

**Session flow:**

1. **Initial implementation** (40 tool calls)
   - Created feature
   - Tests passing
   - All good

2. **Bug report** (5 tool calls)
   - Read issue description
   - Reproduced bug
   - Started investigation

3. **Debugging** (65 tool calls)
   - Added console.log statements
   - Read multiple files to trace execution
   - Tried 3 different approaches
   - Found root cause
   - Fixed bug
   - Verified fix
   - Removed debug statements

   ✅ **COMPACT HERE** - Debug traces are noise now
   - Save: "Fixed bug in X by doing Y"

4. **Continue development**
   - Fresh context
   - Bug is resolved, no need for investigation context

---

### Example 3: Research → Implementation

**Session flow:**

1. **Deep research** (80 tool calls)
   - Researched 5 different libraries
   - Compared features
   - Read documentation
   - Tested 3 options
   - Made decision

   ✅ **COMPACT HERE** - Clear all research, keep decision
   - Save: "Chose library X because Y, Z reasons"

2. **Implementation** (60 tool calls)
   - Implemented with chosen library
   - Followed examples from docs
   - Created integration

   ✅ **COMPACT HERE** - Implementation complete

3. **Documentation** (20 tool calls)
   - Wrote README
   - Added code comments
   - Created examples

---

## Compaction Templates

### Template 1: After Exploration

```markdown
# Exploration Complete

## What I Learned
[Key findings about architecture, patterns, file locations]

## Critical Files
- File A: Does X
- File B: Does Y
- File C: Does Z

## Decisions Made
[Any decisions made during exploration]

## Next Phase
[Planning or Implementation - clear statement of what's next]
```

### Template 2: After Planning

```markdown
# Plan Finalized

## Implementation Plan
[Summary of what will be built]

## Tasks
[Reference TodoWrite or list key tasks]

## Design Decisions
[Technical choices made]

## Files to Create/Modify
[List of files]

## Next Step
[First concrete action to take]
```

### Template 3: Mid-Implementation Checkpoint

```markdown
# Implementation Checkpoint

## Completed
✅ [Feature 1]
✅ [Feature 2]

## In Progress
→ [Feature 3] (X% complete)
→ [Feature 4] (started)

## Blockers
[Any issues preventing progress]

## Next Actions
1. [Concrete next step]
2. [Step after that]
```

### Template 4: After Bug Fix

```markdown
# Bug Fixed

## Bug Description
[What was broken]

## Root Cause
[Why it was broken]

## Fix Applied
[What was changed]

## Files Modified
- [File A]: [Change made]
- [File B]: [Change made]

## Verification
[How fix was tested]
```

---

## Advanced Techniques

### Technique 1: Selective Context Preservation

Before compacting, write critical context to a file:

```markdown
# apps/api/.claude-context.md

## Current Work
Implementing authentication middleware

## Important Variables
- JWT_SECRET: Used for signing tokens
- TOKEN_EXPIRY: 24 hours (86400 seconds)
- REDIS_SESSION_KEY: "session:{token}"

## Critical Functions
- `verifyToken()`: Validates JWT, returns user object
- `createSession()`: Creates session in Redis
- `getSession()`: Retrieves session from Redis

## Recent Changes
- Added auth middleware (2025-03-08)
- Modified login route to use JWT
- Created session management utilities
```

Then after compacting, reference this file:

```markdown
Please read apps/api/.claude-context.md to understand current work
before continuing with authentication implementation.
```

### Technique 2: Memory Files

Use Claude Code's memory persistence:

```bash
# Before compacting
echo "Current focus: Implementing auth middleware. Key files:
- apps/api/src/middleware/auth.ts
- apps/web/src/lib/auth.ts
Decisions: JWT + httpOnly cookies, Redis sessions" > ~/.claude/memory/auth-work.md
```

After compaction, reference memory:

```markdown
I'm working on authentication. Check ~/.claude/memory/auth-work.md for context.
```

### Technique 3: Git Commits as Checkpoints

Use git commits to save work state:

```bash
# Before compacting
git add .
git commit -m "Checkpoint: auth middleware implementation complete

- JWT authentication implemented
- Login page created
- Session management in place
- Ready for testing phase"
```

After compacting:

```markdown
Continue from commit "Checkpoint: auth middleware implementation complete"
Next phase: Write tests for auth flow
```

---

## Troubleshooting

### Problem: Compacted too early, lost context

**Solution:**
1. Use git to recover recent changes: `git diff`
2. Read recently modified files to rebuild context
3. Check TodoWrite for task list
4. Run tests to understand what works

### Problem: Didn't compact, running out of context

**Signs:**
- Responses slowing down
- Claude forgetting earlier decisions
- Re-reading files multiple times
- Losing track of conversation flow

**Solution:**
1. Stop and assess current phase
2. Save critical context to file
3. Run `/compact` with clear summary
4. Continue with fresh context

### Problem: Not sure if should compact

**Decision tree:**
1. Am I mid-implementation of related changes? → NO: Don't compact
2. Have I just completed a phase? → YES: Compact
3. Am I switching to unrelated work? → YES: Compact
4. Is context feeling slow/lossy? → YES: Compact

---

## Configuration Options

### Adjust Threshold

Default: Suggest after 50 tool calls

```bash
# Earlier suggestions (30 calls)
export COMPACT_THRESHOLD=30

# Later suggestions (100 calls)
export COMPACT_THRESHOLD=100

# Disable suggestions
export COMPACT_THRESHOLD=0
```

### Adjust Reminder Interval

Default: Remind every 25 calls after threshold

```bash
# More frequent reminders (every 15 calls)
export COMPACT_INTERVAL=15

# Less frequent (every 50 calls)
export COMPACT_INTERVAL=50
```

### Set for Single Session

```bash
# Before starting Claude Code session
COMPACT_THRESHOLD=75 COMPACT_INTERVAL=30 claude-code
```

---

## Integration with Workflows

### Pre-Commit Workflow

```bash
# Before committing
1. Run verification (build, test, lint)
2. Save implementation status to file
3. Commit changes
4. Compact to clear implementation context
5. Start fresh for next feature
```

### Pre-PR Workflow

```bash
# Before creating PR
1. Ensure all tests pass
2. Update documentation
3. Save summary of changes
4. Compact to clear development context
5. Ready for code review
```

### Feature Complete Workflow

```bash
# Feature complete
1. All tests passing
2. Documentation updated
3. Commit with "Feature: X complete"
4. Write feature summary to memory
5. Compact with summary: "Feature X complete, starting feature Y"
```

---

## Best Practices Summary

1. **Compact at phase boundaries** - Research → Plan → Implement → Test
2. **Don't compact mid-implementation** - Preserve context for active work
3. **Save before compacting** - Write critical context to files or memory
4. **Use descriptive summaries** - Help future-you understand what was done
5. **Leverage git commits** - Use commits as checkpoints
6. **Check TodoWrite** - Task list persists through compaction
7. **Monitor performance** - Compact if responses slow down
8. **Trust your judgment** - The hook suggests, YOU decide

---

This guide provides comprehensive strategies for effective context compaction across different development phases and workflows.
