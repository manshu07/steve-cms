#!/usr/bin/env bash
# Hook State Cleanup Script
# Removes stale session state files from hooks/state/

STATE_DIR=".claude/hooks/state"
MAX_AGE_DAYS=7

echo "🧹 Cleaning up hook session state..."

# Check if state directory exists
if [ ! -d "$STATE_DIR" ]; then
    echo "✓ State directory does not exist, nothing to clean"
    exit 0
fi

# Find and remove session state files older than MAX_AGE_DAYS
REMOVED=0
for file in "$STATE_DIR"/*.json 2>/dev/null; do
    if [ -f "$file" ]; then
        # Get file age in days
        FILE_AGE=$(( ($(date +%s) - $(stat -c %Y "$file" 2>/dev/null || stat -f %m "$file" 2>/dev/null || echo "0")) / 86400 ))

        if [ $FILE_AGE -gt $MAX_AGE_DAYS ]; then
            echo "  Removing: $(basename "$file") (${FILE_AGE} days old)"
            rm "$file"
            ((REMOVED++))
        fi
    fi
done

if [ $REMOVED -eq 0 ]; then
    echo "✓ No stale session files found (older than ${MAX_AGE_DAYS} days)"
else
    echo "✓ Removed $REMOVED stale session file(s)"
fi

# Show current state directory size
if [ "$(ls -A "$STATE_DIR" 2>/dev/null)" ]; then
    SIZE=$(du -sh "$STATE_DIR" 2>/dev/null | cut -f1)
    FILE_COUNT=$(ls -1 "$STATE_DIR"/*.json 2>/dev/null | wc -l)
    echo "  Current: $FILE_COUNT active session files (${SIZE})"
else
    echo "  State directory is empty"
fi

echo "✓ Hook state cleanup complete"
