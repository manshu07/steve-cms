# Continuous Learning - Pattern Extraction

## Session Evaluation

### Evaluation Trigger

```bash
# Triggered on session end
.claude/hooks/stop/evaluate-session.sh
```

### Session Analysis

```python
class SessionAnalyzer:
    """
    Analyze completed Claude Code session to extract patterns
    """

    def analyze_session(self, session):
        """
        Extract reusable patterns from session
        """
        patterns = []

        # 1. Identify task patterns
        task_patterns = self.extract_tasks(session)
        patterns.extend(task_patterns)

        # 2. Identify solution patterns
        solution_patterns = self.extract_solutions(session)
        patterns.extend(solution_patterns)

        # 3. Identify workflow patterns
        workflow_patterns = self.extract_workflows(session)
        patterns.extend(workflow_patterns)

        return patterns
```

## Pattern Types

### Type 1: Code Patterns

```markdown
## Pattern: TypeScript Interface for API Response

**Context:**
When building REST APIs with Express, always include these fields in response interfaces.

**Pattern:**
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  timestamp: string;
}
```

**When to use:**
- All API endpoint responses
- Consistent error handling
- Type safety for frontend

**Confidence:** 0.9
```

### Type 2: Workflow Patterns

```markdown
## Pattern: Test-Driven Bug Fix Workflow

**Context:**
When fixing bugs, follow this TDD workflow to prevent regressions.

**Steps:**
1. Write failing test that reproduces bug
2. Run test to confirm failure
3. Implement fix
4. Run test to confirm pass
5. Write regression test
6. Check for side effects

**When to use:**
- All bug fixes
- Preventing regressions
- Ensuring tests cover edge cases

**Confidence:** 0.85
```

### Type 3: Decision Patterns

```markdown
## Pattern: When to Use useCallback

**Context:**
React optimization decision tree for callback memoization.

**Decision Tree:**
```
Is callback passed to memoized component?
├─ Yes → Use useCallback
└─ No → Does callback have dependencies?
    ├─ Yes → Use useCallback
    └─ No → No memoization needed
```

**When to use:**
- Optimizing React components
- Preventing unnecessary re-renders
- Performance debugging

**Confidence:** 0.75
```

## Skill Evolution

### Pattern → Skill

```python
def evolve_to_skill(pattern, confidence):
    """
    Evolve pattern into full skill when confidence is high
    """
    if confidence > 0.8:
        skill = {
            'name': generate_skill_name(pattern),
            'description': pattern.description,
            'triggers': extract_keywords(pattern),
            'examples': pattern.examples
        }
        save_skill(skill)
```

### Pattern → Command

```python
def evolve_to_command(pattern, frequency):
    """
    Convert high-frequency pattern into reusable command
    """
    if frequency > 10:  # Used in 10+ sessions
        command = {
            'name': generate_command_name(pattern),
            'description': pattern.description,
            'template': pattern.template
        }
        save_command(command)
```

## Learning Quality

### Confidence Scoring

```python
def score_pattern(pattern, session):
    """
    Score pattern based on session success
    """
    score = 0.0

    # Base score from session success
    if session.successful:
        score += 0.5

    # Increment for consistent usage
    if pattern.used_multiple_times:
        score += 0.2

    # Increment for positive feedback
    if session.user_feedback == 'positive':
        score += 0.3

    return min(score, 1.0)
```

### Pattern Validation

```python
def validate_pattern(pattern):
    """
    Validate pattern before saving
    """
    checks = [
        has_description(pattern),
        has_examples(pattern),
        is_specific(pattern),
        is_actionable(pattern)
    ]

    return all(checks)
```

## Storage

### Pattern Storage

```json
{
  "patterns": [
    {
      "id": "ts-api-response-interface",
      "name": "TypeScript API Response Interface",
      "type": "code",
      "confidence": 0.9,
      "sessions_seen": 15,
      "sessions_successful": 14,
      "first_seen": "2025-03-01",
      "last_seen": "2025-03-08",
      "pattern": "..."
    }
  ]
}
```

---

This resources file explains how the continuous learning system extracts and evolves patterns from sessions.
