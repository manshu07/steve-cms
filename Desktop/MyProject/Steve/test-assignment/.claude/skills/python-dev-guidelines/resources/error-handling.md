# Error Handling Guide

## Custom Exception Hierarchy

### Base Exception Classes
```python
from typing import Any

class AppError(Exception):
    """Base exception for application errors."""
    
    def __init__(
        self,
        message: str,
        code: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.code = code or "INTERNAL_ERROR"
        self.context = context or {}
        super().__init__(message)

class ValidationError(AppError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: str | None = None) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            context={"field": field} if field else {},
        )

class NotFoundError(AppError):
    """Raised when a resource is not found."""
    
    def __init__(self, resource: str, identifier: Any) -> None:
        super().__init__(
            message=f"{resource} not found",
            code="NOT_FOUND",
            context={"resource": resource, "identifier": str(identifier)},
        )

class AuthenticationError(AppError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message=message, code="AUTHENTICATION_ERROR")

class AuthorizationError(AppError):
    """Raised when authorization fails."""
    
    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(message=message, code="AUTHORIZATION_ERROR")

class DatabaseError(AppError):
    """Raised when a database operation fails."""
    
    def __init__(self, message: str, query: str | None = None) -> None:
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            context={"query": query} if query else {},
        )
```

## Structured Logging with structlog

### Setup
```python
import logging
import sys

import structlog
from structlog.types import Processor

def setup_logging(log_level: str = "INFO") -> None:
    """Configure structured logging."""
    
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]
    
    # Use JSON in production, pretty print in development
    if log_level == "DEBUG":
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

# Usage
logger = structlog.get_logger()
```

### Logging Patterns
```python
import structlog

logger = structlog.get_logger()

async def process_order(order_id: int) -> dict:
    """Process an order with proper logging."""
    log = logger.bind(order_id=order_id)
    
    await log.ainfo("order_processing_started")
    
    try:
        result = await process_payment(order_id)
        await log.ainfo("payment_completed", amount=result["amount"])
        return result
    except PaymentError as e:
        await log.aerror(
            "payment_failed",
            error=str(e),
            error_code=e.code,
        )
        raise
```

## Sentry Integration

### Setup
```python
import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration

def init_sentry(dsn: str, environment: str) -> None:
    """Initialize Sentry error tracking."""
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        integrations=[AsyncioIntegration()],
        traces_sample_rate=0.1,  # 10% of transactions
        profiles_sample_rate=0.1,
    )

def capture_exception(
    error: Exception,
    context: dict[str, Any] | None = None,
) -> None:
    """Capture exception with context."""
    with sentry_sdk.push_scope() as scope:
        if context:
            for key, value in context.items():
                scope.set_context(key, value)
        sentry_sdk.capture_exception(error)
```

### Error Context Middleware
```python
import structlog
import sentry_sdk
from contextvars import ContextVar

request_context: ContextVar[dict] = ContextVar("request_context", default={})

def set_request_context(**kwargs: Any) -> None:
    """Set context for current request."""
    current = request_context.get()
    request_context.set({**current, **kwargs})
    
    # Also set in structlog and sentry
    structlog.contextvars.bind_contextvars(**kwargs)
    sentry_sdk.set_context("request", kwargs)
```

## Result Pattern (Alternative to Exceptions)

### Using Results for Expected Failures
```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")

@dataclass
class Result(Generic[T, E]):
    """Result type for operations that can fail."""
    value: T | None = None
    error: E | None = None
    
    @property
    def is_success(self) -> bool:
        return self.error is None
    
    @property
    def is_failure(self) -> bool:
        return self.error is not None
    
    def unwrap(self) -> T:
        if self.error:
            raise ValueError(f"Cannot unwrap failure: {self.error}")
        return self.value!  # type: ignore
    
    def unwrap_or(self, default: T) -> T:
        return self.value if self.value is not None else default

# Usage
async def find_user(user_id: int) -> Result[User, str]:
    user = await db.get(User, user_id)
    if user:
        return Result(value=user)
    return Result(error=f"User {user_id} not found")

# Handler
async def get_user_handler(user_id: int) -> User:
    result = await find_user(user_id)
    if result.is_failure:
        raise NotFoundError("User", user_id)
    return result.unwrap()
```

## Error Handler Decorators

### Retry Pattern
```python
import asyncio
from functools import wraps
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable)

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[F], F]:
    """Retry decorator with exponential backoff."""
    
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
            
            raise last_exception
        
        return wrapper  # type: ignore
    
    return decorator

# Usage
@retry(max_attempts=3, delay=1.0, exceptions=(ConnectionError,))
async def fetch_from_api(url: str) -> dict:
    ...
```

### Circuit Breaker Pattern
```python
import asyncio
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time: float | None = None
    
    async def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        if self.state == CircuitState.OPEN:
            if self._should_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
            else:
                raise AppError("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_recovery(self) -> bool:
        if self.last_failure_time is None:
            return False
        return time.monotonic() - self.last_failure_time >= self.recovery_timeout
    
    def _on_success(self) -> None:
        self.failures = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self) -> None:
        self.failures += 1
        self.last_failure_time = time.monotonic()
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN