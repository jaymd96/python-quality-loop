# Project Layout Examples

Detailed comparison of src-layout vs flat-layout with real-world examples.

---

## src-layout (Recommended for Published Packages)

**When to use:**
- Publishing to PyPI or other package repositories
- Complex projects with multiple packages
- Projects that will be installed via pip
- Professional open-source libraries

**Structure:**
```
project-name/
├── pyproject.toml           # Project metadata and dependencies
├── src/
│   └── mypackage/           # Actual package code (importable as 'mypackage')
│       ├── __init__.py
│       ├── _core.py
│       ├── _types.py
│       ├── _exceptions.py
│       ├── _utils.py
│       └── _subpackage/     # Optional subpackages
│           ├── __init__.py
│           └── _module.py
├── tests/                   # Test suite (separate from package)
│   ├── conftest.py
│   ├── test_core.py
│   └── test_subpackage/
│       └── test_module.py
├── docs/                    # Documentation (optional)
│   ├── index.md
│   └── api.md
├── playground/              # Exploration and testing
│   └── package_exploration.py
└── README.md
```

**Key advantages:**
- Clear separation: package code in `src/`, tests elsewhere
- Prevents accidentally importing from project root
- Matches convention of most professional Python projects
- Better for CI/CD and deployment
- Forces explicit installation (package not importable until installed)

**Example pyproject.toml:**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mypackage"
version = "0.1.0"

[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
```

---

## flat-layout (For Simple Projects and Tools)

**When to use:**
- Simple projects, internal tools, scripts
- Projects that won't be published to PyPI
- Single-file or very small packages
- Educational projects, prototypes
- Tools meant to run directly from source

**Structure:**
```
project-name/
├── pyproject.toml           # Minimal project metadata
├── mypackage/               # Package at root level
│   ├── __init__.py
│   ├── _core.py
│   ├── _types.py
│   ├── _exceptions.py
│   └── _utils.py
├── tests/                   # Tests still separate
│   ├── conftest.py
│   ├── test_core.py
│   └── test_utils.py
├── playground/              # Exploration scripts
│   └── package_exploration.py
└── README.md
```

**Key advantages:**
- Simpler directory structure for small projects
- Faster to set up
- Package is importable immediately without installation
- Fine for tools that run directly from source

**Example pyproject.toml:**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mypackage"
version = "0.1.0"
```

---

## Comparing Both Layouts

| Aspect | src-layout | flat-layout |
|--------|-----------|------------|
| **Complexity** | Higher | Lower |
| **Publishing** | Ready for PyPI | Not recommended |
| **Installation** | `pip install mypackage` | Not installable |
| **Import from root** | Not possible | Possible (not recommended) |
| **Professional** | Yes | For small tools |
| **Setup time** | Longer initial setup | Quicker start |
| **Scalability** | Better for growth | Limited |
| **CI/CD** | Better support | Functional |

---

## Real-World Examples

### Example 1: Data Processing Library (src-layout)

Publishing a data processing library to PyPI:

```
data-processor/
├── pyproject.toml
├── src/
│   └── data_processor/
│       ├── __init__.py           # exports: Processor, ProcessingError
│       ├── _core.py              # Processor class
│       ├── _types.py             # ProcessorConfig, Result types
│       ├── _exceptions.py        # ProcessingError, ValidationError
│       ├── _validators.py        # Input validation functions
│       ├── _transformers.py      # Data transformation pipeline
│       └── _io/                  # IO subpackage
│           ├── __init__.py
│           ├── _readers.py
│           └── _writers.py
├── tests/
│   ├── test_core.py
│   ├── test_validators.py
│   ├── test_io/
│   │   ├── test_readers.py
│   │   └── test_writers.py
│   └── conftest.py
├── docs/
│   ├── index.md
│   ├── getting_started.md
│   ├── api_reference.md
│   └── examples.md
├── playground/
│   └── data_processor_exploration.py
├── README.md
└── CHANGELOG.md
```

Why src-layout:
- Published to PyPI for external use
- Multiple related subpackages (io, validators)
- Professional documentation needed
- Clear separation of concerns

### Example 2: Internal Analytics Tool (flat-layout)

Quick tool for team use, no external publishing:

```
team-analytics/
├── pyproject.toml
├── analytics/
│   ├── __init__.py           # exports: Analyzer, AnalysisResult
│   ├── _core.py              # Main Analyzer class
│   ├── _types.py             # AnalysisResult, MetricType
│   ├── _exceptions.py        # AnalysisError
│   ├── _processing.py        # Data processing logic
│   └── _utils.py             # Helpers
├── tests/
│   ├── test_core.py
│   ├── test_processing.py
│   └── conftest.py
├── playground/
│   └── analytics_exploration.py
└── README.md
```

Why flat-layout:
- Simple, internal-only tool
- Single package (no subpackages)
- Runs directly from source
- Small team, fewer concerns about installation

---

## Migration Path

If you start with flat-layout and want to scale:

1. **Create src/ directory**
2. **Move package into src/**
3. **Update pyproject.toml** to include build backend
4. **Tests already in separate directory** - no change needed
5. **Update CI/CD** to run from new structure

Both layouts can coexist during migration if needed.

---

## Decision Tree

```
Is this a package for PyPI?
    ├─ Yes → Use src-layout
    │
    └─ No
        Is it simple and internal?
            ├─ Yes → Use flat-layout
            │
            └─ No (growing complexity)
                → Start with flat, migrate to src-layout later
```

---

## Summary

- **src-layout**: Professional, scalable, ready for publication
- **flat-layout**: Simple, quick, for internal tools
- **Both**: Keep tests separate, use standard module files
- **Migrate**: Easy to transition from flat to src as project grows
