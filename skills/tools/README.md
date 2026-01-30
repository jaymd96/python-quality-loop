# Tools: Utilities & Generation

This category contains utility skills for documentation generation and package integration.

## Overview

These are supporting tools that help with specific tasks like creating AI-friendly documentation for adopted packages.

## Skills

### [llmtxt.md](llmtxt.md)
Create concise documentation for LLM consumption using the llms.txt standard.

**When to use:** After adopting external packages (from package-research decision), to create AI-friendly documentation.

**Covers:**
- llms.txt standard format
- Creating concise API references
- Examples for common operations
- Integration points and quirks
- Performance considerations
- Using the llmtxt template

## When Tools are Used

Tools typically get invoked:
1. **After package adoption** (package-research → adopting external package)
2. **When documenting for AI** (creating context for Claude)
3. **When onboarding team** (sharing package knowledge)

## Example Workflow

```
Phase 0: Discovery

1. Package Research
   ↓
2. Decide to COMPOSE with existing package
   ↓
3. Create llmtxt documentation
   ├─ Read package docs
   ├─ Create concise API reference
   ├─ Add examples
   ├─ Document quirks
   └─ Save to project
   ↓
4. Developer uses llmtxt during implementation
   ├─ Better prompts to Claude
   ├─ Fewer mistakes
   ├─ Faster development
```

## Related

- See [philosophy/package-research.md](../philosophy/package-research.md) for how packages are selected
- See [foundations/](../foundations/) for technical skills
