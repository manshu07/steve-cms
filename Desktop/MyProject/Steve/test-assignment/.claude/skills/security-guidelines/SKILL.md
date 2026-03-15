---
name: security-guidelines
description: Security best practices for web applications, APIs, authentication, authorization, data protection, OWASP compliance, and vulnerability prevention. Use when implementing security features, handling sensitive data, setting up authentication, or securing endpoints. Covers OWASP Top 10, JWT security, input validation, SQL injection prevention, XSS protection, CSRF protection, secrets management, and security headers.
---

# Security Guidelines

## Purpose
Comprehensive security practices for web applications covering authentication, authorization, data protection, and vulnerability prevention.

## When to Use This Skill
- Implementing authentication/authorization
- Handling sensitive data (PII, passwords, tokens)
- Securing API endpoints
- Validating user input
- Setting up encryption
- Configuring security headers
- Implementing session management
- Preventing OWASP Top 10 vulnerabilities

---

## Core Principles

1. **Never Trust User Input** - Always validate and sanitize
2. **Defense in Depth** - Multiple security layers
3. **Principle of Least Privilege** - Minimum required access
4. **Security by Default** - Secure defaults, not opt-in
5. **Encrypt Sensitive Data** - At rest and in transit

---

## Authentication & Authorization

### JWT Best Practices

**Token Structure:**
```typescript
// ✅ Correct: Short-lived JWT with refresh token
const accessToken = jwt.sign(
  { userId, roles },
  process.env.JWT_SECRET,
  { expiresIn: '15m' }  // Short-lived
);

const refreshToken = jwt.sign(
  { userId },
  process.env.REFRESH_SECRET,
  { expiresIn: '7d' }  // Longer-lived
);

// ❌ Wrong: Long-lived access token
const token = jwt.sign(
  { userId },
  secret,
  { expiresIn: '365d' }  // Too long!
);
```

**Token Validation:**
```typescript
function verifyToken(token: string) {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Check expiration
    if (decoded.exp < Date.now() / 1000) {
      throw new Error('Token expired');
    }

    // Check issuer
    if (decoded.iss !== 'your-app') {
      throw new Error('Invalid issuer');
    }

    return decoded;
  } catch (error) {
    throw new Error('Invalid token');
  }
}
```

### Password Security

**Hashing:**
```typescript
import bcrypt from 'bcrypt';

// ✅ Correct: Bcrypt with proper cost factor
async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, 12);  // Cost factor 12
}

// Verify password
async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// ❌ Wrong: MD5, SHA1, or no salt
// const hash = md5(password);  // Never do this!
```

**Password Requirements:**
- Minimum 12 characters
- Include uppercase, lowercase, numbers, symbols
- Check against common password lists
- Don't enforce arbitrary complexity (leads to Post-It notes)

---

## Input Validation

### Validation Layers

**1. Schema Validation (Zod):**
```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(12),
  age: z.number().min(18).max(120),
  name: z.string().max(100).regex(/^[a-zA-Z\s]+$/)
});

function validateUser(input: unknown) {
  return userSchema.parse(input);
}
```

**2. SQL Injection Prevention:**
```typescript
// ✅ Correct: Parameterized queries (Prisma)
const user = await prisma.user.findUnique({
  where: { email: userEmail }  // Safe!
});

// ❌ Wrong: String concatenation
const user = await prisma.$queryRaw`
  SELECT * FROM users WHERE email = '${userEmail}'
`;  // SQL injection risk!
```

**3. XSS Prevention:**
```typescript
// ✅ Correct: Escape user input
import * as DOMPurify from 'dompurify';

const clean = DOMPurify.sanitize(userInput);

// ❌ Wrong: Direct insertion
div.innerHTML = userInput;  // XSS risk!
```

---

## API Security

### Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,  // Limit each IP to 100 requests per window
  message: 'Too many requests',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', apiLimiter);
```

### CORS Configuration

```typescript
// ✅ Correct: Specific origins
app.use(cors({
  origin: ['https://app.example.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// ❌ Wrong: Allow all origins
app.use(cors());  // Security risk!
```

### Security Headers

```typescript
import helmet from 'helmet';

app.use(helmet());

// Additional headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});
```

---

## Data Protection

### Encryption at Rest

```typescript
import crypto from 'crypto';

const algorithm = 'aes-256-gcm';
const key = crypto.scryptSync(process.env.ENCRYPTION_KEY, 'salt', 32);

function encrypt(text: string): { encrypted: string; iv: string; tag: string } {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(algorithm, key, iv);

  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const tag = cipher.getAuthTag();

  return { encrypted, iv: iv.toString('hex'), tag: tag.toString('hex') };
}

function decrypt(encrypted: string, iv: string, tag: string): string {
  const decipher = crypto.createDecipheriv(
    algorithm,
    key,
    Buffer.from(iv, 'hex')
  );

  decipher.setAuthTag(Buffer.from(tag, 'hex'));

  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
}
```

### Sensitive Data Handling

**PII Data:**
- Never log sensitive data (passwords, tokens, SSN)
- Use environment variables for secrets
- Encrypt PII in database
- Implement data retention policies
- Right to be forgotten (GDPR)

**Logging:**
```typescript
// ✅ Correct: Sanitize logs
logger.info('User login', {
  userId: user.id,
  timestamp: new Date()
});

// ❌ Wrong: Log sensitive data
logger.info('User login', {
  userId: user.id,
  password: user.password,  // Never log passwords!
  token: user.token
});
```

---

## OWASP Top 10 Prevention

### A01: Broken Access Control

```typescript
// ✅ Correct: Check authorization on every request
async function updateProfile(req, res) {
  const { userId } = req.params;
  const currentUser = req.user;

  // Verify user owns the resource
  if (currentUser.id !== userId && !currentUser.roles.includes('admin')) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  // Proceed with update
}

// ❌ Wrong: No ownership check
async function updateProfile(req, res) {
  const { userId } = req.params;
  // Anyone can update any profile!
}
```

### A03: Injection

```typescript
// ✅ Correct: Use ORM/parameterized queries
const users = await prisma.user.findMany({
  where: {
    role: userInput.role  // Safe
  }
});

// ❌ Wrong: String concatenation
const users = await prisma.$queryRaw(
  `SELECT * FROM users WHERE role = '${userInput.role}'`
);  // SQL injection!
```

### A07: Identification and Authentication Failures

```typescript
// ✅ Correct: Secure password reset
async function requestPasswordReset(email: string) {
  const user = await prisma.user.findUnique({ where: { email } });

  // Always return success (don't reveal if user exists)
  if (!user) return;

  const token = crypto.randomBytes(32).toString('hex');
  const expires = new Date(Date.now() + 3600000);  // 1 hour

  await prisma.passwordReset.create({
    data: { userId: user.id, token, expires }
  });

  await sendResetEmail(email, token);
}

// ❌ Wrong: Reveals user existence
async function requestPasswordReset(email: string) {
  const user = await prisma.user.findUnique({ where: { email } });

  if (!user) {
    throw new Error('User not found');  // Reveals existence!
  }
}
```

---

## Secrets Management

### Environment Variables

```bash
# .env (gitignored)
DATABASE_URL=postgres://user:pass@host:5432/db
JWT_SECRET=your-secret-key
API_KEY=secret-api-key
ENCRYPTION_KEY=encryption-key
```

### Never Commit Secrets

```yaml
# .gitignore
.env
.env.local
.env.*.local
*.pem
*.key
secrets/
```

### Rotate Secrets Regularly

- JWT secrets every 90 days
- API keys every 60-90 days
- Database credentials every 90 days
- Encryption keys annually (with key rotation plan)

---

## Common Vulnerabilities

### XSS (Cross-Site Scripting)

```typescript
// ✅ Correct: Escape output
import escape from 'escape-html';

res.send({ message: escape(userInput) });

// React automatically escapes (if using {})
<div>{userInput}</div>
```

### CSRF (Cross-Site Request Forgery)

```typescript
import csurf from 'csurf';
import cookieParser from 'cookie-parser';

app.use(cookieParser());
app.use(csurf({ cookie: true }));

app.post('/api/form', csrfProtection, (req, res) => {
  // Token validated automatically
});
```

### Path Traversal

```typescript
import path from 'path';

// ✅ Correct: Validate paths
function getSafePath(filePath: string): string {
  const normalized = path.normalize(filePath);

  // Ensure path doesn't escape base directory
  if (normalized.includes('..')) {
    throw new Error('Invalid path');
  }

  return path.join('/safe/base', normalized);
}

// ❌ Wrong: Direct use
const fileContent = fs.readFileSync(userInput.path);
```

---

## Security Checklist

Before deploying:

- [ ] All inputs validated and sanitized
- [ ] SQL queries parameterized
- [ ] Passwords hashed with bcrypt
- [ ] JWT tokens short-lived (15min)
- [ ] HTTPS enforced in production
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Secrets not in git
- [ ] Logging doesn't expose sensitive data
- [ ] Error messages don't leak info
- [ ] Dependencies scanned for vulnerabilities
- [ ] Session management secure
- [ ] File upload validation
- [ ] API authentication on all endpoints

---

## Quick Reference

### Common Security Libraries

| Library | Purpose |
|---------|---------|
| `bcrypt` | Password hashing |
| `jsonwebtoken` | JWT handling |
| `helmet` | Security headers |
| `express-rate-limit` | Rate limiting |
| `csurf` | CSRF protection |
| `dompurify` | XSS prevention |
| `zod` | Input validation |
| `joi` | Schema validation |

### Security Headers

```
Strict-Transport-Security: max-age=31536000
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
```

---

## Resources

📚 **Detailed Guides:**
- [owasp-top10.md](resources/owasp-top10.md) - OWASP vulnerability prevention
- [authentication-patterns.md](resources/authentication-patterns.md) - Auth implementation patterns

---

## Related Skills

- **error-tracking** - Log security events
- **devops-guidelines** - Secrets management
- **backend-dev-guidelines** - Secure API design
