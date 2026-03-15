---
name: devops-guidelines
description: DevOps and infrastructure guidelines for CI/CD pipelines, Docker containers, GitHub Actions, deployment strategies, infrastructure as code, monitoring, and operations. Use when creating deployment workflows, Dockerfiles, CI/CD configurations, or managing infrastructure. Covers Docker, GitHub Actions, CI/CD, deployment, monitoring, logging, secrets management, and infrastructure automation.
---

# DevOps Guidelines

## Purpose
Comprehensive guide for DevOps best practices including CI/CD, Docker, GitHub Actions, deployment strategies, and infrastructure automation.

## When to Use This Skill
- Creating or modifying CI/CD pipelines
- Writing Dockerfiles or docker-compose files
- Setting up GitHub Actions workflows
- Configuring deployment pipelines
- Implementing monitoring and logging
- Managing secrets and environment variables
- Setting up infrastructure as code

---

## Core Principles

1. **Infrastructure as Code** - All infrastructure defined in code
2. **Immutable Infrastructure** - Replace, don't modify
3. **Automation First** - Automate repetitive tasks
4. **Security Integrated** - Build security into the pipeline
5. **Observability** - Monitor everything that matters

---

## Docker Best Practices

### Dockerfile Guidelines

**Use Multi-Stage Builds:**
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm ci --only=production
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

**Best Practices:**
- Use specific version tags (not `latest`)
- Use `.dockerignore` to exclude unnecessary files
- Minimize layers by combining RUN commands
- Run as non-root user when possible
- Use Alpine images for smaller size

### docker-compose Guidelines

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      - db
      - redis
    ports:
      - "3000:3000"
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres_data:
```

---

## GitHub Actions Workflows

### CI/CD Pipeline Template

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          # Deployment commands
```

### Workflow Best Practices

**Use Actions from Official Repos:**
- `actions/checkout@v4`
- `actions/setup-node@v4`
- `docker/build-push-action@v5`

**Secret Management:**
```yaml
- name: Deploy
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_KEY }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET }}
  run: deploy.sh
```

**Environment-Specific Config:**
```yaml
environments:
  production:
    url: https://app.example.com
  staging:
    url: https://staging.example.com
```

---

## Deployment Strategies

### Blue-Green Deployment

**Concept:** Maintain two identical environments (blue, green)
- Switch traffic instantly
- Zero-downtime deployments
- Easy rollback

**Implementation:**
```yaml
# docker-compose.yml with blue/green
services:
  app-blue:
    image: myapp:v1
    ports:
      - "3000:3000"

  app-green:
    image: myapp:v2
    ports:
      - "3001:3000"
```

### Rolling Deployment

**Concept:** Replace instances gradually
- Deploy to subset of servers
- Monitor for issues
- Continue if healthy

### Canary Deployment

**Concept:** Deploy to small subset of users
- Route 5-10% traffic to new version
- Monitor metrics
- Gradually increase traffic

---

## Monitoring & Logging

### Application Monitoring

**Key Metrics:**
- Request rate and latency
- Error rate
- CPU and memory usage
- Database query performance
- Custom business metrics

**Tools:**
- Prometheus - Metrics collection
- Grafana - Visualization
- Sentry - Error tracking
- DataDog - APM

### Logging Best Practices

**Structured Logging:**
```typescript
logger.info('User created', {
  userId: user.id,
  email: user.email,
  timestamp: new Date().toISOString()
});
```

**Log Levels:**
- ERROR - Application errors
- WARN - Warning conditions
- INFO - Informational messages
- DEBUG - Detailed debugging

**Centralized Logging:**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- CloudWatch Logs
- Google Cloud Logging

---

## Secrets Management

### Best Practices

1. **Never commit secrets to git**
2. **Use environment variables** in production
3. **Rotate secrets regularly**
4. **Use secret management tools**

### GitHub Secrets

```yaml
# Setting secrets in GitHub
# Settings → Secrets and variables → Actions

env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}
```

### Environment Variables

```bash
# .env (gitignored)
DATABASE_URL=postgres://localhost:5432/app
JWT_SECRET=your-secret-here

# Load in Node.js
require('dotenv').config();
```

### Secret Management Tools

- **HashiCorp Vault** - Enterprise secrets
- **AWS Secrets Manager** - AWS secrets
- **Google Secret Manager** - GCP secrets
- **Docker Secrets** - Swarm/Kubernetes secrets

---

## Infrastructure as Code

### Docker Compose

**Use for:**
- Local development
- Simple deployments
- Multi-container applications

### Terraform

**Use for:**
- Cloud infrastructure
- Multi-cloud deployments
- Complex infrastructure

**Example:**
```hcl
resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = "t3.micro"

  tags = {
    Name = "app-server"
    Environment = var.environment
  }
}
```

### Kubernetes

**Use for:**
- Large-scale deployments
- Microservices
- Auto-scaling

**Example:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 3000
```

---

## CI/CD Best Practices

### Pipeline Stages

1. **Build** - Compile and build artifacts
2. **Test** - Run unit and integration tests
3. **Security Scan** - Check for vulnerabilities
4. **Deploy** - Deploy to environment
5. **Verify** - Smoke tests, health checks

### Branching Strategy

**Git Flow:**
- `main` - Production code
- `develop` - Integration branch
- `feature/*` - Feature branches
- `release/*` - Release preparation
- `hotfix/*` - Emergency fixes

**Trunk-Based Development:**
- Single main branch
- Feature flags
- Continuous deployment

---

## Health Checks

### Application Health

```typescript
// Health check endpoint
app.get('/health', (req, res) => {
  const health = {
    uptime: process.uptime(),
    timestamp: Date.now(),
    status: 'healthy'
  };

  // Check dependencies
  try {
    await db.query('SELECT 1');
    health.database = 'healthy';
  } catch (error) {
    health.database = 'unhealthy';
    health.status = 'degraded';
  }

  res.status(health.status === 'healthy' ? 200 : 503).json(health);
});
```

### Docker Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1
```

---

## Backup & Disaster Recovery

### Database Backups

```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DATABASE_URL="postgres://user:pass@host:5432/db"

pg_dump $DATABASE_URL > "$BACKUP_DIR/backup_$DATE.sql"

# Keep last 7 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

### Backup Strategy

- **Daily backups** - Last 7 days
- **Weekly backups** - Last 4 weeks
- **Monthly backups** - Last 12 months
- **Off-site storage** - Cloud storage
- **Regular restore tests** - Verify backups work

---

## Common Mistakes to Avoid

❌ Using `latest` tag in Docker
❌ Committing secrets to git
❌ Hardcoding environment values
❌ No rollback strategy
❌ Skipping health checks
❌ Insufficient monitoring
❌ No backup strategy
❌ Manual deployment process

---

## Quick Reference

### Docker Commands

```bash
# Build image
docker build -t myapp:latest .

# Run container
docker run -p 3000:3000 myapp:latest

# View logs
docker logs -f container_name

# Execute command in container
docker exec -it container_name sh

# Clean up
docker system prune -a
```

### Docker Compose Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Restart service
docker-compose restart service_name

# Stop all
docker-compose down
```

### Deployment Checklist

- [ ] Tests passing
- [ ] No uncommitted changes
- [ ] Environment variables configured
- [ ] Secrets in place
- [ ] Backup created
- [ ] Rollback plan ready
- [ ] Health checks configured
- [ ] Monitoring enabled

---

## Resources

📚 **Detailed Guides:**
- [docker-patterns.md](resources/docker-patterns.md) - Advanced Docker patterns
- [cicd-workflows.md](resources/cicd-workflows.md) - CI/CD pipeline examples
- [infrastructure.md](resources/infrastructure.md) - Infrastructure as code patterns

---

## Related Skills

- **security-guidelines** - Security best practices
- **performance-optimization** - Performance tuning
- **testing-guidelines** - Test automation
