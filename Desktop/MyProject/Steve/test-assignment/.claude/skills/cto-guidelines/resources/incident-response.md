# Incident Response

## Incident Severity Levels

| Level | Description | Response Time | Example |
|-------|-------------|---------------|---------|
| SEV-1 | Critical | 15 min | Production down |
| SEV-2 | High | 1 hour | Major feature broken |
| SEV-3 | Medium | 4 hours | Feature degraded |
| SEV-4 | Low | 24 hours | Minor issue |

## Incident Response Process

### 1. Detection
- Monitoring alerts
- User reports
- Team escalation

### 2. Triage
```markdown
## Incident Triage Template

**Incident ID:** INC-[DATE]-[NUMBER]
**Time Detected:** [Timestamp]
**Detected By:** [Source]
**Initial Severity:** [SEV-1/2/3/4]

**Symptoms:**
- [Description of what's wrong]

**Affected Systems:**
- [List of affected services]

**Impact:**
- Users affected: [Number/Percentage]
- Business impact: [Description]
```

### 3. Response
```markdown
## Incident Response

**Incident Commander:** [Name]
**Communication Lead:** [Name]
**Technical Lead:** [Name]

**War Room:** [Link/Location]

**Status Updates:**
- Frequency: Every 30 min for SEV-1, 1 hour for SEV-2
- Channel: #incident-[id]

**Current Status:**
- [Investigating / Identified / Mitigating / Resolved]
```

### 4. Resolution
```markdown
## Resolution Steps

1. [Step taken]
2. [Step taken]
3. [Step taken]

**Root Cause:** [Description]
**Fix Applied:** [Description]
**Time to Resolution:** [Duration]
```

## Post-Incident Review

### Blameless Postmortem Template
```markdown
# Postmortem: [Incident Title]

## Summary
[One paragraph summary]

## Impact
- Duration: [Start] to [End]
- Users affected: [Number]
- Revenue impact: [Amount]

## Timeline
| Time | Event |
|------|-------|
| 10:00 | Alert triggered |
| 10:05 | Team paged |
| 10:15 | Root cause identified |
| 10:30 | Fix deployed |

## Root Cause
[Detailed technical explanation]

## Contributing Factors
- Factor 1
- Factor 2

## What Went Well
- Quick detection
- Effective communication
- Fast resolution

## What Could Improve
- Better monitoring
- Faster escalation

## Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| Add alerting | Team A | 1 week |
| Update runbook | Team B | 2 weeks |
```

## On-Call Guidelines

### Responsibilities
- First response to alerts
- Escalation when needed
- Documentation of incidents

### Escalation Path
1. On-call engineer
2. Team lead
3. Engineering manager
4. CTO

### On-Call Rotation
- Weekly rotations
- Handoff on Monday
- Primary + Secondary coverage