# FastAPI Testing

## Test Setup

### pytest Configuration
```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short"
env = [
    "DATABASE_URL=sqlite+aiosqlite:///./test.db",
    "SECRET_KEY=test-secret-key",
]

[tool.coverage.run]
source = ["app"]
branch = true
```

### Test Client
```python
# tests/conftest.py
import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.core.database import Base, get_session
from app.core.config import settings

# Test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        yield db_session
    
    app.dependency_overrides[get_session] = override_get_session
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()
```

## API Tests

### Basic Endpoint Tests
```python
# tests/test_api/test_users.py
import pytest
from httpx import AsyncClient
from fastapi import status

class TestUsersAPI:
    """Tests for Users API endpoints."""
    
    @pytest.mark.asyncio
    async def test_create_user(self, client: AsyncClient):
        """Test user creation."""
        response = await client.post(
            "/api/v1/users/",
            json={
                "email": "test@example.com",
                "name": "Test User",
                "password": "password123",
            },
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
    
    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, client: AsyncClient):
        """Test duplicate email validation."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123",
        }
        
        # Create first user
        await client.post("/api/v1/users/", json=user_data)
        
        # Try to create duplicate
        response = await client.post("/api/v1/users/", json=user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @pytest.mark.asyncio
    async def test_list_users(self, client: AsyncClient):
        """Test listing users."""
        # Create test users
        for i in range(3):
            await client.post(
                "/api/v1/users/",
                json={
                    "email": f"user{i}@example.com",
                    "name": f"User {i}",
                    "password": "password123",
                },
            )
        
        response = await client.get("/api/v1/users/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 3
```

### Authentication Tests
```python
# tests/test_api/test_auth.py
import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.security import get_password_hash
from app.models.db_models import User

class TestAuthAPI:
    """Tests for authentication endpoints."""
    
    @pytest.fixture
    async def test_user(self, db_session):
        user = User(
            email="test@example.com",
            name="Test User",
            hashed_password=get_password_hash("password123"),
            is_active=True,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user
    
    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user):
        """Test successful login."""
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123",
            },
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        """Test login with wrong password."""
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "wrongpassword",
            },
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @pytest.mark.asyncio
    async def test_protected_route_with_token(
        self, 
        client: AsyncClient, 
        test_user,
    ):
        """Test accessing protected route with valid token."""
        # Login to get token
        login_response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123",
            },
        )
        token = login_response.json()["access_token"]
        
        # Access protected route
        response = await client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_protected_route_without_token(self, client: AsyncClient):
        """Test accessing protected route without token."""
        response = await client.get("/api/v1/users/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
```

## Service Layer Tests

```python
# tests/test_services/test_user_service.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.repositories.user_repo import UserRepository
from app.models.schemas import UserCreate

class TestUserService:
    """Tests for UserService."""
    
    @pytest.fixture
    def user_service(self, db_session: AsyncSession) -> UserService:
        repo = UserRepository(db_session)
        return UserService(repo)
    
    @pytest.mark.asyncio
    async def test_create_user(self, user_service: UserService):
        """Test user creation via service."""
        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            password="password123",
        )
        
        user = await user_service.create(user_data)
        
        assert user.id is not None
        assert user.email == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_create_duplicate_email_raises_error(
        self,
        user_service: UserService,
    ):
        """Test duplicate email validation in service."""
        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            password="password123",
        )
        
        await user_service.create(user_data)
        
        with pytest.raises(ValueError, match="Email already registered"):
            await user_service.create(user_data)
```

## Repository Tests

```python
# tests/test_repositories/test_user_repo.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repo import UserRepository
from app.models.db_models import User
from app.core.security import get_password_hash

class TestUserRepository:
    """Tests for UserRepository."""
    
    @pytest.fixture
    def user_repo(self, db_session: AsyncSession) -> UserRepository:
        return UserRepository(db_session)
    
    @pytest.mark.asyncio
    async def test_get_user(self, user_repo: UserRepository, db_session: AsyncSession):
        """Test getting user by ID."""
        user = User(
            email="test@example.com",
            name="Test User",
            hashed_password=get_password_hash("password123"),
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        found = await user_repo.get(user.id)
        
        assert found is not None
        assert found.email == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_user(self, user_repo: UserRepository):
        """Test getting non-existent user."""
        found = await user_repo.get(999)
        
        assert found is None
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_api/test_users.py

# Run specific test class
pytest tests/test_api/test_users.py::TestUsersAPI

# Run specific test
pytest tests/test_api/test_users.py::TestUsersAPI::test_create_user

# Run tests matching pattern
pytest -k "user"

# Run with verbose output
pytest -vv

# Run in parallel
pytest -n auto

# Stop on first failure
pytest -x

# Run only failed tests from last run
pytest --lf
```

## Test Fixtures for Common Data

```python
# tests/conftest.py

@pytest.fixture
def user_data() -> dict:
    """Sample user data for tests."""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "password": "password123",
    }

@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        name="Test User",
        hashed_password=get_password_hash("password123"),
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient, test_user: User) -> dict:
    """Get authentication headers for a user."""
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "password123",
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}