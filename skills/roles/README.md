# Roles: Manager-Doer Workflow

This category contains skills for the three roles in the Manager-Doer pattern.

## Overview

The python-quality-loop uses a three-role system to ensure clear responsibility separation and prevent conflicts of interest:

- **Manager**: Sets expectations, evaluates quality, makes go/no-go decisions
- **Developer**: Implements solutions, tests thoroughly, reports status
- **Reviewer**: Independent quality validation, recommends decisions

## Skills

### [manager.md](manager.md)
Manager role for oversight, quality gates, and decisions.

**When to use:** When setting expectations, evaluating iteration reports, or making ACCEPT/ITERATE/ESCALATE decisions.

### [developer.md](developer.md)
Developer role for implementation and testing.

**When to use:** When implementing features, executing the 7-step workflow, or preparing iteration reports.

### [reviewer.md](reviewer.md)
Reviewer role for independent quality evaluation.

**When to use:** When independently evaluating quality gates or verifying that feedback was addressed.

## Pattern Benefits

- **No conflicts of interest**: Developer doesn't evaluate their own work
- **Fresh perspective**: Reviewer catches issues Developer missed
- **Objective decisions**: Manager has clear criteria from quality gates
- **Accountability**: Each role has specific responsibilities

## Related

- See [workflow/](../workflow/) for orchestration and coordination
- See [foundations/](../foundations/) for technical skills used within roles
