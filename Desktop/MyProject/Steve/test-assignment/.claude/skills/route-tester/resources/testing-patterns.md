# Route Testing Patterns & Examples

Complete collection of testing patterns for authenticated routes in the project using cookie-based JWT authentication.

## Table of Contents
- [Testing Methods Overview](#testing-methods-overview)
- [Common Testing Patterns](#common-testing-patterns)
- [Service-Specific Examples](#service-specific-examples)
- [Test Scenarios](#test-scenarios)
- [Database Verification](#database-verification)

---

## Testing Methods Overview

### Method 1: test-auth-route.js (RECOMMENDED)

The `test-auth-route.js` script handles authentication automatically.

**Location**: `scripts/test-auth-route.js`

```bash
# Basic GET request
node scripts/test-auth-route.js http://localhost:3002/api/endpoint

# POST request with JSON data
node scripts/test-auth-route.js \
    http://localhost:3002/api/endpoint \
    POST \
    '{"key":"value"}'

# PUT request
node scripts/test-auth-route.js \
    http://localhost:3002/api/resource/123 \
    PUT \
    '{"field":"updated"}'

# DELETE request
node scripts/test-auth-route.js \
    http://localhost:3002/api/resource/123 \
    DELETE
```

**What the script does:**
1. Gets refresh token from Keycloak (testuser/testpassword)
2. Signs token with JWT secret from `config.ini`
3. Creates cookie header: `refresh_token=<signed-token>`
4. Makes authenticated request
5. Displays response and curl command for manual testing

**Output includes:**
- Request details (URL, method, headers)
- Response status and body
- curl command for manual reproduction
- Any errors encountered

### Method 2: Manual curl with Token

Extract the token from test-auth-route.js output:

```bash
# Script outputs something like:
# 💡 To test manually with curl:
# curl -b "refresh_token=eyJhbGci..." http://localhost:3002/api/endpoint

# Use that token for manual testing:
curl -X POST http://localhost:3002/api/submit \
  -H "Content-Type: application/json" \
  -b "refresh_token=<COPIED_TOKEN>" \
  -d '{"field":"value"}'

# With query parameters
curl -X GET "http://localhost:3002/api/items?status=active&limit=10" \
  -b "refresh_token=<COPIED_TOKEN>"

# File upload
curl -X POST http://localhost:5000/upload \
  -H "Content-Type: multipart/form-data" \
  -b "refresh_token=<COPIED_TOKEN>" \
  -F "file=@/path/to/file.pdf" \
  -F "metadata={\"description\":\"Test\"}"
```

### Method 3: Mock Authentication (Development Only)

Bypass Keycloak entirely using mock auth headers:

```bash
# Setup - add to service .env file
MOCK_AUTH=true
MOCK_USER_ID=test-user
MOCK_USER_ROLES=admin,operations

# Test with mock auth
curl -H "X-Mock-Auth: true" \
     -H "X-Mock-User: test-user" \
     -H "X-Mock-Roles: admin,operations" \
     http://localhost:3002/api/protected

# POST with mock auth
curl -X POST http://localhost:3002/api/submit \
     -H "X-Mock-Auth: true" \
     -H "X-Mock-User: admin" \
     -H "X-Mock-Roles: admin" \
     -H "Content-Type: application/json" \
     -d '{"field":"value"}'
```

**Mock Auth Requirements:**
- `NODE_ENV` must be `development` or `test`
- Mock auth middleware must be added to the route
- Will NEVER work in production (security feature)

---

## Common Testing Patterns

### GET Request Patterns

#### Simple GET
```bash
node scripts/test-auth-route.js http://localhost:3002/api/workflows
```

#### GET with Query Parameters
```bash
node scripts/test-auth-route.js \
    "http://localhost:3002/api/workflows?status=active&limit=10"

# Multiple parameters
node scripts/test-auth-route.js \
    "http://localhost:3002/api/users?role=admin&status=active&page=1&pageSize=20"
```

#### GET with Path Parameters
```bash
node scripts/test-auth-route.js \
    http://localhost:3002/api/workflow/123

# Nested resources
node scripts/test-auth-route.js \
    http://localhost:3002/api/workflow/123/step/456
```

### POST Request Patterns

#### Simple POST
```bash
node scripts/test-auth-route.js \
    http://localhost:3002/api/submit \
    POST \
    '{"field1":"value1","field2":"value2"}'
```

#### Form Submission
```bash
node scripts/test-auth-route.js \
    http://localhost:3000/blog-api/777/submit \
    POST \
    '{"responses":{"4577":"13295"},"submissionID":5,"stepInstanceId":"11"}'
```

#### Workflow Start
```bash
node scripts/test-auth-route.js \
    http://localhost:3002/api/workflow/start \
    POST \
    '{
      "workflowCode":"DHS_CLOSEOUT",
      "entityType":"Submission",
      "entityID":123
    }'
```

#### Workflow Step Completion
```bash
node scripts/test-auth-route.js \
    http://localhost:3002/api/workflow/step/complete \
    POST \
    '{
      "stepInstanceID":789,
      "answers":{
        "decision":"approved",
        "comments":"Looks good"
      }
    }'
```

#### Create User
```bash
node scripts/test-auth-route.js \
    http://localhost:3000/api/users \
    POST \
    '{
      "email":"user@example.com",
      "name":"John Doe",
      "role":"operations"
    }'
```

### PUT Request Patterns

#### Update Resource
```bash
node scripts/test-auth-route.js \
    http://localhost:3002/api/workflow/123 \
    PUT \
    '{"status":"completed","notes":"Finished"}'
```

#### Partial Update
```bash
node scripts/test-auth-route.js \
    http://localhost:3002/api/user/profile \
    PUT \
    '{"preferences":{"theme":"dark","language":"en"}}'
```

### DELETE Request Patterns

#### Delete Resource
```bash
node scripts/test-auth-route.js \
    http://localhost:3002/api/workflow/123 \
    DELETE
```

#### Soft Delete
```bash
node scripts/test-auth-route.js \
    http://localhost:3002/api/item/123/archive \
    POST \
    '{"archived":true,"archivedBy":"user-123"}'
```

---

## Service-Specific Examples

### Form Service (Port 3002)

#### Submit Form Response
```bash
node scripts/test-auth-route.js \
    http://localhost:3000/blog-api/777/submit \
    POST \
    '{
      "responses":{"4577":"Option A","4578":"Option B"},
      "submissionID":5,
      "stepInstanceId":"11"
    }'
```

#### Get Form Data
```bash
node scripts/test-auth-route.js \
    http://localhost:3002/api/form/777/data
```

#### Validate Form Access
```bash
node scripts/test-auth-route.js \
    http://localhost:3002/api/form/777/access/user-123
```

### Email Service (Port 3003)

#### Send Email
```bash
node scripts/test-auth-route.js \
    http://localhost:3003/api/email/send \
    POST \
    '{
      "to":"recipient@example.com",
      "template":"welcome",
      "data":{"name":"John","userId":"123"}
    }'
```

#### Get Email Status
```bash
node scripts/test-auth-route.js \
    http://localhost:3003/api/email/status/msg-123
```

#### List Recent Emails
```bash
node scripts/test-auth-route.js \
    "http://localhost:3003/api/email/recent?limit=20"
```

### Users Service (Port 3000)

#### Get User Profile
```bash
node scripts/test-auth-route.js \
    http://localhost:3000/api/user/profile
```

#### Update User
```bash
node scripts/test-auth-route.js \
    http://localhost:3000/api/user/123 \
    PUT \
    '{"name":"Updated Name","preferences":{"theme":"light"}}'
```

#### List Users
```bash
node scripts/test-auth-route.js \
    "http://localhost:3000/api/users?role=operations&status=active"
```

### Uploads Service (Port 5000)

#### Upload File
```bash
# Get token first, then:
curl -X POST http://localhost:5000/upload \
  -H "Content-Type: multipart/form-data" \
  -b "refresh_token=<TOKEN>" \
  -F "file=@/path/to/document.pdf" \
  -F "metadata={\"type\":\"document\",\"entityId\":123}"
```

#### Get File Info
```bash
node scripts/test-auth-route.js \
    http://localhost:5000/file/info/doc-123
```

---

## Test Scenarios

### Scenario 1: New Route Testing

After creating a new route, test all aspects:

```bash
# 1. Test with valid data
node scripts/test-auth-route.js \
    http://localhost:3002/api/my-new-route \
    POST \
    '{"field1":"value1","field2":"value2"}'

# 2. Test with missing required fields
node scripts/test-auth-route.js \
    http://localhost:3002/api/my-new-route \
    POST \
    '{"field1":"value1"}'

# 3. Test with invalid data types
node scripts/test-auth-route.js \
    http://localhost:3002/api/my-new-route \
    POST \
    '{"field1":123,"field2":["array","when","string","expected"]}'

# 4. Test without authentication (should return 401)
curl http://localhost:3002/api/my-new-route

# 5. Verify database changes
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SELECT * FROM MyTable ORDER BY createdAt DESC LIMIT 1;"
```

### Scenario 2: Route Modification Testing

After modifying an existing route:

```bash
# 1. Test existing functionality still works
node scripts/test-auth-route.js \
    http://localhost:3002/api/existing-route \
    POST \
    '{"existing":"data"}'

# 2. Test new functionality
node scripts/test-auth-route.js \
    http://localhost:3002/api/existing-route \
    POST \
    '{"new":"field","existing":"data"}'

# 3. Test backward compatibility (if applicable)
node scripts/test-auth-route.js \
    http://localhost:3002/api/existing-route \
    POST \
    '{"existing":"data","optional":"field"}'

# 4. Verify database schema changes
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "DESCRIBE MyTable;"

# 5. Test with edge cases
node scripts/test-auth-route.js \
    http://localhost:3002/api/existing-route \
    POST \
    '{"existing":"","edge":null}'
```

### Scenario 3: Authentication Testing

Test authentication and authorization:

```bash
# 1. Test with valid authentication
node scripts/test-auth-route.js http://localhost:3002/api/protected

# 2. Test without authentication
curl http://localhost:3002/api/protected
# Expected: 401 Unauthorized

# 3. Test with expired token (use old token)
curl -b "refresh_token=<OLD_TOKEN>" http://localhost:3002/api/protected
# Expected: 401 Unauthorized

# 4. Test role-based access with mock auth
curl -H "X-Mock-Auth: true" \
     -H "X-Mock-User: user" \
     -H "X-Mock-Roles: user" \
     http://localhost:3002/api/admin-only
# Expected: 403 Forbidden

curl -H "X-Mock-Auth: true" \
     -H "X-Mock-User: admin" \
     -H "X-Mock-Roles: admin" \
     http://localhost:3002/api/admin-only
# Expected: 200 OK
```

### Scenario 4: Error Handling Testing

Test error responses:

```bash
# 1. Test validation errors
node scripts/test-auth-route.js \
    http://localhost:3002/api/submit \
    POST \
    '{"invalid":"data"}'

# 2. Test database constraint violations
node scripts/test-auth-route.js \
    http://localhost:3002/api/user \
    POST \
    '{"email":"existing@example.com"}'

# 3. Test timeout scenarios
node scripts/test-auth-route.js \
    http://localhost:3002/api/slow-endpoint

# 4. Test malformed JSON
node scripts/test-auth-route.js \
    http://localhost:3002/api/submit \
    POST \
    '{invalid json}'
```

### Scenario 5: Performance Testing

Basic performance checks:

```bash
# 1. Time the request
time node scripts/test-auth-route.js \
    http://localhost:3002/api/heavy-operation

# 2. Test with large payloads
node scripts/test-auth-route.js \
    http://localhost:3002/api/bulk-import \
    POST \
    '{"items":['$(for i in {1..100}; do echo '{"id":"'$i'","data":"item'$i'"},'; done | sed 's/,$//')']}'

# 3. Test concurrent requests (using parallel)
for i in {1..10}; do
    node scripts/test-auth-route.js \
        http://localhost:3002/api/endpoint &
done
wait
```

---

## Database Verification

### MySQL Commands

After testing routes that modify data:

```bash
# Connect to MySQL
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev

# Check specific record
mysql> SELECT * FROM WorkflowInstance WHERE id = 123\G

# Check recent records
mysql> SELECT * FROM WorkflowStepInstance WHERE instanceId = 123 ORDER BY createdAt DESC LIMIT 5\G

# Check notifications
mysql> SELECT * FROM WorkflowNotification WHERE recipientUserId = 'user-123' ORDER BY createdAt DESC\G

# Count records
mysql> SELECT COUNT(*) FROM FormSubmission WHERE formId = 777;

# Check relationships
mysql> SELECT
    w.id,
    w.workflowCode,
    w.status,
    COUNT(s.id) as stepCount
FROM WorkflowInstance w
LEFT JOIN WorkflowStepInstance s ON w.id = s.instanceId
WHERE w.id = 123
GROUP BY w.id;
```

### Quick Verification Scripts

```bash
# Check workflow status
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SELECT id, workflowCode, status FROM WorkflowInstance WHERE id = 123;"

# Check recent submissions
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SELECT * FROM FormSubmission ORDER BY createdAt DESC LIMIT 1\G"

# Count notifications
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SELECT COUNT(*) as total FROM WorkflowNotification WHERE status = 'pending';"
```

### Verify Specific Tables

```bash
# Form submissions
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SELECT id, formId, userId, createdAt FROM FormSubmission WHERE id = LAST_INSERT_ID();"

# Workflow instances
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SELECT id, workflowCode, status, currentStep FROM WorkflowInstance WHERE entityID = 123;"

# Users
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SELECT id, email, role, status FROM UserProfile WHERE email = 'test@example.com';"
```

---

## Service Ports Reference

| Service | Port | Base URL |
|---------|------|----------|
| Users   | 3000 | http://localhost:3000 |
| Projects| 3001 | http://localhost:3001 |
| Form    | 3002 | http://localhost:3002 |
| Email   | 3003 | http://localhost:3003 |
| Uploads | 5000 | http://localhost:5000 |

---

## Testing Checklist

Before testing a route:

- [ ] Identify the service (form, email, users, etc.)
- [ ] Find the correct port
- [ ] Check route prefixes in `app.ts`
- [ ] Construct the full URL
- [ ] Prepare request body (if POST/PUT)
- [ ] Determine authentication method
- [ ] Run the test
- [ ] Verify response status and data
- [ ] Check database changes if applicable
- [ ] Check Sentry for errors (if applicable)

After testing:

- [ ] Clean up test data (if needed)
- [ ] Document any issues found
- [ ] Update test cases for regression testing
