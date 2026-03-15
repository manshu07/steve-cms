# Common Python Patterns

## Dataclasses

### Basic Dataclass
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class User:
    id: int
    name: str
    email: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        self.email = self.email.lower()

# Usage
user = User(id=1, name="John", email="John@Example.com")
print(user.email)  # "john@example.com"
```

### Frozen Dataclass (Immutable)
```python
@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float
    
    def __str__(self) -> str:
        return f"{self.latitude}, {self.longitude}"

# Immutable - cannot be changed after creation
coords = Coordinates(40.7128, -74.0060)
# coords.latitude = 0  # Raises FrozenInstanceError
```

## Pydantic Models

### Model with Validation
```python
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int | None = Field(None, ge=0, le=150)
    
    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip()
    
    @model_validator(mode="after")
    def validate_model(self) -> "UserCreate":
        # Cross-field validation
        return self

class User(UserCreate):
    id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Model Configuration
```python
from pydantic import BaseModel, ConfigDict

class StrictModel(BaseModel):
    model_config = ConfigDict(
        strict=True,              # No type coercion
        extra="forbid",           # No extra fields
        str_strip_whitespace=True,
        validate_assignment=True,  # Validate on attribute assignment
    )
    
    name: str
    count: int
```

## Context Managers

### Synchronous Context Manager
```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def timer(name: str) -> Generator[None, None, None]:
    import time
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name} took {elapsed:.2f} seconds")

# Usage
with timer("database_query"):
    # ... expensive operation
    pass
```

### Resource Management
```python
from typing import Iterator

class DatabaseConnection:
    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
        self._connection = None
    
    def __enter__(self) -> "DatabaseConnection":
        self._connection = self._connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._connection:
            self._connection.close()
    
    def _connect(self):
        # Connection logic
        pass
    
    def query(self, sql: str) -> list:
        # Query logic
        return []

# Usage
with DatabaseConnection("postgresql://...") as db:
    results = db.query("SELECT * FROM users")
```

## Singleton Pattern

### Using Module-level Variable
```python
# singleton.py
class Database:
    def __init__(self) -> None:
        self.connected = False

_database: Database | None = None

def get_database() -> Database:
    global _database
    if _database is None:
        _database = Database()
    return _database
```

### Using __new__
```python
class Singleton:
    _instance: "Singleton | None" = None
    
    def __new__(cls) -> "Singleton":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

## Factory Pattern

### Factory with Registry
```python
from typing import Callable, TypeVar

T = TypeVar("T")

class Factory:
    def __init__(self) -> None:
        self._registry: dict[str, type] = {}
    
    def register(self, name: str) -> Callable[[type], type]:
        def decorator(cls: type) -> type:
            self._registry[name] = cls
            return cls
        return decorator
    
    def create(self, name: str, **kwargs: Any) -> Any:
        cls = self._registry.get(name)
        if cls is None:
            raise ValueError(f"Unknown type: {name}")
        return cls(**kwargs)

# Usage
factory = Factory()

@factory.register("email")
class EmailNotification:
    def __init__(self, address: str) -> None:
        self.address = address

@factory.register("sms")
class SMSNotification:
    def __init__(self, phone: str) -> None:
        self.phone = phone

# Create instances
notification = factory.create("email", address="user@example.com")
```

## Strategy Pattern

```python
from abc import ABC, abstractmethod
from typing import Protocol

# Using Protocol (structural typing)
class PaymentStrategy(Protocol):
    def pay(self, amount: float) -> str: ...

class CreditCardPayment:
    def __init__(self, card_number: str) -> None:
        self.card_number = card_number
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} with card {self.card_number[-4:]}"

class PayPalPayment:
    def __init__(self, email: str) -> None:
        self.email = email
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} via PayPal ({self.email})"

class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy
    
    def process(self, amount: float) -> str:
        return self._strategy.pay(amount)

# Usage
processor = PaymentProcessor(CreditCardPayment("1234567890123456"))
result = processor.process(100.0)
```

## Observer Pattern

```python
from collections.abc import Callable
from typing import Any

class EventEmitter:
    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[..., None]]] = {}
    
    def on(self, event: str, callback: Callable[..., None]) -> None:
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    
    def off(self, event: str, callback: Callable[..., None]) -> None:
        if event in self._listeners:
            self._listeners[event].remove(callback)
    
    def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        if event in self._listeners:
            for callback in self._listeners[event]:
                callback(*args, **kwargs)

# Usage
emitter = EventEmitter()

def on_user_created(user_id: int) -> None:
    print(f"User created: {user_id}")

emitter.on("user_created", on_user_created)
emitter.emit("user_created", user_id=123)
```

## Decorator Patterns

### Timing Decorator
```python
import time
from functools import wraps
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable)

def timed(func: F) -> F:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper  # type: ignore

# Usage
@timed
def slow_function() -> None:
    time.sleep(1)
```

### Caching Decorator
```python
from functools import lru_cache
from typing import Any

@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    # Expensive operation
    return sum(range(n))

# With custom cache
def cached(ttl: float = 60.0) -> Callable[[F], F]:
    cache: dict[str, tuple[Any, float]] = {}
    
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = str((args, sorted(kwargs.items())))
            now = time.time()
            
            if key in cache:
                value, timestamp = cache[key]
                if now - timestamp < ttl:
                    return value
            
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        
        return wrapper  # type: ignore
    
    return decorator