# User Stories Guide

## User Story Format

### Basic Format
```
As a [type of user]
I want [action]
So that [benefit/value]
```

### Examples
```
As a customer
I want to filter products by price
So that I can find items within my budget

As an admin
I want to export user data to CSV
So that I can analyze it in spreadsheets

As a new user
I want a guided onboarding tour
So that I can quickly learn how to use the app
```

## Acceptance Criteria

### Format
```
Given [context/initial state]
When [action]
Then [expected outcome]
```

### Examples
```markdown
#### Story: User Login

**Acceptance Criteria:**
- [ ] Given I'm on the login page, when I enter valid credentials, then I'm redirected to dashboard
- [ ] Given I'm on the login page, when I enter invalid credentials, then I see error message
- [ ] Given I'm logged in, when I close browser and return, then I'm still logged in
```

## Story Writing Best Practices

### INVEST Criteria
- **Independent:** Can be developed separately
- **Negotiable:** Details can be discussed
- **Valuable:** Provides value to users
- **Estimable:** Team can estimate effort
- **Small:** Fits in one sprint
- **Testable:** Has clear acceptance criteria

### Story Sizes
- **Epic:** Large, spans multiple sprints
- **Story:** Fits in one sprint (1-8 points)
- **Task:** Technical sub-items (hours)

## Priority Frameworks

### MoSCoW
- **Must Have:** Critical for release
- **Should Have:** Important but not critical
- **Could Have:** Nice to have
- **Won't Have:** Not this release

### RICE Score
```
RICE = (Reach × Impact × Confidence) / Effort

- Reach: Number of users affected
- Impact: How much value (0.25-3)
- Confidence: How sure are we (0.5-1)
- Effort: Person-months
```

## Story Examples by Domain

### Authentication
```markdown
#### Sign Up
As a new visitor
I want to create an account
So that I can access personalized features

Acceptance Criteria:
- [ ] Email validation works
- [ ] Password strength requirements shown
- [ ] Confirmation email sent
- [ ] Account created successfully
```

### E-commerce
```markdown
#### Add to Cart
As a shopper
I want to add items to my cart
So that I can purchase multiple items at once

Acceptance Criteria:
- [ ] Add to cart button updates cart count
- [ ] Cart persists across sessions
- [ ] Quantity can be adjusted
- [ ] Out of stock items are disabled
```

### Dashboard
```markdown
#### View Metrics
As a manager
I want to see team performance metrics
So that I can make informed decisions

Acceptance Criteria:
- [ ] Metrics load within 3 seconds
- [ ] Data updates every 5 minutes
- [ ] Export to PDF available
- [ ] Date range filter works