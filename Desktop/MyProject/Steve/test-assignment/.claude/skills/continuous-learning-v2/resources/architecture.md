# Continuous Learning v2.1 - Instinct System

## Instinct Structure

### What is an Instinct?

An instinct is a small, atomic learned behavior:

```json
{
  "id": "react-usememo-deps",
  "type": "code_pattern",
  "description": "Always include all dependencies in useMemo hooks",
  "pattern": "Include every value used in useMemo in the dependency array",
  "confidence": 0.85,
  "scope": "project",
  "project_id": "repo-hash-abc123",
  "first_seen": "2025-03-08T10:00:00Z",
  "seen_count": 15,
  "success_rate": 0.93
}
```

## Project-Scoped Instincts

### Scope Levels

```json
{
  "scope": "global",
  "applies_to": "all_projects"
}

{
  "scope": "project",
  "project_id": "repo-hash-abc123",
  "applies_to": "this_repo_only"
}
```

### Project Detection

```bash
# detect-project.sh
PROJECT_ID=$(git remote get-url origin | sha256sum | cut -d' ' -f1)
REPO_PATH=$(git rev-parse --show-toplevel | sha256sum | cut -d' ' -f1)
PROJECT_SIGNATURE="${PROJECT_ID}-${REPO_PATH}"
```

## Observation Hook

### Hook Installation

```bash
# Add to .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/skills/continuous-learning-v2/hooks/observe.sh"
          }
        ]
      }
    ]
  }
}
```

### Observer Script

```bash
#!/bin/bash
# observe.sh - Capture tool usage for instinct extraction

TOOL_NAME=$1
FILE_PATH=$2
PROJECT_ID=$3

# Log observation
echo "{
  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
  \"tool\": \"$TOOL_NAME\",
  \"file\": \"$FILE_PATH\",
  \"project_id\": \"$PROJECT_ID\"
}" >> ~/.claude/homunculus/observations.jsonl
```

## Instinct Evolution

### Confidence Scoring

```python
def calculate_confidence(instinct):
    """
    Update instinct confidence based on feedback
    """
    base = instinct['confidence']

    # Increment for each successful use
    for use in instinct['recent_uses']:
        if use['successful']:
            base += 0.05
        else:
            base -= 0.1

    # Decay toward 0.5 over time
    base = (base + 0.5) / 2

    return min(max(base, 0.0), 1.0)
```

### Promotion to Global

```python
def promote_to_global(instinct):
    """
    Promote project instinct to global when seen in 2+ projects
    """
    if instinct['seen_in_projects'] >= 2:
        instinct['scope'] = 'global'
        del instinct['project_id']
        save_instinct(instinct)
```

## Instinct Commands

### Status Command

```bash
# View all instincts
./skills/continuous-learning-v2/scripts/instinct-cli.py status

# Output:
Global Instincts: 15
Project Instincts (abc123): 23
Total Confidence: 0.82
```

### Export Command

```bash
# Export instincts to file
./skills/continuous-learning-v2/scripts/instinct-cli.py export instincts.json
```

### Import Command

```bash
# Import instincts from file
./skills/continuous-learning-v2/scripts/instinct-cli.py import instincts.json
```

### Promote Command

```bash
# Promote instinct to global
./skills/continuous-learning-v2/scripts/instinct-cli.py promote react-hooks-pattern
```

## Configuration

### config.json

```json
{
  "version": "2.1",
  "observer": {
    "enabled": false,
    "run_interval_minutes": 5,
    "min_observations_to_analyze": 20
  },
  "instincts": {
    "confidence_threshold": 0.7,
    "min_occurrences": 3,
    "promote_after_projects": 2
  },
  "storage": {
    "global_path": "~/.claude/homunculus/instincts/",
    "project_path": ".claude/instincts/",
    "observations_file": "observations.jsonl"
  }
}
```

## Background Agent

### Observer Loop

```bash
#!/bin/bash
# observer-loop.sh - Background observation agent

while true; do
  # Check for new observations
  NEW_OBSERVATIONS=$(find ~/.claude/homunculus/observations.jsonl -mmin -5 2>/dev/null)

  if [ -n "$NEW_OBSERVATIONS" ]; then
    # Process observations
    ./scripts/detect-project.sh > .claude/instincts/project-id

    # Analyze and extract instincts
    echo "Analyzing observations..."
    # Trigger background analysis agent
  fi

  # Wait before next check
  sleep 300  # 5 minutes
done
```

## Storage Structure

### Global Instincts

```
~/.claude/homunculus/
├── instincts/
│   ├── global/
│   │   ├── validate-input.json
│   │   ├── handle-errors.json
│   │   └── log-errors.json
│   └── observations.jsonl
```

### Project Instincts

```
.claude/instincts/
├── project-id
├── react-hooks.json
├── nextjs-routes.json
└── api-patterns.json
```

---

This resources file explains the v2.1 instinct-based learning system with project-scoped instincts.
