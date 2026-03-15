# Async Patterns Guide

## asyncio Fundamentals

### Basic Async Functions
```python
import asyncio

async def fetch_data(url: str) -> dict:
    """Async function to fetch data."""
    await asyncio.sleep(0.1)  # Simulated I/O
    return {"url": url, "status": "ok"}

# Running async code
result = asyncio.run(fetch_data("https://api.example.com"))
```

### Task Groups (Python 3.11+)
```python
import asyncio
from collections.abc import Coroutine

async def fetch_all(urls: list[str]) -> list[dict]:
    """Fetch multiple URLs concurrently using TaskGroup."""
    results: list[dict] = []
    
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_data(url)) for url in urls]
    
    return [task.result() for task in tasks]
```

### Gathering Results
```python
async def gather_with_exceptions(urls: list[str]) -> list[dict]:
    """Gather results, handling exceptions."""
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return [
        r for r in results 
        if not isinstance(r, Exception)
    ]
```

## Async Context Managers

### Custom Async Context Manager
```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

class AsyncDatabase:
    async def connect(self) -> None:
        print("Connecting...")
        await asyncio.sleep(0.1)
    
    async def disconnect(self) -> None:
        print("Disconnecting...")
        await asyncio.sleep(0.1)
    
    async def query(self, sql: str) -> list:
        return [{"id": 1, "name": "test"}]

@asynccontextmanager
async def get_db() -> AsyncIterator[AsyncDatabase]:
    db = AsyncDatabase()
    try:
        await db.connect()
        yield db
    finally:
        await db.disconnect()

# Usage
async def main() -> None:
    async with get_db() as db:
        results = await db.query("SELECT * FROM users")
```

## Async Iterators

### Async Generator
```python
from collections.abc import AsyncIterator

async def stream_results(batch_size: int = 100) -> AsyncIterator[dict]:
    """Stream results in batches."""
    offset = 0
    while True:
        batch = await fetch_batch(offset, batch_size)
        if not batch:
            break
        for item in batch:
            yield item
        offset += batch_size

# Usage
async def process_stream() -> list[str]:
    results = []
    async for item in stream_results():
        results.append(item["name"])
    return results
```

## Rate Limiting

### Token Bucket Pattern
```python
import asyncio
import time

class RateLimiter:
    def __init__(self, rate: float, capacity: int) -> None:
        self.rate = rate  # Tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.tokens = min(
                self.capacity,
                self.tokens + elapsed * self.rate
            )
            self.last_update = now
            
            if self.tokens < 1:
                wait_time = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self.tokens = 0
            else:
                self.tokens -= 1

# Usage
limiter = RateLimiter(rate=10, capacity=20)  # 10 req/s, burst of 20

async def rate_limited_fetch(url: str) -> dict:
    await limiter.acquire()
    return await fetch_data(url)
```

## Timeout Handling

### Using asyncio.timeout (Python 3.11+)
```python
async def fetch_with_timeout(url: str, timeout: float = 5.0) -> dict:
    """Fetch with timeout."""
    async with asyncio.timeout(timeout):
        return await fetch_data(url)
    # Raises TimeoutError if exceeded

async def fetch_with_default(url: str, timeout: float = 5.0) -> dict | None:
    """Fetch with timeout, return None on timeout."""
    try:
        async with asyncio.timeout(timeout):
            return await fetch_data(url)
    except TimeoutError:
        return None
```

## Connection Pooling

### Async Pool Pattern
```python
import asyncio
from contextlib import asynccontextmanager

class ConnectionPool:
    def __init__(self, max_connections: int = 10) -> None:
        self.max_connections = max_connections
        self._semaphore = asyncio.Semaphore(max_connections)
        self._connections: list[AsyncDatabase] = []
    
    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[AsyncDatabase]:
        async with self._semaphore:
            db = AsyncDatabase()
            await db.connect()
            try:
                yield db
            finally:
                await db.disconnect()
```

## Best Practices

### 1. Never Block the Event Loop
```python
# ❌ WRONG - Blocks event loop
async def bad_example() -> None:
    time.sleep(5)  # Blocks everything!

# ✅ CORRECT - Non-blocking
async def good_example() -> None:
    await asyncio.sleep(5)  # Yields control
```

### 2. Use asyncio.to_thread for CPU-bound work
```python
async def process_large_file(content: str) -> dict:
    """Offload CPU work to thread pool."""
    result = await asyncio.to_thread(heavy_computation, content)
    return result
```

### 3. Proper Cancellation Handling
```python
async def cancellable_task() -> None:
    """Task that handles cancellation gracefully."""
    try:
        await long_running_operation()
    except asyncio.CancelledError:
        # Cleanup before re-raising
        await cleanup()
        raise
```

### 4. Use Structured Concurrency
```python
async def fetch_user_data(user_id: int) -> dict:
    """Fetch user with related data concurrently."""
    async with asyncio.TaskGroup() as tg:
        user_task = tg.create_task(fetch_user(user_id))
        posts_task = tg.create_task(fetch_posts(user_id))
        comments_task = tg.create_task(fetch_comments(user_id))
    
    return {
        "user": user_task.result(),
        "posts": posts_task.result(),
        "comments": comments_task.result(),
    }