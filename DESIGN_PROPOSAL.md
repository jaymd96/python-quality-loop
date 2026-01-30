# Design Proposal: Generic Python Development Workflow

## Overview

This proposal presents an improved, generic Python development workflow inspired by:
- Project Vend's manager-employee model
- Anthropic's composable agent patterns
- Existing Claude Code skill architecture

The workflow is designed to be:
- **Generic**: Works with any Python project
- **Composable**: Skills work independently or together
- **Procedural**: Structured process beats raw capability
- **Iterative**: Quality gates with ACCEPT/ITERATE/ESCALATE decisions
- **Observable**: Clear status and progress tracking

---

## Architecture Overview

### System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     WORKFLOW ORCHESTRATOR                        │
│                                                                  │
│  Commands: /start-project, /iterate, /check-status, /complete   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    State Management                       │   │
│  │  - Current phase (0-3)                                   │   │
│  │  - Iteration count                                       │   │
│  │  - Quality gate status                                   │   │
│  │  - Active modules                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    MANAGER      │ │   DEVELOPER     │ │    REVIEWER     │
│    (Role)       │ │    (Role)       │ │     (Role)      │
│                 │ │                 │ │                 │
│ - Set goals     │ │ - Investigate   │ │ - Code review   │
│ - Define gates  │ │ - Implement     │ │ - Standards     │
│ - Evaluate      │ │ - Test          │ │ - Quality       │
│ - Decide        │ │ - Report        │ │ - Feedback      │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         │         ┌─────────┴─────────┐         │
         │         │                   │         │
         ▼         ▼                   ▼         ▼
┌─────────────────────────────────────────────────────────────┐
│                      SKILL LAYER                             │
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ python-  │ │ python-  │ │  zen-of- │ │  code-   │       │
│  │ coding   │ │ testing  │ │  python  │ │  review  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ python-  │ │ python-  │ │ python-  │ │ python-  │       │
│  │ layout   │ │ repl     │ │ logging  │ │ package  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Procedures Beat Capability** (Project Vend)
   - Structured workflow enforces quality
   - Each step catches different issues
   - Skipping steps weakens the process

2. **Simple, Composable Patterns** (Anthropic)
   - Avoid framework complexity
   - Skills work independently
   - Combine as needed

3. **Orchestrator-Worker Model** (Anthropic)
   - Central orchestration
   - Specialized worker roles
   - Clear delegation

4. **Quality Gates as Contracts**
   - Measurable criteria
   - Objective decisions
   - Prevents endless iteration

5. **Unix Philosophy: Composition over Reimplementation**
   - Use existing tools before building new ones
   - Small, focused modules that do one thing well
   - Compose via standard interfaces
   - Text streams and structured data as universal interface

6. **Dogfooding (Knuth's Philosophy)**
   - Be the designer, implementor, first user, AND documentation writer
   - "Eat your own dog food" - use the software to find issues
   - Every friction point should be personally felt and addressed
   - The playground is part of the code, not throwaway

7. **Consistent Code Layout**
   - Predictable project structure
   - Standard module organization (`_types.py`, `_exceptions.py`, etc.)
   - Consistent naming patterns
   - One responsibility per file

---

## Unix Philosophy Integration

> "Use tools in preference to unskilled help to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you've finished using them."

### Core Principles Applied

The Unix philosophy informs every phase of the workflow:

| Principle | Application |
|-----------|-------------|
| Do one thing well | Modules under 400 lines, single responsibility |
| Compose via pipes | Functions accept/return standard types |
| Use existing tools | Research packages before implementing |
| Text as interface | JSON/CSV/lines for interoperability |

### Package Research in Phase 0

Before implementing any significant functionality, developers must:

```
Step 0.2: Package Research
├── Define the problem clearly
├── Search PyPI, GitHub, awesome-lists
├── Evaluate top 3-5 candidates
├── Make COMPOSE/EXTEND/BUILD decision
└── Document rationale
```

**Decision Framework**:

| Decision | When to Use |
|----------|-------------|
| COMPOSE | Package scores >= 4.0, good maintenance, fits needs |
| EXTEND | Core is solid but needs thin wrapper (< 100 lines) |
| BUILD | No suitable package, unique requirements, simpler custom solution |

### llmtxt Documentation

When adopting packages (COMPOSE/EXTEND), create concise documentation for AI-assisted development:

```
docs/llmtxt/
├── httpx.md          # HTTP client patterns
├── pydantic.md       # Validation patterns
└── our_api.md        # Internal API reference
```

**llmtxt Format** (2000-4000 tokens):
- Overview: What and when
- Core API: 3-5 most important interfaces
- Patterns: YOUR usage, not just official docs
- Gotchas: Discovered edge cases and workarounds

### Skill Layer Enhancement

New skills support Unix philosophy:

| Skill | Purpose |
|-------|---------|
| package-research | Systematic package evaluation |
| llmtxt-generation | AI-friendly documentation |
| unix-philosophy | Composition design principles |

### Workflow Integration

```
Phase 0: Discovery
├── Step 0.0: Branch Setup (GitOps)
├── Step 0.1: Context Gathering
├── Step 0.2: Package Research      <-- Unix Philosophy
│   ├── Search existing solutions
│   ├── Evaluate candidates
│   ├── Make COMPOSE/EXTEND/BUILD decision
│   └── Create llmtxt (if adopting)
├── Step 0.3: Gap Analysis
├── Step 0.4: Technical Approach
├── Step 0.5: Initial Commit
└── Step 0.6: Manager Approval
```

### Quality Gate Addition

Include composition evaluation in code review:

```yaml
Code Quality:
  # ... existing gates ...
  composition_evaluated: true    # Did developer research packages?
  llmtxt_created: "if_needed"    # Documentation for adopted packages
  module_size: "< 400 lines"     # Single responsibility
```

### Benefits

1. **Reduced Development Time**: Leverage battle-tested implementations
2. **Fewer Bugs**: Mature packages handle edge cases
3. **Better Documentation**: llmtxt captures institutional knowledge
4. **Maintainability**: Smaller, focused modules are easier to update
5. **Consistency**: Standard patterns across the codebase

---

## Dogfooding Integration (Knuth's Philosophy)

> "...the designer of a new system must not only be the implementor and the first large-scale user; the designer should also write the first user manual. ... If I had not participated fully in all these activities, literally hundreds of improvements would never have been made, because I would never have thought of them or perceived why they were important."
> -- Donald Knuth, "The Errors of TeX" (1989)

### Core Principle

**Be the designer, implementor, first user, AND documentation writer.**

The playground creates a continuous feedback loop:

```
Implement -> Playground Explore -> Find Issues -> Update Requirements -> Implement
     ^                                                                      |
     +----------------------------------------------------------------------+
```

### Playground Integration in Workflow

```
Phase 0: Discovery
├── Step 0.0: Branch Setup (GitOps)
├── Step 0.1: Playground Setup      <-- Dogfooding
│   └── Create playground/{module}_exploration.py
├── Step 0.2: Context Gathering
├── Step 0.3: Package Research
├── ...
```

```
Phase 1: Development (each iteration)
├── Step 1: Implementation
├── Step 2: Layout & Organization
├── Step 3: Standards
├── Step 4: Review
├── Step 5: Playground Exploration  <-- Dogfooding
│   ├── Run playground file
│   ├── Test >= 5 scenarios
│   ├── Document discoveries
│   └── Identify missing features
├── Step 6: Testing
└── Step 7: Commit
```

### Discovery Categories

When exploring, developers document:

| Category | Description | Action |
|----------|-------------|--------|
| DISCOVERY | General finding about behavior | Document or discuss |
| FRICTION | API awkwardness | Improve API |
| MISSING | Feature that should exist | Add to backlog |
| UNDOCUMENTED | Unclear behavior | Update docs |
| PERFORMANCE | Efficiency concern | Investigate |

### Quality Gate Addition

```yaml
Code Quality:
  # ... existing gates ...
  playground_runs: true            # Playground executes without error
  scenarios_tested: ">= 5"         # At least 5 usage scenarios
  discoveries_documented: true     # Findings recorded with actions
```

### Benefits

1. **Find Issues Early**: Personal usage reveals problems before users hit them
2. **Better APIs**: Friction points get addressed, not ignored
3. **Living Documentation**: Playground code shows real usage patterns
4. **Test Discovery**: Playground scenarios convert to formal tests
5. **Continuous Improvement**: Feedback loop drives quality

---

## Code Layout Standards

Consistent code layout makes codebases navigable and maintainable.

### Standard Module Structure

```
mypackage/
├── __init__.py          # Public API exports only
├── _types.py            # Dataclasses, enums, type aliases
├── _exceptions.py       # Exception hierarchy
├── _constants.py        # Configuration constants
├── _core.py             # Main implementation
├── _utils.py            # Internal helpers
└── _crud.py             # Database operations (if applicable)
```

### File Naming Conventions

| Pattern | Meaning |
|---------|---------|
| `_name.py` | Private/internal module |
| `name.py` | Public module (rare) |
| `__init__.py` | Package marker with public exports |

### Import Ordering

```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import json
from pathlib import Path

# 3. Third-party packages
import httpx

# 4. Local imports (absolute)
from mypackage.utils import helper

# 5. Local imports (relative)
from ._types import Config
```

### Size Guidelines

| Metric | Guideline |
|--------|-----------|
| File size | < 300 lines |
| Function size | < 50 lines |
| Parameters | < 7 per function |
| Nesting depth | < 4 levels |

### Quality Gate Addition

```yaml
Code Quality:
  # ... existing gates ...
  layout_conventions: true         # Follows standard layout
  file_size: "< 300 lines"         # Single responsibility
  imports_ordered: true            # Correct import ordering
```

---

## Role Definitions

### Manager Role

**Purpose**: Oversight, goal-setting, quality evaluation, decisions

**Responsibilities**:
1. Define project requirements and scope
2. Set quality gates (measurable criteria)
3. Evaluate iteration reports against gates
4. Make ACCEPT/ITERATE/ESCALATE decisions
5. Provide specific, actionable feedback
6. Track portfolio of active developments

**Permissions**:
- Read: Full access to review code
- Write: None (does not implement)
- Execute: Status checks, quality metrics only

**Decision Framework**:

```
┌─────────────────────────────────────┐
│        MANAGER DECISION TREE        │
└─────────────────┬───────────────────┘
                  │
          All gates passing?
         /                  \
       YES                   NO
        │                     │
   Zero issues?         Fixable issues?
   /        \           /           \
  YES       NO        YES           NO
   │         │          │             │
   ▼         ▼          ▼             ▼
ACCEPT   ITERATE    ITERATE      ESCALATE
                  (if under limit)
```

### Developer Role

**Purpose**: Investigation, implementation, testing, reporting

**Responsibilities**:
1. Investigate existing codebase (Phase 0)
2. Plan implementation approach
3. Write production code using skills
4. Run quality checks (standards, review)
5. Test API through experimentation
6. Report findings transparently
7. Implement focused improvements

**Permissions**:
- Read: Full access
- Write: Create and modify files
- Execute: Tests, linters, REPL

**Workflow Steps** (each iteration):

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | python-coding | Write implementation |
| 2 | python-layout | Organize structure & layout |
| 3 | zen-of-python | Check standards |
| 4 | code-review | Deep quality review |
| 5 | playground-exploration | Dogfooding & discovery |
| 6 | python-testing | Write formal tests |

### Reviewer Role

**Purpose**: Independent quality evaluation

**Responsibilities**:
1. Review code against standards (independent of Developer)
2. Evaluate test coverage and quality
3. Check documentation completeness
4. Provide structured feedback
5. Verify improvements were made

**Permissions**:
- Read: Full access
- Write: None (review only)
- Execute: Read-only quality tools

**Why Separate Reviewer?**

From Project Vend research: Manager using same model replicates developer weaknesses. Independent review provides:
- Fresh perspective
- Different evaluation criteria
- Verification that issues were actually fixed
- Additional quality layer

---

## Workflow Phases

### Phase 0: Discovery

**Duration**: 30-60 minutes
**Purpose**: Understand before building

```
┌────────────────────────────────────────────────────────────┐
│                      PHASE 0: DISCOVERY                     │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 0.1: Context Gathering                               │
│  ├─ Read existing codebase                                 │
│  ├─ Identify patterns and conventions                      │
│  └─ Document integration points                            │
│                                                             │
│  Step 0.2: Gap Analysis                                    │
│  ├─ What exists vs. what's needed                          │
│  ├─ Dependencies and constraints                           │
│  └─ Risks and unknowns                                     │
│                                                             │
│  Step 0.3: Technical Approach                              │
│  ├─ Architecture sketch                                    │
│  ├─ Key classes/functions                                  │
│  └─ Implementation sequence                                │
│                                                             │
│  Output: Discovery Report                                  │
│  ├─ Gap analysis document                                  │
│  ├─ Technical approach document                            │
│  └─ Quality gates (proposed or confirmed)                  │
│                                                             │
│  Gate: Manager approval before Phase 1                     │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### Phase 1: Development

**Duration**: 1-2 hours per iteration, typically 2-4 iterations
**Purpose**: Build with quality

```
┌────────────────────────────────────────────────────────────┐
│                   PHASE 1: DEVELOPMENT                      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ITERATION N                                               │
│                                                             │
│  Step 1: Implementation (python-coding)                    │
│  ├─ Write production code                                  │
│  ├─ Type hints on public APIs                              │
│  ├─ Docstrings on public functions                         │
│  └─ Follow existing patterns                               │
│                                                             │
│  Step 2: Organization (python-layout)                      │
│  ├─ Review file structure                                  │
│  ├─ Clean imports                                          │
│  └─ Consistent naming                                      │
│                                                             │
│  Step 3: Standards (zen-of-python)                         │
│  ├─ Evaluate against principles                            │
│  ├─ Fix violations immediately                             │
│  └─ Target >= 85% compliance                               │
│                                                             │
│  Step 4: Review (code-review)                              │
│  ├─ Deep structural review                                 │
│  ├─ Fix critical/major issues                              │
│  └─ Document remaining minor issues                        │
│                                                             │
│  Step 5: Experimentation (python-repl)                     │
│  ├─ Test >= 5 scenarios                                    │
│  ├─ Happy path, edge cases, errors                         │
│  └─ Zero runtime errors                                    │
│                                                             │
│  Step 6: Testing (python-testing)                          │
│  ├─ Write formal tests                                     │
│  ├─ Cover key behaviors                                    │
│  └─ Ensure tests pass                                      │
│                                                             │
│  Output: Iteration Report                                  │
│  ├─ Quality metrics                                        │
│  ├─ Gate evaluation                                        │
│  ├─ Findings summary                                       │
│  └─ Developer recommendation                               │
│                                                             │
│  Gate: Manager evaluates, decides                          │
│  ├─ ACCEPT -> Phase 3                                      │
│  ├─ ITERATE -> Phase 2                                     │
│  └─ ESCALATE -> Stop                                       │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### Phase 2: Refinement

**Duration**: 1-2 hours per iteration
**Purpose**: Focused improvements

```
┌────────────────────────────────────────────────────────────┐
│                    PHASE 2: REFINEMENT                      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Trigger: Manager says ITERATE with specific feedback      │
│                                                             │
│  Manager Provides:                                         │
│  ├─ Gate status (which failed)                             │
│  ├─ Specific improvements needed                           │
│  ├─ Code locations (file:line)                             │
│  └─ Scope boundary (do NOT expand)                         │
│                                                             │
│  Developer Executes:                                       │
│  ├─ Steps 1-6 on affected code ONLY                        │
│  ├─ Focus on Manager-specified items                       │
│  └─ New iteration report                                   │
│                                                             │
│  Reviewer Verifies:                                        │
│  ├─ Issues actually fixed                                  │
│  ├─ No regressions introduced                              │
│  └─ Quality improved                                       │
│                                                             │
│  Loop until:                                               │
│  ├─ ACCEPT (all gates pass)                                │
│  ├─ ESCALATE (limit hit or fundamental issue)              │
│                                                             │
│  Iteration Limit: Typically 3-4                            │
│  ├─ Iteration 1: Broad improvements                        │
│  ├─ Iteration 2: Focused improvements                      │
│  ├─ Iteration 3: Polishing                                 │
│  └─ Iteration 4+: Escalate                                 │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### Phase 3: Completion

**Duration**: 30 minutes
**Purpose**: Production-ready finalization

```
┌────────────────────────────────────────────────────────────┐
│                    PHASE 3: COMPLETION                      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Trigger: Manager says ACCEPT                              │
│                                                             │
│  Step 1: Final Review                                      │
│  ├─ Remove debug code and TODOs                            │
│  ├─ Clean up temporary fixtures                            │
│  └─ Verify all code is production-ready                    │
│                                                             │
│  Step 2: Documentation                                     │
│  ├─ Complete all docstrings                                │
│  ├─ Add usage examples                                     │
│  ├─ Create/update README if needed                         │
│  └─ Document API surface                                   │
│                                                             │
│  Step 3: Final Testing                                     │
│  ├─ Run full test suite                                    │
│  ├─ Verify integration                                     │
│  └─ Performance checks if relevant                         │
│                                                             │
│  Step 4: Integration                                       │
│  ├─ Clean commit history                                   │
│  ├─ Merge to main branch                                   │
│  └─ Clean up feature branch                                │
│                                                             │
│  Output: Completed Module                                  │
│  ├─ Production-ready code                                  │
│  ├─ Complete documentation                                 │
│  ├─ Passing tests                                          │
│  └─ Integration verified                                   │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## Quality Gates Framework

### Gate Categories

```yaml
Quality Gates:

  Code Quality:
    description: Code must be production-ready
    metrics:
      - critical_issues: 0
      - zen_compliance: ">= 85%"
      - docstring_coverage: "100% public APIs"
      - type_hints: "100% public APIs"
    evaluation: code-review + zen-of-python output

  Testing:
    description: Feature must be thoroughly tested
    metrics:
      - scenarios_tested: ">= 5"
      - edge_cases_handled: true
      - runtime_errors: 0
      - test_coverage: ">= 80%"
    evaluation: python-repl + python-testing output

  Integration:
    description: Feature integrates cleanly
    metrics:
      - breaking_changes: 0
      - dependencies_tracked: true
      - patterns_followed: true
    evaluation: code-review + manual verification

  Documentation:
    description: Feature is documented for users
    metrics:
      - public_apis_documented: true
      - examples_provided: ">= 1"
      - complex_logic_explained: true
    evaluation: docstring + README check
```

### Gate Evaluation Format

```yaml
Gate Evaluation:
  module: "data-processor"
  iteration: 2
  timestamp: "2026-01-30T10:00:00Z"

  gates:
    code_quality:
      status: PASS
      critical_issues: 0
      zen_compliance: 87%
      details: "All critical issues resolved"

    testing:
      status: FAIL
      scenarios_tested: 4
      required: 5
      details: "Missing error handling scenario"

    integration:
      status: PASS
      breaking_changes: 0
      details: "Clean integration verified"

    documentation:
      status: PASS
      public_apis: "100% documented"
      examples: 2

  summary:
    passed: 3
    failed: 1
    decision: ITERATE

  feedback:
    - "Add error handling test scenario (missing 1 of 5)"
    - "Test what happens when input file is empty"
    - "Do NOT expand scope beyond this item"
```

---

## Decision Framework

### ACCEPT

**Criteria**:
- All four quality gates PASS
- Zero critical issues
- Developer recommends ACCEPT
- No outstanding blockers

**Action**:
- Proceed to Phase 3
- Finalize and merge

**Message Template**:
```
ACCEPT

All quality gates passing. Code is production-ready.

Gate Status:
  Code Quality: PASS (0 critical, 87% zen-python)
  Testing: PASS (6 scenarios, 0 errors)
  Integration: PASS (no breaking changes)
  Documentation: PASS (100% documented)

Proceed to Phase 3: Finalize, document, merge.
```

### ITERATE

**Criteria**:
- One or more gates FAIL
- Issues are specific and fixable
- Iteration count < limit
- No architectural redesign needed

**Action**:
- Return specific feedback
- Developer makes focused improvements
- Reviewer verifies fixes

**Message Template**:
```
ITERATE

Gate Status:
  Code Quality: PASS
  Testing: FAIL (4 of 5 scenarios)
  Integration: PASS
  Documentation: PASS

Specific Improvements (prioritized):

1. Add error handling test scenario
   Location: tests/test_processor.py
   Missing: Test for empty input file
   Approach: Use pytest.raises with empty fixture

2. [Additional items if any]

Scope: Do NOT expand beyond these items.
Iteration: 2 of 4
```

### ESCALATE

**Criteria**:
- Architectural mismatch discovered
- Scope unclear or conflicting
- Blocker preventing progress
- Iteration limit exceeded
- Fundamental design flaw

**Action**:
- Stop development
- Document issue clearly
- Reassess approach
- May require human decision

**Message Template**:
```
ESCALATE

Development cannot proceed without reassessment.

Issue: Architectural mismatch discovered

Details: The proposed approach conflicts with existing
         event-driven architecture. DataProcessor assumes
         synchronous processing, but system is async.

Iteration: 4 of 4 (limit reached)

Required Action:
  1. Review async patterns in existing codebase
  2. Decide: Adapt approach or change requirements
  3. May need to restart with new design

This requires team discussion.
```

---

## Integration with Existing Skills

### Skill Usage by Phase

```
Phase 0: Discovery
├─ code-review (understand existing code)
└─ [research materials]

Phase 1: Development (each iteration)
├─ Step 1: python-coding (implementation)
├─ Step 2: python-layout (organization)
├─ Step 3: zen-of-python (standards)
├─ Step 4: code-review (quality)
├─ Step 5: python-repl (experimentation)
└─ Step 6: python-testing (formal tests)

Phase 2: Refinement
├─ [Same as Phase 1, focused]
└─ Reviewer verification

Phase 3: Completion
├─ python-coding (finalize)
├─ python-layout (final structure)
├─ python-testing (final verification)
└─ python-logging (add observability if needed)
```

### No Modifications to Existing Skills

All existing skills work as-is. The workflow **sequences** them without modification.

---

## Consolidated Plugin Structure

### Directory Layout

```
generic-workflow/
├── skills/
│   ├── __init__.py              # Plugin entry point
│   ├── manager.md               # Manager role skill
│   ├── developer.md             # Developer role skill
│   ├── reviewer.md              # Reviewer role skill
│   ├── python_coding.md         # Python coding standards
│   ├── python_testing.md        # Testing practices
│   ├── workflow.md              # Overall orchestration
│   └── README.md                # How to use
│
├── templates/
│   ├── discovery_report.md      # Phase 0 output template
│   ├── iteration_report.md      # Per-iteration report
│   ├── gate_evaluation.md       # Quality gate format
│   └── decision_feedback.md     # ACCEPT/ITERATE/ESCALATE
│
├── RESEARCH_FINDINGS.md         # This research
├── DESIGN_PROPOSAL.md           # This design
└── IMPLEMENTATION_GUIDE.md      # How to implement
```

### Plugin Commands

| Command | Purpose |
|---------|---------|
| `/start-project` | Initialize workflow for new project/module |
| `/iterate` | Submit iteration report for evaluation |
| `/check-status` | View status of all active developments |
| `/complete` | Finalize and merge completed work |

---

## Comparison: Old vs New Design

| Aspect | Old Design | New Design |
|--------|------------|------------|
| **Roles** | Manager + Developer | Manager + Developer + Reviewer |
| **Context** | Shared (potential pollution) | Isolated (subagent pattern) |
| **Verification** | Manager only | Manager + Independent Reviewer |
| **Applicability** | Apollo-specific | Generic Python |
| **Orchestration** | Manual | Workflow commands |
| **State** | Templates | Structured data |
| **Skills** | Integrated | Composable, unchanged |

---

## Success Criteria

The workflow is successful when:

1. **Modules complete in 2-4 iterations** (not endless loops)
2. **Quality gates consistently applied** across projects
3. **Reports are clear and actionable** for decisions
4. **Decisions are fast and objective** (gate-based)
5. **Blockers surface early** and get escalated
6. **Code quality is consistent** module-to-module
7. **Time from Phase 0 to Phase 3 is predictable** (4-10 hours typical)

---

## Migration Path

### From Apollo-Specific to Generic

1. **Remove project references**: No Apollo, automotive, or domain assumptions
2. **Parameterize paths**: Project path provided at start, not hardcoded
3. **Generic quality gates**: Defaults work for any Python project
4. **Configurable gates**: Custom gates for specific needs

### Adoption Strategy

1. **Phase 1**: Document generic workflow (this proposal)
2. **Phase 2**: Create consolidated skills
3. **Phase 3**: Test with different project types
4. **Phase 4**: Refine based on usage
5. **Phase 5**: Distribute as reusable plugin

---

## References

- Research Findings: `RESEARCH_FINDINGS.md`
- Implementation Guide: `IMPLEMENTATION_GUIDE.md`
- Skills Directory: `skills/`
