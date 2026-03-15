# Advanced Docker Patterns

Complete guide to Docker best practices, patterns, and advanced configurations.

---

## Table of Contents

1. [Dockerfile Guidelines](#dockerfile-guidelines)
2. [Multi-Stage Builds](#multi-stage-builds)
3. [Docker Compose Patterns](#docker-compose-patterns)
4. [Docker Health Checks](#docker-health-checks)
5. [Docker Optimization](#docker-optimization)
6. [Docker Security](#docker-security)
7. [Docker Networking](#docker-networking)
8. [Docker Volumes](#docker-volumes)
9. [Command Reference](#command-reference)

---

## Dockerfile Guidelines

### Essential Best Practices

**Use Specific Version Tags:**
```dockerfile
# Bad - uses latest
FROM node:latest

# Good - specific version
FROM node:20-alpine
```

**Minimize Layers:**
```dockerfile
# Bad - multiple RUN commands
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git

# Good - combined RUN
RUN apt-get update && \
    apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/*
```

**Use .dockerignore:**
```
# .dockerignore
node_modules
npm-debug.log
.git
.env
*.md
tests/
coverage/
```

**Run as Non-Root User:**
```dockerfile
FROM node:20-alpine

# Create app user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set working directory
WORKDIR /app

# Copy files
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Change ownership
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

EXPOSE 3000
CMD ["node", "server.js"]
```

---

## Multi-Stage Builds

### Node.js Application

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy and build source
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production
WORKDIR /app

# Copy only production dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy built artifacts from builder
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/public ./public

# Set environment
ENV NODE_ENV=production

EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### Go Application

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app

# Install dependencies
COPY go.* ./
RUN go mod download

# Copy source and build
COPY . .
RUN CGO_ENABLED=0 go build -o main .

# Runtime stage (minimal)
FROM alpine:latest
WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/main .

EXPOSE 8080
CMD ["./main"]
```

### Python Application

```dockerfile
# Builder stage
FROM python:3.12-slim AS builder
WORKDIR /app

# Install build dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000
CMD ["python", "app.py"]
```

### React Application

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage with nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Docker Compose Patterns

### Multi-Service Application

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
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    ports:
      - "3000:3000"
    restart: unless-stopped
    networks:
      - app-network
    volumes:
      - app-data:/app/data

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:
  app-data:

networks:
  app-network:
    driver: bridge
```

### Development Environment

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port
    command: npm run dev

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: app_dev
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_dev:/var/lib/postgresql/data

volumes:
  postgres_dev:
```

### Production Deployment

```yaml
version: '3.8'

services:
  app:
    image: myapp:latest
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    secrets:
      - db_password
      - jwt_secret
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        max_attempts: 3
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

secrets:
  db_password:
    external: true
  jwt_secret:
    external: true
```

---

## Docker Health Checks

### Application Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

### Database Health Check

```dockerfile
# PostgreSQL
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pg_isready -U user -d app || exit 1

# MySQL
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD mysqladmin ping -h localhost -u user -p${MYSQL_ROOT_PASSWORD} || exit 1

# MongoDB
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD mongo --eval "db.adminCommand('ping')" || exit 1

# Redis
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD redis-cli ping || exit 1
```

### Custom Health Check Script

```dockerfile
FROM node:20-alpine

# Create health check script
RUN echo '#!/bin/sh' > /healthcheck.sh && \
    echo 'curl -f http://localhost:3000/health || exit 1' >> /healthcheck.sh && \
    chmod +x /healthcheck.sh

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD /healthcheck.sh
```

---

## Docker Optimization

### Image Size Reduction

```dockerfile
# Before optimization: 1.2GB
FROM node:20
COPY . .
RUN npm install
RUN npm run build

# After optimization: 180MB
FROM node:20-alpine AS builder
COPY package*.json ./
RUN npm ci --production
COPY . .
RUN npm run build

FROM node:20-alpine
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
```

### Layer Caching

```dockerfile
# Good - caches dependencies separately
FROM node:20-alpine
WORKDIR /app

# Copy dependency files
COPY package*.json ./
# Install dependencies (cached if package.json unchanged)
RUN npm ci --only=production

# Copy source code
COPY . .
# Build (only runs if source changed)
RUN npm run build

# Bad - no caching benefit
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm ci --only=production
RUN npm run build
```

### BuildKit Features

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build with cache mount
docker build \
  --mount=type=cache,target=/root/.npm \
  --mount=type=bind,source=.,target=/app \
  -t myapp .

# Use multi-platform builds
docker buildx build --platform linux/amd64,linux/arm64 -t myapp .
```

---

## Docker Security

### Scan Images for Vulnerabilities

```bash
# Trivy scanner
trivy image myapp:latest

# Docker scout
docker scout quickview myapp:latest
docker scout cves myapp:latest
```

### Run as Non-Root

```dockerfile
FROM node:20-alpine

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S -u 1001 -G appuser appuser

# Set permissions
WORKDIR /app
COPY --chown=appuser:appuser . .

USER appuser
CMD ["node", "server.js"]
```

### Use Read-Only Root Filesystem

```yaml
# docker-compose.yml
services:
  app:
    image: myapp:latest
    read_only: true
    tmpfs:
      - /tmp
      - /app/cache
```

---

## Docker Networking

### Bridge Network

```yaml
version: '3.8'

services:
  web:
    image: nginx
    networks:
      - frontend

  api:
    image: myapi
    networks:
      - frontend
      - backend

  db:
    image: postgres
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true  # No external access
```

### Custom Network

```bash
# Create network
docker network create --driver bridge my-network

# Connect container
docker network connect my-network my-container

# Disconnect container
docker network disconnect my-network my-container
```

---

## Docker Volumes

### Named Volumes

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    image: myapp
    volumes:
      - app_data:/app/data

volumes:
  postgres_data:
  app_data:
```

### Bind Mounts

```yaml
version: '3.8'

services:
  app:
    image: myapp
    volumes:
      - ./src:/app/src:ro  # Read-only
      - ./data:/app/data:rw  # Read-write
```

### Volume Drivers

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
    driver: local
    driver_opts:
      type: nfs
      o: addr=192.168.1.1,rw
      device: ":/path/to/nfs/share"
```

---

## Command Reference

### Docker Commands

```bash
# Build image
docker build -t myapp:latest .
docker build -t myapp:v1.0 -f Dockerfile.prod .

# Run container
docker run -d -p 3000:3000 --name myapp myapp:latest
docker run -d -p 3000:3000 -e NODE_ENV=production myapp:latest

# Run with environment file
docker run -d --env-file .env myapp:latest

# Run with volume mount
docker run -d -v /host/path:/container/path myapp:latest

# List containers
docker ps
docker ps -a  # Include stopped

# View logs
docker logs myapp
docker logs -f myapp  # Follow logs
docker logs --tail 100 myapp

# Execute command in container
docker exec -it myapp sh
docker exec myapp npm test

# Stop and start
docker stop myapp
docker start myapp
docker restart myapp

# Remove container
docker rm myapp
docker rm -f myapp  # Force remove running container

# Remove image
docker rmi myapp:latest
docker rmi -f $(docker images -q)  # Remove all images

# Clean up
docker system prune -a  # Remove all unused data
docker system prune -a --volumes  # Include volumes
```

### Docker Compose Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f app

# Restart service
docker-compose restart app

# Rebuild and restart
docker-compose up -d --build

# Scale services
docker-compose up -d --scale app=3

# Run one-off command
docker-compose run app npm migrate
docker-compose run --rm app npm test

# Execute in running service
docker-compose exec app sh

# Show running containers
docker-compose ps

# Show resource usage
docker-compose top
```

### Docker Inspect Commands

```bash
# Inspect container
docker inspect myapp

# Get container IP
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' myapp

# Get container ports
docker inspect --format='{{range $p, $conf := .NetworkSettings.Ports}}{{$p}} -> {{(index $conf 0).HostPort}}{{"\n"}}{{end}}' myapp

# Get image layers
docker history myapp:latest

# Get container stats
docker stats myapp
docker stats --no-stream  # Single snapshot
```

---

## Common Patterns

### Init Container Pattern

```dockerfile
# Use dumb-init to handle signals properly
FROM node:20-alpine

RUN apk add --no-cache dumb-init

ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]
```

### Wait-for-it Pattern

```dockerfile
FROM node:20-alpine

# Install wait-for-it script
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -O /usr/local/bin/wait-for-it && \
    chmod +x /usr/local/bin/wait-for-it

# Use in entrypoint
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
```

```bash
# entrypoint.sh
#!/bin/sh
wait-for-it db:5432 -- timeout=30 -- strict -- \
  wait-for-it redis:6379 -- timeout=30 -- strict -- \
  exec "$@"
```

---

## Best Practices Summary

✅ **Always Use:**
- Specific version tags (not `latest`)
- Multi-stage builds
- `.dockerignore` file
- Non-root user
- Health checks
- Environment variables for secrets
- Minimal base images (Alpine)

❌ **Never:**
- Commit secrets to images
- Run as root user
- Use `latest` tag in production
- Skip health checks
- Ignore image size
- Hardcode configuration

---

## Related Resources

- [CI/CD Workflows](cicd-workflows.md) - Docker in CI/CD pipelines
- [Infrastructure](infrastructure.md) - Container orchestration
