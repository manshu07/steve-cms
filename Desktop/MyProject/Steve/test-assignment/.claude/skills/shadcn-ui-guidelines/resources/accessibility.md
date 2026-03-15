# Accessibility Guidelines

## Core Principles

1. **Perceivable** - Information must be presentable
2. **Operable** - Interface must be navigable
3. **Understandable** - Content must be clear
4. **Robust** - Content must work with assistive tech

## Semantic HTML

```tsx
// ✅ Good - Semantic elements
<header>
  <nav>
    <main>
      <article>
        <section>
          <aside>
            <footer>

// ❌ Bad - Div soup
<div className="header">
  <div className="nav">
    <div className="main">
```

## ARIA Labels

```tsx
// Interactive elements need labels
<Button aria-label="Close dialog">
  <X className="h-4 w-4" />
</Button>

// Icon-only buttons
<IconButton aria-label="Add item">
  <Plus />
</IconButton>

// Form inputs
<Input
  aria-label="Search"
  placeholder="Search..."
/>

// Groups
<div role="group" aria-label="Filter options">
  {/* Checkboxes */}
</div>
```

## Focus Management

```tsx
// Focus visible styles
<Button className="focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
  Click me
</Button>

// Skip links
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>

// Focus trap in modals
<DialogContent onOpenAutoFocus={(e) => e.preventDefault()}>
  {/* Dialog content */}
</DialogContent>
```

## Keyboard Navigation

```tsx
// Ensure all interactive elements are focusable
<Button>Clickable</Button>  // ✅ Focusable
<div onClick={handleClick}>Clickable</div>  // ❌ Not focusable

// Use proper elements
<button onClick={handleClick}>Click me</button>  // ✅
<span onClick={handleClick}>Click me</span>  // ❌

// Handle keyboard events
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>
  Clickable
</div>
```

## Screen Reader Only

```tsx
// Hide visually but show to screen readers
<span className="sr-only">Loading</span>

// Show visually but hide from screen readers
<span aria-hidden="true"> decorative icon</span>
```

## Color Contrast

```tsx
// Use theme colors for proper contrast
<p className="text-foreground">Primary text</p>
<p className="text-muted-foreground">Secondary text</p>

// Never hardcode colors without checking contrast
<p className="text-gray-400">May not pass contrast</p>
```

## Form Accessibility

```tsx
// Always associate labels with inputs
<FormItem>
  <FormLabel htmlFor="email">Email</FormLabel>
  <FormControl>
    <Input id="email" type="email" />
  </FormControl>
  <FormDescription>We'll never share your email</FormDescription>
  <FormMessage />
</FormItem>

// Required fields
<FormLabel>
  Email <span className="text-destructive">*</span>
</FormLabel>

// Error announcements
<FormMessage role="alert" />
```

## Images

```tsx
// Decorative images
<Icon className="h-4 w-4" aria-hidden="true" />

// Informative images
<img src="/chart.png" alt="Sales increased 20% in Q4" />

// Complex images
<figure>
  <img src="/diagram.png" alt="Architecture diagram" aria-describedby="diagram-desc" />
  <figcaption id="diagram-desc">Detailed description...</figcaption>
</figure>
```

## Tables

```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead scope="col">Name</TableHead>
      <TableHead scope="col">Email</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {users.map(user => (
      <TableRow key={user.id}>
        <TableCell>{user.name}</TableCell>
        <TableCell>{user.email}</TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>