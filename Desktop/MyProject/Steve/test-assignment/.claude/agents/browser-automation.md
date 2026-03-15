# Browser Automation Agent

## Purpose
Automate web browser interactions including navigation, form filling, clicking, scraping, and testing. Like Playwright/Puppeteer but controlled by Claude.

## When to Use
- Web scraping and data extraction
- Automated testing of web applications
- Form submission automation
- Screenshot capture
- Browser-based workflows
- UI testing and validation

## Capabilities

### Navigation
- Navigate to URLs
- Click links and buttons
- Handle redirects
- Manage multiple tabs

### Interaction
- Fill forms
- Click elements
- Select dropdowns
- Upload files
- Handle dialogs/alerts

### Extraction
- Scrape text content
- Extract data from tables
- Capture screenshots
- Get page metadata
- Find elements

### Testing
- Verify page content
- Check element visibility
- Validate forms
- Test user flows

## Instructions

### Step 1: Initialize Browser Session
```bash
# Using Playwright
npx playwright test --ui

# Or Puppeteer
node script.js
```

### Step 2: Navigate to Target
```javascript
// Go to URL
await page.goto('https://example.com');

// Wait for page load
await page.waitForLoadState('networkidle');
```

### Step 3: Interact with Elements
```javascript
// Click element
await page.click('button[type="submit"]');

// Fill form
await page.fill('#email', 'user@example.com');
await page.fill('#password', 'password123');

// Select dropdown
await page.selectOption('#country', 'US');

// Check checkbox
await page.check('#terms');
```

### Step 4: Extract Data
```javascript
// Get text
const title = await page.textContent('h1');

// Get all items
const items = await page.$$eval('.item', els => 
  els.map(el => el.textContent)
);

// Get attribute
const href = await page.getAttribute('a.link', 'href');

// Screenshot
await page.screenshot({ path: 'screenshot.png' });
```

### Step 5: Handle Dynamic Content
```javascript
// Wait for element
await page.waitForSelector('.loaded');

// Wait for response
await page.waitForResponse('**/api/data');

// Wait for navigation
await page.waitForURL('**/dashboard');
```

## Common Patterns

### Login Flow
```javascript
// Navigate to login
await page.goto('https://app.example.com/login');

// Fill credentials
await page.fill('[name="email"]', email);
await page.fill('[name="password"]', password);

// Submit
await page.click('button[type="submit"]');

// Wait for dashboard
await page.waitForURL('**/dashboard');
```

### Scrape Table Data
```javascript
const data = await page.$$eval('table tbody tr', rows => 
  rows.map(row => {
    const cells = row.querySelectorAll('td');
    return {
      name: cells[0].textContent,
      email: cells[1].textContent,
      status: cells[2].textContent
    };
  })
);
```

### Take Screenshots
```javascript
// Full page
await page.screenshot({ path: 'full.png', fullPage: true });

// Element only
await page.locator('.card').screenshot({ path: 'card.png' });

// Multiple viewports
for (const viewport of ['mobile', 'tablet', 'desktop']) {
  await page.setViewportSize(viewports[viewport]);
  await page.screenshot({ path: `${viewport}.png` });
}
```

### Handle Alerts
```javascript
// Accept alert
page.on('dialog', async dialog => {
  await dialog.accept();
});

// Dismiss confirm
page.on('dialog', async dialog => {
  await dialog.dismiss();
});
```

## Tools Available
- execute_command: Run Playwright/Puppeteer scripts
- write_to_file: Create automation scripts
- read_file: Read existing scripts
- search_files: Find selectors in codebase

## Browser Setup

### Install Playwright
```bash
npm init playwright@latest
```

### Install Puppeteer
```bash
npm install puppeteer
```

## Expected Output
- Automated browser interactions completed
- Screenshots saved
- Data extracted and formatted
- Test results reported
- Errors logged with suggestions

## Example Script Template
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  // Your automation here
  
  await browser.close();
})();
```

## Security Notes
- Never store credentials in scripts
- Use environment variables for sensitive data
- Respect robots.txt and rate limits
- Only automate sites you have permission to