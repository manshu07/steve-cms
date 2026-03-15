# Tailwind CSS Patterns

## Layout Patterns

### Container
```tsx
<div className="container mx-auto px-4">
  {/* Content */}
</div>
```

### Flexbox
```tsx
<div className="flex items-center justify-between">
  <span>Left</span>
  <span>Right</span>
</div>

<div className="flex flex-col gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <Card>1</Card>
  <Card>2</Card>
  <Card>3</Card>
</div>
```

## Spacing Scale

| Class | Pixels |
|-------|--------|
| p-1 | 4px |
| p-2 | 8px |
| p-3 | 12px |
| p-4 | 16px |
| p-6 | 24px |
| p-8 | 32px |

## Typography

```tsx
<h1 className="text-4xl font-bold tracking-tight">Heading</h1>
<h2 className="text-2xl font-semibold">Subheading</h2>
<p className="text-muted-foreground">Description text</p>
<span className="text-sm text-muted-foreground">Small text</span>
```

## Colors (Theme Variables)

```tsx
<div className="bg-background text-foreground">
  <div className="bg-card text-card-foreground">Card</div>
  <div className="bg-primary text-primary-foreground">Primary</div>
  <div className="bg-secondary text-secondary-foreground">Secondary</div>
  <div className="bg-muted text-muted-foreground">Muted</div>
  <div className="bg-destructive text-destructive-foreground">Destructive</div>
</div>
```

## Borders

```tsx
<div className="border rounded-lg">Rounded border</div>
<div className="border-2 border-primary">Primary border</div>
<div className="border-b pb-4">Bottom border</div>
```

## Responsive Design

```tsx
<div className="flex flex-col md:flex-row">
  <div className="w-full md:w-1/2">Left</div>
  <div className="w-full md:w-1/2">Right</div>
</div>

<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {/* Responsive grid */}
</div>
```

## States

```tsx
<Button className="hover:bg-primary/90 active:bg-primary/80">
  Hover States
</Button>

<div className="focus:ring-2 focus:ring-ring focus:ring-offset-2">
  Focus Ring
</div>

<div className="disabled:opacity-50 disabled:pointer-events-none">
  Disabled State
</div>
```

## Common Patterns

### Page Layout
```tsx
<div className="min-h-screen bg-background">
  <header className="border-b">
    <div className="container mx-auto px-4 py-4">
      {/* Header content */}
    </div>
  </header>
  <main className="container mx-auto px-4 py-8">
    {/* Main content */}
  </main>
</div>
```

### Card Grid
```tsx
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
  {items.map(item => (
    <Card key={item.id}>
      <CardContent className="p-4">
        {/* Content */}
      </CardContent>
    </Card>
  ))}
</div>
```

### Form Layout
```tsx
<form className="space-y-6">
  <div className="grid gap-4 md:grid-cols-2">
    <FormField name="firstName" />
    <FormField name="lastName" />
  </div>
  <FormField name="email" />
  <div className="flex justify-end gap-4">
    <Button variant="outline">Cancel</Button>
    <Button type="submit">Save</Button>
  </div>
</form>