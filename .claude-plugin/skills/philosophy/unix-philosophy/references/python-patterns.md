# Python Patterns, Anti-Patterns, and Workflow

Applying Unix philosophy to Python development with practical patterns and integration with the workflow.

---

## Common Python Patterns

### 1. Iterator Chains

Instead of nested list comprehensions, use iterator chains:

```python
# Bad: Creates intermediate lists
all_items = [fetch_item(i) for i in range(1000)]
valid_items = [i for i in all_items if i.is_valid()]
recent_items = [i for i in valid_items if i.age < 30]
top_items = sorted(recent_items, key=lambda x: x.score, reverse=True)[:10]

# Good: Single pass with generators
from itertools import islice

def fetch_items():
    for i in range(1000):
        yield fetch_item(i)

def filter_valid(items):
    for item in items:
        if item.is_valid():
            yield item

def recent_only(items, days=30):
    for item in items:
        if item.age < days:
            yield item

def top_n(items, n=10):
    return sorted(items, key=lambda x: x.score, reverse=True)[:n]

# Compose
result = top_n(recent_only(filter_valid(fetch_items())))

# Only one pass through data, minimal memory
```

### 2. Dataclass-Based Configuration

```python
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class AppConfig:
    """Application configuration."""
    name: str
    debug: bool = False
    log_level: str = "INFO"
    data_dir: Path = Path("./data")

    @classmethod
    def from_file(cls, path: Path) -> "AppConfig":
        """Load config from JSON file."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "debug": self.debug,
            "log_level": self.log_level,
            "data_dir": str(self.data_dir),
        }

# Usage
config = AppConfig.from_file(Path("config.json"))
# config.name → automatic validation, type hints
```

### 3. Factory Functions

```python
# Bad: Multiple classes with different interfaces
class JSONProcessor: ...
class CSVProcessor: ...
class YAMLProcessor: ...

# Usage is inconsistent
json_proc = JSONProcessor(path)
csv_proc = CSVProcessor()
csv_proc.load(path)

# Good: Factory function with consistent interface
def create_processor(format: str) -> Processor:
    """Create processor for specified format."""
    processors = {
        "json": JSONProcessor,
        "csv": CSVProcessor,
        "yaml": YAMLProcessor,
    }

    if format not in processors:
        raise ValueError(f"Unknown format: {format}")

    return processors[format]()

# Usage is consistent
processor = create_processor("json")
data = processor.load(path)
```

### 4. Dependency Injection

```python
# Bad: Dependencies hardcoded
class UserService:
    def __init__(self):
        self.db = Database()  # Hardcoded dependency
        self.logger = logging.getLogger(__name__)  # Hardcoded

    def get_user(self, user_id: int):
        self.logger.info(f"Getting user {user_id}")
        return self.db.query(...)

# Good: Dependencies injected
class UserService:
    def __init__(self, db: Database, logger: logging.Logger):
        self.db = db
        self.logger = logger

    def get_user(self, user_id: int):
        self.logger.info(f"Getting user {user_id}")
        return self.db.query(...)

# Testing: Easy to inject mocks
mock_db = MockDatabase()
test_logger = logging.getLogger("test")
service = UserService(mock_db, test_logger)
result = service.get_user(123)  # Uses mocks
```

---

## Anti-Patterns to Avoid

### 1. God Module

```python
# Bad: One file does everything (800+ lines)
app.py
  - Database setup
  - API routes
  - Business logic
  - Config parsing
  - CLI commands
  - Logging setup
  - Email notifications
  - External API calls

# Good: Split by responsibility
app/
  __init__.py
  _config.py       # Configuration only
  _database.py     # Database setup only
  _api.py          # Routes only
  _business.py     # Logic only
  _cli.py          # CLI only
  _email.py        # Email only
  _external.py     # External APIs only
```

**Why:** Large files are hard to test, understand, and maintain. Hard to reuse individual pieces.

### 2. Not-Invented-Here (NIH) Syndrome

```python
# Bad: Reimplementing solved problems
def validate_email(email: str) -> bool:
    # Hand-rolled regex that doesn't handle all cases
    return re.match(r"^[^@]+@[^@]+$", email)

def retry_request(func, times=3):
    # Hand-rolled retry without exponential backoff or jitter
    for attempt in range(times):
        try:
            return func()
        except Exception:
            if attempt == times - 1:
                raise

# Good: Use existing packages
from email_validator import validate_email
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def make_request(url):
    ...
```

**Why:** Existing packages handle edge cases you'll discover later. Maintained by others. Tested by many users.

### 3. Global State

```python
# Bad: Global dependencies
logger = logging.getLogger(__name__)  # Global
config = load_config()  # Global

def process_data(data):
    logger.info("Processing")  # Uses global
    timeout = config.timeout  # Uses global
    ...

# Good: Explicit dependencies
def process_data(data, logger, config):
    logger.info("Processing")  # Explicit
    timeout = config.timeout  # Explicit
    ...

# Testing: Easy to inject test values
test_logger = logging.getLogger("test")
test_config = Config(timeout=1)
process_data(data, test_logger, test_config)
```

**Why:** Hidden dependencies are hard to test. Explicit makes code clear and testable.

### 4. Mixed I/O and Logic

```python
# Bad: I/O mixed with logic
def calculate_total(items):
    total = sum(item.price for item in items)
    # Surprise! I/O side effect
    save_to_database(total)
    send_notification(f"Total: {total}")
    return total

# Good: Separate concerns
def calculate_total(items):
    """Pure function - no side effects."""
    return sum(item.price for item in items)

def save_calculation(total):
    """Handle side effects separately."""
    save_to_database(total)
    send_notification(f"Total: {total}")

# Usage: Clear when I/O happens
total = calculate_total(items)
if total > 100:
    save_calculation(total)
```

**Why:** Pure logic is testable, reusable, composable. I/O is hard to test.

### 5. Deep Inheritance

```python
# Bad: Tight coupling via inheritance
class Animal:
    def move(self): ...
    def sleep(self): ...

class Dog(Animal):
    def bark(self): ...
    def fetch(self): ...

class Puppy(Dog):
    def play(self): ...
    def whimper(self): ...

# Each level couples to parent
# Hard to test without parent
# Can't mix behaviors

# Good: Composition over inheritance
class Animal:
    def __init__(self, mover: Mover, sleeper: Sleeper):
        self.mover = mover
        self.sleeper = sleeper

class Dog(Animal):
    def __init__(self, mover, sleeper, barker: Barker):
        super().__init__(mover, sleeper)
        self.barker = barker

# Mix and match behaviors
# Each component independently testable
# Composable
```

**Why:** Composition is more flexible than inheritance. Less coupling.

---

## Workflow Integration

### Phase 0: Discovery

**Unix Philosophy application:**
- [ ] Identify core responsibility (what does this module do?)
- [ ] Check if existing packages solve this
- [ ] Consider composability (what types in? what types out?)
- [ ] Plan split into small, focused modules

### Phase 1: Implementation

**Design decisions:**
- [ ] Module split by responsibility (< 400 lines per module)
- [ ] Functions accept/return standard types (int, str, list, dict, Iterator)
- [ ] stdlib used where appropriate (pathlib, subprocess, dataclasses)
- [ ] Popular packages considered before building

**Code review checklist:**
- [ ] Does each module do one thing?
- [ ] Are functions composable (standard in/out)?
- [ ] Is stdlib used (pathlib, subprocess, dataclasses)?
- [ ] Were existing packages considered?
- [ ] Is module under 400 lines?
- [ ] Do functions have < 7 parameters?
- [ ] No global state or hardcoded dependencies?
- [ ] No mixed I/O and logic?

### Phase 2: Refinement

**Code quality:**
- [ ] Test coverage of business logic
- [ ] Dependencies injected (not hardcoded)
- [ ] I/O separated from logic
- [ ] Error handling appropriate
- [ ] Performance acceptable

### Phase 3: Completion

**Final review:**
- [ ] No remaining god modules
- [ ] Clear composition paths between modules
- [ ] Documentation shows usage patterns
- [ ] Test coverage > 85% for logic
- [ ] Ready for reuse by other projects

---

## Metrics and Monitoring

### Module Health Metrics

```python
# Check these periodically

# 1. Lines per module
python -m py_compile mymodule.py
wc -l mymodule.py

# 2. Cyclomatic complexity
pip install radon
radon cc mymodule.py --average

# 3. Test coverage
pip install coverage
coverage run -m pytest
coverage report

# 4. Type hints
pip install pytype
pytype mymodule.py

# 5. Dependency count
pip list | wc -l
```

### Sample Targets

- Lines per module: < 300
- Cyclomatic complexity: < 5 average
- Test coverage: > 85%
- Type hints: 100% on public APIs
- Dependencies: < 20 production packages

---

## Learning More

**Books:**
- "The Art of Unix Programming" by Eric S. Raymond
- "Clean Architecture" by Robert C. Martin

**Tools:**
- `pylint` - Code style and complexity
- `radon` - Cyclomatic complexity
- `mypy` - Type checking
- `pytest` - Testing framework
- `black` - Code formatting

**Practice:**
- Refactor code to remove god modules
- Write small, testable functions
- Practice composition (pipe functions together)
- Use protocols instead of inheritance

---

## Summary

**Patterns:**
- Iterator chains for memory efficiency
- Dataclasses for configuration
- Factory functions for flexibility
- Dependency injection for testability

**Anti-Patterns:**
- God modules (split into pieces)
- NIH syndrome (use existing packages)
- Global state (inject dependencies)
- Mixed I/O and logic (separate concerns)
- Deep inheritance (use composition)

**Goals:**
- Small, focused modules
- Composable functions
- Testable code
- Reusable pieces

Unix philosophy applied: **Do one thing well. Compose via interfaces. Leverage existing tools.**
