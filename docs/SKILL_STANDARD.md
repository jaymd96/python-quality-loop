# Agent Skills Standard Reference

This document describes the Agent Skills standard used by this plugin, based on research from:
- [AgentSkills.io](https://agentskills.io/specification) - The open specification
- [Anthropic Skills Repository](https://github.com/anthropics/skills) - Official examples
- [obra/superpowers](https://github.com/obra/superpowers) - Community implementation

---

## Overview

Agent Skills is a **lightweight, open format** for extending AI agent capabilities with specialized knowledge and workflows.

### Core Principles

1. **Simplicity**: A skill is just a folder with a `SKILL.md` file
2. **Portability**: Skills are files that can be easily shared and versioned
3. **Progressive Disclosure**: Load only what's needed when it's needed
4. **Self-Documenting**: Skills are readable by both humans and agents

---

## Directory Structure

### Minimum Required

```
skill-name/
└── SKILL.md          # Required: instructions + metadata
```

### Full Structure

```
skill-name/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
│   └── script.py
├── references/       # Optional: detailed documentation
│   └── REFERENCE.md
└── assets/           # Optional: templates, resources
    └── template.md
```

---

## SKILL.md Format

### Required Structure

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---

# Skill Title

[Markdown instructions that the agent will follow]
```

### With Optional Fields

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
license: Apache-2.0
compatibility: Designed for Claude Code. Requires git for GitOps features.
metadata:
  author: organization-name
  version: "1.0.0"
  category: development-workflow
allowed-tools: Bash(git:*) Read Write Edit
---

# Skill Title

[Markdown instructions]
```

---

## Field Specifications

### Required Fields

| Field | Constraints | Description |
|-------|-------------|-------------|
| `name` | 1-64 chars, lowercase alphanumeric + hyphens | Unique identifier for the skill |
| `description` | 1-1024 chars | What the skill does AND when to use it |

### Optional Fields

| Field | Constraints | Description |
|-------|-------------|-------------|
| `license` | String | License name or file reference |
| `compatibility` | 1-500 chars | Environment requirements |
| `metadata` | Key-value map | Arbitrary additional metadata |
| `allowed-tools` | Space-delimited | Pre-approved tools (experimental) |

---

## Name Validation Rules

The `name` field must:
- Be 1-64 characters long
- Contain only lowercase alphanumeric characters and hyphens (`a-z`, `0-9`, `-`)
- Not start or end with a hyphen
- Not contain consecutive hyphens (`--`)
- Match the parent directory name (recommended)

### Valid Examples

```yaml
name: pdf-processing
name: data-analysis
name: code-review
name: python-testing
```

### Invalid Examples

```yaml
name: PDF-Processing    # Uppercase not allowed
name: -pdf              # Cannot start with hyphen
name: pdf-              # Cannot end with hyphen
name: pdf--processing   # Consecutive hyphens not allowed
name: pdf processing    # Spaces not allowed
```

---

## Description Best Practices

The `description` field should:
- Describe **what** the skill does
- Describe **when** to use the skill
- Include specific **trigger keywords**
- Be actionable for the agent

### Good Examples

```yaml
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.

description: Manager role for Python development workflow. Use when overseeing module development, defining quality gates, evaluating iteration reports, or making ACCEPT/ITERATE/ESCALATE decisions.

description: Git operations and branch management for iterative development. Use when creating feature branches, managing worktrees, making commits, creating pull requests, or cleaning up after merges.
```

### Poor Examples

```yaml
description: Helps with PDFs.  # Too vague, no triggers

description: Code review.  # What does it do? When to use?

description: A skill for the workflow.  # No actionable information
```

---

## Body Content Guidelines

### Recommended Sections

```markdown
---
name: example-skill
description: What it does and when to use it.
---

# Skill Title

Brief overview of what this skill does and its philosophy.

## Quick Reference

Condensed guidance for common use cases.

## When to Use This Skill

Clear triggers and conditions for activation.

## Instructions

Step-by-step guidance for using the skill.

## Examples

Concrete usage examples with inputs and outputs.

## Guidelines

Do's and don'ts, best practices.

## Common Patterns

Reusable patterns for typical scenarios.

## Anti-Patterns

What to avoid and why.

## References

Links to supporting files or external documentation.
```

### Context Budget

- **Target**: < 5000 tokens for the full SKILL.md
- **SKILL.md**: Keep under 500 lines
- **Details**: Move to `references/` directory
- **Load on demand**: Agent reads references only when needed

---

## Optional Directories

### scripts/

Executable code that agents can run.

**Best Practices**:
- Scripts should be self-contained
- Clearly document dependencies
- Include helpful error messages
- Handle edge cases gracefully

**Supported Languages**: Depends on agent implementation (commonly Python, Bash, JavaScript)

### references/

Additional documentation loaded on demand.

**Common Files**:
- `REFERENCE.md` - Detailed technical reference
- `PATTERNS.md` - Reusable code patterns
- `TEMPLATES.md` - Document templates
- Domain-specific files

**Best Practices**:
- Keep individual files focused (< 500 lines)
- Name files clearly
- Reference from main SKILL.md

### assets/

Static resources for the skill.

**Common Contents**:
- Templates (document templates, configuration templates)
- Images (diagrams, examples)
- Data files (lookup tables, schemas)

---

## Progressive Disclosure

Skills are designed for efficient context management:

### Loading Stages

| Stage | What Loads | Token Budget | When |
|-------|------------|--------------|------|
| **Discovery** | `name` + `description` only | ~100 tokens | Startup |
| **Activation** | Full `SKILL.md` body | < 5000 tokens | Task match |
| **Execution** | Referenced files | As needed | On demand |

### Design for Progressive Loading

1. **Metadata**: Keep `name` and `description` concise
2. **Main Content**: Include essential instructions in SKILL.md
3. **Details**: Move detailed references to separate files
4. **Reference Clearly**: Tell agents when to load additional files

---

## Plugin Configuration (plugin.json)

For Claude Code plugins, include a `plugin.json` in `.claude-plugin/`:

```json
{
  "name": "plugin-name",
  "description": "Brief description of the plugin",
  "version": "1.0.0",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "repository": "https://github.com/org/repo",
  "license": "Apache-2.0",
  "keywords": ["skill", "workflow", "python"],
  "compatibility": "Designed for Claude Code",
  "metadata": {
    "category": "development"
  },
  "skills": [
    {
      "name": "skill-one",
      "path": "skills/skill-one.md",
      "description": "Brief description"
    },
    {
      "name": "skill-two",
      "path": "skills/skill-two.md",
      "description": "Brief description"
    }
  ]
}
```

### Plugin.json Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Plugin identifier |
| `description` | Yes | What the plugin provides |
| `version` | Yes | Semantic version |
| `author` | No | Author information |
| `repository` | No | Source code URL |
| `license` | No | License type |
| `keywords` | No | Discovery tags |
| `compatibility` | No | Requirements |
| `metadata` | No | Additional data |
| `skills` | No | List of skills with paths |

---

## System Prompt Integration

For Claude models, skills are injected into the system prompt using XML:

```xml
<available_skills>
  <skill>
    <name>pdf-processing</name>
    <description>Extracts text and tables from PDF files...</description>
    <location>/path/to/skills/pdf-processing/SKILL.md</location>
  </skill>
  <skill>
    <name>data-analysis</name>
    <description>Analyzes datasets and generates reports...</description>
    <location>/path/to/skills/data-analysis/SKILL.md</location>
  </skill>
</available_skills>
```

---

## Validation

Use the `skills-ref` reference library to validate skills:

```bash
# Validate a skill directory
skills-ref validate ./my-skill

# Generate system prompt XML
skills-ref to-prompt ./skills/*
```

### Validation Checks

- `name` field matches constraints
- `description` field present and non-empty
- Directory name matches `name` field (recommended)
- File structure is valid

---

## Creating a New Skill

### Step 1: Create Directory

```bash
mkdir my-skill-name
cd my-skill-name
```

### Step 2: Create SKILL.md

```bash
cat > SKILL.md << 'EOF'
---
name: my-skill-name
description: What this skill does. Use when [specific triggers].
---

# My Skill Name

Brief overview.

## When to Use

- Trigger condition 1
- Trigger condition 2

## Instructions

1. Step one
2. Step two
3. Step three

## Examples

### Example 1

[Concrete example]

## Guidelines

- Do this
- Avoid that
EOF
```

### Step 3: Add Optional Content

```bash
# If detailed documentation needed
mkdir references
cat > references/REFERENCE.md << 'EOF'
# Detailed Reference

[Extended documentation]
EOF

# If scripts needed
mkdir scripts
cat > scripts/helper.py << 'EOF'
#!/usr/bin/env python3
# Script implementation
EOF
```

### Step 4: Validate

```bash
skills-ref validate ./my-skill-name
```

---

## Checklist for Skill Authors

### Metadata
- [ ] `name` is lowercase, hyphenated, 1-64 chars
- [ ] `description` clearly states what AND when
- [ ] `description` includes trigger keywords
- [ ] Optional fields added if relevant

### Content
- [ ] Clear title and overview
- [ ] "When to Use" section with triggers
- [ ] Step-by-step instructions
- [ ] Concrete examples
- [ ] Guidelines and anti-patterns

### Structure
- [ ] SKILL.md under 500 lines
- [ ] Detailed content in references/
- [ ] Referenced files are focused
- [ ] Clear file organization

### Quality
- [ ] Self-contained (minimal dependencies)
- [ ] Human-readable documentation
- [ ] Agent-actionable instructions
- [ ] Tested with target agent

---

## References

### Official Specifications
- [AgentSkills.io Specification](https://agentskills.io/specification)
- [AgentSkills.io Integration Guide](https://agentskills.io/integrate-skills)

### Reference Implementations
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [skills-ref Library](https://github.com/agentskills/agentskills/tree/main/skills-ref)
- [obra/superpowers Plugin](https://github.com/obra/superpowers)

### Documentation
- [Claude Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
