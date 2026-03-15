---
name: performance-optimization
description: Performance optimization guidelines including code optimization, database query optimization, caching strategies, lazy loading, code splitting, bundle optimization, and performance monitoring. Use when optimizing application performance, reducing latency, improving load times, or scaling applications. Covers frontend performance, backend performance, database optimization, caching, and profiling tools.
---

# Performance Optimization

## Purpose
Comprehensive guide for optimizing application performance across frontend, backend, and database layers.

## When to Use This Skill
- Optimizing slow endpoints
- Improving page load times
- Reducing bundle sizes
- Implementing caching strategies
- Database query optimization
- Memory leak debugging
- Profiling and monitoring performance

---

## Core Principles

1. **Measure First** - Profile before optimizing
2. **Optimize the Critical Path** - Focus on user-facing performance
3. **Cache Everything** - Avoid redundant work
4. **Lazy Load** - Defer non-critical resources
5. **Monitor Continuously** - Performance regression detection

---

## Frontend Performance

### Code Splitting

```typescript
// ✅ Correct: Lazy loading routes
import { lazy } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### Bundle Optimization

```javascript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui-library': ['@mui/material', 'icons-material']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
});
```

### Image Optimization

```typescript
// ✅ Correct: Responsive images
<img
  srcSet={`
    /images/small.webp 480w,
    /images/medium.webp 800w,
    /images/large.webp 1200w
  `}
  sizes="(max-width: 600px) 480px, 800px"
  loading="lazy"
  alt="Product"
/>

// ✅ Use WebP format with fallback
<picture>
  <source srcSet="/images/product.webp" type="image/webp" />
  <source srcSet="/images/product.jpg" type="image/jpeg" />
  <img src="/images/product.jpg" alt="Product" loading="lazy" />
</picture>
```

---

## Backend Performance

### Database Optimization

**N+1 Query Prevention:**
```typescript
// ❌ Wrong: N+1 queries
const users = await prisma.user.findMany();
for (const user of users) {
  user.posts = await prisma.post.findMany({
    where: { userId: user.id }
  });
}
// Results in 1 + N queries

// ✅ Correct: Single query with include
const users = await prisma.user.findMany({
  include: {
    posts: true
  }
});
// Results in 1 query
```

**Query Optimization:**
```typescript
// ✅ Correct: Select only needed fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    email: true
  }
});

// ✅ Correct: Pagination
const users = await prisma.user.findMany({
  take: 20,
  skip: (page - 1) * 20,
  orderBy: { createdAt: 'desc' }
});
```

**Indexing:**
```typescript
// Add indexes for frequently queried fields
await prisma.$executeRaw`
  CREATE INDEX idx_user_email ON users(email);
  CREATE INDEX idx_user_created_at ON users(created_at DESC);
`;
```

### Caching Strategies

**Redis Caching:**
```typescript
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

async function getUser(id: string) {
  // Check cache first
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  // Fetch from database
  const user = await prisma.user.findUnique({ where: { id } });

  // Cache for 5 minutes
  await redis.setex(`user:${id}`, 300, JSON.stringify(user));

  return user;
}
```

**HTTP Caching:**
```typescript
// Cache API responses
app.get('/api/data', async (req, res) => {
  res.set('Cache-Control', 'public, max-age=300'); // 5 minutes
  res.json(data);
});
```

---

## Performance Monitoring

### Web Vitals

Track Core Web Vitals:

```typescript
// LCP (Largest Contentful Paint) - < 2.5s
// FID (First Input Delay) - < 100ms
// CLS (Cumulative Layout Shift) - < 0.1

// Measure with web-vitals library
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

### Backend Metrics

```typescript
// Response time tracking
app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} ${res.statusCode} ${duration}ms`);
  });

  next();
});
```

---

## Profiling Tools

### Frontend Profiling

```typescript
// Performance API
performance.mark('start-processing');

// ... code ...

performance.mark('end-processing');
performance.measure('processing', 'start', 'end-processing');

const measure = performance.getEntriesByName('processing')[0];
console.log(`Processing took: ${measure.duration}ms`);
```

### Backend Profiling

```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate-0x*.log > profile.txt

# Memory profiling
node --heap-prof app.js
```

---

## Common Performance Issues

### Memory Leaks

```typescript
// ❌ Wrong: Unclosed connections
const connections = [];

function handleRequest(req, res) {
  const conn = createConnection();
  connections.push(conn); // Never removed!
}

// ✅ Correct: Proper cleanup
function handleRequest(req, res) {
  const conn = createConnection();
  res.on('finish', () => {
    conn.close();
  });
}
```

### Event Loop Blocking

```typescript
// ❌ Wrong: Synchronous heavy computation
function processLargeArray(data) {
  const results = data.map(item => {
    return heavyComputation(item); // Blocks!
  });
  return results;
}

// ✅ Correct: Async processing
async function processLargeArray(data) {
  const chunks = chunk(data, 1000);
  const results = [];

  for (const chunk of chunks) {
    const chunkResults = await Promise.all(
      chunk.map(item => heavyComputationAsync(item))
    );
    results.push(...chunkResults);

    // Let other events process
    await new Promise(resolve => setImmediate(resolve));
  }

  return results;
}
```

---

## Performance Checklist

### Frontend
- [ ] Code splitting implemented
- [ ] Images optimized (WebP, lazy loading)
- [ ] Bundle size analyzed and optimized
- [ ] Critical CSS inlined
- [ ] Fonts optimized (subset, woff2)
- [ ] Third-party scripts deferred
- [ ] Core Web Vitals measured

### Backend
- [ ] Database queries optimized
- [ ] Indexes added for slow queries
- [ ] Caching implemented (Redis, HTTP)
- [ ] N+1 queries eliminated
- [ ] Response times monitored
- [ ] Memory usage tracked
- [ ] Connection pooling configured

---

## Quick Reference

### Performance Budgets

| Metric | Target |
|--------|--------|
| Initial Load | < 3s |
| Time to Interactive | < 5s |
| First Contentful Paint | < 2s |
| Largest Contentful Paint | < 2.5s |
| API Response (p95) | < 500ms |
| Database Query (p95) | < 100ms |

### Optimization Tools

- **Frontend:** Lighthouse, WebPageTest, Bundle Analyzer
- **Backend:** New Relic, DataDog, Sentry Performance
- **Database:** EXPLAIN, slow query log

---

## Resources

📚 **Detailed Guides:**
- [frontend-performance.md](resources/frontend-performance.md) - Frontend optimization techniques
- [backend-performance.md](resources/backend-performance.md) - Backend scaling and optimization

---

## Related Skills

- **devops-guidelines** - Monitoring infrastructure
- **backend-dev-guidelines** - Efficient API design
- **frontend-dev-guidelines** - React performance
