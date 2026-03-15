# Dependency Injection in FastAPI

## Basic Dependencies

### Simple Dependency
```python
from fastapi import Depends

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

### Class-based Dependencies
```python
class CommonParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonParams = Depends()):
    return {"q": commons.q, "skip": commons.skip, "limit": commons.limit}
```

## Database Session Dependency

### Async Session
```python
# app/api/deps.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.database import async_session_factory

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Type alias for cleaner injection
from typing import Annotated
DBSession = Annotated[AsyncSession, Depends(get_db)]

# Usage in route
@router.get("/users/")
async def list_users(db: DBSession):
    result = await db.execute(select(User))
    return result.scalars().all()
```

## Repository Pattern with DI

### Repository Dependency
```python
# app/api/deps.py
from app.repositories.user_repo import UserRepository

def get_user_repo(db: DBSession) -> UserRepository:
    return UserRepository(db)

UserRepo = Annotated[UserRepository, Depends(get_user_repo)]

# app/repositories/user_repo.py
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def create(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.db.add(user)
        await self.db.flush()
        return user

# Usage in route
@router.get("/users/{user_id}")
async def get_user(user_id: int, repo: UserRepo):
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Service Layer DI

### Service with Repository
```python
# app/api/deps.py
from app.services.user_service import UserService

def get_user_service(repo: UserRepo) -> UserService:
    return UserService(repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]

# app/services/user_service.py
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    async def create_user(self, user_data: UserCreate) -> User:
        # Business logic here
        existing = await self.repo.get_by_email(user_data.email)
        if existing:
            raise ValueError("Email already registered")
        
        hashed_password = hash_password(user_data.password)
        return await self.repo.create(user_data, hashed_password)

# Usage
@router.post("/users/")
async def create_user(user_data: UserCreate, service: UserServiceDep):
    return await service.create_user(user_data)
```

## Authentication Dependencies

### Current User Dependency
```python
# app/api/deps.py
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: DBSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

# Usage
@router.get("/users/me")
async def read_users_me(current_user: CurrentUser):
    return current_user
```

### Active User Dependency
```python
def get_current_active_user(current_user: CurrentUser) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

ActiveUser = Annotated[User, Depends(get_current_active_user)]
```

## Permission Dependencies

### Role-based Access
```python
def require_roles(*roles: str):
    async def role_checker(current_user: CurrentUser) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions",
            )
        return current_user
    return role_checker

# Usage
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(require_roles("admin"))],
):
    # Only admins can delete users
    pass
```

### Owner or Admin Check
```python
async def get_user_or_404(user_id: int, db: DBSession) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_owner_or_admin():
    async def checker(
        user: User = Depends(get_user_or_404),
        current_user: CurrentUser = None,
    ) -> User:
        if current_user.id != user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return checker
```

## Settings Dependency

```python
from functools import lru_cache
from app.core.config import Settings

@lru_cache
def get_settings() -> Settings:
    return Settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]

@router.get("/info")
async def info(settings: SettingsDep):
    return {"app_name": settings.APP_NAME, "version": settings.VERSION}
```

## Pagination Dependency

```python
from pydantic import BaseModel

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 100

def get_pagination(skip: int = 0, limit: int = 100) -> PaginationParams:
    return PaginationParams(skip=skip, limit=min(limit, 100))

Pagination = Annotated[PaginationParams, Depends(get_pagination)]

@router.get("/items/")
async def list_items(pagination: Pagination, db: DBSession):
    result = await db.execute(
        select(Item).offset(pagination.skip).limit(pagination.limit)
    )
    return result.scalars().all()
```

## Yield Dependencies (Cleanup)

```python
async def get_db_with_cleanup() -> AsyncGenerator[AsyncSession, None]:
    session = async_session_factory()
    try:
        yield session
    finally:
        await session.close()

# Or for external resources
async def get_external_api_client():
    client = httpx.AsyncClient()
    try:
        yield client
    finally:
        await client.aclose()
```

## Nested Dependencies

```python
# Dependencies can depend on other dependencies
async def get_repository(db: DBSession) -> Repository:
    return Repository(db)

async def get_service(repo: Repository = Depends(get_repository)) -> Service:
    return Service(repo)

@router.get("/items/")
async def get_items(service: Service = Depends(get_service)):
    return await service.get_items()
```

## Dependency Overrides (Testing)

```python
# In tests
from app.main import app

def override_get_db():
    # Return test database session
    yield test_session

app.dependency_overrides[get_db] = override_get_db

# After tests
app.dependency_overrides = {}