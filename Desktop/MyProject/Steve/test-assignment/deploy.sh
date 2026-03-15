#!/bin/bash
###############################################################################
# Production Deployment Script for BeyondCode Page Builder
# Usage: ./deploy.sh [environment]
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
DEPLOY_USER="deploy"
DEPLOY_HOST="your-server.com"
DEPLOY_PATH="/var/www/${PROJECT_NAME}"

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
    command -v python3 >/dev/null 2>&1 || { log_error "Python 3 is required but not installed."; exit 1; }
    command -v npm >/dev/null 2>&1 || { log_error "npm is required but not installed."; exit 1; }
    command -v git >/dev/null 2>&1 || { log_error "git is required but not installed."; exit 1; }

    log_success "All requirements met"
}

backup_database() {
    log_info "Creating database backup..."

    BACKUP_DIR="${DEPLOY_PATH}/backups"
    BACKUP_FILE="${BACKUP_DIR}/db_backup_$(date +%Y%m%d_%H%M%S).sql"

    ssh ${DEPLOY_USER}@${DEPLOY_HOST} "mkdir -p ${BACKUP_DIR}"
    ssh ${DEPLOY_USER}@${DEPLOY_HOST} "python3 ${DEPLOY_PATH}/${BACKEND_DIR}/manage.py dumpdata > ${BACKUP_FILE}"

    log_success "Database backed up to ${BACKUP_FILE}"
}

deploy_backend() {
    log_info "Deploying backend..."

    # Create temporary directory for deployment
    TEMP_DIR=$(mktemp -d)
    log_info "Created temporary directory: ${TEMP_DIR}"

    # Copy backend files to temp directory
    rsync -av --exclude='__pycache__' \
              --exclude='*.pyc' \
              --exclude='*.pyo' \
              --exclude='local_settings.py' \
              --exclude='.DS_Store' \
              --exclude='media' \
              --exclude='static' \
              ${BACKEND_DIR}/ ${TEMP_DIR}/

    # Install Python dependencies
    log_info "Installing Python dependencies..."
    cd ${TEMP_DIR}
    pip3 install -r requirements.txt --target=${TEMP_DIR}/lib

    # Run migrations
    log_info "Running database migrations..."
    python3 manage.py migrate --noinput

    # Collect static files
    log_info "Collecting static files..."
    python3 manage.py collectstatic --noinput --clear

    # Compress and upload to server
    log_info "Uploading backend to server..."
    tar -czf /tmp/${PROJECT_NAME}-backend.tar.gz -C ${TEMP_DIR} .
    scp /tmp/${PROJECT_NAME}-backend.tar.gz ${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/

    # Extract on server
    ssh ${DEPLOY_USER}@${DEPLOY_HOST} << EOF
        cd ${DEPLOY_PATH}
        tar -xzf /tmp/${PROJECT_NAME}-backend.tar.gz
        rm /tmp/${PROJECT_NAME}-backend.tar.gz

        # Restart Gunicorn
        sudo systemctl reload gunicorn
        sudo systemctl restart gunicorn

        # Clear Python cache
        find . -type d -name __pycache__ -exec rm -rf {} +
        find . -type f -name "*.pyc" -delete
EOF

    # Cleanup
    rm -rf ${TEMP_DIR}
    log_success "Backend deployed successfully"
}

deploy_frontend() {
    log_info "Deploying frontend..."

    # Build frontend for production
    log_info "Building frontend..."
    cd ${FRONTEND_DIR}
    npm run build

    # Upload to server
    log_info "Uploading frontend to server..."
    tar -czf /tmp/${PROJECT_NAME}-frontend.tar.gz -C dist .
    scp /tmp/${PROJECT_NAME}-frontend.tar.gz ${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/

    # Extract on server
    ssh ${DEPLOY_USER}@${DEPLOY_HOST} << EOF
        mkdir -p ${DEPLOY_PATH}/frontend
        cd ${DEPLOY_PATH}/frontend
        tar -xzf /tmp/${PROJECT_NAME}-frontend.tar.gz
        rm /tmp/${PROJECT_NAME}-frontend.tar.gz
EOF

    log_success "Frontend deployed successfully"
}

run_tests() {
    log_info "Running tests..."

    # Backend tests
    log_info "Running backend tests..."
    cd ${BACKEND_DIR}
    python manage.py test --noinput

    # Frontend tests
    log_info "Running frontend tests..."
    cd ${FRONTEND_DIR}
    npm test -- --run

    log_success "All tests passed"
}

verify_deployment() {
    log_info "Verifying deployment..."

    # Check if backend is responding
    log_info "Checking backend health..."
    BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://${DEPLOY_HOST}/api/builder/components/)
    if [ "$BACKEND_STATUS" -eq 200 ]; then
        log_success "Backend is responding"
    else
        log_error "Backend returned status ${BACKEND_STATUS}"
        exit 1
    fi

    # Check if frontend is accessible
    log_info "Checking frontend accessibility..."
    FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://${DEPLOY_HOST}/)
    if [ "$FRONTEND_STATUS" -eq 200 ]; then
        log_success "Frontend is accessible"
    else
        log_error "Frontend returned status ${FRONTEND_STATUS}"
        exit 1
    fi

    log_success "Deployment verification passed"
}

rollback() {
    log_error "Initiating rollback..."

    # Rollback backend
    ssh ${DEPLOY_USER}@${DEPLOY_HOST} << EOF
        cd ${DEPLOY_PATH}
        git reset --hard HEAD~1
        sudo systemctl reload gunicorn
        sudo systemctl restart gunicorn
EOF

    log_success "Rollback completed"
}

# Main deployment flow
main() {
    log_info "Starting deployment to ${ENVIRONMENT}..."
    log_info "Deploying to: ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}"

    # Pre-deployment checks
    check_requirements

    # Run tests (skip on staging)
    if [ "$ENVIRONMENT" != "staging" ]; then
        run_tests
    fi

    # Backup database
    backup_database

    # Deploy backend
    deploy_backend

    # Deploy frontend
    deploy_frontend

    # Verify deployment
    verify_deployment

    log_success "Deployment to ${ENVIRONMENT} completed successfully!"
    log_info "Access your site at: https://${DEPLOY_HOST}"
}

# Trap errors and initiate rollback
trap 'log_error "Deployment failed. Initiating rollback..."; rollback; exit 1' ERR

# Run main function
main "$@"
