# Implementation Guide: Generic Python Development Workflow

A step-by-step guide to using the Manager-Doer workflow for Python development.

## Prerequisites

Before starting, ensure you have:
- A Python project to work on
- Clear requirements for the module/feature
- Access to Claude Code with skill support

## Installation Options

### Option 1: Copy Skills to User Directory

Available in all projects:

```bash
# Create skills directory if needed
mkdir -p ~/.claude/skills

# Copy workflow skills
cp skills/*.md ~/.claude/skills/
```

### Option 2: Copy Skills to Project Directory

Available in this project only:

```bash
# Create skills directory in project
mkdir -p .claude/skills

# Copy workflow skills
cp skills/*.md .claude/skills/
```

### Option 3: Reference Skills Directly

Read skill files as needed without copying.

---

## Starting a New Module

### Step 1: Define Requirements

Write a clear requirement statement:

```
Module: data-processor

Description: Process CSV files and validate data integrity

Requirements:
1. Read CSV files of any size
2. Validate data against schema
3. Report validation errors with line numbers
4. Output cleaned data to new file

Constraints:
- Must handle files > 1GB (streaming)
- Must be thread-safe
- Error messages must be human-readable

Integration:
- Uses existing FileReader class
- Outputs to existing DataStore interface
```

### Step 2: Set Quality Gates

Use defaults or customize:

```yaml
# Default gates (recommended to start)
Quality Gates:
  Code Quality:
    - Zero critical issues
    - >= 85% zen-python compliance
    - Docstrings on public APIs

  Testing:
    - >= 5 scenarios tested
    - Zero runtime errors
    - Edge cases handled

  Integration:
    - No breaking changes
    - Follows existing patterns

  Documentation:
    - Public APIs documented
    - At least 1 usage example

# Optional: Add custom gates
  Performance:
    - Processes 1GB file in < 60 seconds
    - Memory usage < 500MB
```

### Step 3: Set Iteration Limit

```
Iteration Limit: 3

Rationale:
- Iteration 1: Core implementation
- Iteration 2: Quality improvements
- Iteration 3: Polishing

If not done by iteration 3, escalate for reassessment.
```

---

## Phase 0: Discovery

### Step 0.1: Review Existing Code

Use the code-review skill to understand the codebase:

```
Review the existing codebase at [path]:

1. How is data processing currently done?
2. What patterns are used for file handling?
3. Where should new code integrate?
4. What constraints exist?
```

Document findings.

### Step 0.2: Create Gap Analysis

```markdown
# Gap Analysis: data-processor

## Existing Code
- FileReader class handles file I/O (use this)
- DataStore interface for output (implement this)
- Logging uses structlog (follow this)

## What's Missing
- CSV parsing with streaming
- Schema validation
- Error collection and reporting
- Thread-safe processing

## Integration Points
- Input: FileReader.read_lines() -> Iterator[str]
- Output: DataStore.save(record: Record) -> None
- Errors: ErrorCollector.add(error: ValidationError)

## Dependencies
- polars (for efficient CSV parsing)
- pydantic (for schema validation)

## Risks
- Large file performance (need streaming)
- Memory pressure (need batching)
```

### Step 0.3: Create Technical Approach

```markdown
# Technical Approach: data-processor

## Architecture

```
CSV File
    │
    ▼
┌──────────────┐
│ CsvReader    │ (streaming)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Validator    │ (schema-based)
└──────┬───────┘
       │
   ┌───┴───┐
   ▼       ▼
Valid   Invalid
   │       │
   ▼       ▼
DataStore  ErrorCollector
```

## Key Components

1. CsvReader
   - Streams CSV in batches
   - Handles encoding issues
   - Memory-efficient

2. Validator
   - Schema-based validation
   - Collects all errors (doesn't stop on first)
   - Line number tracking

3. DataProcessor
   - Orchestrates reading -> validating -> storing
   - Thread-safe
   - Progress reporting

## Public API

```python
processor = DataProcessor(schema=MySchema)
result = processor.process("input.csv", "output.csv")
print(f"Processed {result.valid_count} records")
print(f"Errors: {len(result.errors)}")
```

## Implementation Sequence

1. CsvReader (foundation)
2. Validator (core logic)
3. DataProcessor (orchestration)
4. Integration tests
```

### Step 0.4: Submit for Approval

```
Phase 0 Complete

Submitting for Manager approval:
- Gap Analysis document
- Technical Approach document
- Proposed quality gates

Awaiting approval before Phase 1.
```

### Manager Response

Manager reviews and responds:

```
APPROVED for Phase 1

Notes:
- Good analysis of existing patterns
- Streaming approach is correct
- Add explicit error handling for encoding issues

Quality Gates: Confirmed as proposed
Iteration Limit: 3
```

---

## Phase 1: Development

### Iteration 1

#### Step 1: Implementation

Use python-coding skill:

```python
# src/data_processor/_reader.py
"""CSV reader with streaming support."""

from typing import Iterator
from pathlib import Path

class CsvReader:
    """Read CSV files in memory-efficient batches."""

    def __init__(self, *, batch_size: int = 1000) -> None:
        self._batch_size = batch_size

    def read_batches(self, path: Path) -> Iterator[list[dict]]:
        """Yield batches of rows from CSV file.

        Args:
            path: Path to CSV file.

        Yields:
            Lists of row dictionaries, batch_size at a time.

        Raises:
            FileNotFoundError: If file doesn't exist.
            CsvParseError: If CSV is malformed.
        """
        # Implementation...
```

#### Step 2: Organization

Use python-layout skill:

```
Reviewed structure:
- _reader.py: CSV reading (done)
- _validator.py: Schema validation (to do)
- _processor.py: Orchestration (to do)
- _types.py: Data types (to do)
- _exceptions.py: Error types (to do)
- __init__.py: Public exports

Layout follows existing patterns.
```

#### Step 3: Standards

Use zen-of-python skill:

```
Zen-Python Evaluation:

Compliance: 82%

Issues found:
1. Line 47: Nested if statements (4 levels)
   Fix: Use guard clauses

2. Line 63: Magic number 1000
   Fix: Use named constant BATCH_SIZE

3. Line 89: Implicit None return
   Fix: Make explicit

All issues fixed. New compliance: 88%
```

#### Step 4: Review

Use code-review skill:

```
Code Review Results:

Critical: 0
Major: 1
Minor: 2

Major Issues:
1. CsvReader.read_batches doesn't handle encoding errors
   Location: _reader.py:52
   Impact: Crashes on non-UTF8 files
   Fix: Add encoding parameter and error handling

Minor Issues:
1. Missing type hint on internal method
2. Docstring could have example

Major issue fixed. Re-review: 0 critical, 0 major.
```

#### Step 5: Experimentation

Use python-repl skill:

```python
# Test scenarios

# 1. Happy path
>>> reader = CsvReader()
>>> batches = list(reader.read_batches(Path("test.csv")))
>>> len(batches)
3
>>> len(batches[0])
1000

# 2. Empty file
>>> list(reader.read_batches(Path("empty.csv")))
[]

# 3. Missing file
>>> list(reader.read_batches(Path("missing.csv")))
FileNotFoundError: ...

# 4. Encoding error
>>> list(reader.read_batches(Path("latin1.csv")))
CsvParseError: Encoding error at byte 1234

# 5. Large file
>>> # 10 million rows
>>> reader = CsvReader(batch_size=10000)
>>> sum(len(b) for b in reader.read_batches(large_file))
10000000

All 5 scenarios pass.
```

#### Step 6: Testing

Use python-testing skill:

```python
# tests/test_reader.py

def test_read_batches_yields_correct_batch_size():
    reader = CsvReader(batch_size=100)
    batches = list(reader.read_batches(fixture_path))
    assert all(len(b) == 100 for b in batches[:-1])

def test_empty_file_yields_no_batches():
    reader = CsvReader()
    assert list(reader.read_batches(empty_file)) == []

def test_missing_file_raises_not_found():
    reader = CsvReader()
    with pytest.raises(FileNotFoundError):
        list(reader.read_batches(Path("missing.csv")))

# All tests pass
```

#### Iteration 1 Report

```markdown
# Iteration 1 Report: data-processor

## Status
- Implementation: 40% (CsvReader complete)
- Zen-Python: 88%
- Code-Review: 0 critical, 0 major, 2 minor
- Tests: 5 scenarios, 5 passed

## Gate Self-Evaluation
- Code Quality: PASS (0 critical, 88% zen)
- Testing: PASS (5 scenarios, 0 errors)
- Integration: PASS (follows patterns)
- Documentation: PARTIAL (needs examples)

## Summary
- CsvReader implemented with streaming
- Encoding errors handled
- Memory-efficient batching works

## Recommendation
[ ] ITERATE

Focus next on:
1. Validator implementation
2. DataProcessor orchestration
3. Complete documentation
```

### Manager Evaluation

```
ITERATE

Gate Status:
  Code Quality: PASS
  Testing: PASS
  Integration: PASS
  Documentation: PARTIAL

Specific Improvements:
1. Continue with Validator implementation
2. Continue with DataProcessor
3. Add usage example to docstrings

Iteration: 1 of 3
```

### Iteration 2

Continue with Steps 1-6, implementing Validator and DataProcessor.

[Similar process...]

### Iteration 3

Final polishing iteration.

[Similar process...]

### Manager Final Evaluation

```
ACCEPT

All quality gates passing. Code is production-ready.

Gate Status:
  Code Quality: PASS (0 critical, 91% zen-python)
  Testing: PASS (12 scenarios, 0 errors)
  Integration: PASS (follows all patterns)
  Documentation: PASS (complete with examples)

Proceed to Phase 3: Finalize and integrate.
```

---

## Phase 3: Completion

### Final Checklist

- [ ] Remove all debug code
- [ ] Remove all TODO comments
- [ ] Complete all docstrings
- [ ] Add module README
- [ ] Run full test suite
- [ ] Verify integration works
- [ ] Clean commit history
- [ ] Ready for merge

### Final Steps

```bash
# Run full test suite
pytest tests/ -v

# Check type hints
mypy src/data_processor

# Format code
ruff format src/ tests/

# Create clean commit
git add -A
git commit -m "Add data-processor module

Implements CSV processing with streaming, validation,
and error collection. Memory-efficient for large files.

- CsvReader: Streaming CSV reader with batching
- Validator: Schema-based validation
- DataProcessor: Orchestration with progress reporting

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Common Scenarios

### Scenario: ESCALATE Decision

If you hit iteration limit or find fundamental issues:

```
ESCALATE

Issue: Performance requirement cannot be met

Details: Processing 1GB in < 60s requires parallel
         processing, but existing FileReader is not
         thread-safe. Redesign needed.

Required Action:
1. Evaluate making FileReader thread-safe
2. OR use different file access pattern
3. Team decision needed

Iteration: 3 of 3 (limit reached)
```

### Scenario: Scope Change Request

If requirements change mid-development:

```
SCOPE CHANGE REQUEST

Current: Process single CSV file
Proposed: Process directory of CSV files

Impact:
- New DirectoryProcessor class needed
- Iteration limit may need extension
- Quality gates unchanged

Awaiting Manager approval before implementing.
```

### Scenario: Blocker Found

If blocked during development:

```
BLOCKER

Issue: Required package 'fastcsv' is not approved
       for production use.

Impact: Cannot implement streaming as planned.

Options:
1. Use approved 'polars' instead (different API)
2. Get 'fastcsv' approved (2-3 day process)
3. Implement custom streaming (more work)

Awaiting guidance.
```

---

## Tips for Success

### For Managers

1. **Be specific** - "Fix encoding handling in _reader.py:52" not "improve error handling"
2. **Use gates** - Decide based on measurable criteria
3. **Enforce limits** - Escalate if limit reached
4. **Document decisions** - Track iteration history

### For Developers

1. **Follow all steps** - Each catches different issues
2. **Use skills** - Don't improvise reviews
3. **Fix immediately** - Don't defer issues
4. **Report honestly** - Don't hide problems

### For Reviewers

1. **Be independent** - Don't just confirm Developer's review
2. **Verify fixes** - Check issues were actually resolved
3. **Be constructive** - Provide actionable suggestions

---

## Troubleshooting

### "Gates keep failing"

Check:
1. Are gates too strict? Adjust if needed
2. Is Developer following all steps?
3. Is feedback specific enough?
4. Consider escalating if no progress

### "Taking too many iterations"

Check:
1. Was scope too large? Break into smaller modules
2. Are requirements clear?
3. Is there a fundamental issue? Escalate
4. Review iteration history for patterns

### "Quality inconsistent"

Check:
1. Are skills being used consistently?
2. Are gates defined clearly?
3. Is Reviewer providing independent evaluation?

---

## Reference

- `RESEARCH_FINDINGS.md` - Background research
- `DESIGN_PROPOSAL.md` - Architecture details
- `skills/README.md` - Skills documentation
- `skills/*.md` - Individual skill files
