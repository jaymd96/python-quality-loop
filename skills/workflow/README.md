# Workflow: Orchestration & Git Integration

This category contains skills for overall workflow orchestration and git-based version control operations.

## Overview

These skills manage the workflow structure across 4 phases and integrate with Git for version control.

## Skills

### [workflow.md](workflow.md)
Overall workflow orchestration coordinator.

**When to use:** When starting a new feature/module, transitioning between phases, or needing guidance on the overall workflow structure.

**Covers:**
- Phase 0: Discovery (understanding requirements, package research, planning)
- Phase 1: Development (implementation with quality gates)
- Phase 2: Refinement (addressing feedback)
- Phase 3: Completion (finalization and merge)

### [gitops.md](gitops.md)
Git operations, branching strategies, and PR workflows.

**When to use:** When creating branches, committing code, managing PRs, or needing guidance on conventional commits.

**Covers:**
- Feature branching strategies
- Conventional commit format
- Commit co-authorship
- Pull request workflows
- Merge and cleanup

## Workflow Phases

```
Phase 0: Discovery (30-60 min)
  ├─ 0.0: Branch Setup (GitOps)
  ├─ 0.1: Playground Setup
  ├─ 0.2: Package Research
  └─ 0.6: Manager Approval

Phase 1: Development (1-2 hrs/iteration, 2-4 iterations)
  ├─ 1.0: Implementation
  ├─ 1.1: Layout & Organization
  ├─ 1.2: Code Standards
  ├─ 1.3: Code Review
  ├─ 1.4: Playground Exploration
  ├─ 1.5: Testing
  ├─ 1.6: Git Commit
  └─ Report & Await Decision

Phase 2: Refinement (if ITERATE decision)
  └─ Focused improvements on flagged issues

Phase 3: Completion (if ACCEPT decision)
  ├─ Final cleanup
  ├─ Create PR
  └─ Merge & cleanup branches
```

## Decision Points

- **ACCEPT**: All quality gates pass → Phase 3
- **ITERATE**: Fixable issues → Phase 2
- **ESCALATE**: Fundamental issues → Stop and reassess

## Related

- See [roles/](../roles/) for Manager-Developer-Reviewer pattern
- See [foundations/](../foundations/) for technical skills
