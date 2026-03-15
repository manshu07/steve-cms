# Testing Guide

## pytest Configuration

### pyproject.toml Setup
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

## Test Structure

### Project Test Layout
```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── factories.py          # Test data factories
├── unit/
│   ├── __init__.py
│   ├── test_services.py
│   └── test_utils.py
└── integration/
    ├── __init__.py
    └── test_api.py
```

## Fixtures

### conftest.py
```python
import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from myproject.main import app
from myproject.core.config import get_settings

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_user() -> dict[str, str]:
    """Sample user data for tests."""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
    }
```

## Unit Testing Patterns

### AAA Pattern (Arrange, Act, Assert)
```python
import pytest
from myproject.services.user_service import UserService

class TestUserService:
    async def test_create_user_success(self) -> None:
        # Arrange
        service = UserService()
        user_data = {"name": "John", "email": "john@example.com"}
        
        # Act
        result = await service.create(user_data)
        
        # Assert
        assert result.id is not None
        assert result.name == "John"
        assert result.email == "john@example.com"
    
    async def test_create_user_invalid_email(self) -> None:
        # Arrange
        service = UserService()
        user_data = {"name": "John", "email": "invalid-email"}
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Invalid email"):
            await service.create(user_data)
```

### Parametrized Tests
```python
@pytest.mark.parametrize("name,expected_valid", [
    ("John Doe", True),
    ("", False),
    ("   ", False),
    ("A" * 101, False),  # Too long
])
async def test_user_name_validation(name: str, expected_valid: bool) -> None:
    service = UserService()
    user_data = {"name": name, "email": "test@example.com"}
    
    if expected_valid:
        result = await service.create(user_data)
        assert result.name == name
    else:
        with pytest.raises(ValidationError):
            await service.create(user_data)
```

## Mocking

### Using pytest-mock
```python
from pytest_mock import MockerFixture
from myproject.external.email_service import EmailService

class TestEmailService:
    async def test_send_email_success(self, mocker: MockerFixture) -> None:
        # Mock external API call
        mock_send = mocker.patch.object(
            EmailService,
            "_call_api",
            return_value={"status": "sent"},
        )
        
        service = EmailService()
        result = await service.send("test@example.com", "Hello")
        
        assert result.status == "sent"
        mock_send.assert_called_once()
    
    async def test_send_email_retry(self, mocker: MockerFixture) -> None:
        # Mock failure then success
        mock_send = mocker.patch.object(
            EmailService,
            "_call_api",
            side_effect=[
                ConnectionError("Network error"),
                {"status": "sent"},
            ],
        )
        
        service = EmailService()
        result = await service.send("test@example.com", "Hello")
        
        assert result.status == "sent"
        assert mock_send.call_count == 2
```

### Async Mocking
```python
from unittest.mock import AsyncMock

async def test_async_mock() -> None:
    mock_fetch = AsyncMock(return_value={"id": 1, "name": "Test"})
    
    result = await mock_fetch()
    
    assert result["id"] == 1
    mock_fetch.assert_awaited_once()
```

## Integration Testing

### Database Tests
```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from myproject.models.user import User
from myproject.repositories.user_repo import UserRepository

@pytest.mark.integration
class TestUserRepository:
    async def test_create_and_find_user(
        self,
        db_session: AsyncSession,
    ) -> None:
        # Arrange
        repo = UserRepository(db_session)
        user_data = {"name": "Test", "email": "test@example.com"}
        
        # Act
        created = await repo.create(user_data)
        found = await repo.find_by_id(created.id)
        
        # Assert
        assert found is not None
        assert found.name == "Test"
```

### API Tests
```python
import pytest
from httpx import AsyncClient

@pytest.mark.integration
class TestUserAPI:
    async def test_create_user(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/users",
            json={"name": "Test", "email": "test@example.com"},
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test"
    
    async def test_get_user_not_found(self, client: AsyncClient) -> None:
        response = await client.get("/api/users/999")
        
        assert response.status_code == 404
```

## Test Factories

### Using factory_boy
```python
import factory
from factory import Faker

from myproject.models.user import User

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    id = factory.Sequence(lambda n: n)
    name = Faker("name")
    email = Faker("email")
    created_at = factory.LazyFunction(datetime.utcnow)

# Usage
def test_with_factory() -> None:
    user = UserFactory.create(name="Custom Name")
    assert user.name == "Custom Name"
    
    users = UserFactory.create_batch(5)
    assert len(users) == 5
```

## Test Coverage

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run specific test file
pytest tests/unit/test_services.py

# Run specific test
pytest tests/unit/test_services.py::TestUserService::test_create_user_success

# Run markers
pytest -m "not slow"      # Skip slow tests
pytest -m integration     # Only integration tests

# Verbose output
pytest -v --tb=long
```

## Best Practices

### 1. One Assertion Per Test (When Possible)
```python
# ❌ Too many assertions
async def test_user_creation() -> None:
    user = await create_user({"name": "John"})
    assert user.id is not None
    assert user.name == "John"
    assert user.email is not None
    assert user.created_at is not None

# ✅ Focused test
async def test_user_creation_assigns_id() -> None:
    user = await create_user({"name": "John"})
    assert user.id is not None
```

### 2. Use Descriptive Test Names
```python
# ❌ Vague
async def test_user() -> None:
    ...

# ✅ Descriptive
async def test_create_user_raises_error_when_email_missing() -> None:
    ...
```

### 3. Test Edge Cases
```python
class TestUserService:
    async def test_create_user_success(self) -> None:
        ...
    
    async def test_create_user_with_empty_name(self) -> None:
        ...
    
    async def test_create_user_with_duplicate_email(self) -> None:
        ...
    
    async def test_create_user_with_sql_injection_attempt(self) -> None:
        ...