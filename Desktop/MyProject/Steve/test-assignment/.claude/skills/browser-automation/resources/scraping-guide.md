# Web Scraping Guide

## Best Practices

1. **Respect robots.txt** - Check before scraping
2. **Rate limiting** - Add delays between requests
3. **User-Agent** - Set appropriate headers
4. **Handle errors** - Retry with exponential backoff
5. **Cache results** - Avoid redundant requests

## Scrape Text
```javascript
const title = await page.textContent('h1');
const paragraphs = await page.$$eval('p', els => els.map(e => e.textContent));
```

## Scrape Links
```javascript
const links = await page.$$eval('a', links => 
  links.map(a => ({
    text: a.textContent,
    href: a.href
  }))
);
```

## Scrape Tables
```javascript
const data = await page.$$eval('table tbody tr', rows => 
  rows.map(row => {
    const cells = row.querySelectorAll('td');
    return {
      name: cells[0]?.textContent,
      email: cells[1]?.textContent,
      status: cells[2]?.textContent
    };
  })
);
```

## Scrape with Pagination
```javascript
const allItems = [];
let hasNext = true;

while (hasNext) {
  const items = await page.$$eval('.item', els => els.map(e => e.textContent));
  allItems.push(...items);
  
  const nextButton = await page.$('.next:not(.disabled)');
  if (nextButton) {
    await nextButton.click();
    await page.waitForLoadState('networkidle');
  } else {
    hasNext = false;
  }
}
```

## Handle Dynamic Content
```javascript
await page.waitForSelector('.loaded');
await page.waitForFunction(() => {
  const items = document.querySelectorAll('.item');
  return items.length > 0;
});