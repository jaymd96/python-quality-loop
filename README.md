# python-quality-loop

A comprehensive Manager-Doer workflow plugin for Claude Code that enforces quality gates throughout iterative Python development.

## What It Does

`python-quality-loop` implements a structured, disciplined approach to Python development using:

- **Manager-Doer Orchestration**: Three specialized roles (Manager, Developer, Reviewer) with clear responsibilities
- **Quality Gates**: Automated checks at each phase to prevent regressions
- **Iterative Phases**: 4-phase workflow (Discovery, Development, Refinement, Completion)
- **Unix Philosophy**: Composition over reimplementation, leveraging existing packages
- **Playground Exploration**: Knuth's dogfooding principle for discovering features
- **GitOps Integration**: Conventional commits, branching strategies, PR workflows
- **Code Standards**: Python layout, coding patterns, and testing standards
- **Literate Programming**: Write Python with meaningful annotations using literate style

## Installation

### Option 1: From GitHub (Recommended)

```bash
/plugin install jaymd96/python-quality-loop
```

### Option 2: From Marketplace

```bash
/plugin install python-quality-loop@official-marketplace
```

### Option 3: Local Development

```bash
git clone https://github.com/jaymd96/python-quality-loop.git
cd python-quality-loop
claude --plugin-dir .
```

## Quick Start

### 1. Start a New Workflow

Use the main workflow coordinator:

```
/python-quality-loop:workflow
```

This guides you through:
- **Phase 0**: Discovery (understand requirements, research packages, plan)
- **Phase 1**: Development (implement with quality gates)
- **Phase 2**: Refinement (address feedback if needed)
- **Phase 3**: Completion (finalize and merge to main)

### 2. Use Specific Roles

Each role has focused responsibilities:

#### Manager
```
/python-quality-loop:manager
```
Oversee progress, set quality expectations, make go/no-go decisions.

#### Developer
```
/python-quality-loop:developer
```
Investigate requirements, implement code, run tests, prepare for review.

#### Reviewer
```
/python-quality-loop:reviewer
```
Independently evaluate quality, compliance with gates, and readiness.

### 3. Use Supporting Skills

Research packages before implementing:
```
/python-quality-loop:package-research
```

Generate AI-friendly documentation:
```
/python-quality-loop:llmtxt-generation
```

Explore features through playground:
```
/python-quality-loop:playground-exploration
```

## Key Concepts

### Quality Gates

Each phase includes quality gates that must pass:

**Code Quality**
- Zero critical issues
- ≥85% adherence to Python Zen philosophy
- Public APIs documented

**Testing**
- ≥5 test scenarios
- Zero runtime errors
- Edge cases handled

**Integration**
- No breaking changes
- Follows existing patterns
- Clear git history

**Documentation**
- Public APIs documented
- Usage examples provided
- Integration points clear

### Workflow Decisions

At the end of each phase, choose:

| Decision | Action |
|----------|--------|
| **ACCEPT** | All gates pass → move to next phase |
| **ITERATE** | Fixable issues → focused improvements with feedback |
| **ESCALATE** | Fundamental issues → stop and reassess approach |

### Manager-Doer Pattern

- **Manager**: Sets expectations, evaluates quality, makes decisions
- **Developer**: Implements solutions, tests thoroughly, reports status
- **Reviewer**: Independent quality validation, recommends decisions

This separation prevents conflicts of interest and ensures objective evaluation.

## Documentation

Comprehensive guides are included:

- **[DESIGN_PROPOSAL.md](DESIGN_PROPOSAL.md)**: Architecture and design rationale
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)**: Step-by-step usage instructions
- **[RESEARCH_FINDINGS.md](RESEARCH_FINDINGS.md)**: Background research and philosophy
- **[SKILL_STANDARD.md](SKILL_STANDARD.md)**: Standards reference for skills
- **[PLUGIN_ARCHITECTURE_LEARNINGS.md](PLUGIN_ARCHITECTURE_LEARNINGS.md)**: Claude Code plugin architecture insights

## Skills Reference

14 skills organized into 5 categories:

### Roles (3)
| Skill | Purpose |
|-------|---------|
| **workflow-manager** | Manager role oversight and decisions |
| **workflow-developer** | Developer role implementation |
| **workflow-reviewer** | Reviewer role quality validation |

### Workflow (2)
| Skill | Purpose |
|-------|---------|
| **python-development-workflow** | Overall orchestration coordinator |
| **gitops-workflow** | Git operations and branching |

### Foundations (4)
| Skill | Purpose |
|-------|---------|
| **python-coding-standards** | Coding patterns and style |
| **python-testing-standards** | Testing with pytest |
| **python-layout** | Project structure and organization |
| **literate-python** | **NEW** - Literate programming annotations |

### Philosophy (3)
| Skill | Purpose |
|-------|---------|
| **unix-philosophy** | Composition over reimplementation |
| **package-research** | Package discovery and evaluation |
| **playground-exploration** | Dogfooding and feature discovery |

### Tools (1)
| Skill | Purpose |
|-------|---------|
| **llmtxt-generation** | AI-friendly documentation |

See [skills/README.md](skills/README.md) for detailed documentation of all skills.

## Examples

### Example 1: Adding a New Feature

```
Phase 0: Discovery
  → What's the requirement?
  → Research similar packages?
  → Plan the approach

Phase 1: Development
  → Implement with tests
  → Check quality gates
  → Manager reviews design

Phase 2: Refinement (if needed)
  → Address feedback
  → Retest quality gates

Phase 3: Completion
  → Final review
  → Merge to main
```

### Example 2: Bug Fix

```
Phase 0: Discovery (quick)
  → Understand the bug
  → Reproduce the issue

Phase 1: Development
  → Fix the issue
  → Add regression test
  → Verify quality

Phase 3: Completion
  → Skip refinement if gates pass
  → Merge to main
```

## Configuration

The plugin works with minimal configuration. For advanced usage, see [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md).

## Requirements

- Claude Code 1.0.33 or later
- Git (for GitOps features)
- Python 3.8+ (for development tasks)

## Philosophy

This plugin is built on several core philosophies:

1. **Manager-Doer Pattern** (from Anthropic's "Project Vend"): Clear role separation prevents conflicts
2. **Quality Gates**: Automated checks catch issues early
3. **Unix Philosophy**: Small, focused tools composed together
4. **Knuth's Dogfooding**: Be your own first user, discover through usage
5. **Iterative Improvement**: ACCEPT/ITERATE/ESCALATE decisions support learning

## Troubleshooting

### Plugin not loading
```bash
# Check if plugin is enabled
/plugin list

# Try restarting Claude Code
# Then test with --plugin-dir flag
claude --plugin-dir ./python-quality-loop
```

### Skills not appearing
Make sure you've restarted Claude Code after installation.

### Git operations failing
Ensure you're in a git repository and have proper permissions.

## Contributing

Found an issue or have suggestions? [Open an issue](https://github.com/jaymd96/python-quality-loop/issues) on GitHub.

## License

Apache-2.0 - See [LICENSE](LICENSE) file for details

## Version

Current: 1.4.0 - Reorganized skills into categories, added literate-python skill

See [CHANGELOG](CHANGELOG.md) for version history and migration guide if upgrading from 1.3.0.

## Support

For questions or issues:
- Check [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for usage help
- Review [RESEARCH_FINDINGS.md](RESEARCH_FINDINGS.md) for philosophy background
- Open an issue on [GitHub](https://github.com/jaymd96/python-quality-loop/issues)
