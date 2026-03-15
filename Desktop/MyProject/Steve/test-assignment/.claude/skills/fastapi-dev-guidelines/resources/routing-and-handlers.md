# FastAPI Routing and Handlers

## Router Setup

### Basic Router
```python
# app/api/v1/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_users():
    return [{"id": 1, "name": "John"}]
```

### Router with Configuration
```python
router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_token)],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Unauthorized"},
    },
)
```

## Path Parameters

### Basic Path Parameters
```python
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# With type validation
@router.get("/items/{item_id}")
async def get_item(item_id: int):
    # item_id is automatically converted to int
    return {"item_id": item_id}

# Path with enum
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model_name": model_name, "message": "Deep Learning FTW!"}
```

### Path Parameters with Validation
```python
from fastapi import Path

@router.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., title="Item ID", description="The unique item ID", ge=1),
):
    return {"item_id": item_id}

# With regex validation
@router.get("/users/{username}")
async def get_user_by_username(
    username: str = Path(..., pattern=r"^[\w-]+$", min_length=3, max_length=50),
):
    return {"username": username}
```

## Query Parameters

### Basic Query Parameters
```python
from typing import Annotated

@router.get("/items/")
async def list_items(
    skip: int = 0,
    limit: int = 10,
):
    return {"skip": skip, "limit": limit}

# Required query parameter
@router.get("/items/{item_id}")
async def read_item(
    item_id: int,
    q: str,  # Required
):
    return {"item_id": item_id, "q": q}
```

### Query Parameters with Validation
```python
from fastapi import Query

@router.get("/items/")
async def list_items(
    q: str | None = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Search items by query string",
        min_length=3,
        max_length=50,
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    return {"q": q, "skip": skip, "limit": limit}

# Multiple values
@router.get("/items/")
async def list_items(
    tags: list[str] = Query(default=[]),
):
    return {"tags": tags}
```

## Request Body

### Pydantic Model Body
```python
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@router.post("/items/")
async def create_item(item: ItemCreate):
    return item

# Multiple body parameters
class User(BaseModel):
    username: str
    email: str

class Item(BaseModel):
    name: str
    price: float

@router.post("/items/")
async def create_item(
    item: Item,
    user: User,
    importance: int = Body(gt=0),
):
    return {"item": item, "user": user, "importance": importance}
```

### Form Data
```python
from fastapi import Form

@router.post("/login/")
async def login(
    username: str = Form(),
    password: str = Form(),
):
    return {"username": username}
```

### File Upload
```python
from fastapi import File, UploadFile

@router.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

## Response Models

### Response Model
```python
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int) -> User:
    # Response will be validated and serialized according to User model
    return {
        "id": user_id,
        "name": "John",
        "email": "john@example.com",
        "created_at": datetime.utcnow(),
    }
```

### Response Model with exclude
```python
@router.get("/users/{user_id}", response_model=User, response_model_exclude={"created_at"})
async def get_user(user_id: int):
    return user

@router.get("/users/", response_model=list[User], response_model_include={"id", "name"})
async def list_users():
    return users
```

### Multiple Response Models
```python
from fastapi.responses import JSONResponse

class Error(BaseModel):
    code: int
    message: str

@router.get(
    "/users/{user_id}",
    response_model=User,
    responses={
        404: {"model": Error, "description": "User not found"},
        400: {"model": Error, "description": "Bad request"},
    },
)
async def get_user(user_id: int):
    user = await get_user_from_db(user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content={"code": 404, "message": "User not found"},
        )
    return user
```

## Status Codes

```python
from fastapi import status

@router.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    return item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    pass
```

## Error Handling

### HTTPException
```python
from fastapi import HTTPException

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    item = await get_item_from_db(item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Item not found"},
        )
    return item
```

### Custom Exception Handler
```python
from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, name: str, code: int):
        self.name = name
        self.code = code

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} caused error with code {exc.code}"},
    )
```

## Middleware in Routes

### Route-level Dependencies
```python
from fastapi import Depends

async def verify_token(token: str = Header(...)):
    if token != "expected-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@router.get("/protected/", dependencies=[Depends(verify_token)])
async def protected_route():
    return {"message": "Protected data"}
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Email sending logic
    pass

@router.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(send_email, email, "Hello!")
    return {"message": "Notification sent in background"}
```

## Streaming Response

```python
from fastapi.responses import StreamingResponse
import io

@router.get("/stream/")
async def stream_data():
    async def generate():
        for i in range(10):
            yield f"data: {i}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.get("/download/")
async def download_file():
    file_like = io.BytesIO(b"file content")
    return StreamingResponse(
        file_like,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=file.txt"},
    )