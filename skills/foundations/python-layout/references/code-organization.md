# Code Organization Within Files

How to structure files for readability and predictability.

---

## File Structure Template

Every module should follow this pattern:

```python
"""Module docstring.

Describe what this module does in 1-3 sentences.
Mention any key concepts or entry points.
"""

# 1. Future imports
from __future__ import annotations

# 2. Imports (in order: stdlib, third-party, local)
import logging
from pathlib import Path
from typing import Optional

import httpx

from mypackage._types import Config
from ._core import Base

# 3. Module-level logger
logger = logging.getLogger(__name__)

# 4. Constants (if any)
DEFAULT_TIMEOUT = 30

# 5. Public classes (most important first, alphabetically or logically)
class MainClass:
    """Main class for this module."""

# 6. Supporting classes
class Helper:
    """Helper class."""

# 7. Public functions
def public_function():
    """Public function."""

# 8. Private functions
def _internal_function():
    """Internal helper function."""
```

**Key rules:**
1. Docstring first (no code before it)
2. Imports organized
3. Logger next (if used)
4. Constants (if any)
5. Classes (most important first)
6. Functions
7. Blank lines between sections

---

## Class Method Ordering

Order methods within a class this way:

```python
class Example:
    """Example class showing method order."""

    # 1. Class variables and docstring
    """Class docstring."""

    class_var = "shared by all instances"

    # 2. __init__ and other constructors
    def __init__(self, name: str) -> None:
        """Initialize the instance."""
        self.name = name
        self._config = {}

    # 3. Properties (@property)
    @property
    def config(self) -> dict:
        """Get configuration."""
        return self._config.copy()

    @property
    def display_name(self) -> str:
        """Get display name."""
        return self.name.title()

    # 4. Public methods (most important first)
    def process(self, data: dict) -> bool:
        """Main public method."""
        return self._validate(data)

    def update(self, **kwargs) -> None:
        """Update configuration."""
        self._config.update(kwargs)

    # 5. Private methods
    def _validate(self, data: dict) -> bool:
        """Validate input data."""
        return bool(data)

    def _prepare(self) -> None:
        """Prepare for processing."""
        self._config.setdefault("ready", True)

    # 6. Magic methods (__repr__, __eq__, etc.)
    def __repr__(self) -> str:
        """Return string representation."""
        return f"{self.__class__.__name__}(name={self.name!r})"

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, Example):
            return NotImplemented
        return self.name == other.name
```

**Order of methods:**

| Section | Purpose | Examples |
|---------|---------|----------|
| 1. **Class docstring** | Document class | Three-line description |
| 2. **Class variables** | Shared state | `class_var = "value"` |
| 3. **`__init__`** | Constructor | Initialize instance |
| 4. **Properties** | Computed attributes | `@property def x()` |
| 5. **Public methods** | Main interface | `def process()` |
| 6. **Private methods** | Implementation | `def _validate()` |
| 7. **Magic methods** | Dunder methods | `__repr__`, `__eq__` |

---

## Complete Example: BlogPost Class

```python
"""Blog post management."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class BlogPost:
    """Represents a blog post."""

    def __init__(
        self,
        title: str,
        content: str,
        author: str,
    ) -> None:
        """Initialize a blog post.

        Args:
            title: Post title (max 200 chars)
            content: Post content (max 50k chars)
            author: Author name

        Raises:
            ValueError: If title is empty or too long
        """
        if not title or len(title) > 200:
            raise ValueError("Title must be 1-200 characters")

        self.title = title
        self.content = content
        self.author = author
        self.created_at = datetime.now()
        self._status = "draft"
        self._tags: list[str] = []

    # Properties
    @property
    def status(self) -> str:
        """Get post status."""
        return self._status

    @property
    def summary(self) -> str:
        """Get first 100 characters as summary."""
        return self.content[:100]

    @property
    def word_count(self) -> int:
        """Count words in content."""
        return len(self.content.split())

    @property
    def tags(self) -> list[str]:
        """Get tags (read-only copy)."""
        return self._tags.copy()

    # Public methods
    def publish(self) -> None:
        """Publish the post."""
        if self._status != "draft":
            raise ValueError(f"Cannot publish post with status {self._status}")
        self._status = "published"
        logger.info(f"Published post: {self.title}")

    def archive(self) -> None:
        """Archive the post."""
        self._status = "archived"
        logger.info(f"Archived post: {self.title}")

    def add_tag(self, tag: str) -> None:
        """Add a tag to the post."""
        if tag not in self._tags:
            self._tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the post."""
        if tag in self._tags:
            self._tags.remove(tag)

    def update_content(self, new_content: str) -> None:
        """Update post content."""
        if not new_content:
            raise ValueError("Content cannot be empty")
        self.content = new_content

    # Private methods
    def _validate_status(self) -> bool:
        """Check if post is in valid state."""
        valid_statuses = {"draft", "published", "archived"}
        return self._status in valid_statuses

    def _format_as_markdown(self) -> str:
        """Format post as markdown."""
        header = f"# {self.title}\n\n"
        meta = f"*By {self.author} on {self.created_at.date()}*\n\n"
        return header + meta + self.content

    # Magic methods
    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"BlogPost(title={self.title!r}, "
            f"author={self.author!r}, "
            f"status={self._status!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality based on title and content."""
        if not isinstance(other, BlogPost):
            return NotImplemented
        return self.title == other.title and self.content == other.content

    def __lt__(self, other: BlogPost) -> bool:
        """Compare posts by creation time."""
        if not isinstance(other, BlogPost):
            return NotImplemented
        return self.created_at < other.created_at

    def __len__(self) -> int:
        """Return word count."""
        return self.word_count
```

**What makes this well-organized:**
- Docstring explains purpose and usage
- Constructor initializes all attributes
- Properties provide computed attributes
- Public methods are the main API
- Private methods handle implementation details
- Magic methods at the end
- Each section has clear purpose

---

## Spacing and Readability

```python
"""Module with proper spacing."""

import logging

logger = logging.getLogger(__name__)


# Blank line between sections
class FirstClass:
    """First class."""

    def method(self) -> None:
        """Method."""
        pass


class SecondClass:
    """Second class."""

    def method(self) -> None:
        """Method."""
        pass


# Blank line before functions
def public_function() -> None:
    """Public function."""
    pass


def _private_function() -> None:
    """Private function."""
    pass
```

**Rules:**
- Two blank lines between top-level definitions (classes, functions)
- One blank line between class methods
- One blank line between sections in a class
- No extra blank lines within functions

---

## Function vs Method Organization

### Standalone Functions

In `_utils.py` or similar:

```python
"""Utility functions."""

def format_date(date: datetime) -> str:
    """Format date as ISO string."""
    return date.isoformat()


def parse_duration(seconds: int) -> str:
    """Parse duration into human-readable format."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    return f"{minutes}m"


def validate_email(email: str) -> bool:
    """Check if string is a valid email."""
    return "@" in email and "." in email


def retry_with_backoff(func, max_retries=3):
    """Retry function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### Class Methods

In `_core.py`:

```python
"""Main implementation."""

class DataProcessor:
    """Process data with validation."""

    def __init__(self, config: Config) -> None:
        """Initialize processor."""
        self.config = config

    def process(self, items: list) -> list:
        """Process items."""
        return [self._process_one(item) for item in items]

    def _process_one(self, item: any) -> any:
        """Process single item."""
        return item
```

**Key difference:**
- Functions: Standalone, stateless, take data as parameters
- Methods: Tied to object, can use `self`, maintain state

---

## Docstring Placement

Always put docstring immediately after the signature:

```python
# Good
class MyClass:
    """Class docstring."""

    def method(self, x: int) -> int:
        """Method docstring."""
        return x * 2


# Bad - docstring in wrong place
class MyClass:

    def method(self, x: int) -> int:
        # Comment here (not a docstring!)
        return x * 2
```

**Why:** Docstrings are accessible via `__doc__`, comments are not. Tools rely on docstrings.

---

## Grouping Related Methods

When you have many methods, group them logically:

```python
class APIClient:
    """HTTP API client."""

    def __init__(self, base_url: str) -> None:
        """Initialize with base URL."""
        self.base_url = base_url

    # ===== GET operations =====

    def get(self, path: str) -> dict:
        """Fetch data from endpoint."""
        return self._request("GET", path)

    def get_item(self, item_id: str) -> dict:
        """Fetch single item."""
        return self.get(f"/items/{item_id}")

    # ===== POST operations =====

    def create(self, data: dict) -> dict:
        """Create new item."""
        return self._request("POST", "/items", data)

    def update(self, item_id: str, data: dict) -> dict:
        """Update existing item."""
        return self._request("POST", f"/items/{item_id}", data)

    # ===== Internal helpers =====

    def _request(self, method: str, path: str, data: dict | None = None) -> dict:
        """Execute HTTP request."""
        # Implementation
        pass
```

**Why:** Makes it easy to find related methods without scrolling past unrelated code.

---

## Summary

**File structure:**
1. Module docstring
2. Imports (organized)
3. Logger (if needed)
4. Constants
5. Classes (most to least important)
6. Functions

**Class structure:**
1. Class docstring
2. Class variables
3. `__init__`
4. Properties (`@property`)
5. Public methods
6. Private methods
7. Magic methods (`__repr__`, `__eq__`, etc.)

**Spacing:**
- Two blank lines between top-level definitions
- One blank line between class methods
- One blank line between sections

Following this structure makes code predictable and easy to navigate.
