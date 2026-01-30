# Design Patterns: Single Responsibility and Composition

Principle 1 and 2: Do one thing well and compose via clear interfaces.

---

## Principle 1: Single Responsibility

### Module Design

Each module should have a single, clear purpose. When you can't describe it in one sentence, split it.

```python
# Good: Single responsibility
# _validation.py - only validation logic
def validate_email(email: str) -> bool:
    """Check if email format is valid."""
    return "@" in email and "." in email

def validate_phone(phone: str) -> bool:
    """Check if phone format is valid."""
    return len(phone) >= 10

# _formatting.py - only formatting logic
def format_email(email: str) -> str:
    """Format email for display."""
    return email.lower().strip()

def format_phone(phone: str) -> str:
    """Format phone for display."""
    return f"+1{phone[-10:]}"
```

```python
# Bad: Mixed responsibilities
# utils.py - does everything
def validate_email(email: str) -> bool: ...
def format_email(email: str) -> str: ...
def send_email(to: str, body: str) -> None: ...  # I/O mixed with validation
def parse_email_config(path: str) -> dict: ...   # Config mixed with email
```

**Why separate:** Each module becomes testable, reusable, and easy to understand.

### Function Design

Each function should do one job. If you'd describe it with "and", split it.

```python
# Good: Single operation per function
def load_config(path: Path) -> Config:
    """Load configuration from file."""
    with open(path) as f:
        return Config(**json.load(f))

def validate_config(config: Config) -> list[ConfigError]:
    """Validate configuration values."""
    errors = []
    if not config.name:
        errors.append(ConfigError("name required"))
    if config.timeout < 1:
        errors.append(ConfigError("timeout must be positive"))
    return errors

def apply_config(config: Config) -> None:
    """Apply configuration to system."""
    os.environ["APP_NAME"] = config.name
    os.environ["APP_TIMEOUT"] = str(config.timeout)

# Usage: Compose as needed
config = load_config(path)
errors = validate_config(config)
if not errors:
    apply_config(config)
```

```python
# Bad: Multiple operations bundled
def load_and_validate_and_apply_config(path: Path) -> None:
    """Load, validate, and apply config (all or nothing)."""
    # Can't load without validating
    # Can't validate without applying
    # Can't test pieces independently
    config = Config(**json.load(open(path)))
    if not config.name:
        raise ValueError("name required")
    os.environ["APP_NAME"] = config.name
```

**Why separate:** You can test loading, validation, and application independently. You can load without applying, or apply a config programmatically without loading from file.

### Size Guideline

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

# After: focused modules
scheduler/
├── __init__.py        # Public API only
├── _types.py          # Task, ScheduledTask dataclasses
├── _queue.py          # Queue implementation (100 lines)
├── _worker.py         # Worker implementation (150 lines)
├── _scheduler.py      # Scheduler orchestration (120 lines)
├── _cli.py            # CLI commands (80 lines)
└── _config.py         # Configuration (70 lines)
```

Each module now has a single responsibility and is < 200 lines.

---

## Principle 2: Compose Via Interfaces

### Composable Function Design

Functions should accept and return standard types (not custom wrappers). This enables composition.

```python
# Good: Composable - standard types in and out
def filter_active(items: Iterable[Item]) -> list[Item]:
    """Filter to active items only."""
    return [item for item in items if item.is_active]

def sort_by_date(items: Iterable[Item]) -> list[Item]:
    """Sort items by creation date (newest first)."""
    return sorted(items, key=lambda x: x.created_at, reverse=True)

def take_recent(items: Iterable[Item], n: int) -> list[Item]:
    """Take first N items."""
    return list(items)[:n]

# Compose freely
all_items = fetch_items()
result = take_recent(sort_by_date(filter_active(all_items)), 10)

# Or reorder composition
result = take_recent(filter_active(sort_by_date(all_items)), 5)

# Or use with generators
result = list(take_recent(filter_active(all_items), 10))
```

```python
# Bad: Non-composable - returns self, holds state
class ItemProcessor:
    def __init__(self, items: list[Item]):
        self.items = items  # Holds state

    def filter_active(self) -> "ItemProcessor":
        self.items = [i for i in self.items if i.is_active]
        return self  # Returns self, not data

    def sort_by_date(self) -> "ItemProcessor":
        self.items = sorted(self.items, key=lambda x: x.created_at)
        return self  # Always returns self

    def get_items(self) -> list[Item]:
        return self.items

# Can't reorder operations
# Can't test pieces independently
# Must use exact sequence
```

### Generator Pipelines

Use generators for memory-efficient composition of large datasets:

```python
def read_lines(path: Path) -> Iterator[str]:
    """Yield lines from file."""
    with open(path) as f:
        for line in f:
            yield line.strip()

def parse_records(lines: Iterable[str]) -> Iterator[Record]:
    """Parse lines into records."""
    for line in lines:
        if line:  # Skip empty lines
            yield Record.from_line(line)

def filter_valid(records: Iterable[Record]) -> Iterator[Record]:
    """Yield only valid records."""
    for record in records:
        if record.is_valid():
            yield record

def group_by_type(records: Iterable[Record]) -> Iterator[tuple[str, list[Record]]]:
    """Group records by type."""
    from itertools import groupby
    for type_name, group in groupby(records, key=lambda r: r.type):
        yield type_name, list(group)

# Compose: Memory efficient, processes one at a time
for record_type, records in group_by_type(
    filter_valid(
        parse_records(
            read_lines(path)
        )
    )
):
    print(f"Type {record_type}: {len(records)} records")
```

**Why generators:** Only loads needed data into memory. Can process gigabyte files with kilobytes of RAM.

### Function Parameter Guidelines

Functions become harder to test and compose as parameters increase:

```python
# Good: Clear parameters, easy to test
def process_data(data: list, timeout: int = 30) -> Result:
    """Process data with timeout."""
    ...

# Acceptable: Some flexibility
def process_data(
    data: list,
    timeout: int = 30,
    retries: int = 3,
    batch_size: int = 100,
) -> Result:
    """Process data with customization."""
    ...

# Bad: Too many parameters
def process_data(
    data: list,
    timeout: int,
    retries: int,
    batch_size: int,
    callback: Callable,
    verbose: bool,
    log_level: int,
) -> Result:
    """Too many parameters = hard to use."""
    # Hard to test all combinations
    # Easy to get wrong
    ...
```

**Rule:** Functions should have < 5 parameters. If more, consider a config object.

---

## Anti-Patterns

### God Module
```python
# Bad: One file does everything
scheduler.py (2000 lines)
    - Scheduling logic
    - Queue management
    - Worker pool
    - CLI interface
    - Config parsing
    - Logging
    - Database access
    - Email notifications

# Fix: Split by responsibility
scheduler/
    _scheduler.py  # Scheduling only
    _queue.py      # Queue only
    _worker.py     # Workers only
    _cli.py        # CLI only
    _config.py     # Config only
    _db.py         # Database only
    _notifications.py  # Notifications only
```

### Function with Side Effects
```python
# Bad: Function does one thing + side effect
def calculate_total(items: list) -> int:
    total = sum(item.price for item in items)
    save_to_database(total)  # Surprise side effect!
    return total

# Good: Separate concerns
def calculate_total(items: list) -> int:
    """Calculate total (pure, no side effects)."""
    return sum(item.price for item in items)

def save_calculation(total: int) -> None:
    """Save total to database."""
    save_to_database(total)

# Usage: Call both when needed
total = calculate_total(items)
if total > 100:
    save_calculation(total)
```

---

## Summary

**Single Responsibility:**
- One module = one purpose
- One function = one job
- Split when hitting 400 lines
- Can describe in one sentence

**Composition:**
- Accept standard types (list, dict, Iterable)
- Return standard types
- Enables reordering and testing
- Generators for memory efficiency

**Guidelines:**
- Modules < 400 lines
- Functions < 50 lines
- Parameters < 5
- One job per function

Modules designed this way are testable, reusable, and composable.
