# Playwright Patterns

## Navigation
```javascript
await page.goto('https://example.com');
await page.goBack();
await page.goForward();
await page.reload();
```

## Waiting
```javascript
await page.waitForSelector('.loaded');
await page.waitForLoadState('networkidle');
await page.waitForURL('**/dashboard');
await page.waitForResponse('**/api/data');
await page.waitForTimeout(1000);
```

## Clicking
```javascript
await page.click('button');
await page.click('text=Submit');
await page.click('[data-testid="submit"]');
await page.dblclick('.item');
await page.click('button', { force: true });
```

## Form Handling
```javascript
await page.fill('#email', 'test@example.com');
await page.type('#search', 'query', { delay: 100 });
await page.selectOption('#country', 'US');
await page.check('#terms');
await page.uncheck('#newsletter');
await page.setInputFiles('#file', 'path/to/file.pdf');
```

## Extraction
```javascript
const text = await page.textContent('h1');
const value = await page.inputValue('#email');
const attr = await page.getAttribute('a', 'href');
const html = await page.innerHTML('.container');
const items = await page.$$eval('.item', els => els.map(e => e.textContent));
```

## Screenshots
```javascript
await page.screenshot({ path: 'screenshot.png' });
await page.screenshot({ path: 'full.png', fullPage: true });
await page.locator('.card').screenshot({ path: 'card.png' });