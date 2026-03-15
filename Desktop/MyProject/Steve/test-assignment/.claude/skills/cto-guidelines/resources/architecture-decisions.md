# Architecture Decision Records

## ADR Template

```markdown
# ADR-[NUMBER]: [Title]

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
What is the issue we're addressing? Why does this decision matter?

## Decision
What is the change we're proposing/have made?

## Consequences
What are the positive and negative outcomes?

## Alternatives Considered
What other options were evaluated?
```

## Example ADR

```markdown
# ADR-003: Adopt PostgreSQL as Primary Database

## Status
Accepted

## Context
Our application requires a relational database with:
- Strong consistency guarantees
- JSON support for flexible schemas
- Proven scalability
- Active community

Current MongoDB setup causing issues with complex queries and transactions.

## Decision
Migrate to PostgreSQL as the primary database.

## Consequences

### Positive
- ACID compliance for financial transactions
- Better JOIN performance
- JSONB for flexible fields
- Mature tooling and ecosystem

### Negative
- Schema migrations more complex
- Need to rewrite data access layer
- Learning curve for team

## Alternatives Considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| MongoDB | Flexible, current | No transactions | Rejected |
| MySQL | Popular, stable | Weaker JSON | Rejected |
| CockroachDB | Distributed | Immature, costly | Future option |
```

## ADR Process

1. **Draft:** Author writes ADR
2. **Review:** Tech leads review
3. **Discussion:** Team meeting if needed
4. **Accept/Reject:** Decision recorded
5. **Implement:** Execute decision

## ADR Index

```markdown
| ADR | Title | Status | Date |
|-----|-------|--------|------|
| 001 | Microservices architecture | Accepted | 2024-01 |
| 002 | API gateway with Kong | Accepted | 2024-02 |
| 003 | PostgreSQL for primary DB | Accepted | 2024-03 |
| 004 | React for frontend | Superseded | 2024-01 |