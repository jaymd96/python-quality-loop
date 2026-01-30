# Research Findings: Manager-Doer Orchestration Workflow

## Executive Summary

This document synthesizes research from four key areas:
1. Existing Manager-Doer implementation analysis
2. Project Vend2 manager-employee model research
3. Anthropic's agent orchestration best practices
4. Existing Claude Code skill patterns

The findings inform design of an improved, generic Python development workflow.

---

## 1. Current Manager-Doer Implementation Analysis

### Source: `/Users/james/Downloads/manager-doer-orchestrator/`

### Architecture Overview

The existing implementation follows a **two-agent architecture**:

| Agent | Role | Tools | Model |
|-------|------|-------|-------|
| **Manager** | Oversight, quality gates, decisions | Read, Glob, Bash (read-only) | Sonnet |
| **Developer** | Implementation, testing, reporting | Read, Write, Edit, Bash (full) | Sonnet |

### Workflow Phases

```
Phase 0: Investigation (30-60 min)
    - Code review of existing code
    - Research and planning
    - Manager approval before proceeding

Phase 1: Development Loop (1-2 hours/iteration, 2-4 iterations)
    - Step 1: Implementation (python-coding)
    - Step 2: Layout (python-layout)
    - Step 3: Standards (zen-of-python)
    - Step 4: Review (code-review)
    - Step 5: Experimentation (python-repl)
    - Report to Manager

Phase 2: Improvement Loop (if ITERATE)
    - Focused improvements only
    - Manager-specified items
    - Validation of fixes

Phase 3: Finalization (30 min)
    - Code cleanup
    - Documentation completion
    - Merge to main
```

### Quality Gates Framework

Four categories with measurable criteria:

1. **Code Quality**
   - Zero critical code-review issues
   - >= 85% zen-of-python compliance
   - Complete docstrings on public APIs

2. **Testing & Validation**
   - >= 5 distinct API scenarios tested
   - All edge cases handled
   - Zero runtime errors

3. **Integration**
   - Clean integration with existing code
   - No breaking changes
   - Dependencies properly tracked

4. **Documentation**
   - All public functions/classes documented
   - Usage examples provided
   - Complex logic explained

### Decision Framework: ACCEPT/ITERATE/ESCALATE

| Decision | Criteria | Action |
|----------|----------|--------|
| **ACCEPT** | All gates passing, code production-ready | Proceed to Phase 3 |
| **ITERATE** | Specific issues identified, fixable, under limit | Return focused feedback |
| **ESCALATE** | Architectural issues, scope unclear, limit hit | Stop and reassess |

### Key Design Principles

1. **Procedures > Capability**: Structured workflow beats raw model intelligence
2. **Specific Feedback**: "Fix N+1 in function X at line 47" not "Improve performance"
3. **Iteration Limits**: Typically 3-4 max to prevent endless loops
4. **Role Separation**: Manager oversees, Developer executes

### Strengths of Current Implementation

- Clear separation of concerns between Manager and Developer
- Structured iteration with quality gates
- Integration with existing Python skills
- Comprehensive decision framework
- Good documentation and templates

### Weaknesses Identified

- Context pollution when both agents in same context window
- No true tool separation (both have access to all tools conceptually)
- Manual orchestration required
- Apollo-specific assumptions baked in
- Heavy reliance on templates vs. structured data

---

## 2. Project Vend2 Manager-Employee Model Research

### Source: Anthropic Research - Project Vend Phase Two

Project Vend was an Anthropic experiment where an AI agent ("Claudius") ran a simulated business with managerial oversight ("Seymour Cash").

### Key Findings

#### Role Definition
- **Manager (CEO)**: Held explicit authority over financial decisions
- **Employee (Shopkeeper)**: Executed day-to-day operations with constraints

#### Communication Pattern
- Asynchronous via "agent-to-agent Slack channel"
- Manager issued directives
- Employee reported results and requested guidance

#### Quality Control Mechanisms
- "Objectives and Key Results" as control system
- Explicit targets: "sell 100 items this week"
- Manager actively reviewed and rejected problematic decisions
- Over 100 requests denied by manager

#### Critical Discovery: Manager Replicates Weaknesses

> "Seymour Cash shared many of the deficiencies and blind spots of Claudius"

The manager (same underlying model) sometimes authorized decisions contradicting its own stated policies - approving lenient treatment "about eight times as often as it denied them."

#### Key Insight: Bureaucracy Matters

> "Forcing procedures and verification steps proved more effective than managerial pressure in improving outcomes."

Tools and scaffolding mattered more than hierarchical structure alone.

### Implications for Our Design

1. **Procedures over hierarchy**: Structured workflow more effective than manager authority alone
2. **Tool scaffolding matters**: Provide independent verification tools, not just oversight
3. **Same model limitations**: Manager can replicate developer weaknesses
4. **Explicit constraints**: Build rules into the process, not just guidelines

---

## 3. Anthropic Agent Orchestration Best Practices

### Sources:
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)

### Core Philosophy

> "The most successful implementations use simple, composable patterns rather than complex frameworks."

Start simple, add complexity only when demonstrably beneficial.

### Workflows vs Agents

| Type | Description | Use Case |
|------|-------------|----------|
| **Workflows** | LLMs orchestrated through predefined code paths | Well-defined, predictable tasks |
| **Agents** | LLMs dynamically direct their own processes | Open-ended, adaptive problems |

### Five Composable Workflow Patterns

1. **Prompt Chaining**: Sequential steps where each processes previous output
   - Example: Generate outline -> Write sections -> Review

2. **Routing**: Classify inputs and direct to specialized handlers
   - Example: Simple queries to Haiku, complex to Sonnet

3. **Parallelization**: Multiple LLM calls simultaneously
   - Sectioning: Independent subtasks
   - Voting: Multiple attempts for confidence

4. **Orchestrator-Workers**: Central LLM delegates to specialized workers
   - Ideal for coding projects requiring unpredictable changes
   - Our Manager-Doer maps to this pattern

5. **Evaluator-Optimizer**: One generates, another evaluates iteratively
   - Effective for refinement tasks
   - Similar to our iteration loop

### Agent Feedback Loop

```
gather context -> take action -> verify work -> repeat
```

### Tool Design Best Practices

- Provide sufficient token space for planning before output
- Use formats resembling naturally occurring internet text
- Eliminate formatting overhead
- Include comprehensive documentation with examples
- Test extensively
- Apply "poka-yoke" principles (mistake-proofing)

### Implementation Principles

1. **Maintain simplicity** in agent design
2. **Prioritize transparency** through explicit planning steps
3. **Craft tool documentation and testing carefully**

### Long-Running Agent Patterns

For complex projects that cannot complete in single context:
- **Initializer agent**: Sets up environment on first run
- **Coding agent**: Makes incremental progress with clear artifacts for next session

### Subagent Best Practices

> "Telling Claude to use subagents to verify details or investigate particular questions, especially early on in a conversation, tends to preserve context availability."

Benefits:
- Each subagent operates with own context window
- Prevents context pollution
- 90.2% better performance than single-agent approaches

---

## 4. Existing Skills Analysis

### Source: `/Users/james/.claude/skills/`

### Skill Categories

#### Python Development Skills

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| `python-coding` | Writing production code | Module layout, naming, type hints, dataclasses |
| `python-layout` | File/package organization | Project structure, import order, size guidelines |
| `python-testing` | Pytest-based testing | Arrange-Act-Assert, fixtures, parametrization |
| `python-repl` | Interactive exploration | REPL playground, prototyping, discovery |
| `python-logging` | Observability | Structured logging, context propagation |
| `python-package` | Package management | Hatch setup, pyproject.toml, publishing |

#### Code Quality Skills

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| `code-review` | Code critique | Categories, severity levels, feedback format |
| `zen-of-python` | Pythonic standards | Evaluation framework, principles-based guidance |

#### Workflow Skills

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| `initializing-feature-worktree` | Git worktree setup | Feature branches, isolated development |
| `committing-workflow-step` | Progress recording | Step-based commits, audit trail |
| `finalizing-module-merge` | Integration | Safety checks, merge process |
| `checking-development-status` | Portfolio overview | Phase tracking, quality metrics |

### Skill Structure Pattern

```yaml
---
name: skill-name
description: When to use this skill. Trigger phrases.
[allowed-tools: optional tool restrictions]
---

# Title

Brief description and philosophy.

## Quick Reference
Condensed guidance for common use.

## Detailed Sections
Expanded patterns, examples, templates.

## References
Links to supporting files.
```

### Common Patterns Across Skills

1. **YAML Frontmatter**: Name, description, optional tool restrictions
2. **Philosophy Statement**: Core principle or approach
3. **Quick Reference**: At-a-glance guidance
4. **Examples**: Concrete code samples
5. **Checklists**: Verification steps
6. **Anti-patterns**: What to avoid
7. **References**: Links to detailed supporting files

### Skill Integration Points

```
Development Flow:
python-coding -> python-layout -> zen-of-python -> code-review -> python-repl

Git Workflow:
initializing-feature-worktree -> committing-workflow-step -> finalizing-module-merge

Status:
checking-development-status (portfolio view)
```

### Key Observations

1. **Modular design**: Each skill has single responsibility
2. **Composable**: Skills work together without tight coupling
3. **Consistent structure**: YAML frontmatter + markdown content
4. **Self-contained**: Each skill usable independently
5. **Reference materials**: Supporting files for detailed guidance

---

## 5. Synthesis: Key Insights for Design

### What Works Well

1. **Structured phases with clear gates**: Phase 0 -> 1 -> 2 -> 3 progression
2. **Specific feedback requirements**: Concrete, actionable guidance
3. **Iteration limits**: Prevents endless loops
4. **Tool scaffolding**: Skills provide procedural support
5. **Explicit decision framework**: ACCEPT/ITERATE/ESCALATE

### What Needs Improvement

1. **Context management**: Need true subagent separation
2. **Generic applicability**: Remove Apollo-specific assumptions
3. **Simplified orchestration**: Reduce manual coordination
4. **Tool verification**: Independent validation vs. oversight alone
5. **Flexibility**: Support different project types and scales

### Design Principles to Adopt

From Project Vend:
- **Procedures beat capability**: Structured workflow > manager authority
- **Tool scaffolding matters**: Verification tools, not just oversight
- **Explicit constraints**: Build rules into process

From Anthropic Best Practices:
- **Simple, composable patterns**: Avoid framework complexity
- **Orchestrator-worker model**: Matches our Manager-Developer structure
- **Subagent isolation**: Separate context windows
- **Transparent planning**: Explicit steps visible to observer

From Existing Skills:
- **Modular, composable skills**: Single responsibility
- **Consistent structure**: YAML frontmatter + markdown
- **Self-contained documentation**: Each skill usable alone
- **Reference materials**: Supporting files for depth

### Recommended Architecture

```
                    ┌─────────────────┐
                    │   Orchestrator  │
                    │   (Workflow)    │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │   Manager   │   │  Developer  │   │  Reviewer   │
    │  (Subagent) │   │  (Subagent) │   │  (Subagent) │
    └─────────────┘   └─────────────┘   └─────────────┘
           │                 │                 │
           │         ┌───────┴───────┐         │
           │         │               │         │
        ┌──▼──┐   ┌──▼──┐       ┌──▼──┐   ┌──▼──┐
        │Gates│   │Code │       │Test │   │Code │
        │Check│   │Write│       │Run  │   │Eval │
        └─────┘   └─────┘       └─────┘   └─────┘
```

---

---

## 6. AgentSkills.io Standard Analysis

### Source: https://agentskills.io

### Overview

Agent Skills is a **lightweight, open format** for extending AI agent capabilities with specialized knowledge and workflows. The standard emphasizes simplicity and portability.

### Core Principle: Progressive Disclosure

Skills use progressive disclosure to manage context efficiently:

1. **Discovery**: At startup, agents load only `name` and `description` (~100 tokens each)
2. **Activation**: When task matches skill description, agent reads full `SKILL.md` instructions
3. **Execution**: Agent follows instructions, loading referenced files as needed

### Directory Structure

```
skill-name/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

### SKILL.md Format

```yaml
---
name: skill-name               # Required: 1-64 chars, lowercase, hyphens only
description: When to use...    # Required: 1-1024 chars, includes trigger keywords
license: Apache-2.0            # Optional: License reference
compatibility: Claude Code     # Optional: 1-500 chars, environment requirements
metadata:                      # Optional: Arbitrary key-value pairs
  author: org-name
  version: "1.0"
allowed-tools: Bash(git:*) Read  # Optional: Experimental, pre-approved tools
---

# Skill Title

[Markdown instructions - no format restrictions]
```

### Field Specifications

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | 1-64 chars, lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens |
| `description` | Yes | 1-1024 chars, describes what AND when to use |
| `license` | No | License name or file reference |
| `compatibility` | No | 1-500 chars, environment requirements |
| `metadata` | No | Arbitrary key-value map |
| `allowed-tools` | No | Space-delimited tool list (experimental) |

### Name Validation Rules

- **Valid**: `pdf-processing`, `data-analysis`, `code-review`
- **Invalid**: `PDF-Processing` (uppercase), `-pdf` (leading hyphen), `pdf--processing` (consecutive hyphens)

### Description Best Practices

Good:
```yaml
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
```

Poor:
```yaml
description: Helps with PDFs.
```

### Optional Directories

| Directory | Purpose | Best Practices |
|-----------|---------|----------------|
| `scripts/` | Executable code | Self-contained, document dependencies, helpful errors |
| `references/` | Additional documentation | Keep files focused (<500 lines), load on demand |
| `assets/` | Static resources | Templates, images, data files |

### Context Budget Recommendations

- **Metadata**: ~100 tokens (loaded at startup for all skills)
- **Instructions**: <5000 tokens recommended (loaded on activation)
- **SKILL.md**: <500 lines (move details to reference files)

### Integration Approaches

**Filesystem-based agents** (Claude Code):
- Skills activated via shell commands: `cat /path/to/skill/SKILL.md`
- Most capable option

**Tool-based agents**:
- Custom tools trigger skills
- Implementation-specific

### System Prompt Format

For Claude models, recommended XML format:

```xml
<available_skills>
  <skill>
    <name>pdf-processing</name>
    <description>Extracts text from PDFs...</description>
    <location>/path/to/skills/pdf-processing/SKILL.md</location>
  </skill>
</available_skills>
```

### Validation

Use `skills-ref` library:
```bash
skills-ref validate ./my-skill
skills-ref to-prompt ./skills/*
```

---

## 7. Anthropic Official Skills Analysis

### Source: https://github.com/anthropics/skills (58.9k stars)

### Repository Purpose

Official repository implementing the Agent Skills standard, demonstrating:
- Production-quality skill examples
- Plugin architecture for Claude Code
- Best practices for skill authoring

### Repository Structure

```
anthropics/skills/
├── .claude-plugin/          # Plugin configuration
├── skills/                  # Example skills
│   ├── docx/               # Document skills (source-available)
│   ├── pdf/                # PDF skills (source-available)
│   ├── pptx/               # PowerPoint skills
│   ├── xlsx/               # Excel skills
│   └── [other examples]
├── spec/                    # Agent Skills specification
│   └── agent-skills-spec.md
├── template/                # Skill template
│   └── SKILL.md
├── README.md
└── THIRD_PARTY_NOTICES.md
```

### Skill Template

The official template provides a starting point:

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here that Claude will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

### Plugin Installation (Claude Code)

```bash
# Register marketplace
/plugin marketplace add anthropics/skills

# Install skill sets
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

### Usage Pattern

```
"Use the PDF skill to extract the form fields from path/to/some-file.pdf"
```

### Licensing

| Type | Skills | License |
|------|--------|---------|
| Open Source | Most skills | Apache 2.0 |
| Source-Available | docx, pdf, pptx, xlsx | Shared for reference only |

### Key Patterns Observed

1. **Minimal Frontmatter**: Only `name` and `description` required
2. **Clear Sections**: Examples, Guidelines, Instructions
3. **Self-Contained**: Each skill folder is independent
4. **Category Organization**: Skills grouped by function

### Recommended Skill Structure

```markdown
---
name: skill-name
description: Complete description with trigger keywords
---

# Skill Title

Brief overview of what this skill does.

## When to Use
Clear triggers for activation.

## Instructions
Step-by-step guidance.

## Examples
Concrete usage examples.

## Guidelines
Do's and don'ts.

## References
Links to supporting files.
```

---

## 8. obra/superpowers Plugin Analysis

### Source: https://github.com/obra/superpowers

### Overview

Superpowers is a "complete software development workflow" built on composable skills. It provides enforced development methodology rather than optional suggestions.

### Plugin Configuration (plugin.json)

```json
{
  "name": "superpowers",
  "description": "Core skills library for Claude Code: TDD, debugging, collaboration patterns, and proven techniques",
  "version": "4.1.1",
  "author": {
    "name": "Jesse Vincent",
    "email": "jesse@fsck.com"
  },
  "homepage": "https://github.com/obra/superpowers",
  "repository": "https://github.com/obra/superpowers",
  "license": "MIT",
  "keywords": ["skills", "tdd", "debugging", "collaboration", "best-practices", "workflows"]
}
```

### Plugin.json Schema

| Field | Type | Purpose |
|-------|------|---------|
| `name` | string | Plugin identifier |
| `description` | string | Functional overview |
| `version` | string | Semantic versioning |
| `author` | object | Developer attribution (name, email) |
| `homepage` | string | Project website |
| `repository` | string | Source code URL |
| `license` | string | License type |
| `keywords` | array | Tags for discoverability |

### Directory Structure

```
superpowers/
├── .claude-plugin/          # Plugin config (plugin.json)
├── skills/                  # Reusable workflow modules
│   ├── test-driven-development
│   ├── systematic-debugging
│   ├── brainstorming
│   ├── writing-plans
│   ├── executing-plans
│   └── code-review
├── commands/                # User-facing CLI commands
│   ├── brainstorm
│   ├── write-plan
│   └── execute-plan
├── agents/                  # Subagent configurations
├── hooks/                   # Automatic triggers
├── lib/                     # Shared utilities
├── tests/                   # Validation tests
└── docs/                    # Platform-specific docs
```

### Key Patterns

1. **Separation of Concerns**:
   - `skills/` = Reusable knowledge modules
   - `commands/` = User-invokable actions
   - `hooks/` = Automatic triggers
   - `agents/` = Subagent configurations

2. **Enforced Workflow**:
   ```
   brainstorming -> git-worktrees -> plan-writing ->
   subagent-execution -> TDD -> code-review -> completion
   ```

3. **Platform Support**:
   - `.claude-plugin/` for Claude Code
   - `.codex/` for Codex
   - `.opencode/` for OpenCode

4. **Subagent Architecture**:
   - Parallel task execution
   - Automated code review stages
   - Spec compliance verification + quality assessment

### Reusable Patterns for Our Design

1. **Plugin Manifest**: Simple `plugin.json` for metadata
2. **Skills as Modules**: Each skill in its own directory with `SKILL.md`
3. **Commands Layer**: Separate commands from skills
4. **Hooks for Automation**: Trigger skills based on context
5. **Cross-Platform**: Support multiple agent platforms

---

## 9. GitOps Workflow Design

### Purpose

Integrate Git operations into the Manager-Doer workflow for:
- Isolated feature development
- Clean commit history
- Automated branch management
- PR creation and review

### Git Workflow Integration

```
Phase 0: Discovery
├── Create feature branch from main
├── Set up git worktree (optional for parallel work)
└── Initialize tracking

Phase 1: Development
├── Atomic commits per step
├── Conventional commit messages
└── Branch stays up-to-date

Phase 2: Refinement
├── Squash or rebase if needed
└── Clean up commit history

Phase 3: Completion
├── Create pull request
├── Address review comments
├── Merge to main
└── Clean up branch/worktree
```

### Branch Naming Convention

```
feature/{module-name}
fix/{issue-description}
refactor/{component-name}
```

### Conventional Commits

```
type(scope): description

Types:
- feat: New feature
- fix: Bug fix
- refactor: Code change (no new feature or bug fix)
- test: Adding tests
- docs: Documentation
- chore: Maintenance

Examples:
feat(catalog): add dependency graph resolution
fix(auth): handle expired token gracefully
test(catalog): add edge case tests for resolver
```

### Worktree Management

For parallel development:

```bash
# Create worktree for feature
git worktree add ../project-feature-name feature/feature-name

# List worktrees
git worktree list

# Remove worktree after merge
git worktree remove ../project-feature-name
```

### Commit Strategy per Phase

| Phase | Commit Pattern | Message Format |
|-------|---------------|----------------|
| Phase 0 | 1 commit | `chore(module): initialize development` |
| Phase 1 | 1 per step | `feat(module): [step description]` |
| Phase 2 | Amend/squash | `fix(module): address review feedback` |
| Phase 3 | Final | `docs(module): complete documentation` |

### Pull Request Template

```markdown
## Summary
Brief description of what this PR accomplishes.

## Changes
- Change 1
- Change 2

## Quality Gates
- [ ] Code Quality: 0 critical, >= 85% zen-python
- [ ] Testing: >= 5 scenarios, 0 errors
- [ ] Integration: No breaking changes
- [ ] Documentation: Public APIs documented

## Test Plan
How to test these changes.

## Related Issues
Closes #123
```

### Merge Strategy

1. **Squash merge** for clean history (default)
2. **Rebase merge** for detailed history (when commits are clean)
3. **Never merge commits** that don't pass CI

### Branch Cleanup

After merge:
```bash
# Delete remote branch
git push origin --delete feature/module-name

# Delete local branch
git branch -d feature/module-name

# Remove worktree if used
git worktree remove ../project-module-name
```

---

## 10. References

### Primary Sources

- Manager-Doer Orchestrator: `/Users/james/Downloads/manager-doer-orchestrator/`
- Claude Code Skills: `/Users/james/.claude/skills/`

### Anthropic Documentation

- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Project Vend Phase Two](https://www.anthropic.com/research/project-vend-2)
- [Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

### Agent Skills Standard

- [AgentSkills.io Specification](https://agentskills.io/specification)
- [AgentSkills.io Integration Guide](https://agentskills.io/integrate-skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [skills-ref Reference Library](https://github.com/agentskills/agentskills/tree/main/skills-ref)

### Community Implementations

- [obra/superpowers](https://github.com/obra/superpowers) - Complete development workflow plugin
- [Agentic Workflows with Claude (Medium)](https://medium.com/@aminsiddique95/agentic-workflows-with-claude-architecture-patterns-design-principles-production-patterns-72bbe4f7e85a)
- [Building AI Agents with Anthropic's 6 Composable Patterns](https://research.aimultiple.com/building-ai-agents/)
