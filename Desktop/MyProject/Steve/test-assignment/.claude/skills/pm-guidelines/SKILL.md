---
name: pm-guidelines
description: Comprehensive product management guidelines for planning, documentation, stakeholder communication, and project execution. Use when creating PRDs, planning sprints, writing requirements, managing roadmaps, or any PM-related task.
---

# Product Management Guidelines

Production-tested patterns and best practices for product management.

## When This Skill Activates

This skill should be used when:
- Creating Product Requirement Documents (PRDs)
- Planning sprints and releases
- Writing user stories and acceptance criteria
- Managing product roadmaps
- Communicating with stakeholders
- Prioritizing features and backlog
- Running meetings and ceremonies

## Quick Reference

### PM Documents
- **PRD:** Product Requirements Document
- **RFC:** Request for Comments
- **A/B Test Plan:** Experiment design
- **Sprint Plan:** Iteration planning
- **Roadmap:** Strategic timeline

## Resources

- [PRD Template](resources/prd-template.md) - Product requirements documentation
- [User Stories](resources/user-stories.md) - Writing effective user stories
- [Sprint Planning](resources/sprint-planning.md) - Running sprints effectively
- [Stakeholder Communication](resources/stakeholder-communication.md) - Updates, reports, alignment
- [Roadmap Planning](resources/roadmap-planning.md) - Strategic planning and prioritization
- [Metrics and KPIs](resources/metrics-and-kpis.md) - Measuring success

## Key Principles

### 1. Start with Why
Every feature, epic, and initiative should have:
- Clear problem statement
- Measurable success criteria
- Alignment with business goals

### 2. Write Clear Requirements
```markdown
## Feature: User Authentication

### Problem
Users cannot securely access their accounts, leading to support tickets and churn.

### Success Metrics
- Reduce password reset tickets by 30%
- Increase successful logins by 15%
- Decrease average login time to < 5 seconds

### User Stories
- As a user, I want to log in with email/password
- As a user, I want to reset my password via email
- As a user, I want to stay logged in securely

### Acceptance Criteria
- [ ] Login form validates email format
- [ ] Password minimum 8 characters
- [ ] "Remember me" functionality works for 30 days
- [ ] Password reset email sent within 1 minute
```

### 3. Prioritize Ruthlessly
Use frameworks like:
- **RICE:** Reach × Impact × Confidence / Effort
- **MoSCoW:** Must, Should, Could, Won't
- **Kano:** Basic, Performance, Delighters

### 4. Communicate Proactively
- Weekly status updates
- Risk escalation early
- Demo completed work

## Document Templates

### PRD Structure
```markdown
# [Feature Name] - Product Requirements Document

## Metadata
- Status: Draft | In Review | Approved
- Owner: [PM Name]
- Team: [Team Name]
- Target Release: [Version/Date]

## Problem Statement
[What problem are we solving? Why now?]

## Goals & Success Metrics
| Goal | Metric | Target |
|------|--------|--------|
| [Goal] | [Metric] | [Target] |

## User Stories
[Detailed user stories with acceptance criteria]

## Requirements
### Functional Requirements
- FR-1: [Requirement]

### Non-Functional Requirements
- NFR-1: [Requirement]

## Out of Scope
[What we're explicitly NOT doing]

## Risks & Dependencies
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|

## Timeline
[Key milestones and dates]
```

## Sprint Planning Template
```markdown
# Sprint [Number] Plan

## Sprint Goals
1. [Primary goal]
2. [Secondary goal]

## Capacity
- Total points: [X]
- Team members: [Names + availability]

## Sprint Backlog
| Ticket | Points | Assignee | Status |
|--------|--------|----------|--------|

## Dependencies
- [Dependency 1]
- [Dependency 2]

## Risks
- [Risk 1]

## Definition of Done
- [ ] Code reviewed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Deployed to staging
```

## Common Commands

```bash
# Create new PRD from template
cp templates/prd-template.md docs/prd/[feature-name].md

# Generate sprint report
npm run report:sprint -- --sprint=X

# Update roadmap
npm run roadmap:update