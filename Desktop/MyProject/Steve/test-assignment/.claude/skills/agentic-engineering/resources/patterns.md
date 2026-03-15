# Agentic Engineering Patterns

## Eval-First Execution Template

### Step 1: Define Success Criteria

```markdown
## Task: Implement User Authentication

Success Criteria:
- User can register with email/password
- User can login with credentials
- Session persists across requests
- Failed login shows appropriate error

Evaluation Metrics:
- Functional: All success criteria met
- Security: Passwords hashed, no plaintext storage
- Performance: Login < 500ms
- Maintainability: Code follows project conventions
```

### Step 2: Decompose Task

```markdown
## Subtasks:

1. Setup database schema (users table)
2. Create password hashing utility
3. Implement registration endpoint
4. Implement login endpoint
5. Create session middleware
6. Add error handling
7. Write tests
8. Document API
```

### Step 3: Execute with Model Routing

```typescript
const taskDecomposition = {
  complex: "Use Opus (expensive) for initial breakdown",
  routine: "Use Haiku (cheap) for standard implementations",
  debugging: "Use Sonnet (balanced) for error diagnosis"
};

const executeTask = async (subtask: string) => {
  const model = selectModel(subtask.complexity);
  return await model.execute(subtask);
};
```

## Cost-Aware Routing

### Task Complexity Matrix

| Complexity | Model | Cost | When to Use |
|------------|-------|------|------------|
| Simple | Haiku | $0.25/M tokens | Boilerplate, CRUD |
| Medium | Sonnet | $3/M tokens | Business logic, algorithms |
| Complex | Opus | $15/M tokens | Architecture, debugging |

### Routing Logic

```typescript
function selectModel(task: Task): Model {
  // Simple tasks (CRUD, boilerplate)
  if (task.type === 'crud' || task.boilerplate) {
    return 'haiku';
  }

  // Complex tasks (architecture, debugging)
  if (task.requiresReasoning || task.isDebugging) {
    return 'opus';
  }

  // Default to balanced
  return 'sonnet';
}
```

## Decomposition Patterns

### Pattern 1: Hierarchical Decomposition

```
Root Task: Build E-commerce Site
├── Frontend (Sonnet)
│   ├── Product Catalog (Haiku)
│   ├── Shopping Cart (Haiku)
│   └── Checkout Flow (Sonnet)
├── Backend (Sonnet)
│   ├── User Management (Haiku)
│   ├── Order Processing (Sonnet)
│   └── Payment Integration (Opus)
└── Database (Sonnet)
    ├── Schema Design (Sonnet)
    └── Migration Scripts (Haiku)
```

### Pattern 2: Dependency-Based Decomposition

```
Task: Implement Real-time Chat

Dependencies:
1. Database schema (foundation) - Haiku
2. WebSocket server (core) - Sonnet
3. Message queue (reliability) - Sonnet
4. Client UI (interface) - Haiku
5. Testing (validation) - Sonnet

Route: Linear execution following dependency graph
```

### Pattern 3: Risk-Based Decomposition

```
Task: Add Payment Processing

High Risk (use Opus with review):
- Payment gateway integration
- Security compliance (PCI DSS)
- Error handling for payments

Low Risk (use Haiku):
- UI for payment form
- Email receipt sending
- Order status updates
```

## Execution Templates

### Template 1: Simple CRUD (Haiku)

```typescript
// Use Haiku for standard CRUD operations
const createUser = {
  model: 'haiku',
  prompt: `
Create a user registration endpoint:
- Email validation (Zod schema)
- Password hashing (bcrypt)
- Store in PostgreSQL
- Return user object without password
  `,
  estimatedCost: '$0.05'
};
```

### Template 2: Business Logic (Sonnet)

```typescript
// Use Sonnet for domain logic
const calculateOrderTotal = {
  model: 'sonnet',
  prompt: `
Implement order total calculation:
- Sum line items
- Apply discounts based on user tier
- Add shipping (varies by location)
- Calculate tax (varies by state)
- Return total with breakdown
  `,
  estimatedCost: '$0.30'
};
```

### Template 3: Complex Architecture (Opus)

```typescript
// Use Opus for architectural decisions
const designAuthSystem = {
  model: 'opus',
  prompt: `
Design authentication architecture for:
- Multi-tenant SaaS application
- OAuth integration (Google, GitHub)
- Role-based access control
- Session management
- Rate limiting

Provide:
- System architecture diagram
- Database schema
- Security considerations
- Implementation roadmap
  `,
  estimatedCost: '$3.00'
};
```

## Cost Optimization

### Budget Tracking

```typescript
interface Budget {
  total: number;
  spent: number;
  remaining: number;
  alert_threshold: number;
}

const trackCost = (task: Task, budget: Budget) => {
  if (budget.spent > budget.alert_threshold) {
    console.warn(`Budget alert: ${budget.spent}/${budget.total}`);
  }

  if (budget.spent > budget.total) {
    throw new Error('Budget exceeded');
  }
};
```

### Prompt Caching

```typescript
// Cache frequently used prompts
const promptCache = new Map();

const getCachedPrompt = (key: string) => {
  if (promptCache.has(key)) {
    return promptCache.get(key);
  }

  const prompt = generatePrompt(key);
  promptCache.set(key, prompt);
  return prompt;
};
```

### Retry Logic

```typescript
async function executeWithRetry(
  task: Task,
  maxRetries = 3
): Promise<Result> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await executeTask(task);
    } catch (error) {
      if (attempt === maxRetries) {
        // Last attempt failed, use Opus to diagnose
        return await diagnoseWithOpus(task, error);
      }
      // Retry with Sonnet (balanced)
      await new Promise(r => setTimeout(r, 1000 * attempt));
    }
  }
}
```

## Multi-Agent Coordination

### Pattern: Specialist Agents

```typescript
const agents = {
  planner: {
    model: 'opus',
    role: 'Break down complex task',
    output: 'Subtask list with dependencies'
  },
  frontend: {
    model: 'sonnet',
    role: 'Implement UI components',
    output: 'React components with TypeScript'
  },
  backend: {
    model: 'sonnet',
    role: 'Implement API endpoints',
    output: 'Express routes with validation'
  },
  integrator: {
    model: 'opus',
    role: 'Review and integrate all components',
    output: 'Functional system with tests'
  }
};
```

### Workflow: Orchestration

```markdown
1. Planner Agent (Opus)
   - Analyzes requirements
   - Creates task breakdown
   - Identifies dependencies

2. Specialist Agents (Sonnet/Haiku)
   - Execute assigned subtasks
   - Report progress and issues

3. Integrator Agent (Opus)
   - Reviews all outputs
   - Identifies integration issues
   - Provides final integration

Cost Optimization:
- Only use Opus for planning/integration (expensive but critical)
- Use Sonnet for most implementation (balanced)
- Use Haiku for simple tasks (cheap)
```

## Quality Gates

### Gate 1: Planning

```markdown
✅ Task decomposed into subtasks
✅ Dependencies identified
✅ Models selected for each subtask
✅ Budget estimated
```

### Gate 2: Execution

```markdown
✅ Each subtask completed
✅ Output matches specification
✅ Errors documented and resolved
✅ Cost within budget
```

### Gate 3: Integration

```markdown
✅ All components integrated
✅ End-to-end tests passing
✅ Performance acceptable
✅ Documentation complete
```

## Evaluation Checklist

### Before Execution

- [ ] Success criteria defined
- [ ] Task decomposed appropriately
- [ ] Models selected based on complexity
- [ ] Budget allocated
- [ ] Quality gates established

### During Execution

- [ ] Tracking actual cost vs estimated
- [ ] Monitoring subtask completion
- [ ] Logging errors and retries
- [ ] Validating outputs at each step

### After Execution

- [ ] All success criteria met
- [ ] Final cost within budget
- [ ] Quality gates passed
- [ ] Document lessons learned

---

This resources file provides comprehensive patterns for eval-first execution, cost-aware model routing, and multi-agent coordination.
