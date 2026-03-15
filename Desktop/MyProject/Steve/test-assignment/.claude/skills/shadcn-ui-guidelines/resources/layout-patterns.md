# Layout Patterns

## Page Layouts

### Dashboard Layout
```tsx
<div className="min-h-screen bg-background">
  <header className="border-b bg-card">
    <div className="container mx-auto px-4 h-16 flex items-center justify-between">
      <h1 className="text-xl font-semibold">Dashboard</h1>
      <nav className="flex gap-4">
        <Button variant="ghost">Home</Button>
        <Button variant="ghost">Settings</Button>
      </nav>
    </div>
  </header>
  <main className="container mx-auto px-4 py-8">
    {/* Content */}
  </main>
</div>
```

### Sidebar Layout
```tsx
<div className="flex min-h-screen">
  <aside className="w-64 border-r bg-card">
    <nav className="p-4 space-y-2">
      <Button variant="ghost" className="w-full justify-start">Home</Button>
      <Button variant="ghost" className="w-full justify-start">Projects</Button>
    </nav>
  </aside>
  <main className="flex-1 p-8">
    {/* Content */}
  </main>
</div>
```

## Section Patterns

### Hero Section
```tsx
<section className="py-12 md:py-24">
  <div className="container mx-auto px-4 text-center">
    <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">
      Welcome
    </h1>
    <p className="text-muted-foreground text-lg max-w-2xl mx-auto mb-8">
      Description goes here
    </p>
    <div className="flex justify-center gap-4">
      <Button size="lg">Get Started</Button>
      <Button size="lg" variant="outline">Learn More</Button>
    </div>
  </div>
</section>
```

### Feature Grid
```tsx
<section className="py-12">
  <div className="container mx-auto px-4">
    <h2 className="text-3xl font-bold text-center mb-8">Features</h2>
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      {features.map(feature => (
        <Card key={feature.id}>
          <CardHeader>
            <CardTitle>{feature.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{feature.description}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  </div>
</section>