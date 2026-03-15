---
name: python-dev-guidelines
description: Comprehensive Python development guidelines for backend development. Use when creating Python modules, working with virtual environments, managing dependencies, handling async patterns, error handling, testing, or any Python-related development task.
---

# Python Development Guidelines

Production-tested patterns and best practices for Python backend development.

## When This Skill Activates

This skill should be used when:
- Creating new Python modules or packages
- Setting up virtual environments and dependency management
- Implementing error handling and logging patterns
- Writing async Python code
- Creating and running tests
- Working with type hints and mypy
- Managing Python project structure

## Quick Reference

### Project Structure
```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── core/
│       ├── models/
│       ├── services/
│       └── utils/
├── tests/
├── pyproject.toml
├── requirements.txt
└── .python-version
```

### Dependency Management
- Use `pyproject.toml` for modern Python projects
- Use `uv` or `poetry` for dependency management
- Pin dependencies in production: `requirements.lock`
- Separate dev dependencies from production

### Code Quality Tools
- **Formatter:** `ruff format` or `black`
- **Linter:** `ruff check` or `pylint`
- **Type checker:** `mypy --strict`
- **Test runner:** `pytest` with `pytest-asyncio`

## Resources

- [Project Setup](resources/project-setup.md) - Virtual environments, pyproject.toml, tooling
- [Code Style](resources/code-style.md) - Formatting, linting, type hints
- [Async Patterns](resources/async-patterns.md) - asyncio, async/await best practices
- [Error Handling](resources/error-handling.md) - Exceptions, logging, sentry integration
- [Testing Guide](resources/testing-guide.md) - pytest, fixtures, mocking
- [Common Patterns](resources/common-patterns.md) - Dataclasses, Pydantic, context managers

## Key Principles

### 1. Type Safety First
```python
from typing import Any
from collections.abc import Callable

# Always type annotate public functions
def process_data(items: list[dict[str, Any]]) -> list[str]:
    return [item["name"] for item in items if "name" in item]
```

### 2. Use Pydantic for Data Validation
```python
from pydantic import BaseModel, Field, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(strict=True)
    
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
```

### 3. Async by Default for I/O Operations
```python
import asyncio
from collections.abc import AsyncIterator

async def fetch_data(urls: list[str]) -> AsyncIterator[dict]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_one(url)) for url in urls]
    for task in tasks:
        yield task.result()
```

### 4. Structured Logging
```python
import structlog

logger = structlog.get_logger()

async def process_order(order_id: int) -> None:
    log = logger.bind(order_id=order_id)
    await log.ainfo("processing_started")
    # ... processing
    await log.ainfo("processing_completed", items_count=5)
```

### 5. Exception Handling with Context
```python
from typing import Never

class AppError(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, context: dict[str, Any] | None = None):
        self.message = message
        self.context = context or {}
        super().__init__(message)

def raise_if_invalid(data: dict) -> None | Never:
    if not data.get("required_field"):
        raise AppError(
            "Missing required field",
            context={"field": "required_field", "data": data}
        )
```

## Testing Standards

```python
import pytest
from pytest_mock import MockerFixture

@pytest.fixture
def sample_user() -> dict[str, str]:
    return {"id": 1, "name": "Test User"}

class TestUserService:
    async def test_create_user_success(self, sample_user: dict) -> None:
        # Arrange, Act, Assert pattern
        result = await create_user(sample_user)
        assert result.id == 1
        
    @pytest.mark.parametrize("invalid_name", ["", None, "   "])
    async def test_create_user_invalid_name(
        self, sample_user: dict, invalid_name: str | None
    ) -> None:
        sample_user["name"] = invalid_name
        with pytest.raises(ValidationError):
            await create_user(sample_user)
```

## Common Commands

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Quality checks
ruff check .
ruff format .
mypy src/

# Testing
pytest -v --cov=src --cov-report=html
pytest -x -q  # Stop on first failure, quiet mode

# Dependencies
uv pip compile pyproject.toml -o requirements.txt