---
description: Run comprehensive code quality checks including linting, type checking, and formatting
---

Run comprehensive code quality checks across the entire monorepo.

## Checks Performed

1. **ESLint** - Linting for code quality and consistency
2. **TypeScript** - Type checking for type safety
3. **Prettier** - Code formatting checks
4. **Build verification** - Ensures all packages build successfully

## Usage

```bash
/code-quality
```

## What Gets Checked

- All packages in `apps/`
- All packages in `packages/`
- Shared configurations
- Root level files

## Exit Codes

- `0` - All checks passed
- `1` - One or more checks failed

## Output Format

```
Running code quality checks...

🔍 ESLint
✅ apps/api - No issues
✅ apps/web - No issues
✅ packages/contracts - No issues

🔷 TypeScript
✅ apps/api - No errors
✅ apps/web - No errors
✅ packages/contracts - No errors

✨ Prettier
✅ All files formatted

🏗️  Build
✅ All packages build successfully

✨ Code quality checks passed!
```

## Fixing Issues

To automatically fix ESLint and Prettier issues:

```bash
npm run lint -- --fix
npm run format
```
