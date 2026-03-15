# Testing Patterns

## E2E Test Structure
```javascript
test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#email', 'test@example.com');
  await page.fill('#password', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

## Assertions
```javascript
await expect(page).toHaveURL('/dashboard');
await expect(page).toHaveTitle('Dashboard');
await expect(page.locator('h1')).toContainText('Welcome');
await expect(page.locator('.alert')).toBeVisible();
await expect(page.locator('button')).toBeEnabled();
await expect(page.locator('input')).toHaveValue('test');
```

## Test Hooks
```javascript
test.describe('User Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('displays homepage', async ({ page }) => {
    await expect(page.locator('h1')).toBeVisible();
  });
});
```

## Visual Testing
```javascript
test('homepage screenshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png');
});
```

## API Mocking
```javascript
test('with mocked API', async ({ page }) => {
  await page.route('**/api/users', route => {
    route.fulfill({
      status: 200,
      body: JSON.stringify([{ id: 1, name: 'Test User' }])
    });
  });
  await page.goto('/users');
});