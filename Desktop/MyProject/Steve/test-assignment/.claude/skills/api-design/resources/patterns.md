# API Design Patterns and Templates

## REST API Conventions

### URL Structure

```
# Resource naming (plural nouns)
GET    /users          # List users
GET    /users/{id}     # Get specific user
POST   /users          # Create user
PUT    /users/{id}     # Update user
PATCH  /users/{id}     # Partial update
DELETE /users/{id}     # Delete user

# Nested resources
GET    /users/{id}/orders
POST   /users/{id}/orders
GET    /orders/{id}/items
```

### HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Valid auth but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource state conflict |
| 422 | Unprocessable Entity | Valid syntax but semantic error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

## Request/Response Templates

### POST Request

```json
POST /api/users
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}

Response: 201 Created
Location: /api/users/123

{
  "id": 123,
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-03-08T10:00:00Z",
  "updated_at": "2025-03-08T10:00:00Z"
}
```

### Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": {
      "field": "email",
      "constraint": "required"
    },
    "request_id": "req_abc123"
  }
}
```

## Pagination

### Query Parameters

```
GET /api/users?page=1&limit=20&sort=-created_at

Response:
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5,
    "has_next": true,
    "has_prev": false
  },
  "links": {
    "self": "/api/users?page=1&limit=20",
    "next": "/api/users?page=2&limit=20",
    "prev": null,
    "first": "/api/users?page=1&limit=20",
    "last": "/api/users?page=5&limit=20"
  }
}
```

### Cursor-Based Pagination

```
GET /api/users?limit=20&cursor=eyJpZCI6MTIzfQ==

Response:
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MjAwfQ==",
    "has_more": true
  }
}
```

## Filtering

### Query String Filtering

```
GET /api/users?status=active&role=admin&created_after=2025-01-01

Response:
{
  "data": [...],
  "meta": {
    "filters": {
      "status": "active",
      "role": "admin",
      "created_after": "2025-01-01"
    },
    "filtered_count": 15,
    "total_count": 100
  }
}
```

### Operator Support

```
# Supported operators
?price[gt]=100
?price[lte]=500
?status[ne]=archived
?name[contains]=john
?tags[in]=premium,vip
```

## Rate Limiting

### Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1646819200
```

### Rate Limit Error

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "retry_after": 60,
    "limit": 1000,
    "window": "hour"
  }
}
```

## Versioning

### URL Versioning

```
/api/v1/users
/api/v2/users
```

### Header Versioning

```
GET /api/users
Accept: application/vnd.myapi.v2+json
```

## API Design Checklist

### Endpoint Design

- [ ] Uses plural nouns for resources
- [ ] Consistent URL structure
- [ ] Appropriate HTTP methods
- [ ] Resource IDs in path, not query
- [ ] Nested resources max 3 levels deep

### Response Format

- [ ] Consistent response structure
- [ ] Proper status codes
- [ ] Helpful error messages
- [ ] Request ID for tracing
- [ ] ISO 8601 timestamps

### Security

- [ ] Authentication required
- [ ] Authorization checks
- [ ] Input validation
- [ ] Output sanitization
- [ ] Rate limiting
- [ ] CORS configured

### Documentation

- [ ] Endpoint description
- [ ] Request parameters
- [ ] Response format
- [ ] Error codes
- [ ] Authentication requirements
- [ ] Rate limits
- [ ] Examples

---

This resources file provides REST API design templates and best practices for production APIs.
