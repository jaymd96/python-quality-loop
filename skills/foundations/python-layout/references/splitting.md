# When to Split vs Combine Modules

Guidance on file organization and when to break code into separate files.

---

## File Size Limits

These are guidelines, not hard rules. They help maintain readability.

| Type | Limit | When to Split |
|------|-------|--------------|
| **Module file** | < 300 lines | Hitting limit = too much responsibility |
| **Class** | < 25 methods | Large class = extract helpers |
| **Function** | < 50 lines | Most functions are 5-20 lines |
| **Method** | < 30 lines | Extract private helpers for clarity |

**The principle:** If you're explaining the file, you probably need to split it.

---

## Decision Tree: When to Split

```
Is the file > 300 lines?
    ├─ Yes → Split it
    │
    └─ No
        Are there 2+ distinct responsibilities?
            ├─ Yes → Consider splitting
            │
            └─ No → Keep together
```

### Responsibility Test

Ask: "What is this module's ONE job?"

**Good answers:**
- "Validate user input"
- "Process data batches"
- "Format output for display"

**Bad answers:**
- "Do everything related to users" ← Too broad
- "Handle data" ← Vague
- "Validate, process, and format" ← Three jobs!

---

## Examples: When to Split

### Example 1: Data Processor Class

**Too much (single file):**
```python
# _processor.py (450 lines)

class DataProcessor:
    def process(self, data): ...
    def validate_input(self, data): ...
    def transform_schema(self, data): ...
    def apply_rules(self, data): ...
    def format_output(self, data): ...
    def export_to_csv(self, data): ...
    def export_to_json(self, data): ...
    def cache_result(self, data): ...
    def log_metrics(self, data): ...
    # ... 40 more methods
```

**Better (split responsibly):**
```
# _core.py (120 lines)
class DataProcessor:
    def process(self, data): ...
    def _validate_input(self, data): ...

# _schema.py (80 lines)
class SchemaTransformer:
    def transform(self, data): ...

# _formatters.py (100 lines)
def format_csv(data): ...
def format_json(data): ...

# _exporters.py (90 lines)
class Exporter:
    def export(self, data, format): ...
    def cache(self, data): ...
```

**Why split:**
- Each file now has one job
- Can import SchemaTransformer without loading formatters
- Easy to test each component
- Clear where to find functionality

---

### Example 2: API Client

**Too much (single file):**
```python
# api_client.py (600+ lines)

class APIClient:
    # Auth methods
    def login(self): ...
    def logout(self): ...
    def refresh_token(self): ...

    # User endpoints
    def get_user(self, id): ...
    def update_user(self, id, data): ...
    def list_users(self): ...

    # Post endpoints
    def get_post(self, id): ...
    def create_post(self, data): ...
    def delete_post(self, id): ...

    # Comment endpoints
    def get_comment(self, id): ...
    def create_comment(self, data): ...

    # Retry logic
    def _retry(self, func): ...

    # Error handling
    def _handle_error(self, response): ...

    # Request formatting
    def _format_request(self, method, path, data): ...
```

**Better (keep related together, split concepts):**
```
_core.py (150 lines)
    class APIClient:
        def __init__(self, base_url): ...
        def _request(self, method, path): ...

_auth.py (80 lines)
    class AuthMixin:
        def login(self): ...
        def logout(self): ...

_users.py (100 lines)
    class UsersMixin:
        def get_user(self): ...
        def list_users(self): ...

_posts.py (120 lines)
    class PostsMixin:
        def get_post(self): ...
        def create_post(self): ...

_errors.py (50 lines)
    def handle_api_error(response): ...
    class APIError(Exception): ...

__init__.py
    from ._core import APIClient
    from ._auth import AuthMixin
    # Use mixins: class APIClient(APIClient, AuthMixin, UsersMixin, PostsMixin)
```

**Or simpler (separate endpoints module):**
```
_client.py (120 lines)
    class APIClient:
        def _request(self, method, path): ...

_endpoints.py (200 lines)
    class Endpoints:
        def get_user(self): ...
        def list_users(self): ...
        def get_post(self): ...
```

---

## When NOT to Split (Keep Together)

### Keep Together: Related Concepts

```python
# _types.py - Keep all types together
@dataclass
class User:
    name: str
    email: str

@dataclass
class Post:
    title: str
    author_id: int

# Not: _user_types.py and _post_types.py
```

**Why:** Types are thin, fast to parse, often imported together.

### Keep Together: Utility Helpers

```python
# _utils.py - Keep related helpers together
def format_date(date): ...
def format_currency(amount): ...
def format_duration(seconds): ...

# Not: _date_formatting.py, _currency_formatting.py, etc.
```

**Why:** Helpers are small, utility-focused, accessed together.

### Keep Together: Exception Hierarchy

```python
# _exceptions.py - All exceptions together
class ProcessorError(Exception): ...
class ValidationError(ProcessorError): ...
class TimeoutError(ProcessorError): ...

# Not: _validation_errors.py, _timeout_errors.py
```

**Why:** Exception hierarchy is cohesive, imported together, usually small.

---

## Splitting Pattern: Extract by Responsibility

```
Original file with too much:

┌─ Validation
├─ Transformation
└─ Export

Split into:

_validators.py
├─ validate_schema()
├─ validate_types()
└─ ValidationError

_transformers.py
├─ TransformPipeline
├─ apply_rules()
└─ TransformError

_exporters.py
├─ CSVExporter
├─ JSONExporter
└─ ExportError
```

Each file:
- Has one responsibility
- Imports shared types from _types.py
- Imports shared exceptions from _exceptions.py
- Can be tested independently

---

## Creating Subpackages

Create a subpackage when:

1. **Feature has 3+ files** - More than 3 related files
2. **Has own types/exceptions** - Domain-specific concepts
3. **Could be used independently** - Self-contained feature
4. **Different maintainers** - Team owns specific feature

### Example: Subpackage Structure

```
mypackage/
├── __init__.py
├── _core.py
├── _types.py
├── _utils.py
└── reports/                 # Subpackage
    ├── __init__.py          # Exports: Report, ReportError
    ├── _core.py             # ReportGenerator class
    ├── _types.py            # Report dataclass
    ├── _exceptions.py       # ReportError
    ├── _formatters.py       # PDF, Excel formatters
    └── _validators.py       # Report validation
```

### When NOT to Create Subpackage

```
# Bad: Over-engineering
myutils/
    ├── __init__.py
    ├── _date.py             # Just formatting functions
    └── _string.py           # Just string functions

# Better: Keep as _utils.py
mypackage/
    ├── _utils.py            # All helpers in one file
```

---

## Flat vs Hierarchical Subpackages

### Flat (Preferred)

```
mypackage/
├── __init__.py
├── _core.py
├── reports/                 # Subpackage
│   ├── __init__.py
│   ├── _core.py
│   └── _formatters.py
├── cache/                   # Subpackage
│   ├── __init__.py
│   └── _core.py
```

**Why:** Easy to navigate, clear structure

### Hierarchical (Avoid)

```
mypackage/
├── __init__.py
└── features/
    ├── __init__.py
    ├── reporting/           # Deep nesting
    │   ├── __init__.py
    │   └── _core.py
    └── caching/
        ├── __init__.py
        └── _core.py
```

**Problem:** Extra import depth (`from mypackage.features.reporting import Report`)

---

## Decision Framework

### Line Count Heuristic

```
< 100 lines
    └─ Keep in one file ✓

100-300 lines
    ├─ Single responsibility? → Keep together ✓
    └─ Multiple concerns? → Split ✓

> 300 lines
    └─ Always split (too much) ✓
```

### Responsibility Heuristic

```
One job?
    ├─ Yes → One file ✓
    └─ No  → Multiple files (one per job) ✓

Imports together?
    ├─ Always → Keep together (like types) ✓
    └─ Sometimes → Could split

Tested together?
    ├─ Yes → Keep together ✓
    └─ No  → Split for independent testing
```

### Practicality Heuristic

```
Will someone search for this code?
    ├─ By filename? → It needs its own file ✓
    └─ By searching? → Filename doesn't matter ✓

Do you jump between sections often?
    ├─ Yes → They should be together ✓
    └─ No  → Could split ✓

Can you describe it in one sentence?
    ├─ Yes → One module ✓
    └─ No  → Multiple modules
```

---

## Common Patterns

### Pattern 1: Core + Utilities

```
mypackage/
├── _core.py           # 150 lines - main class
├── _utils.py          # 80 lines - helper functions
├── _types.py          # 40 lines - data types
└── _exceptions.py     # 20 lines - errors
```

**Total:** ~290 lines, four focused files

### Pattern 2: Core + Formatters

```
mypackage/
├── _core.py           # 120 lines - main logic
├── _formatters.py     # 150 lines - output formatting
├── _validators.py     # 80 lines - input validation
├── _types.py          # 30 lines - types
└── _exceptions.py     # 20 lines - errors
```

**Total:** ~400 lines, five focused files

### Pattern 3: Modular with Subpackage

```
mypackage/
├── __init__.py
├── _core.py           # 100 lines
├── _types.py          # 50 lines
├── _utils.py          # 80 lines
└── formats/           # Subpackage
    ├── __init__.py
    ├── _json.py       # 60 lines
    ├── _csv.py        # 70 lines
    └── _xml.py        # 80 lines
```

**Total:** ~530 lines, still manageable with subpackage

---

## Migration: Combining vs Splitting

### When to Combine Small Files

```
Too many files:
    _users_validators.py (20 lines)
    _posts_validators.py (25 lines)
    _comments_validators.py (30 lines)

Better:
    _validators.py (75 lines) - all validators together
```

**Rule:** If related files are < 50 lines each, combine them.

### When to Split Large Files

```
Too big:
    _processor.py (450 lines) - everything

Better:
    _core.py (120 lines)
    _validators.py (100 lines)
    _formatters.py (120 lines)
    _utils.py (90 lines)
```

**Rule:** If > 300 lines, split by responsibility.

---

## Summary

| Guideline | Rule |
|-----------|------|
| **File size** | < 300 lines |
| **Class size** | < 25 methods |
| **Function size** | < 50 lines |
| **Keep together** | Types, exceptions, related utils |
| **Split when** | Different responsibilities |
| **Subpackage when** | 3+ files, self-contained |
| **Avoid** | Deep nesting, over-engineering |

Best approach: **Start simple, split when needed** rather than over-architect upfront.
