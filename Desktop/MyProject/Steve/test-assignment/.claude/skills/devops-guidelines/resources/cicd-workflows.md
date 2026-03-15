# CI/CD Workflow Examples

Complete examples of CI/CD pipelines for different scenarios and platforms.

## Table of Contents
- [GitHub Actions Workflows](#github-actions-workflows)
- [Deployment Strategies](#deployment-strategies)
- [Environment Management](#environment-management)
- [Monitoring & Notifications](#monitoring--notifications)

---

## GitHub Actions Workflows

### Node.js Application Pipeline

Complete CI/CD for Node.js applications:

```yaml
name: Node.js CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Job 1: Lint and Test
  lint-test:
    name: Lint & Test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run type check
        run: npm run type-check

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
          flags: unittests
          name: codecov-umbrella

      - name: Upload coverage artifacts
        uses: actions/upload-artifact@v3
        with:
          name: coverage-report
          path: coverage/

  # Job 2: Security Scan
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: lint-test

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run npm audit
        run: npm audit --audit-level=moderate
        continue-on-error: true

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        continue-on-error: true
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  # Job 3: Build Docker Image
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [lint-test, security]
    if: github.event_name == 'push'

    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push Docker image
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Image digest
        run: echo ${{ steps.build.outputs.digest }}

  # Job 4: Deploy to Staging
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster myapp-staging \
            --service myapp-service \
            --force-new-deployment

      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster myapp-staging \
            --services myapp-service

      - name: Health check
        run: |
          response=$(curl -s -o /dev/null -w "%{http_code}" https://staging.example.com/health)
          if [ $response -ne 200 ]; then
            echo "Health check failed"
            exit 1
          fi

  # Job 5: Deploy to Production
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://app.example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Create GitHub Release
        id: release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: v${{ github.run_number }}
          release_name: Release v${{ github.run_number }}
          draft: false
          prerelease: false

      - name: Deploy to production
        run: |
          # Deployment commands here
          echo "Deploying to production..."

      - name: Notify Slack
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            Production deployment successful!
            Release: ${{ steps.release.outputs.html_url }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Monorepo Pipeline

For projects with multiple packages/services:

```yaml
name: Monorepo CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  # Detect what changed
  detect-changes:
    name: Detect Changes
    runs-on: ubuntu-latest
    outputs:
      backend: ${{ steps.changes.outputs.backend }}
      frontend: ${{ steps.changes.outputs.frontend }}
      shared: ${{ steps.changes.outputs.shared }}

    steps:
      - uses: actions/checkout@v4

      - uses: dorny/paths-filter@v2
        id: changes
        with:
          filters: |
            backend:
              - 'packages/backend/**'
            frontend:
              - 'packages/frontend/**'
            shared:
              - 'packages/shared/**'

  # Test affected packages
  test-backend:
    name: Test Backend
    needs: detect-changes
    if: needs.detect-changes.outputs.backend == 'true'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          cd packages/backend
          npm ci

      - name: Run tests
        run: |
          cd packages/backend
          npm test

  test-frontend:
    name: Test Frontend
    needs: detect-changes
    if: needs.detect-changes.outputs.frontend == 'true'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          cd packages/frontend
          npm ci

      - name: Run tests
        run: |
          cd packages/frontend
          npm test

      - name: Build
        run: |
          cd packages/frontend
          npm run build
```

---

## Deployment Strategies

### Blue-Green Deployment

Complete blue-green deployment setup:

```yaml
name: Blue-Green Deployment

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build new version (Green)
        run: |
          docker-compose -f docker-compose.green.yml build

      - name: Start Green environment
        run: |
          docker-compose -f docker-compose.green.yml up -d

      - name: Run smoke tests on Green
        run: |
          npm run test:smoke -- --env=green

      - name: Switch traffic to Green
        run: |
          # Update load balancer
          aws elbv2 modify-listener \
            --listener-arn ${{ secrets.LISTENER_ARN }} \
            --default-actions \
              Type=forward,ForwardConfig='{"TargetGroups":[{"TargetGroupArn":"${{ secrets.GREEN_TG_ARN }}","Weight":100}]}'

      - name: Wait and monitor
        run: |
          # Monitor for 5 minutes
          sleep 300

          # Check error rates
          npm run check:errors

      - name: Stop Blue environment
        run: |
          docker-compose -f docker-compose.blue.yml down

      - name: Rollback on failure
        if: failure()
        run: |
          # Switch traffic back to Blue
          aws elbv2 modify-listener \
            --listener-arn ${{ secrets.LISTENER_ARN }} \
            --default-actions \
              Type=forward,ForwardConfig='{"TargetGroups":[{"TargetGroupArn":"${{ secrets.BLUE_TG_ARN }}","Weight":100}]}'

          # Stop Green
          docker-compose -f docker-compose.green.yml down
```

### Canary Deployment

Gradual canary deployment:

```yaml
name: Canary Deployment

on:
  push:
    branches: [main]

jobs:
  canary:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy canary (5% traffic)
        run: |
          # Deploy new version as canary
          kubectl apply -f k8s/canary-deployment.yml

          # Route 5% traffic to canary
          kubectl apply -f k8s/canary-service.yml

      - name: Monitor canary (5 minutes)
        run: |
          for i in {1..30}; do
            # Check error rate
            error_rate=$(npm run get:error-rate)

            if (( $(echo "$error_rate > 1.0" | bc -l) )); then
              echo "Error rate too high: $error_rate"
              exit 1
            fi

            sleep 10
          done

      - name: Increase canary to 25%
        run: |
          kubectl patch service canary-service -p '{"spec":{"selector":{"version":"canary"}}}'

      - name: Monitor canary (10 minutes)
        run: sleep 600

      - name: Full rollout
        run: |
          # Update main deployment
          kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}

          # Remove canary
          kubectl delete deployment canary-deployment
```

---

## Environment Management

### Multi-Environment Configuration

```yaml
name: Multi-Environment Deploy

on:
  push:
    branches:
      - main
      - develop
      - 'release/**'

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Determine environment
        id: env
        run: |
          if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
            echo "environment=production" >> $GITHUB_OUTPUT
            echo "url=https://app.example.com" >> $GITHUB_OUTPUT
          elif [[ "${{ github.ref }}" == "refs/heads/develop" ]]; then
            echo "environment=staging" >> $GITHUB_OUTPUT
            echo "url=https://staging.example.com" >> $GITHUB_OUTPUT
          else
            echo "environment=dev" >> $GITHUB_OUTPUT
            echo "url=https://dev.example.com" >> $GITHUB_OUTPUT
          fi

      - name: Deploy to ${{ steps.env.outputs.environment }}
        env:
          ENVIRONMENT: ${{ steps.env.outputs.environment }}
          DEPLOY_URL: ${{ steps.env.outputs.url }}
        run: |
          # Load environment-specific config
          cp .env.${ENVIRONMENT} .env

          # Deploy
          npm run deploy -- --env=${ENVIRONMENT}

          # Health check
          curl -f ${DEPLOY_URL}/health || exit 1
```

### Environment-Specific Secrets

```yaml
steps:
  - name: Load secrets for environment
    env:
      # Production secrets
      PRODUCTION_DB_URL: ${{ secrets.PRODUCTION_DB_URL }}
      PRODUCTION_API_KEY: ${{ secrets.PRODUCTION_API_KEY }}

      # Staging secrets
      STAGING_DB_URL: ${{ secrets.STAGING_DB_URL }}
      STAGING_API_KEY: ${{ secrets.STAGING_API_KEY }}
    run: |
      if [ "${{ environment }}" == "production" ]; then
        export DATABASE_URL="${PRODUCTION_DB_URL}"
        export API_KEY="${PRODUCTION_API_KEY}"
      else
        export DATABASE_URL="${STAGING_DB_URL}"
        export API_KEY="${STAGING_API_KEY}"
      fi
```

---

## Monitoring & Notifications

### Comprehensive Monitoring

```yaml
name: Deploy with Monitoring

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy application
        run: npm run deploy

      - name: Wait for startup
        run: sleep 60

      - name: Health check
        run: |
          curl -f https://app.example.com/health

      - name: Run synthetic tests
        run: npm run test:synthetic

      - name: Check error rates
        run: |
          ERROR_RATE=$(npm run get:error-rate)
          echo "Error rate: $ERROR_RATE%"

          if (( $(echo "$ERROR_RATE > 0.5" | bc -l) )); then
            echo "Error rate too high, rolling back"
            exit 1
          fi

      - name: Check latency
        run: |
          LATENCY=$(npm run get:latency)
          echo "Latency: ${LATENCY}ms"

          if [ $LATENCY -gt 500 ]; then
            echo "Latency too high, rolling back"
            exit 1
          fi

      - name: Verify monitoring
        run: |
          # Check that metrics are being reported
          curl -f https://metrics.example.com/api/health

      - name: Rollback on failure
        if: failure()
        run: |
          npm run rollback

      - name: Notify on success
        if: success()
        uses: 8398a7/action-slack@v3
        with:
          status: custom
          custom_payload: |
            {
              text: "Deployment successful ✅",
              attachments: [{
                color: "good",
                fields: [
                  { title: "Environment", value: "production", short: true },
                  { title: "Commit", value: "${{ github.sha }}", short: true }
                ]
              }]
            }
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}

      - name: Notify on failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: custom
          custom_payload: |
            {
              text: "Deployment failed ❌",
              attachments: [{
                color: "danger",
                fields: [
                  { title: "Environment", value: "production", short: true },
                  { title: "Commit", value: "${{ github.sha }}", short: true }
                ]
              }]
            }
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Quick Reference

### Workflow Syntax

```yaml
# Basic structure
name: Workflow Name
on:
  push:
    branches: [main]
jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: command
```

### Common Actions

| Action | Purpose |
|--------|---------|
| `actions/checkout@v4` | Checkout repository |
| `actions/setup-node@v4` | Setup Node.js |
| `docker/build-push-action@v5` | Build and push Docker images |
| `aws-actions/configure-aws-credentials@v4` | AWS authentication |
| `codecov/codecov-action@v3` | Upload coverage to Codecov |

### Environment Variables

```yaml
env:
  NODE_ENV: production
  DATABASE_URL: ${{ secrets.DATABASE_URL }}

steps:
  - run: echo ${{ env.DATABASE_URL }}
```

### Conditional Execution

```yaml
# Only on main branch
if: github.ref == 'refs/heads/main'

# Only on success
if: success()

# Only on failure
if: failure()

# Always
if: always()
```

---

## Best Practices

1. **Use specific action versions** (not @latest)
2. **Cache dependencies** for faster builds
3. **Run tests in parallel** when possible
4. **Use artifacts** to share data between jobs
5. **Implement rollback strategy**
6. **Monitor deployments** actively
7. **Notify team** of deployment status
8. **Keep secrets secure** (never in logs)
9. **Use environments** for manual approval
10. **Document workflows** with comments
