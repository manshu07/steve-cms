---
name: browser-automation
description: Browser automation with Playwright/Puppeteer for web scraping, testing, and automated workflows. Use when automating browser interactions, taking screenshots, testing UI, or extracting web data.
---

# Browser Automation Skill

## Purpose
Comprehensive browser automation using Playwright or Puppeteer for testing, scraping, and automation workflows.

## When to Use This Skill
- Web scraping and data extraction
- E2E testing with Playwright/Puppeteer
- Automated screenshots
- Form automation
- Browser-based workflows
- UI validation

## Resources

- [Setup Guide](resources/setup-guide.md)
- [Playwright Patterns](resources/playwright-patterns.md)
- [Puppeteer Patterns](resources/puppeteer-patterns.md)
- [Scraping Guide](resources/scraping-guide.md)
- [Testing Patterns](resources/testing-patterns.md)
- [Common Recipes](resources/common-recipes.md)

## Quick Start

### Install Playwright
```bash
npm init playwright@latest
```

### Basic Script
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com');
  
  // Interact with page
  const title = await page.title();
  console.log(title);
  
  await browser.close();
})();
```

### Common Actions
```javascript
// Navigate
await page.goto('https://example.com');

// Click
await page.click('button');

// Fill form
await page.fill('#email', 'test@example.com');

// Screenshot
await page.screenshot({ path: 'screenshot.png' });

// Extract text
const text = await page.textContent('h1');
```

## Core Principles

1. **Wait for elements** - Always wait before interacting
2. **Handle async properly** - Use async/await
3. **Secure credentials** - Use environment variables
4. **Respect rate limits** - Don't overwhelm servers
5. **Clean up resources** - Close browser when done
6. **Use selectors wisely** - Prefer data-testid attributes

## Selectors Best Practice

```javascript
// ✅ Good - data-testid
await page.click('[data-testid="submit-button"]');

// ✅ Good - role-based
await page.click('button[type="submit"]');

// ⚠️ Avoid - fragile
await page.click('#root > div > div:nth-child(3) > button');
```

## Related Skills
- frontend-dev-guidelines: For testing React components
- error-tracking: For monitoring test failures