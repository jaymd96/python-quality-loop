# Interfaces and Structure: Text-Based and Modular Design

Principle 5 and 6: Text streams as interfaces and small, focused programs.

---

## Principle 5: Text Streams as Interface

### CLI Input/Output Patterns

Design CLIs that work with Unix pipes:

```python
import click
import sys

@click.command()
@click.argument("input", type=click.File("r"), default="-")
@click.argument("output", type=click.File("w"), default="-")
@click.option("--filter", help="Filter expression")
def process(input, output, filter):
    """Process records from INPUT to OUTPUT.

    Use '-' for stdin/stdout (default).
    """
    for line in input:
        record = parse_record(line)

        if filter and not should_include(record, filter):
            continue

        if record.is_valid():
            output.write(format_record(record) + "\n")

# Works with pipes:
# cat data.txt | python process.py | grep "ERROR"
# python process.py input.txt output.txt
# cat data.txt | python process.py --filter "status==error"
```

**Why:** Enables composition with Unix tools. Your program becomes part of larger pipelines.

### JSON Lines for Streaming

Use JSON Lines (`.jsonl`) for streaming structured data. One JSON object per line.

```python
import json
from pathlib import Path
from typing import Iterator, Any

def read_jsonl(path: Path) -> Iterator[dict]:
    """Read JSON Lines file, yielding parsed objects."""
    with open(path) as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def write_jsonl(records: Iterable[dict], path: Path) -> None:
    """Write records as JSON Lines."""
    with open(path, "w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

# Composable with shell tools:
# cat records.jsonl | jq '.status' | sort | uniq -c
# python process.py | jq --slurp 'group_by(.type)'
```

**Why:** Each line is independent. Can parse incrementally. Works with shell tools.

### Structured Output Formats

Support multiple output formats for different use cases:

```python
import click
import csv
import json
import sys
from dataclasses import asdict

@click.command()
@click.option(
    "--format",
    type=click.Choice(["json", "table", "csv", "jsonl"]),
    default="table",
    help="Output format"
)
def list_items(format: str):
    """List items in specified format."""
    items = fetch_items()

    if format == "json":
        # Pretty-printed JSON for humans
        click.echo(json.dumps([asdict(i) for i in items], indent=2))

    elif format == "jsonl":
        # JSON Lines for streaming/processing
        for item in items:
            click.echo(json.dumps(asdict(item)))

    elif format == "csv":
        # CSV for spreadsheets
        writer = csv.DictWriter(
            sys.stdout,
            fieldnames=["id", "name", "status", "created_at"]
        )
        writer.writeheader()
        for item in items:
            writer.writerow({
                "id": item.id,
                "name": item.name,
                "status": item.status,
                "created_at": item.created_at,
            })

    else:  # table
        # Human-readable table
        for item in items:
            click.echo(f"{item.id}\t{item.name}\t{item.status}")
```

**Why:** Different consumers need different formats. Programmers want JSON/CSV, humans want tables.

---

## Principle 6: Small, Focused Programs

### Module Size Guidelines

| Metric | Target | Maximum | What to do if exceeded |
|--------|--------|---------|-------|
| **Lines per module** | < 200 | 400 | Split by responsibility |
| **Functions per module** | < 10 | 15 | Extract related functions |
| **Classes per module** | < 3 | 5 | Move to separate files |
| **Parameters per function** | < 5 | 7 | Use config object |
| **Cyclomatic complexity** | < 5 | 10 | Simplify logic |

### Splitting Large Modules

When a module grows too large, split by responsibility:

```
# Before: monolithic (800 lines)
scheduler.py
  - Task class
  - Queue class
  - Worker class
  - Scheduler class
  - CLI commands
  - Config handling
  - Database access
  - Retry logic

# After: focused modules
scheduler/
├── __init__.py        # Public API only
├── _types.py          # Task, ScheduledTask dataclasses
├── _queue.py          # Queue implementation
├── _worker.py         # Worker implementation
├── _scheduler.py      # Scheduler orchestration
├── _cli.py            # CLI commands
├── _config.py         # Configuration
├── _db.py             # Database access
└── _retry.py          # Retry logic
```

Each module < 200 lines, single responsibility.

### Measuring Complexity

```python
# Simple (cyclomatic complexity ~2)
def process_item(item):
    if item.is_valid():
        return item.process()
    return None

# Moderate (cyclomatic complexity ~5)
def process_item(item):
    if not item:
        raise ValueError("item required")
    if not item.is_valid():
        logger.warning(f"Invalid item: {item}")
        return None
    if item.has_urgent_flag():
        return process_urgent(item)
    return item.process()

# Complex (cyclomatic complexity > 10)
def process_item(item):
    if not item:
        ...
    if not item.is_valid():
        ...
    if item.has_urgent_flag():
        ...
    if item.is_retry():
        ...
    if item.requires_approval():
        ...
    if item.is_sensitive():
        ...
    # Too many branches!
```

**Rule:** If you need a truth table to test all paths, it's too complex. Split it.

---

## Python-Specific Patterns

### Context Managers for Resource Management

```python
from contextlib import contextmanager
from typing import Iterator

@contextmanager
def database_transaction(conn: Connection) -> Iterator[Cursor]:
    """Execute operations in a transaction.

    Automatically commits on success, rolls back on error.
    """
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()

# Usage: Guarantees cleanup
with database_transaction(conn) as cursor:
    cursor.execute("INSERT ...")
    cursor.execute("UPDATE ...")
    # Auto-commits here
```

```python
# Composable with multiple context managers
@contextmanager
def temp_config(content: str) -> Iterator[Path]:
    """Create temporary config file."""
    with tempfile.NamedTemporaryFile(...) as f:
        yield Path(f.name)

# Use together
with database_transaction(conn) as cursor:
    with temp_config("debug: true") as config_path:
        cursor.execute(...)
```

### Decorators for Cross-Cutting Concerns

```python
from functools import wraps
import time

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator - separates retry logic from business logic."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except TransientError as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (2 ** attempt))
            raise last_error
        return wrapper
    return decorator

# Retry logic is separate from business logic
@retry(max_attempts=3, delay=1.0)
def fetch_data(url: str) -> dict:
    """Fetch data - no retry logic here."""
    response = httpx.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

# Usage
data = fetch_data("https://api.example.com/data")
```

### Protocols for Flexible Typing

```python
from typing import Protocol, Iterable

class Serializable(Protocol):
    """Any object that can be serialized to dict."""
    def to_dict(self) -> dict: ...

class Persistable(Protocol):
    """Any object that can be saved and loaded."""
    def save(self, path: Path) -> None: ...

    @classmethod
    def load(cls, path: Path) -> "Persistable": ...

# Functions accept protocols, not concrete types
def export_all(items: Iterable[Serializable], path: Path) -> None:
    """Export any serializable items - doesn't care about concrete type."""
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item.to_dict()) + "\n")

# Works with any type implementing Serializable
export_all(users, Path("users.jsonl"))
export_all(posts, Path("posts.jsonl"))
```

---

## Module Organization Checklist

Before considering a module "done":

**Size**
- [ ] Module under 400 lines
- [ ] Functions under 50 lines
- [ ] Functions have < 7 parameters
- [ ] No cyclomatic complexity > 10

**Responsibility**
- [ ] Can describe purpose in one sentence
- [ ] Related code grouped together
- [ ] Unrelated code in separate modules

**Composability**
- [ ] Functions accept standard types
- [ ] Functions return standard types
- [ ] No hidden state or side effects
- [ ] Can reorder function calls (not order-dependent)

**Testability**
- [ ] No I/O mixed with logic
- [ ] Dependencies injected (not hardcoded)
- [ ] Each function independently testable

**Maintainability**
- [ ] Clear naming (function names describe what they do)
- [ ] Docstrings explain why, not what
- [ ] Minimal comments (code should be clear)
- [ ] Type hints on public APIs

---

## Module Structure Template

```python
"""Module docstring explaining single purpose.

This module handles X, using Y pattern.
See also: related_module for Z functionality.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterator

logger = logging.getLogger(__name__)

# Constants (if any)
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Public classes and functions (most important first)
class MainClass:
    """Primary responsibility."""

def public_function() -> str:
    """Public API."""

# Private/helper functions
def _internal_function() -> None:
    """Internal helper."""
```

---

## Summary

**Text Interfaces:**
- Design CLIs that work with pipes
- Use JSON Lines for streaming
- Support multiple output formats

**Module Organization:**
- Keep modules < 400 lines
- Keep functions < 50 lines
- One responsibility per module
- Clear, composable interfaces

**Python Patterns:**
- Context managers for resource management
- Decorators for cross-cutting concerns
- Protocols for flexible types
- Generators for memory efficiency

Small, focused programs are easier to understand, test, and maintain.
