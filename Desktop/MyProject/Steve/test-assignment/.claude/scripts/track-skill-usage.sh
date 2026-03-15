#!/usr/bin/env bash
# Skill Usage Tracking Script
# Tracks skill activations and provides analytics

ANALYTICS_DIR=".claude/analytics"
ANALYTICS_FILE="$ANALYTICS_DIR/skill-usage.jsonl"
DATE=$(date +%Y-%m-%d)

mkdir -p "$ANALYTICS_DIR"

# Initialize analytics file if it doesn't exist
if [ ! -f "$ANALYTICS_FILE" ]; then
    echo "[]" > "$ANALYTICS_FILE"
fi

# Track skill usage
track_skill() {
    local SKILL_NAME="$1"
    local SESSION_ID="$2"
    local TRIGGER_TYPE="${3:-keyword}"
    local TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    # Create JSON entry
    local ENTRY=$(cat <<EOF
{
  "timestamp": "$TIMESTAMP",
  "skill": "$SKILL_NAME",
  "session_id": "$SESSION_ID",
  "trigger_type": "$TRIGGER_TYPE",
  "date": "$DATE"
}
EOF
)

    # Append to analytics file (JSONL format)
    echo "$ENTRY" >> "$ANALYTICS_FILE"
}

# Show skill usage statistics
show_stats() {
    local DAYS="${1:-30}"

    echo "📊 Skill Usage Statistics (Last $DAYS days)"
    echo ""

    # Count skill activations
    if command -v jq >/dev/null 2>&1; then
        # Get cutoff date
        local CUTOFF_DATE=$(date -d "$DAYS days ago" +%Y-%m-%d 2>/dev/null || date -v-${DAYS}d +%Y-%m-%d)

        echo "Top Skills:"
        cat "$ANALYTICS_FILE" 2>/dev/null | \
            grep -v "^$" | \
            jq -r --arg date "$CUTOFF_DATE" '
                select(.date >= $date) | .skill
            ' 2>/dev/null | \
            sort | uniq -c | sort -rn | head -10 | \
            awk '{printf "  %2dx %s\n", $1, $2}'

        echo ""
        echo "Trigger Types:"
        cat "$ANALYTICS_FILE" 2>/dev/null | \
            grep -v "^$" | \
            jq -r --arg date "$CUTOFF_DATE" '
                select(.date >= $date) | .trigger_type
            ' 2>/dev/null | \
            sort | uniq -c | sort -rn | \
            awk '{printf "  %2dx %s\n", $1, $2}'

        echo ""
        echo "Daily Usage:"
        cat "$ANALYTICS_FILE" 2>/dev/null | \
            grep -v "^$" | \
            jq -r --arg date "$CUTOFF_DATE" '
                select(.date >= $date) | .date
            ' 2>/dev/null | \
            sort | uniq -c | sort -rn | \
            awk '{printf "  %2dx %s\n", $1, $2}'

    else
        echo "⚠️  jq not found. Raw data:"
        tail -20 "$ANALYTICS_FILE" 2>/dev/null
    fi
}

# Clear old analytics
cleanup_old_analytics() {
    local DAYS_TO_KEEP="${1:-90}"

    echo "🧹 Cleaning analytics older than $DAYS_TO_KEEP days..."

    if command -v jq >/dev/null 2>&1; then
        local CUTOFF_DATE=$(date -d "$DAYS_TO_KEEP days ago" +%Y-%m-%d 2>/dev/null || date -v-${DAYS_TO_KEEP}d +%Y-%m-%d)

        # Create temp file with recent entries
        local TEMP_FILE=$(mktemp)
        cat "$ANALYTICS_FILE" | \
            while read -r line; do
                ENTRY_DATE=$(echo "$line" | jq -r '.date' 2>/dev/null)
                if [[ "$ENTRY_DATE" > "$CUTOFF_DATE" ]]; then
                    echo "$line" >> "$TEMP_FILE"
                fi
            done

        # Replace original with filtered
        mv "$TEMP_FILE" "$ANALYTICS_FILE"
        echo "✓ Old analytics removed"
    else
        echo "⚠️  jq not found, skipping cleanup"
    fi
}

# Main script logic
case "${1:-stats}" in
    track)
        if [ -z "$2" ]; then
            echo "Usage: $0 track <skill-name> [session-id] [trigger-type]"
            exit 1
        fi
        track_skill "$2" "${3:-session-$(date +%s)}" "${4:-keyword}"
        ;;
    stats)
        show_stats "${2:-30}"
        ;;
    cleanup)
        cleanup_old_analytics "${2:-90}"
        ;;
    *)
        echo "Skill Usage Analytics"
        echo ""
        echo "Usage:"
        echo "  $0 track <skill-name> [session-id] [trigger-type]"
        echo "  $0 stats [days]"
        echo "  $0 cleanup [days-to-keep]"
        echo ""
        echo "Examples:"
        echo "  $0 track backend-dev-guidelines"
        echo "  $0 stats 7"
        echo "  $0 cleanup 30"
        exit 1
        ;;
esac
