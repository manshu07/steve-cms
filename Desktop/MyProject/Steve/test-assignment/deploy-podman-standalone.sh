#!/bin/bash
###############################################################################
# Podman Standalone Deployment Script (No podman-compose required)
# Usage: ./deploy-podman-standalone.sh [up|down|logs|status]
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PROJECT_NAME="beyondcode"
NETWORK_NAME="${PROJECT_NAME}-network"
POSTGRES_CONTAINER="${PROJECT_NAME}-db"
REDIS_CONTAINER="${PROJECT_NAME}-redis"
BACKEND_CONTAINER="${PROJECT_NAME}-backend"
FRONTEND_CONTAINER="${PROJECT_NAME}-frontend"
NGINX_CONTAINER="${PROJECT_NAME}-nginx"

# Volumes
POSTGRES_VOLUME="${PROJECT_NAME}-postgres-data"
REDIS_VOLUME="${PROJECT_NAME}-redis-data"
MEDIA_VOLUME="${PROJECT_NAME}-media-files"
STATIC_VOLUME="${PROJECT_NAME}-static-files"

# Load environment
if [ -f .env.production ]; then
    export $(cat .env.production | grep -v '^#' | xargs)
else
    echo "Error: .env.production not found"
    exit 1
fi

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Create network
create_network() {
    if ! podman network exists ${NETWORK_NAME}; then
        log_info "Creating network: ${NETWORK_NAME}"
        podman network create ${NETWORK_NAME}
    fi
}

# Create volumes
create_volumes() {
    log_info "Creating volumes..."
    podman volume create ${POSTGRES_VOLUME} 2>/dev/null || true
    podman volume create ${REDIS_VOLUME} 2>/dev/null || true
    podman volume create ${MEDIA_VOLUME} 2>/dev/null || true
    podman volume create ${STATIC_VOLUME} 2>/dev/null || true
    log_success "Volumes created"
}

# Start PostgreSQL
start_postgres() {
    log_info "Starting PostgreSQL..."

    podman run -d \
        --name ${POSTGRES_CONTAINER} \
        --network ${NETWORK_NAME} \
        -e POSTGRES_DB=${DB_NAME:-beyondcode} \
        -e POSTGRES_USER=${DB_USER:-postgres} \
        -e POSTGRES_PASSWORD=${DB_PASSWORD:-changeme} \
        -v ${POSTGRES_VOLUME}:/var/lib/postgresql/data:Z \
        -p 5432:5432 \
        --health-cmd "pg_isready -U ${DB_USER:-postgres}" \
        --health-interval 10s \
        --health-timeout 5s \
        --health-retries 5 \
        docker.io/postgres:15-alpine

    log_success "PostgreSQL started"
}

# Start Redis
start_redis() {
    log_info "Starting Redis..."

    podman run -d \
        --name ${REDIS_CONTAINER} \
        --network ${NETWORK_NAME} \
        -v ${REDIS_VOLUME}:/data:Z \
        -p 6379:6379 \
        --health-cmd "redis-cli ping" \
        --health-interval 10s \
        --health-timeout 5s \
        --health-retries 5 \
        docker.io/redis:7-alpine \
        redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru

    log_success "Redis started"
}

# Start Backend
start_backend() {
    log_info "Starting Backend..."

    # Build image if not exists
    if ! podman image exists ${PROJECT_NAME}-backend:latest; then
        log_info "Building backend image..."
        podman build -f Containerfile.backend -t ${PROJECT_NAME}-backend:latest .
    fi

    podman run -d \
        --name ${BACKEND_CONTAINER} \
        --network ${NETWORK_NAME} \
        -e DEBUG=${DEBUG:-False} \
        -e SECRET_KEY=${SECRET_KEY} \
        -e DATABASE_URL=postgresql://${DB_USER:-postgres}:${DB_PASSWORD:-changeme}@${POSTGRES_CONTAINER}:5432/${DB_NAME:-beyondcode} \
        -e REDIS_URL=redis://${REDIS_CONTAINER}:6379/0 \
        -e ALLOWED_HOSTS=${ALLOWED_HOSTS:-localhost,127.0.0.1} \
        -e CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS:-http://localhost:3000} \
        -v ${MEDIA_VOLUME}:/app/media:Z \
        -v ${STATIC_VOLUME}:/app/static:Z \
        -p 8000:8000 \
        --health-cmd "curl -f http://localhost:8000/api/health/ || exit 1" \
        --health-interval 30s \
        --health-timeout 10s \
        --health-retries 3 \
        --restart unless-stopped \
        localhost/${PROJECT_NAME}-backend:latest

    log_success "Backend started"
}

# Start Frontend
start_frontend() {
    log_info "Starting Frontend..."

    # Build image if not exists
    if ! podman image exists ${PROJECT_NAME}-frontend:latest; then
        log_info "Building frontend image..."
        podman build -f Containerfile.frontend -t ${PROJECT_NAME}-frontend:latest .
    fi

    podman run -d \
        --name ${FRONTEND_CONTAINER} \
        --network ${NETWORK_NAME} \
        -e VITE_API_URL=${VITE_API_URL:-http://localhost:8000} \
        -e NODE_ENV=production \
        -p 3000:3000 \
        --health-cmd "curl -f http://localhost:3000/ || exit 1" \
        --health-interval 30s \
        --health-timeout 10s \
        --health-retries 3 \
        --restart unless-stopped \
        localhost/${PROJECT_NAME}-frontend:latest

    log_success "Frontend started"
}

# Setup database
setup_database() {
    log_info "Waiting for database to be ready..."
    sleep 10

    log_info "Running migrations..."
    podman exec ${BACKEND_CONTAINER} python manage.py migrate --noinput

    log_info "Seeding component registry..."
    podman exec ${BACKEND_CONTAINER} python manage.py seed_component_registry

    log_info "Creating superuser..."
    podman exec ${BACKEND_CONTAINER} python manage.py shell --command "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@beyondcode.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

    log_success "Database setup complete"
}

# Start all services
start_all() {
    log_info "Starting all services..."

    create_network
    create_volumes

    # Start database and cache first
    start_postgres
    start_redis

    # Wait for databases to be healthy
    log_info "Waiting for databases to be healthy..."
    sleep 15

    # Start application services
    start_backend
    sleep 10

    start_frontend

    # Setup database
    setup_database

    log_success "All services started successfully"

    echo ""
    echo "============================================"
    echo "  DEPLOYMENT SUCCESSFUL"
    echo "============================================"
    echo ""
    echo "Access your application at:"
    echo "  Frontend:  http://localhost:3000"
    echo "  Backend:   http://localhost:8000"
    echo "  API:       http://localhost:8000/api/"
    echo "  Admin:     http://localhost:8000/admin/"
    echo ""
    echo "Default superuser: admin / admin123"
    echo "============================================"
}

# Stop all services
stop_all() {
    log_info "Stopping all services..."

    podman stop ${NGINX_CONTAINER} 2>/dev/null || true
    podman stop ${FRONTEND_CONTAINER} 2>/dev/null || true
    podman stop ${BACKEND_CONTAINER} 2>/dev/null || true
    podman stop ${REDIS_CONTAINER} 2>/dev/null || true
    podman stop ${POSTGRES_CONTAINER} 2>/dev/null || true

    podman rm ${NGINX_CONTAINER} 2>/dev/null || true
    podman rm ${FRONTEND_CONTAINER} 2>/dev/null || true
    podman rm ${BACKEND_CONTAINER} 2>/dev/null || true
    podman rm ${REDIS_CONTAINER} 2>/dev/null || true
    podman rm ${POSTGRES_CONTAINER} 2>/dev/null || true

    log_success "All services stopped"
}

# Show logs
show_logs() {
    local container=${2:-}
    if [ -n "$container" ]; then
        podman logs -f $container
    else
        log_info "Showing logs from all containers..."
        podman logs -f ${BACKEND_CONTAINER} ${FRONTEND_CONTAINER} ${POSTGRES_CONTAINER} 2>/dev/null || true
    fi
}

# Show status
show_status() {
    log_info "Container status:"
    podman ps --filter "name=${PROJECT_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

# Main command handler
case "${1:-start}" in
    start|up)
        start_all
        ;;
    stop|down)
        stop_all
        ;;
    restart)
        stop_all
        sleep 2
        start_all
        ;;
    logs)
        show_logs "$@"
        ;;
    status)
        show_status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|logs|status}"
        echo ""
        echo "Commands:"
        echo "  start, up    - Start all services"
        echo "  stop, down   - Stop all services"
        echo "  restart      - Restart all services"
        echo "  logs [name]  - Show logs (optionally for specific container)"
        echo "  status       - Show container status"
        exit 1
        ;;
esac
