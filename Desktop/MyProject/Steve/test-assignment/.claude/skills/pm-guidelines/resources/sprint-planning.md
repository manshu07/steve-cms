# Sprint Planning Guide

## Sprint Structure

### Typical Sprint
- **Duration:** 2 weeks
- **Ceremonies:** Planning, Daily Standups, Review, Retro

## Sprint Planning Meeting

### Agenda
1. Review product goals (10 min)
2. Discuss proposed sprint backlog (30 min)
3. Break down stories into tasks (20 min)
4. Team commitment (10 min)

### Inputs
- Prioritized backlog
- Team capacity
- Velocity data
- Dependencies identified

### Outputs
- Sprint goal
- Sprint backlog
- Task breakdown
- Capacity allocation

## Capacity Planning

```markdown
## Team Capacity

| Team Member | Availability | Points Capacity |
|-------------|--------------|-----------------|
| Developer A | 100% | 8 |
| Developer B | 80% | 6 |
| Developer C | 100% | 8 |
| **Total** | | **22** |
```

## Sprint Backlog Format

```markdown
# Sprint 42 Plan

## Sprint Goal
Complete user authentication flow including password reset.

## Capacity
- Total points: 22
- Sprint dates: Jan 15 - Jan 29

## Sprint Backlog

| Ticket | Title | Points | Assignee | Status |
|--------|-------|--------|----------|--------|
| AUTH-101 | Login form | 3 | Dev A | In Progress |
| AUTH-102 | Password validation | 2 | Dev B | To Do |
| AUTH-103 | Reset email flow | 5 | Dev C | To Do |
| AUTH-104 | Session management | 5 | Dev A | To Do |
| AUTH-105 | OAuth integration | 8 | Dev B | Backlog |

## Risks
- OAuth provider approval pending

## Definition of Done
- [ ] Code reviewed and merged
- [ ] Unit tests passing
- [ ] QA verified
- [ ] Documentation updated
```

## Daily Standup

### Format
```
1. What I completed yesterday
2. What I'm working on today
3. Any blockers
```

### Best Practices
- Time box to 15 minutes
- Focus on blockers
- Take discussions offline

## Sprint Review

### Agenda
1. Demo completed work (30 min)
2. Stakeholder feedback (15 min)
3. Update backlog (15 min)

## Sprint Retrospective

### Format
```
What went well?
What could be improved?
Action items for next sprint
```

### Action Item Template
```markdown
| Issue | Action Item | Owner | Due Date |
|-------|-------------|-------|----------|
| Too many meetings | No-meeting Wednesdays | PM | Next sprint |