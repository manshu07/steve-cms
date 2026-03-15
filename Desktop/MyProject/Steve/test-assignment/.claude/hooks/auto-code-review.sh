#!/bin/bash
# Auto Code Review Hook
# Runs when files are saved/edited to provide instant feedback

# Get the file being edited
FILE_PATH="${CLAUDE_TOOL_INPUT:-}"
FILE_EXT="${FILE_PATH##*.}"

# Determine review type based on file extension
case "$FILE_EXT" in
    py)
        echo "🐍 Python file detected - Python best practices apply"
        echo "💡 Tip: Use 'python-code-reviewer' agent for full review"
        ;;
    ts|tsx)
        echo "📘 TypeScript file detected - Frontend guidelines apply"
        echo "💡 Tip: Use 'code-architecture-reviewer' agent for full review"
        ;;
    js|jsx)
        echo "📜 JavaScript file detected - Best practices apply"
        ;;
    md)
        echo "📝 Markdown file detected"
        ;;
    *)
        # No specific review for other files
        ;;
esac

# Check for common issues in any file
if grep -q "TODO\|FIXME\|XXX\|HACK" "$FILE_PATH" 2>/dev/null; then
    echo "⚠️ Found TODO/FIXME markers in $FILE_PATH"
fi

exit 0