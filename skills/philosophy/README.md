# Philosophy: Design Principles

This category contains skills focused on design philosophy: composition over building, Unix principles, and Knuth's dogfooding philosophy.

## Overview

These skills guide the *thinking* behind how code is designed, what gets built vs. what gets composed, and how to discover missing functionality.

## Skills

### [unix-philosophy.md](unix-philosophy.md)
Unix philosophy principles for Python development.

**When to use:** Before implementing (Phase 0), when deciding whether to build or compose.

**Covers:**
- Composition over reimplementation
- Do one thing and do it well
- Make it easy to combine modules
- Leveraging existing tools
- Small, focused, composable modules

### [package-research.md](package-research.md)
Research existing packages before implementing.

**When to use:** During Phase 0, Step 0.2 (Package Research).

**Covers:**
- Systematic package discovery (PyPI, GitHub)
- Evaluation criteria (maintenance, license, security, fit)
- Build vs Compose decision framework
- Documentation of decisions
- Creating llmtxt for adopted packages

### [playground.md](playground.md)
Playground-driven development using Knuth's dogfooding philosophy.

**When to use:** During Step 5 (Playground Exploration), or when discovering features through usage.

**Covers:**
- Creating exploration/playground files
- Discovering features through real usage
- Finding missing functionality
- Converting experiments to tests
- Identifying API friction points

## Core Principles

### Don't Reinvent the Wheel
Before implementing, always research existing solutions. Most problems have been solved before. Using existing packages:
- Reduces bugs
- Leverages community expertise
- Enables focus on unique logic
- Simplifies maintenance

### Be Your Own First User (Dogfooding)
Write playground code that uses your module *exactly* like a user would:
- Discover what's missing
- Identify API friction
- Find edge cases
- Convert experiments to tests

### One Tool, One Job
Design modules to do one thing excellently:
- Easier to understand
- Easier to test
- Easier to compose
- Harder to overfit

## Philosophy Workflow

```
Phase 0: Discovery

1. Understand Problem
   ↓
2. Package Research (unix-philosophy + package-research)
   ├─ Search existing solutions
   ├─ Evaluate top candidates
   ├─ Decide: Build, Extend, or Compose
   └─ Document decision
   ↓
3. Initial Planning
   └─ Design for composition
   ↓
4. Playground Setup (playground)
   └─ Create exploration file
   ↓
5. Manager Approval
   └─ Proceed with implementation
```

## Related

- See [foundations/](../foundations/) for technical skills
- See [workflow/](../workflow/) for overall orchestration
- See [tools/](../tools/) for documentation of composed packages
