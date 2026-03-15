---
name: fastapi-dev-guidelines
description: Comprehensive FastAPI development guidelines for building high-performance APIs. Use when creating FastAPI routes, Pydantic models, dependency injection, middleware, authentication, background tasks, WebSocket endpoints, or any FastAPI-related development task.
---

# FastAPI Development Guidelines

Production-tested patterns and best practices for FastAPI development.

## When This Skill Activates

This skill should be used when:
- Creating FastAPI applications and routes
- Building REST APIs with async support
- Implementing Pydantic models for validation
- Setting up dependency injection
- Adding authentication and authorization
- Working with background tasks
- Implementing WebSocket endpoints
- Testing FastAPI applications

## Quick Reference

### Project Structure
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── models/
│   │   └── schemas.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   └── orders.py
│   │   └── deps.py
│   ├── services/
│   │   └── user_service.py
│   └── repositories/
│       └── user_repo.py
├── tests/
├── pyproject.toml
└── .env
```

### Key Concepts
- **Pydantic Models:** Data validation and serialization
- **Dependency Injection:** FastAPI's DI system
- **Path Operations:** Route handlers with type hints
- **Middleware:** Request/response processing
- **Background Tasks:** Async task execution
- **WebSockets:** Real-time communication

## Resources

- [Project Setup](resources/project-setup.md) - Application structure, configuration
- [Routing and Handlers](resources/routing-and-handlers.md) - Routes, path params, query params
- [Pydantic Models](resources/pydantic-models.md) - Validation, serializers
- [Dependency Injection](resources/dependency-injection.md) - DI patterns, database sessions
- [Authentication](resources/authentication.md) - JWT, OAuth2, security
- [Testing](resources/testing.md) - pytest, TestClient, async tests

## Key Principles

### 1. Application Factory Pattern
```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.api.v1 import users, orders

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()
    yield
    # Shutdown
    await database.disconnect()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
    )
    
    # Include routers
    app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])
    
    return app

app = create_app()
```

### 2. Pydantic Models
```python
# app/models/schemas.py
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool = True
    created_at: datetime
```

### 3. Route Handlers
```python
# app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from app.models.schemas import User, UserCreate
from app.services.user_service import UserService
from app.api.deps import get_user_service

router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    return await service.create(user_data)

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    user = await service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### 4. Dependency Injection
```python
# app/api/deps.py
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService

# Database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with get_session() as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_db)]

# Repository
def get_user_repo(db: DBSession) -> UserRepository:
    return UserRepository(db)

UserRepo = Annotated[UserRepository, Depends(get_user_repo)]

# Service
def get_user_service(repo: UserRepo) -> UserService:
    return UserService(repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
```

### 5. Configuration
```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MyAPI"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = {"env_file": ".env", "case_sensitive": True}

settings = Settings()
```

## Common Commands

```bash
# Run development server
uvicorn app.main:app --reload

# Run production server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run with workers
uvicorn app.main:app --workers 4

# Testing
pytest
pytest --cov=app --cov-report=html

# Generate requirements
pip freeze > requirements.txt
```

## OpenAPI Configuration

```python
app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://example.com/logo.png"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi