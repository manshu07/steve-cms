---
name: django-dev-guidelines
description: Comprehensive Django development guidelines for building robust web applications and APIs. Use when creating Django models, views, serializers, URL routing, middleware, authentication, Django REST Framework APIs, testing Django applications, or any Django-related development task.
---

# Django Development Guidelines

Production-tested patterns and best practices for Django web development.

## When This Skill Activates

This skill should be used when:
- Creating Django models and migrations
- Building Django REST Framework (DRF) APIs
- Implementing authentication and permissions
- Creating views (FBV and CBV)
- Working with Django ORM
- Setting up middleware
- Testing Django applications
- Managing Django settings across environments

## Quick Reference

### Project Structure
```
project/
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/
│   ├── orders/
│   └── products/
├── manage.py
└── pyproject.toml
```

### Key Django Concepts
- **Models:** ORM layer, database schema
- **Views:** Request handlers (FBV/CBV)
- **Serializers:** DRF data validation/serialization
- **URLs:** URL routing configuration
- **Middleware:** Request/response processing
- **Signals:** Event-driven architecture
- **Management Commands:** CLI utilities

## Resources

- [Project Setup](resources/project-setup.md) - Settings, apps, configuration
- [Models and ORM](resources/models-and-orm.md) - Models, queries, migrations
- [Views and Serializers](resources/views-and-serializers.md) - DRF patterns, CBV/FBV
- [Authentication](resources/authentication.md) - Auth, permissions, JWT
- [Testing](resources/testing.md) - pytest-django, factories, APIClient
- [Best Practices](resources/best-practices.md) - Performance, security, deployment

## Key Principles

### 1. Use Django Settings Pattern
```python
# config/settings/base.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "corsheaders",
    # Local apps
    "apps.users",
    "apps.orders",
]

# config/settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ["api.example.com"]
```

### 2. Model Design
```python
# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model with additional fields."""
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return self.email
```

### 3. DRF Serializer Pattern
```python
# apps/users/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """User serializer with nested relationships."""
    
    full_name = serializers.SerializerMethodField()
    orders_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "phone",
            "orders_count", "created_at"
        ]
        read_only_fields = ["id", "created_at"]
    
    def get_full_name(self, obj: User) -> str:
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Email already exists")
        return value.lower()
```

### 4. ViewSet Pattern
```python
# apps/users/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """User API endpoints."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self) -> models.QuerySet[User]:
        """Filter queryset based on user permissions."""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(id=self.request.user.id)
        return queryset
    
    @action(detail=False, methods=["get"])
    def me(self, request) -> Response:
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
```

### 5. URL Routing
```python
# apps/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]

# config/urls.py
from django.urls import path, include

urlpatterns = [
    path("api/v1/", include("apps.users.urls")),
    path("api/v1/", include("apps.orders.urls")),
]
```

## Common Commands

```bash
# Create project and apps
django-admin startproject config .
python manage.py startapp apps.users

# Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Run server
python manage.py runserver

# Testing
pytest
pytest --cov=apps

# Shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Collect static
python manage.py collectstatic
```

## Django REST Framework Configuration

```python
# config/settings/base.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}