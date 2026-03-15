# Project Setup Guide

## Virtual Environment Management

### Using uv (Recommended)
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"
uv pip compile pyproject.toml -o requirements.txt
```

### Using poetry
```bash
# Install poetry
pip install poetry

# Create new project
poetry new myproject

# Add dependencies
poetry add fastapi uvicorn
poetry add --group dev pytest ruff mypy

# Install all dependencies
poetry install
```

## pyproject.toml Template

```toml
[project]
name = "myproject"
version = "0.1.0"
description = "A Python backend project"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "pydantic>=2.5.0",
    "structlog>=24.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py311"
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short"
```

## Project Structure Standards

```
project/
├── src/
│   └── package_name/
│       ├── __init__.py          # Package initialization
│       ├── main.py              # Entry point
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py        # Settings/configuration
│       │   ├── exceptions.py    # Custom exceptions
│       │   └── logging.py       # Logging setup
│       ├── models/
│       │   ├── __init__.py
│       │   └── schemas.py       # Pydantic models
│       ├── services/
│       │   ├── __init__.py
│       │   └── user_service.py
│       ├── repositories/
│       │   ├── __init__.py
│       │   └── user_repo.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── unit/
│   └── integration/
├── pyproject.toml
├── .python-version              # Pin Python version
├── .env.example
└── README.md
```

## Configuration Management

### Using pydantic-settings
```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    app_name: str = "MyApp"
    debug: bool = False
    environment: str = "development"
    
    # Database
    database_url: str
    database_pool_size: int = 5
    
    # External services
    redis_url: str | None = None
    
    # Security
    secret_key: str
    allowed_hosts: list[str] = ["localhost"]

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

## Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
```

Install: `pre-commit install`