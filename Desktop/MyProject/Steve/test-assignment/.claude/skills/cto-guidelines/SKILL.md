---
name: cto-guidelines
description: Comprehensive technical leadership guidelines for architecture decisions, team management, technology strategy, and engineering excellence. Use when making architecture decisions, hiring, managing technical debt, setting standards, or any technical leadership task.
---

# CTO Guidelines

Production-tested patterns and best practices for technical leadership.

## When This Skill Activates

This skill should be used when:
- Making architecture and technology decisions
- Setting engineering standards and processes
- Managing technical debt and legacy systems
- Building and scaling engineering teams
- Security and compliance planning
- Budget and vendor management
- Incident response and reliability

## Quick Reference

### Key Responsibilities
- **Strategy:** Technology roadmap, vendor decisions
- **People:** Hiring, culture, career development
- **Execution:** Architecture, standards, processes
- **Operations:** Reliability, security, cost

## Resources

- [Architecture Decision Records](resources/architecture-decisions.md) - ADRs and technical decisions
- [Team Scaling](resources/team-scaling.md) - Hiring, structure, culture
- [Technical Debt Management](resources/technical-debt.md) - Managing legacy and debt
- [Security Standards](resources/security-standards.md) - Security policies and compliance
- [Incident Response](resources/incident-response.md) - Handling outages and incidents
- [Vendor Management](resources/vendor-management.md) - Tool selection and contracts

## Key Principles

### 1. Architecture Decisions
```markdown
# ADR-001: Use Microservices Architecture

## Status
Accepted

## Context
Monolith is becoming difficult to scale and deploy independently.

## Decision
Split into microservices bounded by business domains.

## Consequences
- Faster deployments per service
- Increased operational complexity
- Need for service mesh and observability
```

### 2. Team Structure
- Small autonomous teams (5-8 people)
- Clear ownership and accountability
- Minimize dependencies between teams

### 3. Technical Standards
- Code review required
- CI/CD for all services
- Testing standards (unit, integration, e2e)
- Documentation requirements

### 4. Scaling Guidelines
| Team Size | Structure | Process |
|-----------|-----------|---------|
| 1-10 | Flat | Ad-hoc |
| 10-30 | Squads | Light process |
| 30-100 | Tribes | Formal process |
| 100+ | Chapters | Heavy process |

## Decision Frameworks

### Build vs Buy
```markdown
## Decision: Authentication System

| Factor | Build | Buy |
|--------|-------|-----|
| Time to market | 3 months | 1 week |
| Maintenance | Ongoing | Handled |
| Customization | Full | Limited |
| Cost | $50K/year | $20K/year |
| Risk | Technical debt | Vendor lock-in |

**Decision:** Buy (Auth0) - faster time to market, lower risk
```

### Technology Selection
```markdown
## Tech Selection: Database for User Service

### Requirements
- ACID compliance
- Horizontal scaling
- JSON support
- Team familiarity

### Candidates
| Database | Pros | Cons |
|----------|------|------|
| PostgreSQL | Mature, ACID | Vertical scaling |
| MongoDB | Flexible schema | No ACID |
| CockroachDB | Distributed | Newer, complex |

**Decision:** PostgreSQL with read replicas
```

## Common Processes

### Weekly Rhythm
- Monday: Engineering all-hands
- Tuesday-Thursday: Team focus time
- Friday: Demo and retro

### Monthly Reviews
- Technical debt assessment
- Security audit review
- Vendor performance
- Team health check

### Quarterly Planning
- Architecture review
- Tech roadmap update
- Budget planning
- Hiring plan