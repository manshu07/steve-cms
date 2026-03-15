#!/usr/bin/env bash
# Validate Claude Code Skills Structure
# Usage: .claude/scripts/validate-skill.sh [skill-name]
# If skill-name is provided, validates only that skill
# Otherwise, validates all skills in .claude/skills/

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_SKILLS=0
VALID_SKILLS=0
INVALID_SKILLS=0
WARNINGS=0

# Validate a single skill
validate_skill() {
    local skill_dir="$1"
    local skill_name=$(basename "$skill_dir")
    local has_errors=0
    local has_warnings=0

    echo -e "${BLUE}=== Validating: $skill_name ===${NC}"
    TOTAL_SKILLS=$((TOTAL_SKILLS + 1))

    # Check 1: SKILL.md exists
    if [ ! -f "$skill_dir/SKILL.md" ]; then
        echo -e "${RED}✗ MISSING: SKILL.md (required)${NC}"
        ((has_errors++))
    else
        echo -e "${GREEN}✓ SKILL.md exists${NC}"

        # Check 2: YAML frontmatter with name
        if ! grep -q "^name:" "$skill_dir/SKILL.md"; then
            echo -e "${RED}✗ MISSING: 'name:' in YAML frontmatter${NC}"
            has_errors=$((has_errors + 1))
        else
            local name=$(grep "^name:" "$skill_dir/SKILL.md" | cut -d' ' -f2-)
            echo -e "${GREEN}  ✓ name: $name${NC}"
        fi

        # Check 3: YAML frontmatter with description
        if ! grep -q "^description:" "$skill_dir/SKILL.md"; then
            echo -e "${RED}✗ MISSING: 'description:' in YAML frontmatter${NC}"
            has_errors=$((has_errors + 1))
        else
            local desc=$(grep "^description:" "$skill_dir/SKILL.md" | cut -d' ' -f2- | cut -c1-60)
            echo -e "${GREEN}  ✓ description: ${desc}...${NC}"
        fi

        # Check 4: Description length (should be < 1024 chars)
        local desc_length=$(grep "^description:" "$skill_dir/SKILL.md" | cut -d':' -f2- | wc -c | tr -d ' ')
        if [ "$desc_length" -gt 1024 ]; then
            echo -e "${YELLOW}⚠ WARNING: Description exceeds 1024 characters (${desc_length} chars)${NC}"
            has_warnings=$((has_warnings + 1))
        fi

        # Check 5: SKILL.md line count (should be < 500 lines per 500-line rule)
        local line_count=$(wc -l < "$skill_dir/SKILL.md" | tr -d ' ')
        if [ "$line_count" -gt 500 ]; then
            echo -e "${YELLOW}⚠ WARNING: SKILL.md exceeds 500 lines (${line_count} lines)${NC}"
            echo -e "${YELLOW}  Consider using progressive disclosure with reference files${NC}"
            has_warnings=$((has_warnings + 1))
        fi
    fi

    # Check 6: Optional directories (informational only)
    local has_resources=0
    local has_references=0
    local has_assets=0
    local has_scripts=0

    [ -d "$skill_dir/resources" ] && has_resources=1
    [ -d "$skill_dir/references" ] && has_references=1
    [ -d "$skill_dir/assets" ] && has_assets=1
    [ -d "$skill_dir/scripts" ] && has_scripts=1

    if [ $has_resources -eq 1 ]; then
        echo -e "${GREEN}  ✓ resources/ (present)${NC}"
    fi
    if [ $has_references -eq 1 ]; then
        echo -e "${GREEN}  ✓ references/ (present)${NC}"
    fi
    if [ $has_assets -eq 1 ]; then
        echo -e "${GREEN}  ✓ assets/ (present)${NC}"
    fi
    if [ $has_scripts -eq 1 ]; then
        echo -e "${GREEN}  ✓ scripts/ (present)${NC}"
    fi

    # Check 7: No non-standard directories
    for dir in "$skill_dir"/*/; do
        if [ -d "$dir" ]; then
            local dirname=$(basename "$dir")
            case "$dirname" in
                resources|references|assets|scripts)
                    # Standard directory, OK
                    ;;
                *)
                    echo -e "${YELLOW}⚠ NOTE: Non-standard directory: $dirname/${NC}"
                    has_warnings=$((has_warnings + 1))
                    ;;
            esac
        fi
    done

    # Summary for this skill
    if [ $has_errors -eq 0 ]; then
        echo -e "${GREEN}✓ VALID${NC}"
        VALID_SKILLS=$((VALID_SKILLS + 1))
    else
        echo -e "${RED}✗ INVALID${NC}"
        INVALID_SKILLS=$((INVALID_SKILLS + 1))
    fi

    if [ $has_warnings -gt 0 ]; then
        WARNINGS=$((WARNINGS + has_warnings))
    fi

    echo ""
}

# Main execution
SKILLS_DIR=".claude/skills"

if [ ! -d "$SKILLS_DIR" ]; then
    echo -e "${RED}Error: $SKILLS_DIR directory not found${NC}"
    exit 1
fi

# Check if specific skill requested
if [ -n "$1" ]; then
    skill_path="$SKILLS_DIR/$1"
    if [ ! -d "$skill_path" ]; then
        echo -e "${RED}Error: Skill '$1' not found in $SKILLS_DIR${NC}"
        exit 1
    fi
    validate_skill "$skill_path"
else
    # Validate all skills
    echo -e "${BLUE}Validating all skills in $SKILLS_DIR${NC}"
    echo ""

    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -d "$skill_dir" ]; then
            validate_skill "$skill_dir"
        fi
    done
fi

# Final summary
echo -e "${BLUE}=== Validation Summary ===${NC}"
echo -e "Total skills:     ${TOTAL_SKILLS}"
echo -e "${GREEN}Valid skills:     ${VALID_SKILLS}${NC}"
echo -e "${RED}Invalid skills:   ${INVALID_SKILLS}${NC}"
echo -e "${YELLOW}Total warnings:  ${WARNINGS}${NC}"
echo ""

if [ $INVALID_SKILLS -gt 0 ]; then
    echo -e "${RED}✗ Validation FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}✓ All skills are valid!${NC}"
    exit 0
fi
