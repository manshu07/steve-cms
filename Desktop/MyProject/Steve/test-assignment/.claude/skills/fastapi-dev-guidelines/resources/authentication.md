# FastAPI Authentication

## OAuth2 with JWT

### Setup
```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: Any, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(subject: Any) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
```

### Token Models
```python
# app/models/schemas.py
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: int | None = None
    exp: int | None = None
```

### OAuth2 Login Route
```python
# app/api/v1/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import verify_password, create_access_token, create_refresh_token
from app.models.schemas import Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: DBSession = Depends(get_db),
) -> Token:
    user = await db.execute(
        select(User).where(User.email == form_data.username)
    )
    user = user.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )
```

### Token Refresh
```python
@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: DBSession = Depends(get_db),
) -> Token:
    try:
        payload = jwt.decode(
            refresh_token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        user_id = payload.get("sub")
        user = await db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return Token(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Current User Dependency

### Get Current User
```python
# app/api/deps.py
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: DBSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
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
```

### Active User Check
```python
async def get_current_active_user(current_user: CurrentUser) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

ActiveUser = Annotated[User, Depends(get_current_active_user)]
```

## User Registration

```python
# app/api/v1/users.py
from app.core.security import get_password_hash

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: DBSession,
) -> User:
    # Check if email exists
    existing = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=get_password_hash(user_data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
```

## API Key Authentication

```python
from fastapi import Header, HTTPException

async def get_api_key(api_key: str = Header(..., alias="X-API-Key")) -> str:
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# Usage
@router.get("/protected/")
async def protected_route(api_key: str = Depends(get_api_key)):
    return {"message": "Protected data"}
```

## Role-based Access Control

### Role Middleware
```python
from functools import wraps

def require_role(*roles: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: CurrentUser, **kwargs):
            if current_user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions",
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Or as a dependency
def check_roles(roles: list[str]):
    async def role_checker(current_user: CurrentUser) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user
    return role_checker

# Usage
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(check_roles(["admin"]))],
):
    # Only admins can delete users
    pass
```

## OAuth2 with External Providers

### Google OAuth
```python
from authlib.integrations.httpx_client import AsyncOAuth2Client

# config
GOOGLE_CLIENT_ID = "your-client-id"
GOOGLE_CLIENT_SECRET = "your-client-secret"
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google/callback"

@router.get("/auth/google")
async def google_login():
    client = AsyncOAuth2Client(
        client_id=GOOGLE_CLIENT_ID,
        redirect_uri=GOOGLE_REDIRECT_URI,
        scope="openid email profile",
    )
    uri, state = client.create_authorization_url("https://accounts.google.com/o/oauth2/v2/auth")
    return {"authorization_url": uri, "state": state}

@router.get("/auth/google/callback")
async def google_callback(code: str, state: str, db: DBSession):
    client = AsyncOAuth2Client(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )
    
    token = await client.fetch_token(
        "https://oauth2.googleapis.com/token",
        code=code,
    )
    
    # Get user info
    user_info = await client.get("https://www.googleapis.com/oauth2/v3/userinfo")
    user_data = user_info.json()
    
    # Find or create user
    user = await get_or_create_user_from_google(db, user_data)
    
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )
```

## Password Reset

```python
from app.core.email import send_email
from app.core.security import create_reset_token, verify_reset_token

@router.post("/password-reset/request")
async def request_password_reset(email: str, db: DBSession):
    user = await db.execute(select(User).where(User.email == email))
    user = user.scalar_one_or_none()
    
    if user:
        token = create_reset_token(user.id)
        await send_email(
            to=email,
            subject="Password Reset",
            body=f"Reset link: {settings.FRONTEND_URL}/reset-password?token={token}",
        )
    
    return {"message": "If email exists, reset link sent"}

@router.post("/password-reset/confirm")
async def confirm_password_reset(
    token: str,
    new_password: str,
    db: DBSession,
):
    user_id = verify_reset_token(token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = await db.get(User, user_id)
    user.hashed_password = get_password_hash(new_password)
    await db.commit()
    
    return {"message": "Password updated successfully"}
```

## CORS Configuration

```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)