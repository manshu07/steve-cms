# Product Requirements Document Template

## Document Header

```markdown
# [Feature/Product Name] - Product Requirements Document

| Field | Value |
|-------|-------|
| Status | Draft / In Review / Approved / In Progress |
| Created | [Date] |
| Updated | [Date] |
| Owner | [PM Name] |
| Team | [Team Name] |
| Target Release | [Version/Date] |
| Stakeholders | [List of stakeholders] |
```

## Sections

### 1. Executive Summary
Brief overview of what this PRD covers. 2-3 sentences maximum.

### 2. Problem Statement
```markdown
## Problem Statement

### Current State
[Describe the current situation and its issues]

### Pain Points
- Pain point 1
- Pain point 2

### Impact
[Quantify the business impact if possible]
- Support tickets: X/week
- Revenue impact: $X
- User churn: X%

### Why Now?
[Why is this the right time to solve this?]
```

### 3. Goals & Success Metrics
```markdown
## Goals & Success Metrics

### Primary Goal
[The main objective]

### Success Metrics
| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| [Metric 1] | X | Y | [How measured] |
| [Metric 2] | X | Y | [How measured] |

### Leading Indicators
- [Indicator that will show early progress]

### Lagging Indicators
- [Indicator that shows final outcome]
```

### 4. User Stories
```markdown
## User Stories

### Epic: [Epic Name]

#### Story 1: [Story Title]
**As a** [type of user]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

**Notes:**
- Additional context or constraints

#### Story 2: [Story Title]
...
```

### 5. Requirements
```markdown
## Requirements

### Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-1 | [Requirement] | Must/Should/Could | |
| FR-2 | [Requirement] | Must/Should/Could | |

### Non-Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| NFR-1 | Performance: [specific requirement] | Must | |
| NFR-2 | Security: [specific requirement] | Must | |
| NFR-3 | Accessibility: [specific requirement] | Should | |

### Technical Requirements
- [Technical constraint or requirement]
- [Integration requirement]
```

### 6. Out of Scope
```markdown
## Out of Scope

### Explicitly Not Included
- [Feature/requirement explicitly excluded]
- [Future phase items]

### Future Considerations
- [Items to consider for later releases]
```

### 7. Risks & Dependencies
```markdown
## Risks & Dependencies

### Risks
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|------------|--------|------------|-------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Plan] | [Name] |

### Dependencies
| Dependency | Type | Status | Impact if Delayed |
|------------|------|--------|-------------------|
| [Dependency 1] | Internal/External | On Track/At Risk | |

### Assumptions
- [Assumption 1]
- [Assumption 2]
```

### 8. Timeline & Milestones
```markdown
## Timeline & Milestones

### Key Milestones
| Milestone | Date | Deliverable |
|-----------|------|-------------|
| Design Complete | [Date] | Mockups approved |
| Development Start | [Date] | Sprint kickoff |
| Alpha Release | [Date] | Internal testing |
| Beta Release | [Date] | Limited rollout |
| GA Release | [Date] | Full launch |

### Phases
**Phase 1: [Name] ([Date Range])**
- Deliverables
- Key activities

**Phase 2: [Name] ([Date Range])**
- Deliverables
- Key activities
```

### 9. Stakeholders & Approvals
```markdown
## Stakeholders & Approvals

### Required Approvals
| Role | Name | Status | Date |
|------|------|--------|------|
| Engineering Lead | | Pending | |
| Design Lead | | Pending | |
| Product Lead | | Pending | |

### Communication Plan
- [How updates will be shared]
- [Cadence of updates]
```

### 10. Appendix
```markdown
## Appendix

### Related Documents
- [Link to related PRDs]
- [Link to research]
- [Link to designs]

### Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial version |
```

## Complete Example

```markdown
# User Dashboard Redesign - Product Requirements Document

| Field | Value |
|-------|-------|
| Status | In Review |
| Created | 2024-01-15 |
| Updated | 2024-01-20 |
| Owner | Jane Smith |
| Team | Platform Team |
| Target Release | Q2 2024 |
| Stakeholders | Sales, Support, Engineering |

## Problem Statement

### Current State
The current user dashboard displays outdated metrics and has a confusing navigation structure.

### Pain Points
- Users cannot find key actions
- Data is 24 hours delayed
- Mobile experience is broken

### Impact
- Support tickets: 50/week related to dashboard
- Users abandon dashboard after 30 seconds (avg)
- NPS score: 32 (low)

### Why Now?
Major customer requested improvement, contract renewal dependent on Q2 delivery.

## Goals & Success Metrics

### Primary Goal
Improve dashboard usability and data freshness to increase user engagement.

### Success Metrics
| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| Dashboard NPS | 32 | 50+ | Quarterly survey |
| Avg session time | 30 sec | 2 min+ | Analytics |
| Support tickets | 50/week | <10/week | Zendesk |

## User Stories

### Epic: Dashboard Redesign

#### Story 1: View Real-time Metrics
**As a** dashboard user
**I want to** see metrics updated within 5 minutes
**So that** I can make timely decisions

**Acceptance Criteria:**
- [ ] Given I'm on the dashboard, when data updates, then I see changes within 5 min
- [ ] Given I'm viewing metrics, when I refresh, then data is current

## Requirements

### Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-1 | Display real-time metrics | Must | < 5 min latency |
| FR-2 | Mobile responsive design | Must | All screen sizes |
| FR-3 | Customizable widgets | Should | Drag and drop |

### Non-Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| NFR-1 | Page load < 3 seconds | Must | Measured at P95 |
| NFR-2 | WCAG 2.1 AA compliant | Should | Accessibility |

## Out of Scope
- Dark mode (Phase 2)
- Custom dashboard templates (Phase 3)

## Risks & Dependencies
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Data pipeline delays | Medium | High | Parallel workstream |

## Timeline
| Milestone | Date | Deliverable |
|-----------|------|-------------|
| Design Complete | Feb 1 | Final mockups |
| Development Start | Feb 15 | Sprint kickoff |
| Alpha Release | Mar 15 | Internal testing |
| GA Release | Apr 1 | Full launch |