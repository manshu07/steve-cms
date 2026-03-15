# Puppeteer Patterns

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
await page.waitForNavigation();
await page.waitForNetworkIdle();
await page.waitForTimeout(1000);
await page.waitForFunction(() => document.readyState === 'complete');
```

## Clicking
```javascript
await page.click('button');
await page.click('button[type="submit"]');
await page.tap('.mobile-button');
```

## Form Handling
```javascript
await page.type('#email', 'test@example.com');
await page.type('#search', 'query', { delay: 100 });
await page.select('#country', 'US');
await page.click('#checkbox');
await page.uploadFile('#file', 'path/to/file.pdf');
```

## Extraction
```javascript
const text = await page.$eval('h1', el => el.textContent);
const value = await page.$eval('#email', el => el.value);
const items = await page.$$eval('.item', els => els.map(e => e.textContent));
const html = await page.evaluate(() => document.body.innerHTML);
```

## Screenshots
```javascript
await page.screenshot({ path: 'screenshot.png' });
await page.screenshot({ path: 'full.png', fullPage: true });
await page.screenshot({ path: 'mobile.png', viewport: { width: 375, height: 667 } });