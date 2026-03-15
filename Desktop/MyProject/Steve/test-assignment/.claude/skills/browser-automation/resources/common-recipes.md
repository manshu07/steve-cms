# Common Recipes

## Login Flow
```javascript
async function login(page, email, password) {
  await page.goto('/login');
  await page.fill('#email', email);
  await page.fill('#password', password);
  await page.click('button[type="submit"]');
  await page.waitForURL('/dashboard');
}
```

## Form Submission
```javascript
async function submitForm(page, data) {
  await page.fill('#name', data.name);
  await page.fill('#email', data.email);
  await page.selectOption('#country', data.country);
  await page.check('#terms');
  await page.click('button[type="submit"]');
  await page.waitForSelector('.success-message');
}
```

## Handle File Upload
```javascript
await page.setInputFiles('#file', 'path/to/file.pdf');
// Or with buffer
await page.setInputFiles('#file', {
  name: 'test.pdf',
  mimeType: 'application/pdf',
  buffer: Buffer.from('file content')
});
```

## Handle Multiple Tabs
```javascript
const [newPage] = await Promise.all([
  page.context().waitForEvent('page'),
  page.click('a[target="_blank"]')
]);
await newPage.waitForLoadState();
```

## Handle Iframes
```javascript
const frame = page.frameLocator('iframe');
await frame.fill('#input', 'test');
```

## Take Element Screenshot
```javascript
const element = await page.locator('.card');
await element.screenshot({ path: 'card.png' });
```

## Scroll to Element
```javascript
await page.locator('.footer').scrollIntoViewIfNeeded();
```

## Handle Infinite Scroll
```javascript
let previousHeight = 0;
while (true) {
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(1000);
  const currentHeight = await page.evaluate(() => document.body.scrollHeight);
  if (currentHeight === previousHeight) break;
  previousHeight = currentHeight;
}