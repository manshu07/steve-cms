# Skill Directory Structure Standards

## Overview

This document defines the standard directory structure for Claude Code skills. All skills should follow this structure for consistency and maintainability.

## Required Structure

Every skill MUST have:

```
skill-name/
└── SKILL.md (required)
```

### SKILL.md Requirements

**File:** `SKILL.md` (required)

**YAML Frontmatter** (required):
```yaml
---
name: skill-name
description: Brief description including trigger keywords (max 1024 chars)
---
```

**Content:**
- Markdown instructions and guidance
- Under 500 lines (per Anthropic's 500-line rule)
- Use progressive disclosure for detailed content

## Optional Resource Directories

Skills may include one or more of these optional directories:

### 1. `resources/` (Common Convention)

**Purpose:** General resource files (documentation, examples, patterns)

**When to use:**
- Skill has reference documentation
- Skill includes code examples
- Skill needs pattern libraries

**Example:**
```
backend-dev-guidelines/
├── SKILL.md
└── resources/
    ├── patterns.md
    ├── examples.md
    └── architecture.md
```

**Note:** This is the most widely used convention (35/36 skills use it)

### 2. `references/` (Official Standard)

**Purpose:** Documentation to be loaded into context as needed

**When to use:**
- Large reference documents (>10k words)
- API documentation
- Domain schemas
- Best practice guides

**Best Practices:**
- Keep SKILL.md lean
- Include grep patterns in SKILL.md for finding relevant sections
- Add table of contents for files >100 lines

### 3. `scripts/` (Executable Code)

**Purpose:** Executable code (Python, Bash, TypeScript, etc.)

**When to use:**
- Same code rewritten repeatedly
- Deterministic reliability needed
- Token-intensive operations

**Benefits:**
- Token efficient
- May execute without loading into context
- Testable and maintainable

**Example:**
```
continuous-learning-v2/
├── SKILL.md
└── scripts/
    ├── extract-patterns.py
    └── analyze-commits.sh
```

### 4. `assets/` (Output Files)

**Purpose:** Files used in output, not loaded into context

**When to use:**
- Templates (HTML, React, PowerPoint)
- Images (logos, icons, brand assets)
- Boilerplate code
- Font files
- Sample documents

**Example:**
```
frontend-slides/
├── SKILL.md
└── assets/
    ├── templates/
    │   ├── presentation.html
    │   └── slide-template.html
    └── fonts/
        └── custom-font.ttf
```

## Directory Naming Convention

### Recommended: `resources/`

**Rationale:**
- Widely adopted (35/36 skills)
- Simple and generic
- Works for most use cases
- Easy to remember

### When to Use Other Directories

- **Use `scripts/`**: When you have executable code
- **Use `assets/`**: When you have templates or output files
- **Use `references/`**: When following strict skill-developer guidelines

### Migration Path

If you have a skill using non-standard directories:

1. **Keep it** if it works
2. **Consider renaming** to `resources/` for consistency
3. **Document** your choice in SKILL.md

## Validation

Use the validation script to check skill structure:

```bash
# Validate all skills
.claude/scripts/validate-skill.sh

# Validate specific skill
.claude/scripts/validate-skill.sh skill-name
```

The script checks:
- ✓ SKILL.md exists
- ✓ YAML frontmatter with `name:` and `description:`
- ✓ Description < 1024 characters
- ✓ SKILL.md < 500 lines
- ✓ No non-standard directories (warns if found)

## Examples

### Minimal Skill (No Resources)

```
frontend-patterns/
└── SKILL.md  # All content inline (642 lines - exceeds 500-line rule)
```

### Standard Skill (Resources)

```
backend-dev-guidelines/
├── SKILL.md  # Main guidelines
└── resources/
    ├── patterns.md
    ├── examples.md
    └── architecture.md
```

### Complex Skill (Multiple Resource Types)

```
continuous-learning-v2/
├── SKILL.md
├── scripts/
│   ├── extract-patterns.py
│   └── analyze-commits.sh
└── resources/
    ├── patterns.md
    └── examples.md
```

## Decision Tree

```
Does your skill need extra files?
├─ No → Use SKILL.md only (like frontend-patterns)
└─ Yes → What type of files?
    ├─ Executable code? → Add scripts/
    ├─ Templates/images? → Add assets/
    ├─ Reference docs? → Add references/ OR resources/
    └─ General resources? → Add resources/ (recommended)
```

## Summary

| Directory | Purpose | When to Use | Prevalence |
|-----------|---------|-------------|------------|
| `SKILL.md` | Main content | **Always required** | 36/36 (100%) |
| `resources/` | General resources | Most common | 35/36 (97%) |
| `scripts/` | Executable code | Code automation | 1/36 (3%) |
| `references/` | Context docs | Large references | 0/36 (0%) |
| `assets/` | Output files | Templates/images | 0/36 (0%) |

**Recommendation:** Use `resources/` for most cases. It's simple, widely adopted, and works well.

---

**Last Updated:** 2025-03-09
**Validated By:** `.claude/scripts/validate-skill.sh`
