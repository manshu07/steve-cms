---
description: Run browser automation tests with Playwright
---

# Browser Test Command

Run browser automation and E2E tests using Playwright.

## Usage

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/login.spec.ts

# Run with UI mode
npx playwright test --ui

# Run in headed mode
npx playwright test --headed

# Run specific browser
npx playwright test --project=chromium
```

## Common Options

| Option | Description |
|--------|-------------|
| `--ui` | Open UI mode |
| `--headed` | Show browser |
| `--debug` | Debug mode |
| `--project=chromium` | Run in Chromium |
| `--project=firefox` | Run in Firefox |
| `--project=webkit` | Run in WebKit |

## Generate Tests

```bash
# Codegen tool
npx playwright codegen https://example.com
```

## View Reports

```bash
npx playwright show-report