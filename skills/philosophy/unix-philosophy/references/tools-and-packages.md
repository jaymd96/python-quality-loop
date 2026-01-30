# Tools and Packages: Leverage Existing Solutions

Principle 3 and 4: Leverage stdlib and reuse existing tools instead of reimplementing.

---

## Principle 3: Leverage Standard Library

### Before Writing, Check stdlib

Standard library has mature, well-tested solutions for common problems:

| Need | stdlib Module | Don't Reinvent |
|------|---------------|----------------|
| **File paths** | `pathlib` | String manipulation of paths |
| **File operations** | `shutil` | Manual file copy/move/delete |
| **JSON handling** | `json` | Custom parsing or regex |
| **CSV handling** | `csv` | Manual string splitting |
| **Dates/times** | `datetime` | Custom date parsing |
| **Temporary files** | `tempfile` | Manual temp file management |
| **Subprocesses** | `subprocess` | `os.system()` or shell scripts |
| **URL parsing** | `urllib.parse` | Regex on URLs |
| **Configuration** | `configparser` | Manual INI parsing |
| **CLI arguments** | `argparse` | Manual `sys.argv` parsing |
| **Async I/O** | `asyncio` | Threading for I/O operations |
| **Data classes** | `dataclasses` | Manual `__init__` methods |
| **Enums** | `enum` | String constants everywhere |
| **Type hints** | `typing` | Docstring-based types |

### stdlib Patterns

**File operations with pathlib + shutil:**
```python
from pathlib import Path
import shutil
from datetime import datetime

def backup_config(src: Path, backup_dir: Path) -> Path:
    """Backup configuration file with timestamp."""
    # Create directory if it doesn't exist
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Add timestamp to backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = backup_dir / f"{src.stem}_{timestamp}{src.suffix}"

    # Copy with metadata preservation
    shutil.copy2(src, dest)

    return dest

# Usage
config_file = Path("/etc/myapp/config.yaml")
backups = Path("/var/backups/myapp")
backup = backup_config(config_file, backups)
print(f"Backed up to {backup}")
```

**Subprocess with proper error handling:**
```python
import subprocess
from pathlib import Path

def run_git_command(args: list[str], cwd: Path) -> str:
    """Run git command and return output."""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,  # Capture stdout/stderr
        text=True,            # Return strings, not bytes
        check=True,           # Raise on non-zero exit
    )
    return result.stdout.strip()

# Usage
try:
    current_branch = run_git_command(["branch", "--show-current"], Path("."))
    print(f"Current branch: {current_branch}")
except subprocess.CalledProcessError as e:
    print(f"Git error: {e.stderr}")
```

**Temporary files with automatic cleanup:**
```python
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

@contextmanager
def temp_config(content: str) -> Iterator[Path]:
    """Create temporary config file, cleanup on exit."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".yaml",
        delete=False  # Delete manually to avoid issues
    ) as f:
        f.write(content)
        temp_path = Path(f.name)

    try:
        yield temp_path
    finally:
        temp_path.unlink(missing_ok=True)  # Safe delete

# Usage
with temp_config("debug: true") as config_file:
    result = run_app(config_file)
# File automatically deleted here
```

**Dataclasses instead of manual classes:**
```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Config:
    """Configuration with automatic __init__, __repr__, __eq__."""
    name: str
    timeout: int = 30
    retries: int = 3
    tags: list[str] = field(default_factory=list)

# Automatic features:
config = Config(name="app", tags=["prod"])
print(config)  # Nice repr
assert config == Config(name="app", timeout=30, retries=3, tags=["prod"])

# vs manual class (100+ lines of boilerplate)
```

---

## Principle 4: Reuse Existing Tools

### Package Research First

Before implementing, always check:

1. **stdlib** - Is it in the standard library?
2. **PyPI** - Is there a well-maintained package?
3. **Awesome lists** - What do experts recommend?

```python
# Decision flow
Does stdlib have it?
    ├─ Yes → Use stdlib (best: no dependency, built-in, well-tested)
    │
    └─ No
        Does a popular package exist?
            ├─ Yes → Evaluate it
            │   ├─ Active maintenance?
            │   ├─ Good documentation?
            │   ├─ Large community?
            │   ├─ Security track record?
            │   └─ Lightweight vs your needs?
            │       ├─ Yes → Use it
            │       └─ No → Build custom
            │
            └─ No → Build custom solution
```

### Common Replacements

| Instead of Writing | Use Package | Why |
|--------------------|-------------|-----|
| HTTP requests | `httpx` or `requests` | HTTP is complex, these handle it |
| Rate limiting | `limits` or `tenacity` | Prevents service abuse |
| Retries | `tenacity` | Exponential backoff is non-trivial |
| Validation | `pydantic` | Type checking + error messages |
| CLI framework | `click` or `typer` | Argument parsing + help + validation |
| Config management | `pydantic-settings` | Environment variables + file parsing |
| Date handling | `pendulum` | Timezones are notoriously tricky |
| Async utilities | `anyio` | Abstracts asyncio complexity |
| Testing utilities | `pytest` + plugins | Better than unittest |
| Logging structure | `structlog` | JSON logs for production |

### Build vs Compose Decision

**COMPOSE (use existing package) when:**
- Well-maintained package exists
- Saves significant implementation time (> 4 hours)
- Provides battle-tested edge case handling
- Has active community/support
- No major version churn
- License compatible with your project

**BUILD (custom solution) when:**
- No suitable package exists
- Package would be heavier than custom solution
- Unique requirements not met by packages
- Security concerns with dependencies
- Package is unmaintained or declining
- Simple enough that benefit < maintenance burden

### Example: Build vs Compose

```python
# SCENARIO: Need to limit API calls to 100/second

# Option 1: COMPOSE with tenacity
import tenacity

@tenacity.retry(
    wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
    retry=tenacity.retry_if_result(lambda x: x is None),
    stop=tenacity.stop_after_attempt(3),
)
def fetch_data(url: str):
    """Fetch data with automatic retry."""
    response = httpx.get(url)
    if response.status_code == 429:
        return None  # Triggers retry
    return response.json()

# Pros: Battle-tested, handles edge cases, well-documented
# Cons: Extra dependency

# Option 2: BUILD custom
import time
from typing import Callable, TypeVar

T = TypeVar("T")

def retry_with_backoff(func: Callable[..., T], max_attempts: int = 3) -> T:
    """Retry with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            wait_time = 2 ** attempt
            time.sleep(wait_time)

# Pros: No dependency, simple
# Cons: Doesn't handle all edge cases (timeouts, rate limits, etc.)

# RECOMMENDATION: Compose. The package handles edge cases you'll discover later.
```

### Dependency Management

When using packages:

1. **Pin versions** - Reproducible builds
   ```
   httpx==0.24.1
   pydantic==2.5.0
   ```

2. **Use minimal set** - Every dependency is maintenance burden
   - Use `pip freeze` to see what's installed
   - Remove unused dependencies

3. **Review licenses** - Ensure compatibility with your project
   - MIT/Apache-2.0 = safe
   - GPL = requires source code sharing
   - AGPL = even more restrictive

4. **Monitor security** - Use `pip-audit` or `safety`
   ```bash
   pip-audit --fix
   safety check
   ```

---

## Comparison: Build vs Compose Examples

### Example 1: Retry Logic
```python
# Build custom (50 lines)
import time

def retry(func, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception:
            if attempt == max_attempts - 1:
                raise
            time.sleep(2 ** attempt)

# Compose existing (2 lines)
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def my_function():
    ...

# Winner: Compose (less code, more features, tested)
```

### Example 2: JSON Configuration
```python
# Build custom (100+ lines)
def load_config(path: str) -> dict:
    with open(path) as f:
        return json.load(f)

def validate_config(config: dict) -> list[str]:
    errors = []
    if "name" not in config:
        errors.append("name required")
    if not isinstance(config.get("timeout"), int):
        errors.append("timeout must be int")
    return errors

# Compose existing (10 lines)
from pydantic import BaseModel, Field

class Config(BaseModel):
    name: str
    timeout: int = Field(default=30, gt=0)
    debug: bool = False

config = Config.model_validate_json(config_json)

# Winner: Compose (automatic validation, type checking, error messages)
```

### Example 3: Small Tool
```python
# Build custom (20 lines)
def split_file(path: str, output_dir: str, chunk_size: int):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    chunk_num = 0

    with open(path) as f:
        chunk_lines = []
        for line in f:
            chunk_lines.append(line)
            if len(chunk_lines) >= chunk_size:
                out_path = output_dir / f"chunk_{chunk_num:05d}.txt"
                with open(out_path, "w") as out:
                    out.writelines(chunk_lines)
                chunk_num += 1
                chunk_lines = []

# Winner: Build (simple, no new dependency needed)
```

---

## Decision Framework

| Factor | Build | Compose |
|--------|-------|---------|
| **Implementation time** | Days/weeks | Hours/minutes |
| **Maintenance burden** | Ongoing | Automatic |
| **Edge cases** | You discover later | Already handled |
| **Dependencies** | None | 1 package |
| **Customization** | Complete control | Limited to API |
| **Security issues** | You fix | Maintainer fixes |
| **Community** | None | Helpful |

**Default: Compose unless good reason to build.**

---

## Summary

**Leverage stdlib:** Check `pathlib`, `subprocess`, `dataclasses`, `asyncio` before writing.

**Reuse packages:** Research before building. Popular packages save time and handle edge cases.

**Guidelines:**
- Stdlib first (no dependencies, well-tested)
- PyPI second (active projects, community support)
- Build last (only when justified)

The Unix philosophy: stand on the shoulders of giants, don't reinvent wheels.
