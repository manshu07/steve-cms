# Agent Harness Construction Templates

## Tool Definition Templates

### Template 1: Micro-Tool (High-Risk Operations)

```typescript
/**
 * DEPLOY-PROD
 * High-risk deployment tool with granular controls
 */
{
  name: "deploy_prod",
  description: "Deploy application to production environment",
  input_schema: {
    type: "object",
    properties: {
      service: {
        type: "string",
        enum: ["api", "worker", "web"],
        description: "Service to deploy"
      },
      version: {
        type: "string",
        pattern: "^v\\d+\\.\\d+\\.\\d+$",
        description: "Version tag (e.g., v1.2.3)"
      },
      confirm: {
        type: "boolean",
        description: "Must be true to execute"
      }
    },
    required: ["service", "version", "confirm"]
  },
  output_schema: {
    status: "success|warning|error",
    summary: "string",
    next_actions: ["string"],
    artifacts: {
      deployment_id: "string",
      rollback_version: "string"
    }
  }
}
```

### Template 2: Medium Tool (Common Operations)

```typescript
/**
 * EDIT-FILE
 * Standard file editing tool with error recovery
 */
{
  name: "edit_file",
  description: "Edit a file with automatic backup and rollback",
  input_schema: {
    type: "object",
    properties: {
      file_path: {
        type: "string",
        description: "Absolute path to file"
      },
      operation: {
        type: "string",
        enum: ["replace", "insert", "delete"]
      },
      old_text: {
        type: "string",
        description: "Text to replace (for replace operation)"
      },
      new_text: {
        type: "string",
        description: "New text"
      },
      create_backup: {
        type: "boolean",
        default: true
      }
    },
    required: ["file_path", "operation", "new_text"]
  },
  output_schema: {
    status: "success|warning|error",
    summary: "string",
    next_actions: ["string"],
    artifacts: {
      backup_path: "string",
      lines_changed: "number"
    },
    error_recovery: {
      root_cause: "string",
      retry_instruction: "string",
      stop_condition: "string"
    }
  }
}
```

### Template 3: Macro Tool (Batch Operations)

```typescript
/**
 * BATCH-PROCESS
 * Efficient batch processing for low-risk operations
 */
{
  name: "batch_process",
  description: "Process multiple files in a single operation",
  input_schema: {
    type: "object",
    properties: {
      operations: {
        type: "array",
        items: {
          type: "object",
          properties: {
            tool: "string",
            parameters: "object"
          }
        }
      },
      continue_on_error: {
        type: "boolean",
        default: false
      }
    },
    required: ["operations"]
  },
  output_schema: {
    status: "success|warning|error",
    summary: "string",
    next_actions: ["string"],
    artifacts: {
      results: "array",
      successful: "number",
      failed: "number"
    }
  }
}
```

## Observation Format Templates

### Success Response Template

```json
{
  "status": "success",
  "summary": "File updated successfully",
  "next_actions": [
    "Run tests to verify changes",
    "Commit file with descriptive message"
  ],
  "artifacts": {
    "file_path": "/path/to/file.ts",
    "lines_changed": 5,
    "backup_path": "/backups/file.ts.bak"
  }
}
```

### Warning Response Template

```json
{
  "status": "warning",
  "summary": "File updated but tests failed",
  "next_actions": [
    "Review test output: /tmp/test-failure.log",
    "Fix failing tests",
    "Re-run tests"
  ],
  "artifacts": {
    "file_path": "/path/to/file.ts",
    "test_log": "/tmp/test-failure.log"
  }
}
```

### Error Response Template

```json
{
  "status": "error",
  "summary": "Failed to update file",
  "next_actions": [
    "Check file permissions",
    "Verify file exists"
  ],
  "artifacts": {},
  "error_recovery": {
    "root_cause": "Permission denied",
    "retry_instruction": "Run with elevated privileges or check file permissions",
    "stop_condition": "If 3 retries fail, check system permissions"
  }
}
```

## Architecture Pattern Examples

### ReAct Pattern (Exploratory Tasks)

```typescript
// ReAct Agent for Code Investigation
const reactAgent = {
  tools: ["search_code", "read_file", "grep_file", "list_files"],
  reasoning: "I need to find where authentication is implemented. First, I'll search for common auth patterns.",
  action: "search_code",
  observation: "Found 5 files with 'auth' in the name",
  next_reasoning: "Let me read the most relevant file to understand the implementation"
};
```

### Function-Calling Pattern (Structured Flows)

```typescript
// Function-Calling Agent for Deployments
const functionCallingAgent = {
  tools: [
    "run_tests",
    "build_image",
    "deploy_staging",
    "run_smoke_tests",
    "deploy_production"
  ],
  workflow: [
    { tool: "run_tests", required: true },
    { tool: "build_image", required: true },
    { tool: "deploy_staging", required: true },
    { tool: "run_smoke_tests", required: true },
    { tool: "deploy_production", confirm: true }
  ]
};
```

### Hybrid Pattern (Recommended)

```typescript
// Hybrid Agent: ReAct Planning + Function-Calling Execution
const hybridAgent = {
  planning: {
    tools: ["search", "read", "analyze"],
    pattern: "react",
    goal: "Understand codebase structure"
  },
  execution: {
    tools: ["edit", "test", "commit"],
    pattern: "function-calling",
    goal: "Implement changes deterministically"
  }
};
```

## Benchmarking Templates

### Metrics Tracker

```typescript
interface AgentMetrics {
  // Completion metrics
  completion_rate: number;        // Tasks completed / tasks started
  pass_at_1: number;              // Completed on first attempt
  pass_at_3: number;              // Completed within 3 attempts

  // Efficiency metrics
  retries_per_task: number;      // Average retries needed
  cost_per_success: number;       // Cost per successful task

  // Performance metrics
  avg_completion_time: number;   // Average time to completion
  token_usage_per_task: number;   // Average tokens consumed

  // Error analysis
  error_by_type: Record<string, number>;
  recovery_success_rate: number;  // Successful recoveries / total errors
}
```

## Anti-Patterns to Avoid

### ❌ Bad: Overlapping Tools

```typescript
// BAD: Three tools that do similar things
{
  tools: [
    "read_file",      // Reads entire file
    "read_lines",     // Reads specific lines
    "read_section"    // Reads a section
  ]
}

// GOOD: One tool with optional parameters
{
  tools: [
    {
      name: "read_file",
      parameters: {
        file_path: "string",
        line_start: "number (optional)",
        line_end: "number (optional)",
        section: "string (optional)"
      }
    }
  ]
}
```

### ❌ Bad: Opaque Error Output

```typescript
// BAD: No recovery information
{
  error: "Failed to deploy"
}

// GOOD: Actionable error with recovery path
{
  error: "Deployment failed: Container health check timeout",
  error_recovery: {
    root_cause: "Application not responding within 30s",
    retry_instruction: "Check application logs: docker logs <container>",
    stop_condition: "Abort if health check fails 3 times"
  }
}
```

## Quality Checklist

For each tool definition, verify:

### Input Quality
- [ ] Schema-first validation with Zod/JSON Schema
- [ ] Narrow, specific inputs (no catch-all parameters)
- [ ] Clear parameter descriptions
- [ ] Appropriate default values

### Output Quality
- [ ] Deterministic output structure
- [ ] Status field (success/warning/error)
- [ ] One-line summary
- [ ] Actionable next_steps
- [ ] Artifact references

### Error Handling
- [ ] Root cause hint
- [ ] Safe retry instruction
- [ ] Explicit stop condition
- [ ] Error type classification

### Context Budget
- [ ] Minimal system prompt
- [ ] Large docs in external files
- [ ] Skills loaded on-demand
- [ ] Compact at phase boundaries

---

This resources file provides comprehensive templates for agent tool design, observation formatting, and benchmarking.
