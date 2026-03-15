---
name: coding-standards
description: Project coding standards and best practices for TypeScript, React, Express, and general development. Use when writing code, reviewing code, or ensuring consistency across the codebase. Covers ESLint/Prettier configuration, code style conventions, naming conventions, file organization, and quality standards.
---

# Coding Standards

## Purpose
Establish consistent coding standards across the NovaSales AI monorepo for maintainability, readability, and quality.

## When to Use This Skill
- Writing new code or features
- Reviewing pull requests
- Refactoring existing code
- Setting up new files or modules
- Ensuring consistency across teams

---

## Quick Reference

### Code Style Configuration

**Tools:**
- ESLint: `@novasales/eslint-config` (shared package)
- Prettier: `@novasales/prettier-config` (shared package)
- 4 space indentation (not tabs)
- Single quotes for strings
- Semicolons required
- 100 character line width

**Linting:**
```bash
# Run ESLint
npm run lint

# Fix ESLint issues automatically
npm run lint -- --fix

# Type check
npm run typecheck
```

---

## TypeScript Conventions

### Type Definitions

**✅ GOOD: Explicit types for exports/public APIs**
```typescript
// Public API - always explicit
export interface UserProfile {
    id: string;
    name: string;
    email: string;
    preferences: UserPreferences;
}

export async function getUserProfile(id: string): Promise<UserProfile> {
    // ...
}
```

**✅ GOOD: Type inference for internal logic**
```typescript
// Internal - inference is fine
async function processUser(user: User) {
    const validated = validateUser(user); // Type inferred
    const result = await saveToDatabase(validated);
    return result;
}
```

**❌ BAD: Avoid `any`**
```typescript
// Don't use any
function process(data: any) {
    return data.value;
}

// Use unknown or generics
function process<T extends { value: string }>(data: T) {
    return data.value;
}
```

---

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| **Files** | camelCase for code, PascalCase for components | `userService.ts`, `UserProfile.tsx` |
| **Interfaces** | PascalCase, no `I` prefix | `User`, `UserProfile` |
| **Types** | PascalCase | `UserRole`, `ApiResponse` |
| **Enums** | PascalCase | `Status`, `ErrorCode` |
| **Classes** | PascalCase | `UserService`, `ApiController` |
| **Functions/Methods** | camelCase | `getUserById()`, `handleSubmit()` |
| **Constants** | UPPER_SNAKE_CASE | `MAX_RETRIES`, `API_BASE_URL` |
| **Private members** | camelCase with `_` prefix | `_cache`, `_validate()` |

---

## React Conventions

### Component Structure

```typescript
// 1. Imports
import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';

// 2. Types/Interfaces
interface UserProfileProps {
    userId: string;
    onUpdate?: () => void;
}

// 3. Component
export function UserProfile({ userId, onUpdate }: UserProfileProps) {
    // 4. Hooks (order: state → derived → refs → effects)
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // 5. Derived state
    const isAdmin = user?.role === 'admin';

    // 6. Event handlers
    const handleSave = async () => {
        await api.updateUser(userId);
        onUpdate?.();
    };

    // 7. Effects
    useEffect(() => {
        api.getUser(userId).then(setUser);
    }, [userId]);

    // 8. Conditional rendering
    if (isLoading) {
        return <div>Loading...</div>;
    }

    // 9. Return JSX
    return (
        <div>
            <h1>{user?.name}</h1>
            <Button onClick={handleSave}>Save</Button>
        </div>
    );
}
```

### Component Rules

**✅ DO:**
- Use function components with hooks
- Destructure props in signature
- Use TypeScript interfaces for props
- Handle loading and error states
- Use semantic HTML

**❌ DON'T:**
- Use class components (legacy)
- Nest components (define at file level)
- Prop drill (use context or composition)
- Ignore accessibility

---

## Express/Backend Conventions

### Layered Architecture

```
routes/         → Route definitions ONLY
controllers/    → Request handlers
services/       → Business logic
repositories/   → Database access
middleware/     → Express middleware
utils/          → Helper functions
```

### Route Pattern

```typescript
// routes/userRoutes.ts - CLEAN: routes only
import { Router } from 'express';
import { UserController } from '../controllers/UserController';

const router = Router();
const controller = new UserController();

router.get('/', async (req, res) => controller.getUsers(req, res));
router.get('/:id', async (req, res) => controller.getUser(req, res));
router.post('/', async (req, res) => controller.createUser(req, res));

export default router;
```

### Controller Pattern

```typescript
// controllers/UserController.ts
import { BaseController } from './BaseController';
import { z } from 'zod';

export class UserController extends BaseController {
    async createUser(req: any, res: any) {
        try {
            // Validate input
            const schema = z.object({
                name: z.string().min(1),
                email: z.string().email()
            });
            const data = schema.parse(req.body);

            // Delegate to service
            const user = await this.userService.create(data);

            // Return response
            return this.success(res, user, 201);
        } catch (error) {
            this.handleError(error, 'createUser');
        }
    }
}
```

---

## File Organization

### Directory Structure

```
app-or-package/
├── src/
│   ├── components/     # React components
│   │   ├── ui/         # Base UI components
│   │   └── features/   # Feature components
│   ├── pages/          # Page components
│   ├── hooks/          # Custom hooks
│   ├── lib/            # Utilities and clients
│   ├── services/       # API services
│   ├── types/          # Type definitions
│   └── styles/         # Global styles
├── public/             # Static assets
└── tests/              # Test files
```

### Import Order

```typescript
// 1. Node.js built-ins
import { readFile } from 'fs';

// 2. External packages
import express from 'express';
import React from 'react';

// 3. Internal modules (alias imports)
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';

// 4. Relative imports
import { logger } from '../utils/logger';
import { MyComponent } from './MyComponent';

// 5. Type imports (if separate)
import type { User } from '@/types';
```

---

## Code Quality Standards

### ESLint Rules

**Must Pass:**
- No unused variables
- No implicit any (use explicit types)
- No console.log in production (use logger)
- All async errors handled

**Should Pass:**
- Prefer const over let
- Use template literals over string concatenation
- Destructure objects and arrays
- Use meaningful variable names

### TypeScript Strict Mode

**Enabled in tsconfig.json:**
```json
{
    "compilerOptions": {
        "strict": true,
        "noUncheckedIndexedAccess": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true
    }
}
```

---

## Error Handling Standards

### Frontend

```typescript
// ✅ GOOD: Specific error handling
try {
    await api.updateUser(data);
} catch (error) {
    if (error instanceof ApiError) {
        if (error.status === 401) {
            // Handle auth error
        } else if (error.status === 404) {
            // Handle not found
        }
    }
    // Log to Sentry
    Sentry.captureException(error);
    // Show user-friendly message
    showToast('Failed to update user');
}
```

### Backend

```typescript
// ✅ GOOD: Use BaseController
async updateUser(req: any, res: any) {
    try {
        // ... logic
        return this.success(res, user);
    } catch (error) {
        // BaseController sends to Sentry automatically
        this.handleError(error, 'updateUser');
    }
}
```

---

## Comment Standards

### When to Comment

**✅ GOOD COMMENTS:**
- Explain WHY something is done (complex business logic)
- Document public APIs
- Note workarounds for bugs
- Mark TODO/FIXME items

**❌ BAD COMMENTS:**
- Restate obvious code
- Comment out code (delete it instead)
- Outdated comments

### Comment Style

```typescript
// ✅ Single line for brief notes
// Check if user has admin permissions

/**
 * ✅ Multi-line for documentation
 * Creates a new user account with the provided data.
 * Sends a verification email to the user.
 *
 * @param data - User creation data
 * @returns Created user object
 * @throws {ValidationError} If data is invalid
 * @throws {AuthError} If email already exists
 */
async createUser(data: CreateUserDto): Promise<User> {
    // ...
}

// ✅ TODO markers
// TODO: Add rate limiting (ticket #123)
// FIXME: This is a temporary workaround
// HACK: Quick fix for the demo
```

---

## Testing Standards

### Test File Location

```
src/
├── services/
│   └── userService.ts
└── services/
    └── userService.test.ts  # Co-located with source
```

### Test Structure

```typescript
describe('UserService', () => {
    describe('createUser', () => {
        it('should create a new user', async () => {
            // Arrange
            const data = { name: 'John', email: 'john@example.com' };

            // Act
            const result = await userService.create(data);

            // Assert
            expect(result).toHaveProperty('id');
            expect(result.email).toBe(data.email);
        });

        it('should throw validation error for invalid email', async () => {
            // Arrange
            const data = { name: 'John', email: 'invalid' };

            // Act & Assert
            await expect(userService.create(data)).rejects.toThrow(ValidationError);
        });
    });
});
```

---

## Git Commit Standards

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Build process or tooling

**Examples:**
```
feat(auth): add JWT token refresh flow

Implement automatic token refresh using refresh tokens.
Tokens are stored in httpOnly cookies for security.

Closes #123
```

```
fix(api): handle database connection errors

Add proper error handling and retry logic for database
connection failures during startup.
```

---

## Resources

- **ESLint Config:** `packages/eslint-config/`
- **Prettier Config:** `packages/prettier-config/`
- **TypeScript Config:** Root `tsconfig.json`
- **EditorConfig:** `.editorconfig` (if present)

---

## Related Skills

- **backend-dev-guidelines** - Backend patterns and architecture
- **frontend-dev-guidelines** - React patterns and best practices
- **error-tracking** - Sentry integration
- **testing-guidelines** - Test patterns and frameworks
