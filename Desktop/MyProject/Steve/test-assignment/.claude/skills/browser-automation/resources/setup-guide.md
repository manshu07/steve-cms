# Browser Automation Setup Guide

## Playwright Setup

### Installation
```bash
npm init playwright@latest
```

### Configuration
```javascript
// playwright.config.js
module.exports = {
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
  ],
};
```

## Puppeteer Setup

### Installation
```bash
npm install puppeteer
```

### Basic Setup
```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox']
  });
  const page = await browser.newPage();
  // ... automation
  await browser.close();
})();
```

## Environment Variables
```bash
# .env
BROWSER_HEADLESS=true
BROWSER_TIMEOUT=30000
BASE_URL=http://localhost:3000