"""
Generic Python Development Workflow Plugin

A Manager-Doer orchestration system for iterative Python development
with quality gates and structured decision frameworks.

Roles:
    - Manager: Oversight, goal-setting, quality evaluation, decisions
    - Developer: Investigation, implementation, testing, reporting
    - Reviewer: Independent quality evaluation

Phases:
    - Phase 0: Discovery - Understand before building
    - Phase 1: Development - Build with quality (iterative)
    - Phase 2: Refinement - Focused improvements
    - Phase 3: Completion - Production-ready finalization

Commands:
    - /start-project: Initialize workflow for new project/module
    - /iterate: Submit iteration report for evaluation
    - /check-status: View status of all active developments
    - /complete: Finalize and merge completed work

Inspired by:
    - Project Vend's manager-employee model
    - Anthropic's composable agent patterns
    - Claude Code skill architecture

Usage:
    Copy the skills/*.md files to your .claude/skills/ directory
    or use the workflow.md skill directly for orchestration.
"""

__version__ = "1.0.0"
__author__ = "Generic Python Workflow"

# Skill registry
SKILLS = [
    "manager",
    "developer",
    "reviewer",
    "python_coding",
    "python_testing",
    "workflow",
]

# Phase definitions
PHASES = {
    0: "Discovery",
    1: "Development",
    2: "Refinement",
    3: "Completion",
}

# Decision types
DECISIONS = [
    "ACCEPT",
    "ITERATE",
    "ESCALATE",
]

# Default quality gates
DEFAULT_GATES = {
    "code_quality": {
        "critical_issues": 0,
        "zen_compliance": 85,
        "docstring_coverage": 100,
    },
    "testing": {
        "scenarios_tested": 5,
        "runtime_errors": 0,
        "test_coverage": 80,
    },
    "integration": {
        "breaking_changes": 0,
        "patterns_followed": True,
    },
    "documentation": {
        "public_apis_documented": True,
        "examples_provided": 1,
    },
}
