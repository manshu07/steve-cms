# Pydantic Models in FastAPI

## Basic Models

### Simple Model
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True
```

### Model with Field Validation
```python
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int | None = Field(None, ge=0, le=150)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "age": 30,
                }
            ]
        }
    }
```

## Model Inheritance

### Base Models Pattern
```python
from datetime import datetime

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool = True
    created_at: datetime
```

## Validation

### Field Validators
```python
from pydantic import field_validator, model_validator

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str
    
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()
    
    @field_validator("email")
    @classmethod
    def email_must_be_lowercase(cls, v: str) -> str:
        return v.lower()
    
    @model_validator(mode="after")
    def passwords_match(self) -> "UserCreate":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
```

### Custom Validators
```python
from pydantic import field_validator
import re

class User(BaseModel):
    phone: str
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r"^\+?1?\d{9,15}$", v):
            raise ValueError("Invalid phone number format")
        return v
```

## Model Configuration

### ConfigDict Options
```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,      # Enable ORM mode
        str_strip_whitespace=True, # Strip whitespace from strings
        validate_assignment=True,  # Validate on attribute assignment
        extra="forbid",           # Forbid extra fields
        str_max_length=1000,      # Max string length
        str_min_length=1,         # Min string length
    )
    
    id: int
    name: str
```

### JSON Schema Customization
```python
class Item(BaseModel):
    name: str
    price: float
    
    model_config = ConfigDict(
        json_schema_extra={
            "title": "Item",
            "description": "An item in the store",
            "examples": [
                {"name": "Widget", "price": 19.99},
            ],
        }
    )
```

## Nested Models

### Nested Model Structure
```python
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class User(BaseModel):
    id: int
    name: str
    address: Address

# Request example
{
    "id": 1,
    "name": "John",
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "country": "USA",
        "postal_code": "10001"
    }
}
```

### Lists and Dictionaries
```python
class Order(BaseModel):
    id: int
    items: list[OrderItem]
    metadata: dict[str, str]
    tags: set[str]
```

## Union Types and Discriminators

### Union Types
```python
from typing import Union, Literal

class Dog(BaseModel):
    pet_type: Literal["dog"]
    bark: str

class Cat(BaseModel):
    pet_type: Literal["cat"]
    meow: str

class Pet(BaseModel):
    pet: Union[Dog, Cat] = Field(..., discriminator="pet_type")
```

## Optional Fields

```python
from typing import Optional

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    is_active: bool | None = None

# All fields optional for PATCH requests
```

## Computed Fields

```python
from pydantic import computed_field

class User(BaseModel):
    first_name: str
    last_name: str
    
    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

## Model Serialization

### Dump to Dictionary/JSON
```python
user = User(id=1, name="John", email="john@example.com")

# To dict
data = user.model_dump()
# {"id": 1, "name": "John", "email": "john@example.com"}

# To dict with exclude
data = user.model_dump(exclude={"id"})

# To dict with only specific fields
data = user.model_dump(include={"name", "email"})

# To JSON
json_str = user.model_dump_json()
```

### Model from Dictionary
```python
# From dict
user = User.model_validate({"id": 1, "name": "John", "email": "john@example.com"})

# From ORM object (requires from_attributes=True)
user = User.model_validate(db_user)

# From JSON string
user = User.model_validate_json('{"id": 1, "name": "John", "email": "john@example.com"}')
```

## Email and URL Types

```python
from pydantic import BaseModel, EmailStr, HttpUrl

class Contact(BaseModel):
    email: EmailStr
    website: HttpUrl

# Automatically validates email and URL formats
```

## Date and Time Types

```python
from datetime import datetime, date, time, timedelta

class Event(BaseModel):
    name: str
    date: date
    start_time: time
    end_time: time
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Secret Types

```python
from pydantic import SecretStr, SecretBytes

class Credentials(BaseModel):
    password: SecretStr
    api_key: SecretStr
    
    def get_password(self) -> str:
        return self.password.get_secret_value()
```

## Custom Types

```python
from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator
from typing import Annotated

# Custom type with preprocessing
ObjectId = Annotated[str, BeforeValidator(lambda v: str(v) if v else v)]

class Document(BaseModel):
    id: ObjectId
    name: str