---
name: error-tracking
description: Add Sentry v8 error tracking and performance monitoring to your project services. Use this skill when adding error handling, creating new controllers, instrumenting cron jobs, or tracking database performance. ALL ERRORS MUST BE CAPTURED TO SENTRY - no exceptions.
---

# Sentry Integration Skill

## Purpose
Enforce comprehensive Sentry v8 error tracking and performance monitoring across all project services.

## When to Use This Skill
- Adding error handling to any code
- Creating new controllers or routes
- Instrumenting cron jobs
- Tracking database performance
- Adding performance spans
- Handling workflow errors

## 🚨 CRITICAL RULE

**ALL ERRORS MUST BE CAPTURED TO SENTRY** - No exceptions. Never use console.error alone.

---

## Quick Start

### 1. Controller Error Handling

```typescript
// ✅ CORRECT - Use BaseController
import { BaseController } from '../controllers/BaseController';

export class MyController extends BaseController {
    async myMethod() {
        try {
            // ... your code
        } catch (error) {
            this.handleError(error, 'myMethod'); // Automatically sends to Sentry
        }
    }
}
```

### 2. Route Error Handling

```typescript
import * as Sentry from '@sentry/node';

router.get('/route', async (req, res) => {
    try {
        // ... your code
    } catch (error) {
        Sentry.captureException(error, {
            tags: { route: '/route', method: 'GET' },
            extra: { userId: req.user?.id }
        });
        res.status(500).json({ error: 'Internal server error' });
    }
});
```

### 3. Workflow Error Handling

```typescript
import { WorkflowSentryHelper } from '../workflow/utils/sentryHelper';

WorkflowSentryHelper.captureWorkflowError(error, {
    workflowCode: 'DHS_CLOSEOUT',
    instanceId: 123,
    stepId: 456,
    userId: 'user-123',
    operation: 'stepCompletion'
});
```

### 4. Cron Jobs (MANDATORY Pattern)

```typescript
#!/usr/bin/env node
// FIRST LINE after shebang - CRITICAL!
import '../instrument';
import * as Sentry from '@sentry/node';

async function main() {
    return await Sentry.startSpan({
        name: 'cron.job-name',
        op: 'cron'
    }, async () => {
        // Your cron job logic
    });
}
```

### 5. Database Performance

```typescript
import { DatabasePerformanceMonitor } from '../utils/databasePerformance';

const result = await DatabasePerformanceMonitor.withPerformanceTracking(
    'findMany',
    'UserProfile',
    async () => {
        return await PrismaService.main.userProfile.findMany();
    }
);
```

---

## Error Levels

- **fatal**: System unusable (database down, critical service failure)
- **error**: Operation failed, needs immediate attention
- **warning**: Recoverable issues, degraded performance
- **info**: Informational messages
- **debug**: Detailed debugging (dev only)

---

## Required Context

```typescript
import * as Sentry from '@sentry/node';

Sentry.withScope((scope) => {
    // ALWAYS include these if available
    scope.setUser({ id: userId });
    scope.setTag('service', 'form'); // or 'email', 'users'
    scope.setTag('environment', process.env.NODE_ENV);

    // Add operation-specific context
    scope.setContext('operation', {
        type: 'workflow.start',
        workflowCode: 'DHS_CLOSEOUT',
        entityId: 123
    });

    Sentry.captureException(error);
});
```

---

## Service Status

### Form Service ✅ Complete
- Sentry v8 fully integrated
- All workflow errors tracked
- SystemActionQueueProcessor instrumented

### Email Service 🟡 In Progress
- Phase 1-2 complete (6/22 tasks)
- 189 ErrorLogger.log() calls remaining

---

## Testing Endpoints

### Form Service
```bash
curl http://localhost:3002/blog-api/api/sentry/test-error
curl http://localhost:3002/blog-api/api/sentry/test-workflow-error
curl http://localhost:3002/blog-api/api/sentry/test-database-performance
```

### Email Service
```bash
curl http://localhost:3003/notifications/api/sentry/test-error
curl http://localhost:3003/notifications/api/sentry/test-email-error
curl http://localhost:3003/notifications/api/sentry/test-performance
```

---

## Key Files

### Form Service
- `blog-api/src/instrument.ts` - Sentry initialization
- `blog-api/src/workflow/utils/sentryHelper.ts` - Workflow errors
- `blog-api/src/utils/databasePerformance.ts` - DB monitoring
- `blog-api/src/controllers/BaseController.ts` - Controller base

### Email Service
- `notifications/src/instrument.ts` - Sentry initialization
- `notifications/src/utils/EmailSentryHelper.ts` - Email errors
- `notifications/src/controllers/BaseController.ts` - Controller base

---

## Common Mistakes to Avoid

❌ NEVER use console.error without Sentry
❌ NEVER swallow errors silently
❌ NEVER expose sensitive data in error context
❌ NEVER use generic error messages without context
❌ NEVER skip error handling in async operations
❌ NEVER forget to import instrument.ts as first line in cron jobs

---

## Implementation Checklist

When adding Sentry to new code:

- [ ] Imported Sentry or appropriate helper
- [ ] All try/catch blocks capture to Sentry
- [ ] Added meaningful context to errors
- [ ] Used appropriate error level
- [ ] No sensitive data in error messages
- [ ] Added performance tracking for slow operations
- [ ] Tested error handling paths
- [ ] For cron jobs: instrument.ts imported first

---

## Resources

📚 **Detailed Guides:**
- [code-patterns.md](resources/code-patterns.md) - Complete code examples for all scenarios
- [configuration.md](resources/configuration.md) - Setup, installation, and configuration guides

---

## Documentation

- Full implementation: `/dev/active/email-sentry-integration/`
- Form service docs: `/blog-api/docs/sentry-integration.md`
- Email service docs: `/notifications/docs/sentry-integration.md`

---

## Related Skills

- **database-verification** - Before database operations
- **workflow-builder** - For workflow error context
- **backend-dev-guidelines** - For controller patterns
