# Sentry Configuration & Setup Guide

Complete guide for setting up and configuring Sentry v8 across your project services.

## Table of Contents
- [Installation](#installation)
- [Service Initialization](#service-initialization)
- [Configuration Files](#configuration-files)
- [Environment Variables](#environment-variables)
- [Helper Classes](#helper-classes)
- [Testing Setup](#testing-setup)

---

## Installation

### Core Dependencies

```bash
# Form Service (blog-api)
cd blog-api
npm install @sentry/node @sentry/profiling-node

# Email Service (notifications)
cd notifications
npm install @sentry/node @sentry/profiling-node
```

### Version Requirements

- `@sentry/node`: ^8.0.0
- `@sentry/profiling-node`: ^8.0.0
- Node.js: 18+ or 20+

---

## Service Initialization

### Form Service (blog-api)

**Location**: `./blog-api/src/instrument.ts`

```typescript
import * as Sentry from '@sentry/node';
import { nodeProfilingIntegration } from '@sentry/profiling-node';

// Validate required environment variables
if (!process.env.SENTRY_DSN) {
    console.warn('[Sentry] SENTRY_DSN not set, error tracking disabled');
} else {
    Sentry.init({
        dsn: process.env.SENTRY_DSN,
        environment: process.env.NODE_ENV || 'development',

        // Performance monitoring
        tracesSampleRate: parseFloat(process.env.SENTRY_TRACES_SAMPLE_RATE || '0.1'),
        profilesSampleRate: parseFloat(process.env.SENTRY_PROFILES_SAMPLE_RATE || '0.1'),

        // Integrations
        integrations: [
            nodeProfilingIntegration(),
            // Add HTTP integration for request tracking
            new Sentry.Integrations.Http({ tracing: true }),
            // Add Express integration
            new Sentry.Integrations.Express({
                app: require('express')()
            })
        ],

        // Before send hook for filtering
        beforeSend(event, hint) {
            // Filter out sensitive data
            if (event.request) {
                delete event.request.cookies;
                delete event.request.headers?.authorization;
            }

            // Add custom tags
            event.tags = event.tags || {};
            event.tags.service = 'form';

            return event;
        },

        // Environment-specific settings
        ...(process.env.NODE_ENV === 'production' && {
            tracesSampleRate: 0.1,
            profilesSampleRate: 0.1
        }),

        ...(process.env.NODE_ENV === 'development' && {
            tracesSampleRate: 1.0, // Track everything in dev
            profilesSampleRate: 1.0,
            debug: true
        })
    });

    console.log('[Sentry] Initialized for form service');
}
```

### Email Service (notifications)

**Location**: `./notifications/src/instrument.ts`

```typescript
import * as Sentry from '@sentry/node';
import { nodeProfilingIntegration } from '@sentry/profiling-node';

if (!process.env.SENTRY_DSN) {
    console.warn('[Sentry] SENTRY_DSN not set, error tracking disabled');
} else {
    Sentry.init({
        dsn: process.env.SENTRY_DSN,
        environment: process.env.NODE_ENV || 'development',

        tracesSampleRate: parseFloat(process.env.SENTRY_TRACES_SAMPLE_RATE || '0.1'),
        profilesSampleRate: parseFloat(process.env.SENTRY_PROFILES_SAMPLE_RATE || '0.1'),

        integrations: [
            nodeProfilingIntegration(),
            new Sentry.Integrations.Http({ tracing: true }),
            new Sentry.Integrations.Express({
                app: require('express')()
            })
        ],

        beforeSend(event, hint) {
            if (event.request) {
                delete event.request.cookies;
                delete event.request.headers?.authorization;
            }

            event.tags = event.tags || {};
            event.tags.service = 'email';

            return event;
        },

        ...(process.env.NODE_ENV === 'production' && {
            tracesSampleRate: 0.1,
            profilesSampleRate: 0.1
        }),

        ...(process.env.NODE_ENV === 'development' && {
            tracesSampleRate: 1.0,
            profilesSampleRate: 1.0,
            debug: true
        })
    });

    console.log('[Sentry] Initialized for email service');
}
```

---

## Configuration Files

### Form Service Config

**Location**: `./blog-api/config.ini`

```ini
[sentry]
; Data Source Name (required)
dsn = https://your-sentry-dsn@sentry.io/project-id

; Environment (development, staging, production)
environment = development

; Performance monitoring sample rates
; Higher = more performance data, more cost
tracesSampleRate = 0.1
profilesSampleRate = 0.1

; Release tracking (optional, for deployment tracking)
release = blog-api@1.0.0

[databaseMonitoring]
; Enable database query performance tracking
enableDbTracing = true

; Slow query threshold (milliseconds)
slowQueryThreshold = 100

; Log all database queries (development only)
logDbQueries = false

; Capture database errors to Sentry
dbErrorCapture = true

; Detect and warn about N+1 queries
enableN1Detection = true
```

### Email Service Config

**Location**: `./notifications/config.ini`

```ini
[sentry]
dsn = https://your-sentry-dsn@sentry.io/project-id
environment = development
tracesSampleRate = 0.1
profilesSampleRate = 0.1
release = notifications@1.0.0

[emailMonitoring]
; Track email send failures
trackSendFailures = true

; Track email delivery status
trackDelivery = true

; Sample rate for email tracking (1.0 = all emails)
emailSampleRate = 1.0

; Capture email content (be careful with PII)
captureEmailContent = false
```

---

## Environment Variables

### Required

```bash
# Sentry DSN (get from Sentry dashboard)
SENTRY_DSN=https://dsn@sentry.io/project-id

# Environment
NODE_ENV=production
```

### Optional

```bash
# Performance Monitoring
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_PROFILES_SAMPLE_RATE=0.1

# Release Tracking
SENTRY_RELEASE=blog-api@1.0.0

# Debug Mode (development only)
SENTRY_DEBUG=true
NODE_ENV=development
```

### Docker Compose Example

```yaml
version: '3.8'
services:
  blog-api:
    environment:
      - SENTRY_DSN=${SENTRY_DSN}
      - NODE_ENV=production
      - SENTRY_TRACES_SAMPLE_RATE=0.1
      - SENTRY_PROFILES_SAMPLE_RATE=0.1
      - SENTRY_RELEASE=blog-api@${VERSION}
```

---

## Helper Classes

### BaseController

**Location**: `./blog-api/src/controllers/BaseController.ts`

```typescript
import * as Sentry from '@sentry/node';

export abstract class BaseController {
    protected handleError(
        error: Error,
        method: string,
        context?: Record<string, any>
    ): never {
        Sentry.withScope((scope) => {
            // Add method name
            scope.setTag('controller.method', method);

            // Add service tag
            scope.setTag('service', 'form');

            // Add custom context
            if (context) {
                scope.setContext('controller_context', context);
            }

            // Capture exception
            Sentry.captureException(error);
        });

        // Re-throw for Express error handler
        throw error;
    }

    protected async withErrorHandling<T>(
        method: string,
        fn: () => Promise<T>,
        context?: Record<string, any>
    ): Promise<T> {
        try {
            return await fn();
        } catch (error) {
            this.handleError(error as Error, method, context);
            throw error; // TypeScript requires this
        }
    }
}
```

### WorkflowSentryHelper

**Location**: `./blog-api/src/workflow/utils/sentryHelper.ts`

```typescript
import * as Sentry from '@sentry/node';

export interface WorkflowErrorContext {
    workflowCode: string;
    instanceId: number;
    stepId?: number;
    userId?: string;
    operation: string;
    metadata?: Record<string, any>;
}

export class WorkflowSentryHelper {
    static captureWorkflowError(
        error: Error,
        context: WorkflowErrorContext
    ) {
        Sentry.withScope((scope) => {
            // Workflow tags
            scope.setTag('workflow.code', context.workflowCode);
            scope.setTag('workflow.instance', context.instanceId);
            scope.setTag('service', 'form');

            if (context.stepId) {
                scope.setTag('workflow.step', context.stepId);
            }

            if (context.operation) {
                scope.setTag('workflow.operation', context.operation);
            }

            // User context
            if (context.userId) {
                scope.setUser({ id: context.userId });
            }

            // Detailed error context
            scope.setContext('workflow_error', {
                workflowCode: context.workflowCode,
                instanceId: context.instanceId,
                stepId: context.stepId,
                operation: context.operation,
                metadata: context.metadata
            });

            // Capture with level based on severity
            const level = this.getSeverityLevel(error);
            Sentry.captureException(error, { level });
        });
    }

    static captureStepExecution(context: {
        workflowCode: string;
        instanceId: number;
        stepId: number;
        stepName: string;
        stepType: string;
    }) {
        Sentry.withScope((scope) => {
            scope.setTag('workflow.code', context.workflowCode);
            scope.setTag('workflow.step', context.stepId);
            scope.setTag('step.type', context.stepType);
            scope.setTag('service', 'form');

            scope.setContext('step_execution', context);

            Sentry.captureMessage(`Step executed: ${context.stepName}`, {
                level: 'info'
            });
        });
    }

    static captureStepCompletion(context: {
        workflowCode: string;
        instanceId: number;
        stepId: number;
        result: string;
    }) {
        Sentry.withScope((scope) => {
            scope.setTag('workflow.code', context.workflowCode);
            scope.setTag('workflow.step', context.stepId);
            scope.setTag('service', 'form');

            scope.setContext('step_completion', context);

            Sentry.captureMessage(`Step completed: ${context.result}`, {
                level: 'info'
            });
        });
    }

    private static getSeverityLevel(error: Error): 'fatal' | 'error' | 'warning' | 'info' | 'debug' {
        // Customize based on error types
        if (error.message.includes('database')) return 'fatal';
        if (error.message.includes('timeout')) return 'warning';
        return 'error';
    }
}
```

### DatabasePerformanceMonitor

**Location**: `./blog-api/src/utils/databasePerformance.ts`

```typescript
import * as Sentry from '@sentry/node';

export class DatabasePerformanceMonitor {
    static async withPerformanceTracking<T>(
        operation: string,
        table: string,
        queryFn: () => Promise<T>
    ): Promise<T> {
        const startTime = Date.now();

        try {
            const result = await queryFn();
            const duration = Date.now() - startTime;

            // Log slow queries
            if (duration > 100) {
                Sentry.withScope((scope) => {
                    scope.setTag('db.operation', operation);
                    scope.setTag('db.table', table);
                    scope.setTag('db.slow_query', 'true');
                    scope.setTag('service', 'form');

                    Sentry.captureMessage(
                        `Slow query: ${operation} on ${table} (${duration}ms)`,
                        { level: 'warning' }
                    );
                });
            }

            return result;

        } catch (error) {
            const duration = Date.now() - startTime;

            Sentry.withScope((scope) => {
                scope.setTag('db.operation', operation);
                scope.setTag('db.table', table);
                scope.setTag('service', 'form');

                scope.setContext('database_error', {
                    operation,
                    table,
                    duration,
                    errorType: error.constructor.name
                });

                Sentry.captureException(error);
            });

            throw error;
        }
    }

    static async detectN1Queries<T>(
        operationName: string,
        queryFn: () => Promise<T>
    ): Promise<T> {
        const queryCount = { count: 0 };
        const originalQuery = PrismaService.main;

        // Monkey-patch to count queries (development only)
        if (process.env.NODE_ENV === 'development') {
            // Implementation would track query count
        }

        try {
            const result = await queryFn();

            // Warn if too many queries
            if (queryCount.count > 10) {
                Sentry.captureMessage(
                    `Possible N+1 query detected in ${operationName}: ${queryCount.count} queries`,
                    { level: 'warning' }
                );
            }

            return result;

        } catch (error) {
            Sentry.captureException(error, {
                tags: {
                    'db.operation': operationName,
                    'service': 'form'
                }
            });
            throw error;
        }
    }
}
```

### EmailSentryHelper

**Location**: `./notifications/src/utils/EmailSentryHelper.ts`

```typescript
import * as Sentry from '@sentry/node';

export interface EmailErrorContext {
    emailType: string;
    template: string;
    recipient: string;
    metadata?: Record<string, any>;
}

export class EmailSentryHelper {
    static captureEmailError(
        error: Error,
        context: EmailErrorContext
    ) {
        Sentry.withScope((scope) => {
            scope.setTag('email.type', context.emailType);
            scope.setTag('email.template', context.template);
            scope.setTag('service', 'email');

            scope.setContext('email_error', {
                emailType: context.emailType,
                template: context.template,
                recipient: this.sanitizeEmail(context.recipient),
                metadata: context.metadata
            });

            // Sanitized email context
            scope.setUser({
                email: this.sanitizeEmail(context.recipient)
            });

            Sentry.captureException(error);
        });
    }

    static captureEmailSent(context: {
        emailType: string;
        template: string;
        recipients: string[];
    }) {
        Sentry.withScope((scope) => {
            scope.setTag('email.type', context.emailType);
            scope.setTag('email.status', 'sent');
            scope.setTag('service', 'email');

            scope.setContext('email_sent', {
                emailType: context.emailType,
                template: context.template,
                recipientCount: context.recipients.length
            });

            Sentry.captureMessage('Email sent successfully', {
                level: 'info'
            });
        });
    }

    private static sanitizeEmail(email: string): string {
        // Keep domain, mask user part
        const [local, domain] = email.split('@');
        if (!domain) return '***@***';

        const maskedLocal = local.length > 2
            ? local[0] + '*' * (local.length - 2) + local[local.length - 1]
            : '***';

        return `${maskedLocal}@${domain}`;
    }
}
```

---

## Testing Setup

### Form Service Test Endpoints

**Location**: `./blog-api/src/routes/sentry-test.routes.ts`

```typescript
import express from 'express';
import * as Sentry from '@sentry/node';

const router = express.Router();

// Test basic error capture
router.get('/test-error', (req, res) => {
    try {
        throw new Error('Test error from form service');
    } catch (error) {
        Sentry.captureException(error, {
            tags: { test: 'true' }
        });
        res.json({ status: 'error captured' });
    }
});

// Test workflow error
router.get('/test-workflow-error', (req, res) => {
    const { WorkflowSentryHelper } = require('../workflow/utils/sentryHelper');

    try {
        throw new Error('Test workflow error');
    } catch (error) {
        WorkflowSentryHelper.captureWorkflowError(error, {
            workflowCode: 'TEST_WORKFLOW',
            instanceId: 999,
            stepId: 1,
            userId: 'test-user',
            operation: 'test'
        });
        res.json({ status: 'workflow error captured' });
    }
});

// Test database performance
router.get('/test-database-performance', async (req, res) => {
    const { DatabasePerformanceMonitor } = require('../utils/databasePerformance');

    try {
        const result = await DatabasePerformanceMonitor.withPerformanceTracking(
            'findMany',
            'UserProfile',
            async () => {
                return await PrismaService.main.userProfile.findMany({
                    take: 5
                });
            }
        );
        res.json({ status: 'performance tracked', count: result.length });
    } catch (error) {
        Sentry.captureException(error);
        res.status(500).json({ error: 'Test failed' });
    }
});

// Test error boundary
router.get('/test-error-boundary', async (req, res) => {
    const transaction = Sentry.startTransaction({
        op: 'test',
        name: 'error-boundary-test'
    });

    try {
        await Sentry.startSpan({
            name: 'inner.operation',
            parentSpan: transaction
        }, async () => {
            throw new Error('Inner operation failed');
        });
    } catch (error) {
        Sentry.withScope((scope) => {
            scope.setSpan(transaction);
            Sentry.captureException(error);
        });
    } finally {
        transaction.finish();
    }

    res.json({ status: 'error boundary tested' });
});

export default router;
```

### Email Service Test Endpoints

**Location**: `./notifications/src/routes/sentry-test.routes.ts`

```typescript
import express from 'express';
import * as Sentry from '@sentry/node';
import { EmailSentryHelper } from '../utils/EmailSentryHelper';

const router = express.Router();

router.get('/test-error', (req, res) => {
    try {
        throw new Error('Test error from email service');
    } catch (error) {
        Sentry.captureException(error, {
            tags: { service: 'email', test: 'true' }
        });
        res.json({ status: 'error captured' });
    }
});

router.get('/test-email-error', (req, res) => {
    try {
        throw new Error('Test email send error');
    } catch (error) {
        EmailSentryHelper.captureEmailError(error, {
            emailType: 'welcome',
            template: 'welcome-email',
            recipient: 'test@example.com',
            metadata: { userId: 'test-123' }
        });
        res.json({ status: 'email error captured' });
    }
});

router.get('/test-performance', async (req, res) => {
    const transaction = Sentry.startTransaction({
        op: 'email.send',
        name: 'test-email-performance'
    });

    try {
        await Sentry.startSpan({
            name: 'email.prepare',
            parentSpan: transaction
        }, async () => {
            await new Promise(resolve => setTimeout(resolve, 50));
        });

        await Sentry.startSpan({
            name: 'email.send',
            parentSpan: transaction
        }, async () => {
            await new Promise(resolve => setTimeout(resolve, 100));
        });

        res.json({ status: 'performance tracked' });
    } catch (error) {
        Sentry.captureException(error);
        res.status(500).json({ error: 'Test failed' });
    } finally {
        transaction.finish();
    }
});

export default router;
```

---

## Verification Checklist

After setup, verify:

- [ ] Sentry.init called in instrument.ts
- [ ] SENTRY_DSN environment variable set
- [ ] Tracing enabled (tracesSampleRate > 0)
- [ ] Test endpoints accessible
- [ ] Errors appear in Sentry dashboard
- [ ] Performance data appears in Sentry
- [ ] Service tags properly applied
- [ ] User context captured
- [ ] Sensitive data filtered

---

## Troubleshooting

### No events appearing in Sentry

1. Check SENTRY_DSN is set correctly
2. Check network connectivity to Sentry
3. Enable debug mode: `SENTRY_DEBUG=true`
4. Check Sentry.init is called

### Performance data not appearing

1. Ensure tracesSampleRate > 0
2. Check Express integration is added
3. Verify HTTP integration is enabled
4. Check for transaction.finish() calls

### Context not appearing

1. Verify Sentry.withScope usage
2. Check tags and context syntax
3. Ensure setUser called before capture
4. Verify beforeSend hook not filtering data
