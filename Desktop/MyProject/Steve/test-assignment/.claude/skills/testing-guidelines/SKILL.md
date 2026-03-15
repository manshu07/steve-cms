---
name: testing-guidelines
description: Comprehensive testing guidelines including unit testing, integration testing, E2E testing, test automation, TDD, testing frameworks (Jest, Vitest, Playwright), and test best practices. Use when writing tests, setting up testing infrastructure, or implementing test strategies. Covers test organization, mocking, assertions, test coverage, and CI/CD integration.
---

# Testing Guidelines

## Purpose
Complete guide for testing applications including unit, integration, and E2E testing with modern frameworks and best practices.

## When to Use This Skill
- Writing unit tests
- Setting up integration tests
- Implementing E2E tests
- Configuring test runners
- Writing testable code
- Mocking dependencies
- Measuring test coverage
- Setting up TDD workflow

---

## Testing Pyramid

```
        /\
       /  \     E2E Tests (Few)
      /____\    - Critical user flows
     /      \   - Integration points
    /        \  - Full system
   /__________\
  /            \  Integration Tests (More)
 /  Services    \ - API endpoints
 /   Database     \ - Component interaction
/________________\
/                 \ Unit Tests (Most)
/  Functions       \ - Pure functions
/   Classes         \ - Isolated logic
/____________________\ - Fast execution
```

---

## Unit Testing

### Jest/Vitest Setup

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'dist/']
    }
  }
});
```

### Writing Unit Tests

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from './UserService';

describe('UserService', () => {
  let service: UserService;
  let mockDb: any;

  beforeEach(() => {
    mockDb = {
      user: {
        findUnique: vi.fn(),
        create: vi.fn(),
        update: vi.fn()
      }
    };
    service = new UserService(mockDb);
  });

  describe('getUserById', () => {
    it('should return user when found', async () => {
      const mockUser = { id: 1, name: 'John' };
      mockDb.user.findUnique.mockResolvedValue(mockUser);

      const result = await service.getUserById(1);

      expect(result).toEqual(mockUser);
      expect(mockDb.user.findUnique).toHaveBeenCalledWith({
        where: { id: 1 }
      });
    });

    it('should return null when user not found', async () => {
      mockDb.user.findUnique.mockResolvedValue(null);

      const result = await service.getUserById(999);

      expect(result).toBeNull();
    });

    it('should throw on database error', async () => {
      mockDb.user.findUnique.mockRejectedValue(new Error('DB Error'));

      await expect(service.getUserById(1))
        .rejects
        .toThrow('DB Error');
    });
  });
});
```

### Best Practices

1. **Test One Thing** - Each test should verify one behavior
2. **Arrange-Act-Assert** - Clear test structure
3. **Descriptive Names** - Test names should explain what they test
4. **Independence** - Tests shouldn't depend on each other
5. **Fast Execution** - Unit tests should run in milliseconds

---

## Integration Testing

### API Testing

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { app } from './app';
import { TestDatabase } from './test-utils';

describe('User API', () => {
  let db: TestDatabase;
  let server: any;

  beforeAll(async () => {
    db = new TestDatabase();
    await db.migrate();
    server = app.listen(0); // Random port
  });

  afterAll(async () => {
    await server.close();
    await db.close();
  });

  it('POST /api/users should create user', async () => {
    const response = await fetch(`http://localhost:${server.port}/api/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'John', email: 'john@example.com' })
    });

    expect(response.status).toBe(201);
    const data = await response.json();
    expect(data).toHaveProperty('id');
    expect(data.name).toBe('John');
  });

  it('GET /api/users/:id should return user', async () => {
    // First create a user
    const { id } = await db.createUser({ name: 'Jane' });

    const response = await fetch(`http://localhost:${server.port}/api/users/${id}`);
    const data = await response.json();

    expect(data.name).toBe('Jane');
  });
});
```

---

## E2E Testing

### Playwright E2E

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Authentication', () => {
  test('should login user', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'user@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome');
  });

  test('should show validation error', async ({ page }) => {
    await page.goto('/login');
    await page.click('button[type="submit"]');

    const error = page.locator('.error-message');
    await expect(error).toBeVisible();
    await expect(error).toContainText('Email is required');
  });
});
```

---

## Test Coverage

### Coverage Targets

```json
{
  "coverageThreshold": {
    "global": {
      "branches": 80,
      "functions": 80,
      "lines": 80,
      "statements": 80
    }
  }
}
```

### What to Test

**✅ Test:**
- Business logic
- Edge cases
- Error handling
- Validation
- Critical paths

**❌ Don't Test:**
- Third-party libraries
- Framework internals
- Trivial getters/setters
- Constant values

---

## Mocking

### Mocking Dependencies

```typescript
import { vi } from 'vitest';

// Mock external service
vi.mock('./emailService', () => ({
  sendEmail: vi.fn().mockResolvedValue({ success: true })
}));

// Mock environment variables
process.env.JWT_SECRET = 'test-secret';

// Mock time
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
vi.useRealTimers();
```

---

## TDD Workflow

1. **Red** - Write failing test
2. **Green** - Write minimal code to pass
3. **Refactor** - Improve code while tests pass

```bash
# Watch mode for TDD
npm test -- --watch

# Run tests on file change
npm test -- --watch src/
```

---

## Testing Checklist

Before committing code:

- [ ] Unit tests for new functions
- [ ] Integration tests for API endpoints
- [ ] E2E tests for critical flows
- [ ] Tests for edge cases
- [ ] Error scenarios tested
- [ ] Coverage above 80%
- [ ] All tests passing
- [ ] No flaky tests

---

## Quick Reference

### Testing Frameworks

| Framework | Best For |
|-----------|----------|
| Jest | Node.js, React |
| Vitest | Fast TypeScript projects |
| Playwright | E2E browser tests |
| Supertest | HTTP endpoint testing |

### Common Test Commands

```bash
npm test              # Run all tests
npm test -- --watch   # Watch mode
npm test -- --coverage # With coverage
npm test -- ui        # Interactive UI
```

---

## Resources

📚 **Detailed Guides:**
- [testing-patterns.md](resources/testing-patterns.md) - Advanced testing patterns
- [mocking-strategies.md](resources/mocking-strategies.md) - Mocking techniques

---

## Related Skills

- **backend-dev-guidelines** - Testable code design
- **browser-automation** - E2E test automation
- **error-tracking** - Monitor test failures
