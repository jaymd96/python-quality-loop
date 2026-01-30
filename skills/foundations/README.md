# Foundations: Core Technical Skills

This category contains skills for Python coding standards, testing, project layout, and literate programming.

## Overview

These are the core technical skills that guide implementation, testing, and code quality. They form the foundation of the Developer role's work.

## Skills

### [python-coding.md](python-coding.md)
Python coding standards and patterns.

**When to use:** During implementation (Step 1 of Developer workflow) to write code that adheres to standards.

**Covers:**
- Zen of Python principles (explicit > implicit, simple > complex, etc.)
- Type hints and annotations
- Function design and composition
- Error handling patterns
- Documentation standards

### [python-testing.md](python-testing.md)
Python testing with pytest.

**When to use:** During testing (Step 5 of Developer workflow) to write comprehensive test coverage.

**Covers:**
- Test structure and organization
- pytest patterns and fixtures
- Edge case identification
- Test documentation
- Coverage targets

### [python-layout.md](python-layout.md)
Python project and module structure guidance.

**When to use:** During layout phase (Step 2 of Developer workflow) to organize code consistently.

**Covers:**
- Module structure and file organization
- File naming conventions
- Package organization
- Code organization within files
- Public API design

### [literate-python.md](literate-python.md)
Write Python with literate programming annotations.

**When to use:** When writing Python code that should include meaningful documentation, or when user requests literate programming style.

**Covers:**
- Litterate annotation syntax (`#>` markers)
- When to annotate (why, not what)
- Annotation patterns for algorithms, business logic, edge cases
- Integration with Litterate documentation generator
- Reference: [literate-python-patterns.md](references/literate-python-patterns.md)

## Quality Gates for Foundations

The Manager evaluates these gates using foundations skills:

- **Code Quality**: Zero critical issues, ≥85% Zen compliance, 100% docstrings on public APIs, 100% type hints
- **Testing**: ≥5 scenarios tested, zero runtime errors, edge cases handled
- **Layout**: Consistent structure, files under size limits, proper organization

## Implementation Steps

The Developer typically follows these steps, using foundations skills:

1. **Implementation** (python-coding) - Write code following standards
2. **Layout** (python-layout) - Organize code consistently
3. **Code Review** (zen-of-python) - Check compliance with principles
4. **Playground** (literate-python optional) - Document complex logic
5. **Testing** (python-testing) - Write comprehensive tests

## Related

- See [workflow/](../workflow/) for overall orchestration
- See [philosophy/](../philosophy/) for design principles
- See [tools/](../tools/) for documentation generation
