# Manager-Doer Workflow Plugin

A Claude Code plugin implementing structured, iterative Python development using the Manager-Doer pattern with quality gates, GitOps integration, Unix philosophy composition principles, Knuth's dogfooding philosophy, and consistent code layout standards.

## Overview

This plugin provides:
- **Structured Workflow**: Phased development (Discovery, Development, Refinement, Completion)
- **Role-Based Skills**: Manager, Developer, and Reviewer roles with clear responsibilities
- **Quality Gates**: Measurable criteria for code quality, testing, integration, and documentation
- **GitOps Integration**: Branch management, conventional commits, PR workflows
- **Iteration Control**: ACCEPT/ITERATE/ESCALATE decision framework
- **Unix Philosophy**: Composition over reimplementation, package research, llmtxt documentation
- **Dogfooding (Knuth's Philosophy)**: Be the first user of your own code through playground exploration
- **Consistent Code Layout**: Standard module organization, file naming, and import ordering

## Installation

### Option 1: Claude Code Plugin (Recommended)

```bash
# From Claude Code, install from local path
/plugin install /path/to/generic-workflow

# Or if published to a repository
/plugin install manager-doer-workflow
```

### Option 2: Copy to User Skills Directory

Copy skills to your global Claude Code skills directory:

```bash
# Create skills directory if needed
mkdir -p ~/.claude/skills/

# Copy all skills
cp skills/*.md ~/.claude/skills/

# Copy plugin configuration
cp -r .claude-plugin ~/.claude/
```

### Option 3: Copy to Project Skills Directory

Copy skills to your project for project-specific use:

```bash
# Create project skills directory
mkdir -p .claude/skills/

# Copy skills
cp path/to/generic-workflow/skills/*.md .claude/skills/
```

### Option 4: Use Directly

Reference skills by reading files when needed in your Claude Code session.

---

## Skills Organization

Skills are organized into 5 categories for easier navigation:

- **[Roles](roles/)** - Manager-Doer pattern roles (Manager, Developer, Reviewer)
- **[Workflow](workflow/)** - Orchestration and Git integration
- **[Foundations](foundations/)** - Core technical skills (Python coding, testing, layout, literate programming)
- **[Philosophy](philosophy/)** - Design principles (Unix philosophy, package research, dogfooding)
- **[Tools](tools/)** - Utility skills (llmtxt documentation generation)

## Quick Skill Finder

### By Task

| Task | Skills |
|------|--------|
| **Starting a new feature** | [workflow/workflow](workflow/) → [philosophy/](philosophy/) (research packages) |
| **Implementing code** | [foundations/python-coding](foundations/python-coding.md) |
| **Testing code** | [foundations/python-testing](foundations/python-testing.md) |
| **Organizing code** | [foundations/python-layout](foundations/python-layout.md) |
| **Adding annotations** | [foundations/literate-python](foundations/literate-python.md) |
| **Designing with composition** | [philosophy/unix-philosophy](philosophy/unix-philosophy.md) |
| **Evaluating packages** | [philosophy/package-research](philosophy/package-research.md) |
| **Trying out code** | [philosophy/playground](philosophy/playground.md) |
| **Documenting packages** | [tools/llmtxt](tools/llmtxt.md) |
| **Managing Git** | [workflow/gitops](workflow/gitops.md) |
| **Manager decisions** | [roles/manager](roles/manager.md) |
| **Developer execution** | [roles/developer](roles/developer.md) |
| **Independent review** | [roles/reviewer](roles/reviewer.md) |

## 14 Skills Total

**Roles (3):**
- Manager - Oversight and decisions
- Developer - Implementation and execution
- Reviewer - Independent quality validation

**Workflow (2):**
- Workflow - Overall orchestration
- GitOps - Git operations and branching

**Foundations (4):**
- Python Coding - Code standards
- Python Testing - Test standards
- Python Layout - File organization
- Literate Python - Documentation annotations

**Philosophy (3):**
- Unix Philosophy - Composition principles
- Package Research - Package evaluation
- Playground - Dogfooding and exploration

**Tools (1):**
- llmtxt - Documentation generation

---

## Quick Start

### 1. Start a New Module

```
I need to implement [module description].

Requirements:
- [Requirement 1]
- [Requirement 2]

Use the Manager-Doer workflow with default quality gates.
```

### 2. Phase 0: Discovery

Developer:
1. Creates feature branch: `git checkout -b feature/module-name`
2. **Creates playground file** - `playground/{module}_exploration.py`
3. Reviews existing codebase
4. **Package research** - Searches for existing packages, evaluates candidates, makes COMPOSE/EXTEND/BUILD decision
5. Creates llmtxt documentation for adopted packages (if any)
6. Creates gap analysis and technical approach
7. Commits: `chore(module): initialize development`
8. Submits for Manager approval (including build vs compose decision)

### 3. Phase 1: Development

Developer iterates through Steps 1-7:
1. **Implementation** (python-coding)
2. **Layout & Organization** (python-layout)
3. **Standards** (zen-of-python)
4. **Review** (code-review)
5. **Playground Exploration** (playground-exploration) - Dogfooding!
6. **Testing** (python-testing)
7. **Commit** (gitops-workflow)

Submits iteration report to Manager.

### 4. Manager Decision

- **ACCEPT**: All gates pass -> Phase 3
- **ITERATE**: Specific improvements needed -> Phase 2
- **ESCALATE**: Fundamental issues -> Stop

### 5. Phase 2: Refinement (if ITERATE)

Developer makes focused improvements based on Manager feedback.

### 6. Phase 3: Completion (if ACCEPT)

Developer:
1. Final cleanup and documentation
2. Creates pull request
3. Merges to main after approval
4. Cleans up branch

---

## Workflow Diagram

```
                    ┌─────────────────┐
                    │   REQUIREMENTS  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Phase 0        │
                    │  Discovery      │
                    │  + Branch Setup │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
             ┌──────│  Phase 1        │──────┐
             │      │  Development    │      │
             │      │  (Steps 1-7)    │      │
             │      └────────┬────────┘      │
             │               │               │
             │      ┌────────▼────────┐      │
             │      │  Manager        │      │
             │      │  Evaluation     │      │
             │      └────────┬────────┘      │
             │               │               │
             │     ┌─────────┼─────────┐     │
             │     │         │         │     │
             │  ACCEPT   ITERATE   ESCALATE  │
             │     │         │         │     │
             │     │         └─────────┼─────┘
             │     │                   │
             │     │         ┌────────▼────────┐
             │     │         │  Phase 2        │
             │     │         │  Refinement     │
             │     │         └────────┬────────┘
             │     │                  │
             │     │         ┌────────┘
             │     │         │
             │     ▼         ▼
             │  ┌──────────────────┐
             │  │  Phase 3         │
             └──│  Completion      │
                │  + PR & Merge    │
                └──────────────────┘
```

---

## Quality Gates

### Default Gates

```yaml
Code Quality:
  critical_issues: 0
  zen_compliance: ">= 85%"
  docstrings: "100% public APIs"
  type_hints: "100% public APIs"

Testing:
  scenarios_tested: ">= 5"
  runtime_errors: 0
  edge_cases: "handled"

Integration:
  breaking_changes: 0
  patterns_followed: true

Documentation:
  public_apis: "documented"
  examples: ">= 1"
```

### Custom Gates

Adjust for specific needs:

```yaml
# Performance-critical module
Performance:
  response_time: "< 100ms"
  memory: "< 50MB"
```

---

## GitOps Integration

### Branch Naming

```
feature/{module-name}    # New features
fix/{issue-description}  # Bug fixes
refactor/{component}     # Code improvements
```

### Conventional Commits

```
feat(scope): description     # New feature
fix(scope): description      # Bug fix
refactor(scope): description # Code change
test(scope): description     # Adding tests
docs(scope): description     # Documentation
chore(scope): description    # Maintenance
```

### Commit Strategy by Phase

| Phase | Commit Pattern |
|-------|---------------|
| Phase 0 | `chore(module): initialize development` |
| Phase 1 | `feat(module): iteration N implementation` |
| Phase 2 | `fix(module): address iteration N feedback` |
| Phase 3 | `docs(module): complete documentation` |

---

## Decision Framework

| Decision | Criteria | Action |
|----------|----------|--------|
| **ACCEPT** | All gates pass | Phase 3 |
| **ITERATE** | Fixable issues | Specific feedback |
| **ESCALATE** | Fundamental issues | Stop, reassess |

---

## Iteration Limits

| Iteration | Expectation |
|-----------|------------|
| 1 | Initial implementation |
| 2 | Quality improvements |
| 3 | Polishing |
| 4+ | Escalate |

---

## File Structure

```
dotskill/
├── .claude-plugin/
│   └── plugin.json                              # Plugin configuration
├── skills/
│   ├── README.md                                # This file
│   │
│   ├── roles/                                   # Manager-Doer pattern
│   │   ├── README.md
│   │   ├── manager.md
│   │   ├── developer.md
│   │   └── reviewer.md
│   │
│   ├── workflow/                                # Orchestration
│   │   ├── README.md
│   │   ├── workflow.md
│   │   └── gitops.md
│   │
│   ├── foundations/                             # Core technical skills
│   │   ├── README.md
│   │   ├── python-coding.md
│   │   ├── python-testing.md
│   │   ├── python-layout.md
│   │   ├── literate-python.md                  # NEW: Literate programming
│   │   └── references/
│   │       └── literate-python-patterns.md
│   │
│   ├── philosophy/                              # Design principles
│   │   ├── README.md
│   │   ├── unix-philosophy.md
│   │   ├── package-research.md
│   │   └── playground.md
│   │
│   └── tools/                                   # Utility skills
│       ├── README.md
│       └── llmtxt.md
│
├── scripts/                                     # NEW: Utility scripts
│   └── send-feedback-to-lab.py                 # Bridge to claude-skill-lab
│
├── templates/
│   ├── llmtxt_template.md                      # Template for llmtxt documents
│   └── playground_template.py                   # Starter playground file
│
├── RESEARCH_FINDINGS.md                         # Research behind design
├── DESIGN_PROPOSAL.md                           # Architecture proposal
├── IMPLEMENTATION_GUIDE.md                      # Step-by-step guide
├── SKILL_STANDARD.md                            # Skill format reference
├── INTEGRATION_GUIDE.md                         # NEW: Integration guide
└── CHANGELOG.md                                 # NEW: Version history
```

---

## Related Documentation

- `../RESEARCH_FINDINGS.md` - Research behind this design
- `../DESIGN_PROPOSAL.md` - Full architecture proposal
- `../IMPLEMENTATION_GUIDE.md` - How to use step-by-step
- `../SKILL_STANDARD.md` - Agent Skills format reference

---

## Standards Compliance

This plugin follows the **Agent Skills** standard:
- [AgentSkills.io Specification](https://agentskills.io/specification)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)

Each skill file uses the standard format:
```yaml
---
name: skill-name
description: When to use this skill...
---

# Skill Title

[Instructions...]
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.4.0 | 2026-01 | **Reorganized** skills into 5 categories (roles, workflow, foundations, philosophy, tools); **Added** literate-python skill for literate programming annotations; **Added** bridge integration with claude-skill-lab for auto-feedback capture; **Renamed** skills to kebab-case |
| 1.3.0 | 2026-01 | Added dogfooding philosophy (playground-exploration) and code layout standards (python-layout) |
| 1.2.0 | 2026-01 | Added Unix philosophy skills (package-research, llmtxt, unix-philosophy) |
| 1.1.0 | 2026-01 | Added GitOps integration |
| 1.0.0 | 2026-01 | Initial release |

---

## Credits

Inspired by:
- [Project Vend](https://www.anthropic.com/research/project-vend-2) - Anthropic
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) - Anthropic
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Anthropic
- [obra/superpowers](https://github.com/obra/superpowers) - Jesse Vincent
- [The Errors of TeX](http://www.literateprogramming.com/knuthweb.pdf) - Donald Knuth (dogfooding philosophy)

---

## License

Apache-2.0
