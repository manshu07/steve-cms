# Sentry Error Tracking - Code Patterns & Examples

Complete code examples for Sentry v8 integration across different scenarios in your project.

## Table of Contents
- [Controller Patterns](#controller-patterns)
- [Route Handler Patterns](#route-handler-patterns)
- [Workflow Error Patterns](#workflow-error-patterns)
- [Cron Job Patterns](#cron-job-patterns)
- [Database Performance Patterns](#database-performance-patterns)
- [Async Operation Patterns](#async-operation-patterns)
- [Service-Specific Patterns](#service-specific-patterns)

---

## Controller Patterns

### Using BaseController (Recommended)

```typescript
import { BaseController } from '../controllers/BaseController';
import { PrismaService } from '../services/PrismaService';

export class UserProfileController extends BaseController {
    private prisma: PrismaService;

    constructor() {
        super();
        this.prisma = PrismaService.getInstance();
    }

    async getProfile(req: Request, res: Response) {
        try {
            const userId = req.params.id;

            // Automatic performance tracking
            const profile = await this.prisma.main.userProfile.findUnique({
                where: { id: userId }
            });

            return res.json(profile);
        } catch (error) {
            // Automatically sends to Sentry with context
            this.handleError(error, 'getProfile', {
                userId: req.params.id,
                endpoint: 'GET /user/:id'
            });
        }
    }

    async updateProfile(req: Request, res: Response) {
        try {
            const userId = req.params.id;
            const updates = req.body;

            const profile = await this.prisma.main.userProfile.update({
                where: { id: userId },
                data: updates
            });

            return res.json(profile);
        } catch (error) {
            this.handleError(error, 'updateProfile', {
                userId,
                updates: JSON.stringify(updates)
            });
        }
    }
}
```

### Custom Controller with Enhanced Error Context

```typescript
import * as Sentry from '@sentry/node';
import { BaseController } from '../controllers/BaseController';

export class FormSubmissionController extends BaseController {
    async submitForm(req: Request, res: Response) {
        try {
            const { formId, formData } = req.body;

            // Validate
            if (!formId || !formData) {
                throw new Error('Missing required fields');
            }

            // Process submission
            const result = await this.processSubmission(formId, formData);

            return res.json(result);
        } catch (error) {
            // Enhanced error context
            Sentry.withScope((scope) => {
                scope.setUser({ id: req.user?.id });
                scope.setTag('form.id', req.body.formId);
                scope.setTag('form.type', 'submission');
                scope.setContext('submission', {
                    formDataKeys: Object.keys(req.body.formData || {}),
                    formId: req.body.formId,
                    timestamp: new Date().toISOString()
                });

                Sentry.captureException(error);
            });

            return res.status(500).json({
                error: 'Form submission failed',
                submissionId: this.generateSubmissionId()
            });
        }
    }
}
```

---

## Route Handler Patterns

### Basic Route Error Handling

```typescript
import express from 'express';
import * as Sentry from '@sentry/node';

const router = express.Router();

router.get('/api/users/:id', async (req, res) => {
    try {
        const userId = req.params.id;
        const user = await fetchUser(userId);

        res.json(user);
    } catch (error) {
        // Capture with route context
        Sentry.captureException(error, {
            tags: {
                route: '/api/users/:id',
                method: 'GET',
                endpoint: 'getUser'
            },
            user: { id: req.params.id },
            extra: {
                userId: req.params.id,
                query: JSON.stringify(req.query)
            }
        });

        res.status(500).json({ error: 'Failed to fetch user' });
    }
});
```

### Advanced Route with Performance Tracking

```typescript
import * as Sentry from '@sentry/node';

router.post('/api/forms/submit', async (req, res) => {
    // Start transaction for performance tracking
    const transaction = Sentry.startTransaction({
        op: 'http.server',
        name: 'POST /api/forms/submit'
    });

    try {
        // Form validation span
        await Sentry.startSpan({
            name: 'form.validation',
            op: 'validation',
            parentSpan: transaction
        }, async () => {
            validateFormData(req.body);
        });

        // Database save span
        const result = await Sentry.startSpan({
            name: 'database.save',
            op: 'db.query',
            parentSpan: transaction
        }, async () => {
            return await saveFormSubmission(req.body);
        });

        // Notification send span
        await Sentry.startSpan({
            name: 'notification.send',
            op: 'notification',
            parentSpan: transaction
        }, async () => {
            await sendNotification(result);
        });

        res.json(result);
    } catch (error) {
        Sentry.withScope((scope) => {
            scope.setSpan(transaction);
            scope.setTag('form.type', req.body.formType);
            scope.setContext('form_data', {
                formId: req.body.formId,
                fieldCount: Object.keys(req.body.data || {}).length
            });

            Sentry.captureException(error);
        });

        res.status(500).json({ error: 'Submission failed' });
    } finally {
        transaction.finish();
    }
});
```

---

## Workflow Error Patterns

### WorkflowSentryHelper Usage

```typescript
import { WorkflowSentryHelper } from '../workflow/utils/sentryHelper';

export class WorkflowProcessor {
    async processWorkflow(workflowCode: string, instanceId: number) {
        try {
            // Load workflow
            const workflow = await this.loadWorkflow(workflowCode);

            // Process steps
            for (const step of workflow.steps) {
                await this.processStep(step, instanceId);
            }

        } catch (error) {
            // Capture workflow error with full context
            WorkflowSentryHelper.captureWorkflowError(error, {
                workflowCode,
                instanceId,
                stepId: error.stepId || null,
                userId: error.userId || 'system',
                operation: error.operation || 'processWorkflow',
                metadata: {
                    stepCount: workflow.steps.length,
                    currentStep: error.stepIndex,
                    workflowState: error.state
                }
            });

            throw error; // Re-throw for upstream handling
        }
    }
}
```

### Step-Specific Error Handling

```typescript
export class WorkflowStepProcessor {
    async executeStep(
        workflowCode: string,
        instanceId: number,
        stepId: number
    ) {
        try {
            const step = await this.loadStep(stepId);

            // Track step execution
            await WorkflowSentryHelper.captureStepExecution({
                workflowCode,
                instanceId,
                stepId,
                stepName: step.name,
                stepType: step.type
            });

            // Execute step logic
            const result = await this.executeStepLogic(step);

            // Track completion
            await WorkflowSentryHelper.captureStepCompletion({
                workflowCode,
                instanceId,
                stepId,
                result: result.status
            });

            return result;

        } catch (error) {
            WorkflowSentryHelper.captureWorkflowError(error, {
                workflowCode,
                instanceId,
                stepId,
                operation: 'executeStep',
                metadata: {
                    stepName: step.name,
                    stepType: step.type,
                    errorPhase: 'execution'
                }
            });

            throw error;
        }
    }
}
```

---

## Cron Job Patterns

### Basic Cron Job with Sentry

```typescript
#!/usr/bin/env node

// CRITICAL: Must be first import
import '../instrument';
import * as Sentry from '@sentry/node';

interface CronJobResult {
    success: boolean;
    recordsProcessed: number;
    errors: string[];
}

async function main(): Promise<CronJobResult> {
    return await Sentry.startSpan({
        name: 'cron.process-queue',
        op: 'cron',
        attributes: {
            'cron.job': 'process-queue',
            'cron.startTime': new Date().toISOString(),
        }
    }, async () => {
        try {
            console.log('[Cron] Starting queue processing');

            const result = await processQueue();

            console.log('[Cron] Completed:', result);

            return result;

        } catch (error) {
            // Capture cron job error
            Sentry.captureException(error, {
                tags: {
                    'cron.job': 'process-queue',
                    'error.type': 'execution_error'
                },
                level: 'error'
            });

            console.error('[Cron] Error:', error);
            throw error;

        } finally {
            // Flush Sentry events before exit
            await Sentry.flush(2000);
        }
    });
}

main()
    .then((result) => {
        console.log('[Cron] Success:', result);
        process.exit(0);
    })
    .catch((error) => {
        console.error('[Cron] Fatal error:', error);
        process.exit(1);
    });
```

### Advanced Cron with Detailed Monitoring

```typescript
#!/usr/bin/env node

import '../instrument';
import * as Sentry from '@sentry/node';

interface JobMetrics {
    total: number;
    successful: number;
    failed: number;
    skipped: number;
}

async function processDailyReports() {
    const jobName = 'daily-reports';
    const startTime = Date.now();

    return await Sentry.startSpan({
        name: `cron.${jobName}`,
        op: 'cron',
        attributes: {
            'cron.job': jobName,
            'cron.startTime': new Date().toISOString(),
        }
    }, async (span) => {
        const metrics: JobMetrics = {
            total: 0,
            successful: 0,
            failed: 0,
            skipped: 0
        };

        try {
            // Fetch pending reports
            const reports = await fetchPendingReports();
            metrics.total = reports.length;

            console.log(`[Cron] Processing ${reports.length} reports`);

            // Process each report
            for (const report of reports) {
                try {
                    // Individual report span
                    await Sentry.startSpan({
                        name: `report.process.${report.id}`,
                        op: 'report.process',
                        parentSpan: span
                    }, async () => {
                        await generateReport(report);
                        metrics.successful++;
                    });

                } catch (error) {
                    metrics.failed++;

                    // Individual report error
                    Sentry.withScope((scope) => {
                        scope.setTag('report.id', report.id);
                        scope.setTag('report.type', report.type);
                        scope.setContext('report', {
                            id: report.id,
                            type: report.type,
                            recipient: report.recipient
                        });

                        Sentry.captureException(error, {
                            level: 'warning'
                        });
                    });
                }
            }

            // Record metrics
            span?.setAttribute('cron.total', metrics.total);
            span?.setAttribute('cron.successful', metrics.successful);
            span?.setAttribute('cron.failed', metrics.failed);

            const duration = Date.now() - startTime;
            console.log(`[Cron] Completed in ${duration}ms`, metrics);

            return metrics;

        } catch (error) {
            Sentry.captureException(error, {
                tags: {
                    'cron.job': jobName,
                    'error.type': 'job_failure'
                },
                extra: {
                    metrics: JSON.stringify(metrics),
                    duration: Date.now() - startTime
                }
            });

            throw error;

        } finally {
            await Sentry.flush(2000);
        }
    });
}

processDailyReports()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error('[Cron] Fatal:', error);
        process.exit(1);
    });
```

---

## Database Performance Patterns

### Using DatabasePerformanceMonitor

```typescript
import { DatabasePerformanceMonitor } from '../utils/databasePerformance';

export class UserRepository {
    async findActiveUsers(limit: number = 10) {
        // Wrap query with performance tracking
        return await DatabasePerformanceMonitor.withPerformanceTracking(
            'findMany',
            'UserProfile',
            async () => {
                return await PrismaService.main.userProfile.findMany({
                    where: { status: 'active' },
                    take: limit,
                    include: {
                        preferences: true,
                        notifications: true
                    }
                });
            }
        );
    }

    async findUserWithPosts(userId: string) {
        // Track N+1 queries
        return await DatabasePerformanceMonitor.detectN1Queries(
            'findUserWithPosts',
            async () => {
                const user = await PrismaService.main.userProfile.findUnique({
                    where: { id: userId }
                });

                if (!user) return null;

                // This would trigger N+1 warning
                const posts = await PrismaService.main.post.findMany({
                    where: { authorId: userId }
                });

                return { ...user, posts };
            }
        );
    }
}
```

### Custom Database Monitoring

```typescript
import * as Sentry from '@sentry/node';

export class CustomDbMonitor {
    static async trackQuery<T>(
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

                    Sentry.captureMessage(
                        `Slow query detected: ${operation} on ${table} took ${duration}ms`,
                        {
                            level: 'warning',
                            extra: {
                                operation,
                                table,
                                duration
                            }
                        }
                    );
                });
            }

            return result;

        } catch (error) {
            const duration = Date.now() - startTime;

            Sentry.withScope((scope) => {
                scope.setTag('db.operation', operation);
                scope.setTag('db.table', table);
                scope.setTag('db.error', 'true');

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
}
```

---

## Async Operation Patterns

### Parallel Async Operations with Spans

```typescript
import * as Sentry from '@sentry/node';

export class DataSyncService {
    async syncUserData(userId: string) {
        const transaction = Sentry.startTransaction({
            op: 'data.sync',
            name: 'syncUserData'
        });

        try {
            // Parallel operations
            const [profile, settings, activity] = await Promise.all([
                Sentry.startSpan({
                    name: 'sync.profile',
                    op: 'sync.operation',
                    parentSpan: transaction
                }, () => this.syncProfile(userId)),

                Sentry.startSpan({
                    name: 'sync.settings',
                    op: 'sync.operation',
                    parentSpan: transaction
                }, () => this.syncSettings(userId)),

                Sentry.startSpan({
                    name: 'sync.activity',
                    op: 'sync.operation',
                    parentSpan: transaction
                }, () => this.syncActivity(userId))
            ]);

            return { profile, settings, activity };

        } catch (error) {
            Sentry.withScope((scope) => {
                scope.setSpan(transaction);
                scope.setUser({ id: userId });
                Sentry.captureException(error);
            });

            throw error;

        } finally {
            transaction.finish();
        }
    }
}
```

### Sequential Async Operations

```typescript
export class WorkflowExecutor {
    async executeWorkflow(steps: WorkflowStep[]) {
        return await Sentry.startSpan({
            name: 'workflow.execute',
            op: 'workflow'
        }, async (parentSpan) => {
            const results = [];

            for (const step of steps) {
                try {
                    const result = await Sentry.startSpan({
                        name: `step.${step.name}`,
                        op: 'workflow.step',
                        parentSpan,
                        attributes: {
                            'step.type': step.type,
                            'step.index': step.index
                        }
                    }, async () => {
                        return await this.executeStep(step);
                    });

                    results.push(result);

                } catch (error) {
                    // Step error - capture but continue?
                    Sentry.withScope((scope) => {
                        scope.setTag('step.name', step.name);
                        scope.setTag('step.index', step.index);

                        Sentry.captureException(error, {
                            level: 'error'
                        });
                    });

                    // Decide whether to continue or fail
                    if (step.critical) {
                        throw error;
                    }
                }
            }

            return results;
        });
    }
}
```

---

## Service-Specific Patterns

### Form Service Patterns

```typescript
// blog-api/src/workflow/utils/sentryHelper.ts
export class WorkflowSentryHelper {
    static captureWorkflowError(
        error: Error,
        context: WorkflowErrorContext
    ) {
        Sentry.withScope((scope) => {
            scope.setTag('workflow.code', context.workflowCode);
            scope.setTag('workflow.instance', context.instanceId);
            scope.setTag('service', 'form');

            if (context.stepId) {
                scope.setTag('workflow.step', context.stepId);
            }

            scope.setContext('workflow_error', {
                workflowCode: context.workflowCode,
                instanceId: context.instanceId,
                stepId: context.stepId,
                operation: context.operation,
                metadata: context.metadata
            });

            if (context.userId) {
                scope.setUser({ id: context.userId });
            }

            Sentry.captureException(error);
        });
    }
}
```

### Email Service Patterns

```typescript
// notifications/src/utils/EmailSentryHelper.ts
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
                recipient: context.recipient,
                metadata: context.metadata
            });

            // Sanitize email before sending
            const sanitizedEmail = this.sanitizeEmail(context.recipient);
            scope.setUser({ email: sanitizedEmail });

            Sentry.captureException(error);
        });
    }

    static captureEmailSent(context: EmailSentContext) {
        Sentry.withScope((scope) => {
            scope.setTag('email.type', context.emailType);
            scope.setTag('email.status', 'sent');

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
}
```

---

## Error Boundary Patterns

### React Error Boundary with Sentry

```typescript
import * as Sentry from '@sentry/react';

class ErrorBoundary extends React.Component {
    componentDidCatch(error, errorInfo) {
        Sentry.withScope((scope) => {
            scope.setContext('react', {
                componentStack: errorInfo.componentStack
            });

            Sentry.captureException(error);
        });
    }

    render() {
        if (this.state.hasError) {
            return <ErrorFallback />;
        }

        return this.props.children;
    }
}
```

### Express Error Handler

```typescript
import * as Sentry from '@sentry/node';

app.use(Sentry.Handlers.errorHandler());

app.use((err, req, res, next) => {
    // Additional custom error handling
    Sentry.withScope((scope) => {
        scope.setUser({ id: req.user?.id });
        scope.setTag('route', req.path);
        scope.setContext('request', {
            method: req.method,
            path: req.path,
            query: req.query
        });

        Sentry.captureException(err);
    });

    res.status(500).json({ error: 'Internal server error' });
});
```

---

## Summary

**Key Patterns:**
1. **Controllers**: Use BaseController for automatic error capture
2. **Routes**: Manual Sentry.captureException with rich context
3. **Workflows**: WorkflowSentryHelper for domain-specific errors
4. **Cron Jobs**: Always import instrument.ts first
5. **Database**: DatabasePerformanceMonitor for query tracking
6. **Async**: Sentry.startSpan for performance tracking

**Required Context:**
- User ID (always if available)
- Service name (form, email, users, etc.)
- Operation type (workflow.step, database.query, etc.)
- Request/operation-specific metadata

**Never Forget:**
- Import instrument.ts as FIRST line in cron jobs
- Use meaningful tags and context
- Sanitize sensitive data before sending
- Always re-throw after capturing (unless you can recover)
