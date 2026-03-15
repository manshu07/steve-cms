# Route Testing - Debugging Guide

Comprehensive troubleshooting guide for debugging authentication issues and failed route tests.

## Table of Contents
- [Common HTTP Error Codes](#common-http-error-codes)
- [Authentication Issues](#authentication-issues)
- [Service Issues](#service-issues)
- [Database Issues](#database-issues)
- [Network Issues](#network-issues)
- [Debugging Tools](#debugging-tools)

---

## Common HTTP Error Codes

### 401 Unauthorized

**Symptoms:**
- Request returns 401 status
- "Unauthorized" or "Invalid token" message
- Cookie rejected

**Possible Causes:**
1. Token expired
2. Incorrect cookie format
3. JWT secret mismatch
4. Keycloak not running
5. Missing refresh_token cookie

**Solutions:**

```bash
# 1. Check Keycloak is running
docker ps | grep keycloak

# If not running, start it:
docker-compose up -d keycloak

# 2. Regenerate token with test-auth-route.js
node scripts/test-auth-route.js http://localhost:3002/api/health

# 3. Verify config.ini has correct jwtSecret
cat blog-api/config.ini | grep jwtSecret

# 4. Check Keycloak is accessible
curl -I http://localhost:8081

# 5. Verify token format (should be in cookie)
# Expected: Cookie: refresh_token=eyJhbGci...
# Wrong: Authorization: Bearer eyJhbGci...
```

**Debug Steps:**

```bash
# Enable verbose logging in service
export NODE_ENV=development
export DEBUG=*

# Check service logs
pm2 logs blog-api

# Verify token manually
# Copy token from test-auth-route.js output
# Decode at https://jwt.io to check contents
```

---

### 403 Forbidden

**Symptoms:**
- Request returns 403 status
- "Access denied" or "Insufficient permissions" message
- User authenticated but not authorized

**Possible Causes:**
1. User lacks required role
2. Resource permissions incorrect
3. Route requires specific permissions
4. User not in correct group

**Solutions:**

```bash
# 1. Use mock auth with admin role
curl -H "X-Mock-Auth: true" \
     -H "X-Mock-User: test-admin" \
     -H "X-Mock-Roles: admin" \
     http://localhost:3002/api/protected

# 2. Check user roles in database
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SELECT id, email, role FROM UserProfile WHERE email = 'testuser@example.com';"

# 3. Verify route permissions
# Check route definition in service code
grep -r "requiresRole" src/

# 4. Check Keycloak roles
# Access Keycloak admin console
# http://localhost:8081/auth/admin/
```

**Debug Steps:**

```bash
# Add logging to middleware
# In your auth middleware:
console.log('[Auth] User:', user);
console.log('[Auth] Roles:', user.roles);
console.log('[Auth] Required:', requiredRoles);

# Test with different roles
curl -H "X-Mock-Auth: true" \
     -H "X-Mock-Roles: user" \
     http://localhost:3002/api/protected

curl -H "X-Mock-Auth: true" \
     -H "X-Mock-Roles: admin" \
     http://localhost:3002/api/protected
```

---

### 404 Not Found

**Symptoms:**
- Request returns 404 status
- "Not Found" or "Route not found" message
- No matching route

**Possible Causes:**
1. Incorrect URL
2. Missing route prefix
3. Route not registered
4. Wrong service/port

**Solutions:**

```bash
# 1. Check service is running
pm2 list

# 2. Verify correct port
curl http://localhost:3002/api/health

# 3. Check route prefixes in app.ts
cat blog-api/src/app.ts | grep "app.use"

# Example output:
# app.use('/blog-api/api', formRoutes);
# app.use('/api/workflow', workflowRoutes);

# 4. Test root endpoint
curl http://localhost:3002/

# 5. List all routes (if debug endpoint available)
curl http://localhost:3002/api/routes
```

**Debug Steps:**

```bash
# Find route definition
grep -r "router.get.*'your-route'" src/

# Check Express route listing
# Add to app.ts for debugging:
app._router.stack.forEach((r) => {
    if (r.route && r.route.path) {
        console.log(r.route.path);
    }
});

# Verify service configuration
cat blog-api/config.ini | grep -A 5 "[server]"
```

**Full URL Construction:**

```
Full URL = Base URL + Route Prefix + Route Path

Example:
- Base: http://localhost:3002
- Prefix: /blog-api/api
- Route: /777/submit
- Full: http://localhost:3000/blog-api/777/submit
```

---

### 500 Internal Server Error

**Symptoms:**
- Request returns 500 status
- "Internal Server Error" message
- Application crashed or threw error

**Possible Causes:**
1. Database connection issue
2. Missing required fields
3. Validation error
4. Application code error
5. Missing environment variables

**Solutions:**

```bash
# 1. Check service logs for error details
pm2 logs blog-api --lines 50

# 2. Check Sentry for error details
# Access Sentry dashboard
# Look for recent errors

# 3. Verify request body matches schema
node scripts/test-auth-route.js \
    http://localhost:3002/api/endpoint \
    POST \
    '{"field":"value"}'

# 4. Check database connectivity
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SELECT 1;"

# 5. Verify environment variables
cat blog-api/.env | grep -v "SECRET\|PASSWORD"
```

**Debug Steps:**

```bash
# Enable detailed error messages (development only)
export NODE_ENV=development

# Add error logging middleware
app.use((err, req, res, next) => {
    console.error('[Error]', err);
    console.error('[Stack]', err.stack);
    res.status(500).json({
        error: err.message,
        stack: process.env.NODE_ENV === 'development' ? err.stack : undefined
    });
});

# Test with minimal data
node scripts/test-auth-route.js \
    http://localhost:3002/api/endpoint \
    POST \
    '{}'

# Check for required fields
grep -A 10 "req.body" src/routes/your-route.ts
```

**Common 500 Errors:**

```bash
# Database connection error
# Solution: Check MySQL is running
docker ps | grep mysql

# Validation error
# Solution: Check request body matches schema
# Look for Zod/Joi validation in route

# Undefined variable error
# Solution: Check service logs for exact error
# Look for missing dependencies or imports

# Timeout error
# Solution: Increase timeout or optimize query
# Check for long-running database queries
```

---

## Authentication Issues

### Keycloak Not Running

**Symptoms:**
- Cannot get tokens
- Connection refused errors
- test-auth-route.js fails

**Solutions:**

```bash
# Check if Keycloak is running
docker ps | grep keycloak

# Start Keycloak
docker-compose up -d keycloak

# Check Keycloak logs
docker-compose logs keycloak

# Verify Keycloak is accessible
curl http://localhost:8081/auth/realms/yourRealm/.well-known/openid-configuration
```

### JWT Secret Mismatch

**Symptoms:**
- Tokens generated but rejected
- "Invalid signature" error
- Authentication works with test-auth-route.js but manual curl fails

**Solutions:**

```bash
# Check JWT secret in config.ini
cat blog-api/config.ini | grep jwtSecret

# Verify all services use same secret
grep -r "jwtSecret" */config.ini

# Restart services after changing secret
pm2 restart all

# Regenerate token with new secret
node scripts/test-auth-route.js http://localhost:3002/api/health
```

### Cookie Format Issues

**Symptoms:**
- Token present but rejected
- "Missing cookie" error
- Manual curl works but test script doesn't

**Solutions:**

```bash
# Check cookie name (should be refresh_token)
grep -r "cookie" blog-api/src/middleware/

# Verify cookie format
# Correct: Cookie: refresh_token=eyJhbGci...
# Wrong: Authorization: Bearer eyJhbGci...

# Test cookie manually
curl -v -b "refresh_token=TOKEN" http://localhost:3002/api/endpoint
```

---

## Service Issues

### Service Not Running

**Symptoms:**
- Connection refused
- ECONNREFUSED error
- Service not in pm2 list

**Solutions:**

```bash
# Check service status
pm2 list

# Start service
pm2 start blog-api/src/server.js --name blog-api

# Check service logs
pm2 logs blog-api

# Restart service
pm2 restart blog-api

# Check port is in use
netstat -tlnp | grep 3002
# or
lsof -i :3002
```

### Service Port Conflicts

**Symptoms:**
- Port already in use error
- Service fails to start
- Wrong service responding

**Solutions:**

```bash
# Find process using port
lsof -i :3002

# Kill process if needed
kill -9 <PID>

# Change port in config.ini
[server]
port = 3005

# Update service to use new port
pm2 restart blog-api --update-env
```

### Service Crash Loop

**Symptoms:**
- Service keeps restarting
- PM2 shows "errored" status
- Logs show crash

**Solutions:**

```bash
# Check crash logs
pm2 logs blog-api --err

# Check for syntax errors
npm run lint

# Check for missing dependencies
npm install

# Run service directly for better error output
NODE_ENV=development node blog-api/src/server.js

# Check for unhandled promises
# Add to process:
process.on('unhandledRejection', (err) => {
    console.error('Unhandled rejection:', err);
});
```

---

## Database Issues

### Database Not Running

**Symptoms:**
- Connection refused errors
- "Can't connect to MySQL" error
- Services fail to start

**Solutions:**

```bash
# Check MySQL is running
docker ps | grep mysql

# Start MySQL
docker-compose up -d mysql

# Check MySQL logs
docker-compose logs mysql

# Test MySQL connection
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev -e "SELECT 1;"
```

### Database Connection Pool Exhausted

**Symptoms:**
- "Pool exhausted" errors
- Slow queries
- Requests timeout

**Solutions:**

```bash
# Check database connections
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SHOW PROCESSLIST;"

# Kill long-running queries
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "KILL <process_id>;"

# Restart services to release connections
pm2 restart all

# Check connection pool settings
grep -r "connectionLimit" blog-api/src/
```

### Database Schema Issues

**Symptoms:**
- "Table doesn't exist" error
- "Column not found" error
- Migration errors

**Solutions:**

```bash
# Check database schema
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SHOW TABLES;"

# Check table structure
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "DESCRIBE WorkflowInstance;"

# Run pending migrations
npm run migrate

# Sync Prisma schema
npx prisma db push
```

---

## Network Issues

### Docker Network Issues

**Symptoms:**
- Services can't communicate
- Connection timeout errors
- Intermittent failures

**Solutions:**

```bash
# Check Docker network
docker network ls

# Check which network services are on
docker inspect local-mysql | grep Network

# Test connectivity between containers
docker exec blog-api ping local-mysql

# Restart Docker network
docker-compose down
docker-compose up -d
```

### Firewall Issues

**Symptoms:**
- Connection timeout from host
- Can access from inside Docker but not host
- Specific ports blocked

**Solutions:**

```bash
# Check firewall rules
sudo iptables -L

# Test local connection
curl http://localhost:3002/api/health

# Check if port is listening
netstat -tlnp | grep 3002

# Temporarily disable firewall (testing only)
sudo ufw disable
# Remember to re-enable: sudo ufw enable
```

---

## Debugging Tools

### Service Logs

```bash
# Real-time logs
pm2 logs blog-api

# Logs for specific service
pm2 logs blog-api --lines 100

# Error logs only
pm2 logs blog-api --err

# Clear logs
pm2 flush
```

### Database Queries

```bash
# Enable slow query log
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SET GLOBAL slow_query_log = 'ON';"

# Check slow queries
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;"

# Monitor queries in real-time
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev \
    -e "SHOW PROCESSLIST;"
```

### HTTP Debugging

```bash
# Verbose curl output
curl -v http://localhost:3002/api/endpoint

# Show response headers
curl -I http://localhost:3002/api/endpoint

# Show full request/response
curl -v -X POST http://localhost:3002/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"field":"value"}'

# Time request
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:3002/api/endpoint

# curl-format.txt contents:
# time_namelookup: %{time_namelookup}\n
# time_connect: %{time_connect}\n
# time_starttransfer: %{time_starttransfer}\n
# time_total: %{time_total}\n
```

### Authentication Debugging

```bash
# Decode JWT token (from jwt.io or command line)
# Copy token and decode to see:
# - User ID
# - Roles
# - Expiration time
# - Issuer

# Test authentication flow
node scripts/test-auth-route.js http://localhost:3002/api/health

# Check token expiration
# Copy token, decode, check "exp" timestamp
# Convert to human-readable:
node -e "console.log(new Date(1678900000 * 1000).toISOString())"
```

---

## Quick Reference

### Essential Commands

```bash
# Service management
pm2 list                    # List all services
pm2 logs <service>         # View logs
pm2 restart <service>      # Restart service
pm2 stop <service>         # Stop service

# Database
docker exec -i local-mysql mysql -u root -ppassword1 blog_dev -e "QUERY"

# Authentication
node scripts/test-auth-route.js <URL>

# Testing
curl -v <URL>              # Verbose curl
curl -I <URL>              # Headers only
```

### Common Error Patterns

| Error | Cause | Quick Fix |
|-------|-------|-----------|
| 401 | Token expired | Regenerate with test-auth-route.js |
| 403 | Missing role | Use mock auth with admin role |
| 404 | Wrong URL | Check app.ts for route prefixes |
| 500 | App error | Check pm2 logs and Sentry |
| ECONNREFUSED | Service down | pm2 restart <service> |
| Timeout | Database slow | Check MySQL, optimize query |

### Debugging Checklist

- [ ] Service running? (`pm2 list`)
- [ ] Correct port? (Check config.ini)
- [ ] Keycloak running? (`docker ps | grep keycloak`)
- [ ] Token valid? (Regenerate with test-auth-route.js)
- [ ] Database accessible? (`docker exec -i local-mysql mysql -e "SELECT 1;"`)
- [ ] Logs reviewed? (`pm2 logs <service>`)
- [ ] Sentry checked? (Dashboard for errors)
- [ ] Network OK? (`curl http://localhost:<port>/api/health`)
