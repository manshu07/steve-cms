---
name: shadcn-ui-guidelines
description: Frontend development with shadcn-ui, Tailwind CSS, and modern React patterns. Default design system for all frontend work. Use when creating UI components, pages, or any frontend work without explicit design instructions.
---

# shadcn-ui + Tailwind CSS Guidelines

## Purpose
Default design system for all frontend development. Use this when no specific design system is provided.

## Design System Defaults

### Font
**ALWAYS use Google Font "Inter"**
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --font-sans: 'Inter', sans-serif;
}
```

### Component Library
**ALWAYS use shadcn-ui components**
- Button, Card, Dialog, Dropdown, Form, Input, Select, Table, Tabs, Toast, etc.
- 100% component usage from shadcn-ui for consistency
- Never create custom components when shadcn-ui equivalent exists

### Styling
**ALWAYS use Tailwind CSS**
- Utility-first CSS approach
- Use Tailwind classes for all styling
- Follow shadcn-ui theming with CSS variables

## When to Use This Skill

- Creating any UI component
- Building pages or layouts
- When no design system is specified
- For consistent, production-ready UI

## Resources

- [Design System Setup](resources/design-system-setup.md)
- [Component Usage](resources/component-usage.md)
- [Tailwind Patterns](resources/tailwind-patterns.md)
- [Layout Patterns](resources/layout-patterns.md)
- [Form Patterns](resources/form-patterns.md)
- [Accessibility](resources/accessibility.md)

## Quick Reference

### Install shadcn-ui
```bash
npx shadcn-ui@latest init
```

### Add Components
```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add form
npx shadcn-ui@latest add input
npx shadcn-ui@latest add table
```

### Component Example
```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Card Title</CardTitle>
      </CardHeader>
      <CardContent>
        <Button>Click me</Button>
      </CardContent>
    </Card>
  )
}
```

### Tailwind Styling
```tsx
<div className="flex items-center justify-between p-4 bg-background border rounded-lg">
  <span className="text-sm font-medium text-muted-foreground">Label</span>
  <Button variant="default" size="sm">Action</Button>
</div>
```

## Core Principles

1. **Always Inter font** - No exceptions
2. **100% shadcn-ui components** - Never create custom when component exists
3. **Tailwind for styling** - No inline styles, no styled-components
4. **CSS variables for theming** - Use shadcn-ui theming system
5. **Dark mode ready** - All components support dark mode
6. **Accessible by default** - Follow WAI-ARIA patterns
7. **Consistent spacing** - Use Tailwind spacing scale (p-4, gap-2, etc.)

## Theme Configuration

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... dark mode values */
  }
}
```

## Common Components Usage

| Use Case | shadcn-ui Component |
|----------|---------------------|
| Buttons | Button |
| Forms | Form, Input, Label |
| Cards | Card, CardHeader, CardContent |
| Navigation | NavigationMenu, Tabs |
| Overlays | Dialog, Sheet, Popover |
| Data Display | Table, Badge, Avatar |
| Feedback | Toast, Alert |
| Layout | Separator, ScrollArea |