# Import Ordering Guidelines

Standard import organization for all Python files.

---

## The Five Groups

Always order imports in this exact sequence:

### 1. Future Imports (if needed)

```python
from __future__ import annotations
from __future__ import division
```

**Rules:**
- Must be first (before everything)
- Usually just `annotations`
- Enables newer Python features in older versions

**Why:**
- Changes how Python parses the file
- Must be at the very top

---

### 2. Standard Library Imports

```python
import json
import logging
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TypeAlias
```

**Rules:**
- No third-party packages
- Alphabetically sorted (optional but consistent)
- `import X` before `from X import Y`

**Examples:**
```python
# Good
import sys
import time
from pathlib import Path
from typing import Optional

# Acceptable (also alphabetical)
import json
import logging
from collections import defaultdict
from dataclasses import dataclass
```

---

### 3. Third-Party Packages

```python
import httpx
import pandas as pd
import pydantic
from fastapi import FastAPI
from pydantic import BaseModel
```

**Rules:**
- Any package not in stdlib
- Alphabetically sorted
- Again: `import X` before `from X import Y`

**Examples:**
```python
# Good
import httpx
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Bad - stdlib and third-party mixed
import json
import httpx  # ❌ Not together
from pathlib import Path
from fastapi import FastAPI
```

---

### 4. Local Imports (Absolute Paths)

```python
from mypackage.utils import helper
from mypackage._types import Config
from mypackage._core import Processor
```

**Rules:**
- Full path from project root
- Not relative imports
- Alphabetically sorted by path

**When to use:**
- Importing from elsewhere in project
- Makes dependencies explicit
- Works from any directory

**Example:**
```python
# Good - absolute, explicit
from mypackage.utils import validate_input
from mypackage._core import Processor
from mypackage._types import Config

# Bad - relative, unclear what package
from ..utils import validate_input
```

---

### 5. Local Imports (Relative Paths)

```python
from ._core import Processor
from ._types import Config, Result
from ._utils import validate_input
```

**Rules:**
- Only within the same package
- `from .module import X`
- Never `from ..` to go up levels (use absolute instead)
- Alphabetically sorted

**When to use:**
- Importing from sibling modules in same package
- Within package implementation
- More concise than absolute paths

**Example:**
```python
# In mypackage/_core.py

# Good - relative for siblings
from ._types import Config
from ._exceptions import ProcessingError

# Also good - absolute (both work)
from mypackage._types import Config

# Bad - going up levels
from ..utils import helper  # ❌ Use absolute instead
```

---

## Complete Example

```python
"""Module docstring explaining what this module does."""

# 1. Future imports
from __future__ import annotations

# 2. Standard library
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TypeAlias

# 3. Third-party packages
import httpx
import pandas as pd
from pydantic import BaseModel, Field

# 4. Local absolute imports
from mypackage._constants import MAX_RETRIES
from mypackage._exceptions import ValidationError
from mypackage._types import Config, Result
from mypackage.utils import retry_with_backoff

# 5. Local relative imports (within same package)
from ._core import BaseProcessor
from ._validators import validate_input

logger = logging.getLogger(__name__)
```

---

## Import Style Rules

### Use `import X` for Modules

```python
# Good
import json
import logging

# Less good (get specific names)
from logging import *  # ❌ Never use *
```

**Why:** Clear what you're using (`json.dumps()` vs `dumps()`)

### Use `from X import Y` for Specific Names

```python
# Good - when importing multiple items
from typing import Optional, TypeAlias, TypedDict
from pathlib import Path
from dataclasses import dataclass

# Also good - short module name
import pd as pandas  # ❌ Don't alias (use import pandas as pd)
```

### Alias When Name is Long or Unclear

```python
# Good - clarifies intent
import pandas as pd
import numpy as np
from urllib.parse import urlparse as parse_url

# Bad - unclear aliases
import pandas as p
import numpy as n_
```

---

## Preventing Circular Imports

Circular imports happen when modules import each other:

```python
# mypackage/_core.py
from ._types import Config

# mypackage/_types.py
from ._core import Processor  # ❌ Circular!
```

**Solutions:**

### 1. Move shared types to _types.py

```python
# _types.py - has Config
@dataclass
class Config:
    name: str

# _core.py - imports Config
from ._types import Config

class Processor:
    def __init__(self, config: Config):
        self.config = config
```

### 2. Use TYPE_CHECKING for type hints

```python
# _core.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._types import Config

class Processor:
    def __init__(self, config: "Config"):  # String annotation
        self.config = config
```

**Why:** TYPE_CHECKING block only runs during type checking, not at runtime.

### 3. Import inside function (last resort)

```python
# _core.py
class Processor:
    def process(self) -> Result:
        from ._types import Result  # Import only when needed
        return Result(success=True)
```

---

## Import Organization in Different File Types

### In _core.py (Implementation)

```python
from __future__ import annotations

# stdlib
import logging
from typing import Optional

# third-party
import httpx

# local - get types and exceptions first
from ._constants import DEFAULT_TIMEOUT
from ._exceptions import ProcessingError
from ._types import Config, Result

# local - utility imports
from ._utils import validate_input

logger = logging.getLogger(__name__)

class Processor:
    """Implementation here."""
```

### In _validators.py (Helpers)

```python
from __future__ import annotations

# stdlib
from typing import Callable

# local - import what you validate
from ._types import Config, Result
from ._exceptions import ValidationError

def validate_config(config: Config) -> None:
    """Validate configuration."""
    if not config.name:
        raise ValidationError("Name required")
```

### In __init__.py (Exports)

```python
"""Public API."""

# Only local imports for re-exporting
from ._core import Processor
from ._exceptions import ProcessorError
from ._types import Config, Result

__all__ = ["Processor", "Config", "Result", "ProcessorError"]
```

---

## Sorting Rules (Optional but Consistent)

Within each group, alphabetically sort by:

1. **Module name** first
2. **Import style** second (import before from)

```python
# Standard library - alphabetical
import json
import logging
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

# Third-party - alphabetical
import httpx
import pandas
from fastapi import FastAPI
from pydantic import BaseModel

# Local - alphabetical
from mypackage import utils
from mypackage._core import Processor
from mypackage._types import Config
from ._utils import helper
```

---

## Tools for Import Organization

### Use `isort` (Recommended)

Install: `pip install isort`

Check: `isort --check-only mypackage/`

Fix: `isort mypackage/`

Configuration in `pyproject.toml`:
```toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_mode = 3  # Vertical hanging indent
include_trailing_comma = true
force_single_line = false
```

### Use ruff

Newer, faster alternative to isort:

```bash
ruff check --select I mypackage/  # Check
ruff check --fix --select I mypackage/  # Fix
```

---

## Common Mistakes

```python
# ❌ Relative imports mixed with absolute
from mypackage._types import Config
from ._core import Processor

# ✅ Fix: Keep them separated (absolute first, then relative)
from mypackage._types import Config
from ._core import Processor

# ❌ Third-party mixed with stdlib
import json
import httpx  # Where does stdlib end?
from pathlib import Path

# ✅ Fix: Add blank line between groups
import json
from pathlib import Path

import httpx

# ❌ Wildcard imports
from mypackage._types import *

# ✅ Fix: Import specific names
from mypackage._types import Config, Result

# ❌ Unsorted within groups
import sys
import json  # Not alphabetical
from pathlib import Path

# ✅ Fix: Sort alphabetically
import json
import sys
from pathlib import Path
```

---

## Summary

1. **Five groups:** future → stdlib → third-party → local absolute → local relative
2. **Blank lines:** One between groups
3. **Alphabetical:** Optional but consistent within groups
4. **Style:** `import X`, `from Y import Z`
5. **Aliases:** Only for clarity (pandas as pd, numpy as np)
6. **Tools:** Use isort or ruff to automate

Following these rules makes imports predictable and maintainable.
