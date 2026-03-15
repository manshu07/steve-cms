# Code Style Guide

## Type Hints Best Practices

### Basic Type Annotations
```python
from typing import Any, Literal, TypeAlias
from collections.abc import Callable, Sequence

# Basic types (Python 3.10+)
def greet(name: str) -> str:
    return f"Hello, {name}"

# Optional types
def find_user(user_id: int) -> User | None:
    ...

# Union types
def process(value: int | str | float) -> str:
    return str(value)

# Type aliases
UserId: TypeAlias = int
JsonDict: TypeAlias = dict[str, Any]

# Callable types
Handler: TypeAlias = Callable[[Request], Response]

# Literal types for fixed values
Status: TypeAlias = Literal["pending", "active", "completed"]
```

### Generic Types
```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Repository(Generic[T]):
    def __init__(self, model: type[T]) -> None:
        self.model = model
    
    def get(self, id: int) -> T | None:
        ...

# Usage
user_repo: Repository[User] = Repository(User)
```

### Protocol Types (Structural Subtyping)
```python
from typing import Protocol

class Serializable(Protocol):
    def to_dict(self) -> dict[str, Any]: ...
    def from_dict(self, data: dict[str, Any]) -> "Serializable": ...

def serialize(obj: Serializable) -> str:
    return json.dumps(obj.to_dict())
```

## Formatting Standards

### Ruff Configuration
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "F",      # pyflakes
    "I",      # isort
    "N",      # pep8-naming
    "W",      # pycodestyle warnings
    "UP",     # pyupgrade
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "SIM",    # flake8-simplify
    "TCH",    # flake8-type-checking
]

[tool.ruff.lint.isort]
known-first-party = ["myproject"]
```

### Import Organization
```python
# Standard library
from __future__ import annotations
import asyncio
from collections.abc import AsyncIterator
from typing import Any

# Third-party
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import structlog

# Local imports
from myproject.core.config import get_settings
from myproject.models.schemas import User
from myproject.services.user_service import UserService
```

## Naming Conventions

```python
# Variables and functions: snake_case
user_count = 10
total_price = 99.99

def calculate_total(items: list[Item]) -> float:
    ...

# Classes: PascalCase
class UserProfile:
    ...

class OrderProcessor:
    ...

# Constants: SCREAMING_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30.0

# Private members: single underscore prefix
class Service:
    def __init__(self) -> None:
        self._connection = None  # Private by convention
    
    def _validate_input(self, data: dict) -> bool:  # Internal method
        ...

# Name mangling: double underscore
class Base:
    def __private_method(self) -> None:  # Becomes _Base__private_method
        ...
```

## Docstring Standards

### Google Style
```python
def fetch_user(user_id: int, include_deleted: bool = False) -> User | None:
    """Fetch a user by their ID.

    Args:
        user_id: The unique identifier of the user.
        include_deleted: Whether to include soft-deleted users.

    Returns:
        The user object if found, None otherwise.

    Raises:
        DatabaseError: If there's a connection issue.

    Example:
        >>> user = fetch_user(123)
        >>> if user:
        ...     print(user.name)
    """
    ...
```

### Class Docstrings
```python
class UserRepository:
    """Repository for user data operations.

    Provides CRUD operations for users with caching support.
    Uses Redis for distributed caching.

    Attributes:
        db: Database session for queries.
        cache: Redis client for caching.
    """

    def __init__(self, db: AsyncSession, cache: Redis) -> None:
        """Initialize the repository.

        Args:
            db: Async database session.
            cache: Redis client instance.
        """
        self.db = db
        self.cache = cache
```

## Code Organization Patterns

### Feature-based Structure
```python
# features/users/__init__.py
from .models import User, UserCreate, UserUpdate
from .service import UserService
from .repository import UserRepository
from .router import router

__all__ = [
    "User",
    "UserCreate", 
    "UserUpdate",
    "UserService",
    "UserRepository",
    "router",
]
```

### Dependency Injection
```python
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

@lru_cache
def get_user_service() -> UserService:
    return UserService(UserRepository())

# In FastAPI routes
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

@router.get("/users/{user_id}")
async def get_user(user_id: int, service: UserServiceDep) -> User:
    return await service.get(user_id)