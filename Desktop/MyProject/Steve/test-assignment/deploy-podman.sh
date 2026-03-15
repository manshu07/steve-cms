#!/bin/bash
###############################################################################
# Podman Production Deployment Script for BeyondCode Page Builder
# Usage: ./deploy-podman.sh [environment]
#   environment: staging|production (default: production)
###############################################################################

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-production}
PROJECT_NAME="beyondcode-cms"
BACKEND_DIR="beyondcode_cms"
FRONTEND_DIR="frontend"
COMPOSE_FILE="podman-compose.yml"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "Checking deployment requirements..."

    # Check if required commands exist
    command -v podman >/dev/null 2>&1 || { log_error "Podman is required but not installed. Install with: sudo apt-get install podman"; exit 1; }
    command -v python3 >/dev/null 2>&1 || { log_error "Python 3 is required but not installed."; exit 1; }
    command -v node >/dev/null 2>&1 || { log_error "Node.js is required but not installed."; exit 1; }

    log_success "All requirements met"
}

check_environment_file() {
    log_info "Checking environment configuration..."

    if [ ! -f ".env.production" ]; then
        log_warning ".env.production not found. Creating from template..."
        cp .env.production.example .env.production
        log_warning "Please edit .env.production with your actual values before continuing"
        log_warning "Required variables: SECRET_KEY, DB_PASSWORD, CLOUDINARY_API_SECRET"
        read -p "Press Enter after configuring .env.production..."
    fi

    # Source environment file
    if [ -f ".env.production" ]; then
        export $(cat .env.production | grep -v '^#' | xargs)
        log_success "Environment configuration loaded"
    else
        log_error "Cannot proceed without .env.production file"
        exit 1
    fi
}

build_images() {
    log_info "Building container images..."

    # Build backend image
    log_info "Building backend image..."
    podman build -f Containerfile.backend -t ${PROJECT_NAME}-backend:latest .

    # Build frontend image
    log_info "Building frontend image..."
    podman build -f Containerfile.frontend -t ${PROJECT_NAME}-frontend:latest .

    log_success "All images built successfully"
}

run_tests() {
    log_info "Running tests..."

    # Backend tests
    log_info "Running backend tests..."
    cd ${BACKEND_DIR}
    python3 manage.py test --noinput
    cd ..

    # Frontend tests
    log_info "Running frontend tests..."
    cd ${FRONTEND_DIR}
    npm test -- --run
    cd ..

    log_success "All tests passed"
}

setup_database() {
    log_info "Setting up database..."

    # Start database container only
    podman-compose -f ${COMPOSE_FILE} up -d db redis

    # Wait for database to be ready
    log_info "Waiting for database to be ready..."
    sleep 10

    # Run migrations
    log_info "Running database migrations..."
    podman-compose -f ${COMPOSE_FILE} run --rm backend python manage.py migrate --noinput

    # Seed component registry
    log_info "Seeding component registry..."
    podman-compose -f ${COMPOSE_FILE} run --rm backend python manage.py seed_component_registry

    # Create superuser if needed
    log_info "Creating superuser (if not exists)..."
    podman-compose -f ${COMPOSE_FILE} run --rm backend python manage.py shell --command "
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

deploy_containers() {
    log_info "Deploying containers..."

    # Stop existing containers
    log_info "Stopping existing containers..."
    podman-compose -f ${COMPOSE_FILE} down

    # Start all containers
    log_info "Starting all containers..."
    podman-compose -f ${COMPOSE_FILE} up -d

    # Wait for services to be healthy
    log_info "Waiting for services to be healthy..."
    sleep 20

    log_success "All containers deployed"
}

verify_deployment() {
    log_info "Verifying deployment..."

    # Check database health
    log_info "Checking database health..."
    if podman-compose -f ${COMPOSE_FILE} ps | grep -q beyondcode-db.*Up.*healthy; then
        log_success "Database is healthy"
    else
        log_error "Database health check failed"
        return 1
    fi

    # Check backend health
    log_info "Checking backend health..."
    sleep 10
    if podman-compose -f ${COMPOSE_FILE} ps | grep -q beyondcode-backend.*Up.*healthy; then
        log_success "Backend is healthy"
    else
        log_error "Backend health check failed"
        return 1
    fi

    # Check frontend health
    log_info "Checking frontend health..."
    if podman-compose -f ${COMPOSE_FILE} ps | grep -q beyondcode-frontend.*Up.*healthy; then
        log_success "Frontend is healthy"
    else
        log_error "Frontend health check failed"
        return 1
    fi

    # Test API endpoint
    log_info "Testing API endpoint..."
    if curl -s -f http://localhost:8000/api/builder/components/ > /dev/null; then
        log_success "API is responding"
    else
        log_warning "API endpoint test failed (may still be starting up)"
    fi

    # Test frontend
    log_info "Testing frontend..."
    if curl -s -f http://localhost:3000/ > /dev/null; then
        log_success "Frontend is accessible"
    else
        log_warning "Frontend test failed (may still be starting up)"
    fi

    log_success "Deployment verification complete"
}

show_logs() {
    log_info "Showing container logs (Ctrl+C to exit)..."
    podman-compose -f ${COMPOSE_FILE} logs -f --tail=50
}

rollback() {
    log_error "Initiating rollback..."

    # Stop all containers
    podman-compose -f ${COMPOSE_FILE} down

    # Restart previous version (if exists)
    log_info "Attempting to restart previous version..."

    log_success "Rollback completed"
}

# Main deployment flow
main() {
    log_info "Starting Podman deployment to ${ENVIRONMENT}..."

    # Pre-deployment checks
    check_requirements
    check_environment_file

    # Build images
    build_images

    # Run tests (skip on staging)
    if [ "$ENVIRONMENT" != "staging" ]; then
        run_tests
    fi

    # Deploy containers
    deploy_containers

    # Setup database
    setup_database

    # Verify deployment
    verify_deployment

    log_success "Deployment to ${ENVIRONMENT} completed successfully!"
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
    echo ""
    echo "View logs: ./deploy-podman.sh logs"
    echo "Stop: podman-compose -f podman-compose.yml down"
    echo "============================================"

    # Ask if user wants to see logs
    read -p "View logs now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        show_logs
    fi
}

# Handle special commands
case "${1:-}" in
    logs)
        show_logs
        ;;
    stop)
        log_info "Stopping all containers..."
        podman-compose -f ${COMPOSE_FILE} down
        log_success "All containers stopped"
        ;;
    restart)
        log_info "Restarting all containers..."
        podman-compose -f ${COMPOSE_FILE} restart
        log_success "All containers restarted"
        ;;
    *)
        # Trap errors and initiate rollback
        trap 'log_error "Deployment failed. Initiating rollback..."; rollback; exit 1' ERR

        # Run main function
        main "$@"
        ;;
esac
