# Standard Module Patterns

Proven patterns for organizing Python code into standard module files.

---

## Pattern: __init__.py - Public API Only

**Purpose:** Export public API. Users import from package, not from internal modules.

**Rules:**
1. Only import and re-export public symbols
2. Use `__all__` to explicitly define API
3. Never define classes/functions in `__init__.py`
4. Keep it short (< 20 lines)
5. No side effects on import

**Good: Minimal exports**
```python
"""Public API for mypackage."""

from ._core import MainClass, process_data
from ._exceptions import ProcessingError
from ._types import Config, Result

__all__ = [
    "MainClass",
    "process_data",
    "ProcessingError",
    "Config",
    "Result",
]
```

**Bad: Logic in __init__.py**
```python
# ❌ Don't do this
from ._core import MainClass

class Wrapper(MainClass):  # ❌ Define classes here
    pass

# ❌ Side effects on import
print("Package loaded")  # ❌ Noisy
```

---

## Pattern: _types.py - Type Definitions

**Purpose:** Single location for all type definitions. Prevents circular imports.

**What goes here:**
- Dataclasses
- TypedDicts
- Type aliases
- Enums
- Named tuples

**Never here:**
- Logic or functions
- Class methods
- Configuration values (use _constants.py)

**Good: Clean type definitions**
```python
"""Type definitions for mypackage."""

from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias

class MetricType(Enum):
    """Types of metrics supported."""
    COUNT = "count"
    DURATION = "duration"
    SIZE = "size"

@dataclass(frozen=True)
class Config:
    """Configuration for Processor."""
    timeout: int = 30
    retries: int = 3
    batch_size: int = 100

@dataclass
class Result:
    """Processing result."""
    success: bool
    items: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    duration: float = 0.0

# Type alias
ProcessorFn: TypeAlias = callable[[Result], Result]
```

**Why:**
- Dataclass is immutable (frozen=True) if config never changes
- Default factory for mutable defaults (safe)
- Enum for restricted values
- Type alias for complex types
- No methods, just structure

---

## Pattern: _exceptions.py - Exception Hierarchy

**Purpose:** All exceptions in one place. Establish clear error types.

**Rules:**
1. Base exception inherits from Exception
2. All custom exceptions inherit from base
3. Use semantic exception names
4. One per file unless very small project

**Good: Clear hierarchy**
```python
"""Exceptions for mypackage."""

class ProcessorError(Exception):
    """Base exception for all processor errors."""
    pass

class ValidationError(ProcessorError):
    """Input validation failed."""
    pass

class ConfigurationError(ProcessorError):
    """Invalid configuration provided."""
    pass

class ProcessingError(ProcessorError):
    """Processing operation failed."""
    pass

class TimeoutError(ProcessingError):
    """Operation exceeded timeout."""
    pass

class RetryableError(ProcessingError):
    """Error that might succeed if retried."""
    pass
```

**Why:**
- Users can catch `ProcessorError` to catch any error
- Users can catch `ValidationError` specifically
- Hierarchy reflects domain logic
- Easier debugging with semantic names

**Usage:**
```python
try:
    processor.process(data)
except ValidationError:
    # Handle input issues
    fix_input()
except TimeoutError:
    # Handle timeout specifically
    use_backup()
except ProcessorError:
    # Catch any other processor error
    log_error()
```

---

## Pattern: _constants.py - Configuration Defaults

**Purpose:** All constants in one place. Single source of truth for configuration.

**Rules:**
1. UPPER_SNAKE_CASE for all constants
2. Group related constants with comments
3. Provide meaningful names, not just values
4. Don't put logic, only literals

**Good: Well-organized constants**
```python
"""Constants for mypackage."""

# Limits
MAX_BATCH_SIZE = 1000
MIN_BATCH_SIZE = 1
MAX_TIMEOUT_SECONDS = 300
MIN_TIMEOUT_SECONDS = 1

# Defaults
DEFAULT_BATCH_SIZE = 100
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_RETRIES = 3

# Formats
SUPPORTED_FORMATS = {"json", "csv", "parquet"}
DEFAULT_FORMAT = "json"

# Performance
CACHE_SIZE = 10_000
THREAD_POOL_SIZE = 4

# Paths
BUFFER_SIZE_BYTES = 1024 * 1024  # 1 MB
```

**Bad: Scattered magic numbers**
```python
# ❌ In _core.py
if batch.size > 1000:  # What's 1000?
    split_batch()

# ❌ In _processors.py
time.sleep(0.5)  # Why 0.5?

# ❌ In _validators.py
if len(data) > 100_000:  # Where does this come from?
    raise Error()
```

---

## Pattern: _core.py - Main Implementation

**Purpose:** Core business logic. Main classes and functions.

**Rules:**
1. Import types from _types.py
2. Import exceptions from _exceptions.py
3. Use constants from _constants.py
4. Keep file < 300 lines
5. One main class per file (usually)

**Good: Clean core implementation**
```python
"""Core processor implementation."""

from __future__ import annotations

import logging
from ._types import Config, Result, MetricType
from ._exceptions import ValidationError, ProcessingError
from ._constants import DEFAULT_BATCH_SIZE, MAX_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)

class Processor:
    """Main processor class."""

    def __init__(self, config: Config | None = None) -> None:
        self.config = config or Config()
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate configuration."""
        if self.config.timeout > MAX_TIMEOUT_SECONDS:
            raise ValidationError(
                f"Timeout {self.config.timeout} exceeds maximum "
                f"{MAX_TIMEOUT_SECONDS}"
            )

    def process(self, items: list) -> Result:
        """Process items."""
        if not items:
            return Result(success=True, items=[])

        try:
            return self._process_batch(items)
        except Exception as e:
            raise ProcessingError(f"Processing failed: {e}")

    def _process_batch(self, items: list) -> Result:
        """Internal batch processing."""
        # Implementation details
        return Result(success=True, items=items)
```

**Why:**
- Dependencies at top (types, exceptions, constants)
- Logging instance for debugging
- Config validated on init
- Public methods have clear contracts
- Private methods for implementation details

---

## Pattern: _utils.py - Helpers

**Purpose:** Reusable utility functions. Keep _core.py focused.

**Rules:**
1. Only utility functions, no classes
2. Pure functions preferred (no side effects)
3. Focused on one job
4. Document edge cases in docstrings

**Good: Focused utilities**
```python
"""Utility functions for mypackage."""

from typing import TypeAlias

Validator: TypeAlias = callable[[any], bool]

def validate_input(data: any, validator: Validator) -> bool:
    """Check if data passes validation."""
    if data is None:
        return False
    return validator(data)

def format_duration(seconds: float) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = seconds / 60
        return f"{minutes:.1f}m"

def retry_with_backoff(
    func: callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> any:
    """Retry function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
```

**Bad: Too much logic in utils**
```python
# ❌ Too generic
def do_thing(x, y, z):
    return x + y + z  # What does this mean?

# ❌ Side effects
def process_and_save(data):
    result = process(data)
    save_to_file(result)  # Side effect!
    return result
```

---

## Complete Example: Blog Post Package

```
blog_posts/
├── __init__.py
│   # Exports: Post, PostError, InvalidPostError
│
├── _types.py
│   # Post dataclass with title, content, author, created_at
│   # PublishStatus enum (DRAFT, PUBLISHED, ARCHIVED)
│   # PostMetadata dataclass
│
├── _exceptions.py
│   # PostError (base)
│   # InvalidPostError
│   # PublicationError
│
├── _constants.py
│   # MAX_TITLE_LENGTH = 200
│   # MAX_CONTENT_LENGTH = 50_000
│   # DEFAULT_STATUS = DRAFT
│   # SUPPORTED_FORMATS = {"html", "markdown"}
│
├── _core.py
│   # class BlogPost: main implementation
│   # create(), update(), publish(), archive()
│
├── _validators.py
│   # validate_title()
│   # validate_content()
│   # validate_metadata()
│
└── _formatters.py
    # format_as_html()
    # format_as_markdown()
    # generate_preview()
```

`__init__.py`:
```python
"""Blog post management."""

from ._core import BlogPost
from ._exceptions import PostError, InvalidPostError
from ._types import Post, PublishStatus

__all__ = ["BlogPost", "Post", "PublishStatus", "PostError", "InvalidPostError"]
```

---

## Summary

| File | Contains | Rules |
|------|----------|-------|
| `__init__.py` | Exports only | < 20 lines, use `__all__` |
| `_types.py` | Dataclasses, enums, TypeAlias | No logic, no functions |
| `_exceptions.py` | Exception hierarchy | Inherit from base, semantic names |
| `_constants.py` | Configuration defaults | UPPER_SNAKE_CASE, grouped, literals |
| `_core.py` | Main classes and logic | < 300 lines, one responsibility |
| `_utils.py` | Helper functions | Pure functions, reusable |

Following these patterns makes code predictable and maintainable.
