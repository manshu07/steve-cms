#!/bin/bash

# Code Quality Reminder Hook
# Runs after code edits to remind about quality checks

# Skip if environment variable is set
if [ -n "$SKIP_QUALITY_REMINDER" ]; then
    exit 0
fi

# Only show reminder if files were edited
EDITED_FILES=$(cat 2>/dev/null)

if [ -z "$EDITED_FILES" ]; then
    exit 0
fi

# Check if TypeScript, TSX, or JavaScript files were edited
if echo "$EDITED_FILES" | grep -E '\.(ts|tsx|js|jsx)$' > /dev/null; then
    cat << 'EOF'

🔍 Code Quality Reminder

You've edited TypeScript/JavaScript files. Before committing:

1. Run linting:   npm run lint
2. Type check:    npm run typecheck
3. Format code:   npm run format

Use /code-quality to run all checks at once.

EOF
fi
