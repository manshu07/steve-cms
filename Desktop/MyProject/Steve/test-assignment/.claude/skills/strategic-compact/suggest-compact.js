#!/usr/bin/env node

/**
 * Strategic Compact Suggestion Hook
 *
 * Tracks tool usage and suggests manual /compact at strategic intervals.
 * Runs on PreToolUse for Edit and Write operations.
 *
 * Configuration via environment variables:
 * - COMPACT_THRESHOLD: Tool calls before first suggestion (default: 50)
 * - COMPACT_INTERVAL: Reminders after threshold (default: 25)
 *
 * Usage: Add to ~/.claude/settings.json hooks
 */

const fs = require('fs');
const path = require('path');

// Configuration
const THRESHOLD = parseInt(process.env.COMPACT_THRESHOLD || '50', 10);
const INTERVAL = parseInt(process.env.COMPACT_INTERVAL || '25', 10);

// Counter file path
const COUNTER_FILE = path.join(__dirname, '.compact-counter');

// ANSI colors for terminal output
const colors = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

/**
 * Read current counter value
 */
function readCounter() {
  try {
    const data = fs.readFileSync(COUNTER_FILE, 'utf8');
    return parseInt(data, 10) || 0;
  } catch (error) {
    // File doesn't exist yet
    return 0;
  }
}

/**
 * Write counter value
 */
function writeCounter(count) {
  try {
    fs.writeFileSync(COUNTER_FILE, count.toString(), 'utf8');
  } catch (error) {
    // Silently fail if we can't write
  }
}

/**
 * Display suggestion message
 */
function suggestCompact(count) {
  const atThreshold = count >= THRESHOLD && (count - THRESHOLD) % INTERVAL === 0;

  if (atThreshold) {
    const phase = count === THRESHOLD
      ? 'Initial threshold reached'
      : `Every ${INTERVAL} calls after threshold`;

    console.error('');
    console.error(`${colors.bold}${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
    console.error(`${colors.bold}${colors.yellow}⚠️  STRATEGIC COMPACT SUGGESTION${colors.reset}`);
    console.error(`${colors.bold}${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
    console.error('');
    console.error(`${colors.bold}Tool calls:${colors.reset} ${count}`);
    console.error(`${colors.bold}Phase:${colors.reset} ${phase}`);
    console.error('');
    console.error(`${colors.bold}Consider running:${colors.reset} ${colors.cyan}/compact${colors.reset}`);
    console.error('');
    console.error(`${colors.bold}When to compact:${colors.reset}`);
    console.error(`  ✓ After ${colors.cyan}research → planning${colors.reset} phase`);
    console.error(`  ✓ After ${colors.cyan}planning → implementation${colors.reset} phase`);
    console.error(`  ✓ After ${colors.cyan}debugging${colors.reset} before next feature`);
    console.error(`  ✗ ${colors.yellow}NOT mid-implementation${colors.reset} (preserves context)`);
    console.error('');
    console.error(`${colors.bold}What survives:${colors.reset}`);
    console.error(`  • CLAUDE.md instructions`);
    console.error(`  • TodoWrite task list`);
    console.error(`  • Files on disk`);
    console.error(`  • Git state`);
    console.error('');
    console.error(`${colors.bold}What's lost:${colors.reset}`);
    console.error(`  • File contents previously read`);
    console.error(`  • Multi-step conversation context`);
    console.error(`  • Tool call history`);
    console.error('');
    console.error(`${colors.dim}To disable: Set COMPACT_THRESHOLD=0 in environment${colors.reset}`);
    console.error(`${colors.bold}${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
    console.error('');
  }
}

/**
 * Main execution
 */
function main() {
  // Disable if threshold is 0
  if (THRESHOLD === 0) {
    return;
  }

  // Read and increment counter
  const count = readCounter() + 1;
  writeCounter(count);

  // Suggest compaction at threshold and intervals
  if (count >= THRESHOLD && (count - THRESHOLD) % INTERVAL === 0) {
    suggestCompact(count);
  }
}

// Run
main();
