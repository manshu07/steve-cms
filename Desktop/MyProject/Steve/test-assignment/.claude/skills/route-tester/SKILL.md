---
name: route-tester
description: Test authenticated routes in the project using cookie-based authentication. Use this skill when testing API endpoints, validating route functionality, or debugging authentication issues. Includes patterns for using test-auth-route.js and mock authentication.
---

# Route Tester Skill

## Purpose
Provides patterns for testing authenticated routes using cookie-based JWT authentication with Keycloak.

## When to Use This Skill
- Testing new API endpoints
- Validating route functionality after changes
- Debugging authentication issues
- Testing POST/PUT/DELETE operations
- Verifying request/response data

---

## Quick Start

### 1. Test with test-auth-route.js (RECOMMENDED)

```bash
# GET request
node scripts/test-auth-route.js http://localhost:3002/api/endpoint

# POST request
node scripts/test-auth-route.js \
    http://localhost:3002/api/submit \
    POST \
    '{"field":"value"}'
```

The script automatically:
- Gets refresh token from Keycloak
- Signs token with JWT secret from `config.ini`
- Creates cookie header
- Makes authenticated request
- Displays curl command for manual testing

### 2. Manual curl with Token

```bash
# Copy token from test-auth-route.js output
curl -X POST http://localhost:3002/api/submit \
  -H "Content-Type: application/json" \
  -b "refresh_token=<TOKEN>" \
  -d '{"field":"value"}'
```

### 3. Mock Authentication (Development)

```bash
# Add to .env:
MOCK_AUTH=true

curl -H "X-Mock-Auth: true" \
     -H "X-Mock-User: test-user" \
     -H "X-Mock-Roles: admin" \
     http://localhost:3002/api/protected
```

---

## Authentication Overview

The project uses:
- **Keycloak** for SSO (realm: yourRealm)
- **Cookie-based JWT** tokens (not Bearer headers)
- **Cookie name**: `refresh_token`
- **JWT signing**: Secret from `config.ini`

**Test Credentials:**
- Username: `testuser`
- Password: `testpassword`

---

## Service Ports

| Service | Port | Base URL |
|---------|------|----------|
| Users   | 3000 | http://localhost:3000 |
| Projects| 3001 | http://localhost:3001 |
| Form    | 3002 | http://localhost:3002 |
| Email   | 3003 | http://localhost:3003 |
| Uploads | 5000 | http://localhost:5000 |

---

## URL Construction

**Full URL** = Base URL + Route Prefix + Route Path

Example:
- Base: `http://localhost:3002`
- Prefix: `/blog-api/api`
- Route: `/777/submit`
- **Full**: `http://localhost:3000/blog-api/777/submit`

Check prefixes in service `app.ts`:
```typescript
app.use('/blog-api/api', formRoutes);
app.use('/api/workflow', workflowRoutes);
```

---

## Common Testing Patterns

### Form Submission
```bash
node scripts/test-auth-route.js \
    http://localhost:3000/blog-api/777/submit \
    POST \
    '{"responses":{"4577":"13295"},"submissionID":5}'
```

### Workflow Start
```bash
node scripts/test-auth-route.js \
    http://localhost:3002/api/workflow/start \
    POST \
    '{"workflowCode":"DHS_CLOSEOUT","entityType":"Submission","entityID":123}'
```

### GET with Query Parameters
```bash
node scripts/test-auth-route.js \
    "http://localhost:3002/api/workflows?status=active&limit=10"
```

---

## Database Verification

After testing routes that modify data:

```bash
# Connect to MySQL
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev

# Check specific record
mysql> SELECT * FROM WorkflowInstance WHERE id = 123;

# Check recent records
mysql> SELECT * FROM WorkflowStepInstance WHERE instanceId = 123 ORDER BY createdAt DESC LIMIT 5;

# Quick verification
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SELECT * FROM FormSubmission ORDER BY createdAt DESC LIMIT 1\G"
```

---

## Common Errors & Quick Fixes

### 401 Unauthorized
- **Cause**: Token expired or invalid
- **Fix**: Regenerate token with test-auth-route.js

### 403 Forbidden
- **Cause**: User lacks required role
- **Fix**: Use mock auth with admin role

### 404 Not Found
- **Cause**: Incorrect URL or missing route prefix
- **Fix**: Check app.ts for route prefixes

### 500 Internal Server Error
- **Cause**: Application error
- **Fix**: Check pm2 logs and Sentry

---

## Testing Checklist

Before testing:
- [ ] Identify service and port
- [ ] Check route prefixes in app.ts
- [ ] Construct full URL
- [ ] Prepare request body (if POST/PUT)

After testing:
- [ ] Verify response status
- [ ] Check response data
- [ ] Verify database changes
- [ ] Check Sentry for errors

---

## Key Files

- `scripts/test-auth-route.js` - Main testing script
- `blog-api/src/app.ts` - Form service routes
- `notifications/src/app.ts` - Email service routes
- `auth/src/app.ts` - Users service routes
- `config.ini` - Service configuration

---

## Resources

📚 **Detailed Guides:**
- [testing-patterns.md](resources/testing-patterns.md) - Comprehensive testing patterns and examples
- [debugging-guide.md](resources/debugging-guide.md) - Troubleshooting and debugging techniques

---

## Related Skills

- **database-verification** - Verify database changes
- **error-tracking** - Check for captured errors
- **backend-dev-guidelines** - Controller and route patterns
