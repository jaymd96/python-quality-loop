# Changelog

All notable changes to the python-quality-loop plugin are documented here.

## [1.4.0] - 2026-01-30

### Added
- **literate-python skill**: New skill for writing Python with literate programming annotations using Litterate syntax (`#>` markers)
- **Skill categorization**: Organized 14 skills into 5 logical categories:
  - `roles/` - Manager-Doer pattern (Manager, Developer, Reviewer)
  - `workflow/` - Orchestration and Git integration
  - `foundations/` - Core technical skills (Coding, Testing, Layout, Literate Python)
  - `philosophy/` - Design principles (Unix philosophy, Package Research, Playground)
  - `tools/` - Utilities (llmtxt generation)
- **Category READMEs**: Each category now has its own README explaining purpose, skills, and relationships

### Changed
- **BREAKING**: Skill file paths have changed due to reorganization
  - `skills/manager.md` → `skills/roles/manager.md`
  - `skills/python_coding.md` → `skills/foundations/python-coding.md`
  - All skills renamed from snake_case to kebab-case (Anthropic convention)
- **plugin.json**: Updated all skill paths to reflect new directory structure
- **Version bump**: 1.3.0 → 1.4.0 (major reorganization)

### Documentation
- Updated `skills/README.md` with category navigation and quick skill finder
- Added per-category README files for better context and relationships
- Updated version history and file structure documentation

### Migration Guide

If you're using older versions, update your skill references:

**Before (v1.3.0):**
```bash
/python-quality-loop:python-coding
/python-quality-loop:python-testing
```

**After (v1.4.0):**
```bash
/python-quality-loop:python-coding-standards
/python-quality-loop:python-testing-standards
```

All skills are still accessible via the same command names. The paths are internal only.

### Technical Details

- Total skills: 14 (13 existing + 1 new)
- Directory structure: 5 categories + references
- Skill naming: Kebab-case throughout
- Files moved/renamed: 12 existing + 1 new

### Related Files
- See `skills/README.md` for complete skill organization
- See `skills/foundations/literate-python.md` for annotation guide
- See `skills/foundations/references/literate-python-patterns.md` for examples

---

## [1.3.0] - 2026-01-29

### Added
- Playground skill for Knuth's dogfooding philosophy
- Python layout skill for consistent code organization
- Support for playground exploration files

### Changed
- Enhanced developer workflow documentation

---

## [1.2.0] - 2026-01-28

### Added
- Unix philosophy skill
- Package research skill
- llmtxt documentation generation skill

---

## [1.1.0] - 2026-01-27

### Added
- GitOps workflow skill
- Conventional commit support
- PR and branching documentation

---

## [1.0.0] - 2026-01-26

### Initial Release
- Manager-Doer workflow pattern
- 3 role skills (Manager, Developer, Reviewer)
- 7 technical skills (Workflow, GitOps, Coding, Testing, etc.)
- Quality gates framework
- ACCEPT/ITERATE/ESCALATE decision model
