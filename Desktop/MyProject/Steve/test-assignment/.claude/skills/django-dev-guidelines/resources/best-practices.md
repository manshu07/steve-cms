# Django Best Practices

## Performance

### Query Optimization
```python
# ❌ N+1 queries problem
orders = Order.objects.all()
for order in orders:
    print(order.user.email)  # Query for each order

# ✅ Use select_related for foreign keys
orders = Order.objects.select_related("user").all()
for order in orders:
    print(order.user.email)  # No extra query

# ✅ Use prefetch_related for reverse/m2m
orders = Order.objects.prefetch_related("items").all()
for order in orders:
    for item in order.items.all():  # No extra query per order
        print(item.product_name)

# ✅ Combined
orders = (
    Order.objects
    .select_related("user")
    .prefetch_related("items")
    .all()
)
```

### Database Indexing
```python
class Order(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["user", "status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["status", "-created_at"]),
        ]
```

### Caching
```python
from django.core.cache import cache

def get_user_orders(user_id: int) -> list:
    cache_key = f"user_orders:{user_id}"
    orders = cache.get(cache_key)
    
    if orders is None:
        orders = list(
            Order.objects
            .filter(user_id=user_id)
            .select_related("user")
            .values()
        )
        cache.set(cache_key, orders, timeout=300)  # 5 minutes
    
    return orders

# Invalidate cache on change
def invalidate_user_orders(user_id: int) -> None:
    cache.delete(f"user_orders:{user_id}")
```

### Pagination
```python
# Always paginate list endpoints
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100

class OrderViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
```

## Security

### Settings Security
```python
# config/settings/production.py

# Never set DEBUG = True in production
DEBUG = False

# Always set ALLOWED_HOSTS
ALLOWED_HOSTS = ["api.example.com"]

# Security headers
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Secret key from environment
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
```

### SQL Injection Prevention
```python
# ❌ NEVER do this
Order.objects.raw(f"SELECT * FROM orders WHERE id = {order_id}")

# ✅ Use parameterized queries
Order.objects.raw("SELECT * FROM orders WHERE id = %s", [order_id])

# ✅ Best: Use ORM
Order.objects.get(id=order_id)
```

### Input Validation
```python
# Always validate input
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def create_user(email: str) -> User:
    try:
        validate_email(email)
    except ValidationError:
        raise ValueError("Invalid email format")
    
    return User.objects.create(email=email.lower())
```

### Rate Limiting
```python
# config/settings/base.py
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
}
```

## Error Handling

### Custom Exception Handler
```python
# apps/core/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
import structlog

logger = structlog.get_logger()

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        # Log the error
        logger.error(
            "api_error",
            status_code=response.status_code,
            error=str(exc),
            context=context,
        )
        
        # Standardize error response
        error_data = {
            "error": {
                "code": response.status_code,
                "message": response.data.get("detail", "An error occurred"),
                "details": response.data if isinstance(response.data, dict) else None,
            }
        }
        response.data = error_data
    
    return response

# settings.py
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
}
```

## Task Queue

### Celery Configuration
```python
# config/celery.py
from celery import Celery

app = Celery("myproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# config/settings/base.py
CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = "UTC"

# apps/orders/tasks.py
from config.celery import app
from django.core.mail import send_mail

@app.task
def send_confirmation_email(order_id: int) -> None:
    from .models import Order
    order = Order.objects.get(id=order_id)
    
    send_mail(
        f"Order #{order.id} Confirmed",
        f"Thank you for your order of ${order.total_amount}",
        "orders@example.com",
        [order.user.email],
    )

# Usage
send_confirmation_email.delay(order.id)
```

## Logging

### Structured Logging
```python
# config/settings/base.py
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

# Usage in code
import structlog

logger = structlog.get_logger()

def process_order(order_id: int) -> None:
    logger.info("processing_order", order_id=order_id)
    # ... processing
    logger.info("order_processed", order_id=order_id, status="success")
```

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production

# Install dependencies
COPY requirements/production.txt .
RUN pip install --no-cache-dir -r production.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run with gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Health Checks

```python
# apps/core/views.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request) -> JsonResponse:
    """Basic health check endpoint."""
    checks = {
        "status": "healthy",
        "database": "ok",
        "cache": "ok",
    }
    
    # Check database
    try:
        connection.ensure_connection()
    except Exception:
        checks["database"] = "error"
        checks["status"] = "unhealthy"
    
    # Check cache
    try:
        cache.set("health_check", "ok", 1)
        if cache.get("health_check") != "ok":
            raise Exception("Cache not working")
    except Exception:
        checks["cache"] = "error"
        checks["status"] = "unhealthy"
    
    status_code = 200 if checks["status"] == "healthy" else 503
    return JsonResponse(checks, status=status_code)

# config/urls.py
urlpatterns = [
    path("health/", health_check),
    # ... other URLs
]