# Style Presets Reference

Curated visual styles for `frontend-slides` presentations.

Use this file for:
- The mandatory viewport-fitting CSS base
- Preset selection and mood mapping
- CSS gotchas and validation rules

**Abstract shapes only.** Avoid illustrations unless user explicitly asks.

---

## Table of Contents

- [Viewport Fit Is Non-Negotiable](#viewport-fit-is-non-negotiable)
- [Mandatory Base CSS](#mandatory-base-css)
- [Preset Catalog](#preset-catalog)
- [Animation Feel Mapping](#animation-feel-mapping)
- [CSS Gotchas](#css-gotchas)
- [Validation Sizes](#validation-sizes)
- [Anti-Patterns](#anti-patterns)

---

## Viewport Fit Is Non-Negotiable

Every slide must fully fit in one viewport.

### Golden Rule

```
Each slide = exactly one viewport height.
Too much content = split into more slides.
Never scroll inside a slide.
```

### Density Limits

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullets or 2 paragraphs |
| Feature grid | 6 cards maximum |
| Code slide | 8-10 lines maximum |
| Quote slide | 1 quote + attribution |
| Image slide | 1 image, ideally under 60vh |

**When content exceeds limits → split into multiple slides**

---

## Mandatory Base CSS

Copy this block into every generated presentation. Then theme on top of it.

```css
/* ===========================================
   VIEWPORT FITTING: MANDATORY BASE STYLES
   =========================================== */

html, body {
    height: 100%;
    overflow-x: hidden;
}

html {
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}

.slide {
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    position: relative;
}

.slide-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-height: 100%;
    overflow: hidden;
    padding: var(--slide-padding);
}

:root {
    /* Typography scales with viewport */
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --h3-size: clamp(1rem, 2.5vw, 1.75rem);
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.65rem, 1vw, 0.875rem);

    /* Spacing scales with viewport */
    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
    --element-gap: clamp(0.25rem, 1vw, 1rem);
}

/* Cards and containers stay within bounds */
.card, .container, .content-box {
    max-width: min(90vw, 1000px);
    max-height: min(80vh, 700px);
}

/* Lists breathe but stay readable */
.feature-list, .bullet-list {
    gap: clamp(0.4rem, 1vh, 1rem);
}

.feature-list li, .bullet-list li {
    font-size: var(--body-size);
    line-height: 1.4;
}

/* Grids adapt to viewport */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: clamp(0.5rem, 1.5vw, 1rem);
}

/* Images fit within viewport */
img, .image-container {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
}

/* ===========================================
   RESPONSIVE BREAKPOINTS
   =========================================== */

/* Short screens (laptops in landscape, tablets) */
@media (max-height: 700px) {
    :root {
        --slide-padding: clamp(0.75rem, 3vw, 2rem);
        --content-gap: clamp(0.4rem, 1.5vw, 1rem);
        --title-size: clamp(1.25rem, 4.5vw, 2.5rem);
        --h2-size: clamp(1rem, 3vw, 1.75rem);
    }
}

/* Very short screens */
@media (max-height: 600px) {
    :root {
        --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem);
        --content-gap: clamp(0.3rem, 1vw, 0.75rem);
        --title-size: clamp(1.1rem, 4vw, 2rem);
        --body-size: clamp(0.7rem, 1.2vw, 0.95rem);
    }

    /* Hide decorative elements */
    .nav-dots, .keyboard-hint, .decorative {
        display: none;
    }
}

/* Ultra-short screens (phones in landscape) */
@media (max-height: 500px) {
    :root {
        --slide-padding: clamp(0.4rem, 2vw, 1rem);
        --title-size: clamp(1rem, 3.5vw, 1.5rem);
        --h2-size: clamp(0.9rem, 2.5vw, 1.25rem);
        --body-size: clamp(0.65rem, 1vw, 0.85rem);
    }
}

/* Narrow screens (phones in portrait) */
@media (max-width: 600px) {
    :root {
        --title-size: clamp(1.25rem, 7vw, 2.5rem);
    }

    .grid {
        grid-template-columns: 1fr;
    }
}

/* ===========================================
   ACCESSIBILITY
   =========================================== */

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }

    html {
        scroll-behavior: auto;
    }
}
```

---

## Viewport Checklist

Every presentation MUST have:

- [ ] Every `.slide` has `height: 100vh`, `height: 100dvh`, `overflow: hidden`
- [ ] All typography uses `clamp()` for scaling
- [ ] All spacing uses `clamp()` or viewport units
- [ ] Images have `max-height` constraints
- [ ] Grids adapt with `auto-fit` + `minmax()`
- [ ] Short-height breakpoints at 700px, 600px, 500px
- [ ] If anything feels cramped, the slide is split

---

## Mood to Preset Mapping

| Mood | Good Presets |
|------|--------------|
| Impressed / Confident | Bold Signal, Electric Studio, Dark Botanical |
| Excited / Energized | Creative Voltage, Neon Cyber, Split Pastel |
| Calm / Focused | Notebook Tabs, Paper & Ink, Swiss Modern |
| Inspired / Moved | Dark Botanical, Vintage Editorial, Pastel Geometry |

---

## Preset Catalog

### 1. Bold Signal

**Vibe:** Confident, high-impact, keynote-ready

**Best for:** Pitch decks, launches, strong statements

**Fonts:**
- Archivo Black (headings)
- Space Grotesk (body)

**Palette:**
- Base: Charcoal #1a1a1a
- Accent: Hot orange #ff4500
- Text: Crisp white #ffffff

**Signature elements:**
- Oversized section numbers (01, 02, 03)
- High-contrast card on dark field
- Strong vertical rhythm

**Preview code snippet:**
```css
:root {
    --bg-color: #1a1a1a;
    --text-color: #ffffff;
    --accent-color: #ff4500;
}

.section-number {
    font-family: 'Archivo Black', sans-serif;
    font-size: clamp(8rem, 20vw, 15rem);
    color: var(--accent-color);
    opacity: 0.2;
    position: absolute;
    top: -2rem;
    right: 2rem;
}
```

---

### 2. Electric Studio

**Vibe:** Clean, bold, agency-polished

**Best for:** Client presentations, strategic reviews

**Fonts:**
- Manrope (all weights)

**Palette:**
- Black: #000000
- White: #ffffff
- Accent: Saturated cobalt #0066ff

**Signature elements:**
- Two-panel split layouts
- Sharp editorial alignment
- Generous whitespace

**Preview code snippet:**
```css
.split-panel {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--content-gap);
}

.panel {
    padding: var(--slide-padding);
}

.panel-left {
    background: #000000;
    color: #ffffff;
}

.panel-right {
    background: #0066ff;
    color: #ffffff;
}
```

---

### 3. Creative Voltage

**Vibe:** Energetic, retro-modern, playful confidence

**Best for:** Creative studios, brand work, product storytelling

**Fonts:**
- Syne (headings)
- Space Mono (body, code)

**Palette:**
- Base: Deep navy #0a0e27
- Accent 1: Electric blue #4361ee
- Accent 2: Neon yellow #f9d71c

**Signature elements:**
- Halftone textures (using radial-gradient)
- Badges and tags
- Punchy contrast

**Preview code snippet:**
```css
.halftone {
    background-image: radial-gradient(
        circle,
        rgba(67, 97, 238, 0.1) 1px,
        transparent 1px
    );
    background-size: 8px 8px;
}

.badge {
    background: var(--accent-2);
    color: var(--base);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-family: 'Space Mono', monospace;
    font-size: var(--small-size);
}
```

---

### 4. Dark Botanical

**Vibe:** Elegant, premium, atmospheric

**Best for:** Luxury brands, thoughtful narratives, premium products

**Fonts:**
- Cormorant (headings - elegant serif)
- IBM Plex Sans (body - clean sans)

**Palette:**
- Base: Near-black #0d0d0d
- Text: Warm ivory #f5f0e6
- Accent 1: Blush #e8b4b8
- Accent 2: Gold #c9a961
- Accent 3: Terracotta #c17f59

**Signature elements:**
- Blurred abstract circles (backdrop-filter)
- Fine horizontal rules
- Restrained, elegant motion

**Preview code snippet:**
```css
.blob {
    position: absolute;
    border-radius: 50%;
    background: var(--accent-2);
    opacity: 0.3;
    filter: blur(60px);
    animation: float 20s ease-in-out infinite;
}

.rule {
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        var(--accent-2),
        transparent
    );
}
```

---

### 5. Notebook Tabs

**Vibe:** Editorial, organized, tactile

**Best for:** Reports, reviews, structured storytelling

**Fonts:**
- Bodoni Moda (headings)
- DM Sans (body)

**Palette:**
- Base: Charcoal #1a1a1a
- Paper: Cream #f5f0e6
- Tabs: Pastel rainbow (blue #a8dadc, pink #f4acb7, mint #b7e4c7)

**Signature elements:**
- Paper sheet effect with shadow
- Colored side tabs
- Binder ring details

**Preview code snippet:**
```css
.paper-sheet {
    background: var(--paper);
    box-shadow:
        0 4px 6px -1px rgba(0, 0, 0, 0.1),
        0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.tab {
    position: absolute;
    left: -12px;
    width: 24px;
    height: clamp(2rem, 5vh, 3rem);
    border-radius: 4px 0 0 4px;
}

.tab-blue { background: #a8dadc; }
.tab-pink { background: #f4acb7; }
.tab-mint { background: #b7e4c7; }

.binder-ring {
    position: absolute;
    top: 1rem;
    left: 50%;
    transform: translateX(-50%);
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    border: 3px solid rgba(255,255,255,0.2);
}
```

---

### 6. Pastel Geometry

**Vibe:** Approachable, modern, friendly

**Best for:** Product overviews, onboarding, lighter brand decks

**Fonts:**
- Plus Jakarta Sans (all)

**Palette:**
- Field: Pale blue #e0f2f1
- Card: Cream #fef9f3
- Accents: Soft pink #f8c8dc, mint #c7f9cc, lavender #d7b8f8

**Signature elements:**
- Vertical pills
- Rounded cards
- Soft shadows
- Clean geometry

**Preview code snippet:**
```css
.pill {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: var(--accent-pink);
    border-radius: 9999px;
    font-size: var(--small-size);
    font-weight: 600;
}

.card {
    background: var(--card-bg);
    border-radius: 1rem;
    padding: var(--content-gap);
    box-shadow:
        0 1px 3px rgba(0,0,0,0.1),
        0 1px 2px rgba(0,0,0,0.06);
}
```

---

### 7. Split Pastel

**Vibe:** Playful, modern, creative

**Best for:** Agency intros, workshops, portfolios

**Fonts:**
- Outfit (all)

**Palette:**
- Field 1: Peach #ffd6a5
- Field 2: Lavender #d8b4e2
- Accent: Mint #a8dadc

**Signature elements:**
- Split backdrop (diagonal or vertical)
- Rounded tags
- Light grid overlays

**Preview code snippet:**
```css
.split-backdrop {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        135deg,
        var(--field-1) 0%,
        var(--field-1) 50%,
        var(--field-2) 50%,
        var(--field-2) 100%
    );
}

.grid-overlay {
    background-image:
        linear-gradient(rgba(0,0,0,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,0,0,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}

.tag {
    background: var(--accent);
    border-radius: 9999px;
    padding: 0.25rem 0.75rem;
    font-size: var(--small-size);
}
```

---

### 8. Vintage Editorial

**Vibe:** Witty, personality-driven, magazine-inspired

**Best for:** Personal brands, opinionated talks, storytelling

**Fonts:**
- Fraunces (headings - strong serif)
- Work Sans (body)

**Palette:**
- Base: Cream #faf7f2
- Text: Charcoal #1a1a1a
- Accents: Dusty warm (terracotta #c17f59, ochre #d4a373)

**Signature elements:**
- Geometric accents (circles, lines)
- Bordered callouts
- Punchy serif headlines

**Preview code snippet:**
```css
blockquote {
    font-family: 'Fraunces', serif;
    font-size: var(--h2-size);
    font-style: italic;
    color: var(--accent-ochre);
    position: relative;
    padding-left: var(--content-gap);
}

blockquote::before {
    content: '"';
    position: absolute;
    left: 0;
    font-size: 4rem;
    line-height: 1;
    color: var(--accent-terracotta);
}

.geometric-accent {
    width: clamp(40px, 8vw, 80px);
    height: clamp(40px, 8vw, 80px);
    border: 3px solid var(--accent-terracotta);
    border-radius: 50%;
}
```

---

### 9. Neon Cyber

**Vibe:** Futuristic, techy, kinetic

**Best for:** AI, infra, dev tools, future-of-X talks

**Fonts:**
- Clash Display (headings)
- Satoshi (body)

**Palette:**
- Base: Midnight navy #0a0e27
- Accent 1: Cyan #00f0ff
- Accent 2: Magenta #ff00ff

**Signature elements:**
- Glow effects (box-shadow)
- Particle backgrounds
- Grid motion
- Data-radar energy

**Preview code snippet:**
```css
.glow {
    box-shadow:
        0 0 20px var(--accent-cyan),
        0 0 40px var(--accent-cyan),
        0 0 60px var(--accent-cyan);
}

.particles {
    background-image: radial-gradient(
        circle,
        var(--accent-cyan) 1px,
        transparent 1px
    );
    background-size: 30px 30px;
    animation: pulse 4s ease-in-out infinite;
}

.grid-scan {
    background-image:
        linear-gradient(transparent 95%, var(--accent-magenta) 95%),
        linear-gradient(90deg, transparent 95%, var(--accent-magenta) 95%);
    background-size: 8px 8px;
}
```

---

### 10. Terminal Green

**Vibe:** Developer-focused, hacker-clean

**Best for:** APIs, CLI tools, engineering demos

**Fonts:**
- JetBrains Mono (all)

**Palette:**
- Base: GitHub dark #0d1117
- Accent: Terminal green #00ff41
- Text: Off-white #c9d1d9

**Signature elements:**
- Scan lines
- Command-line framing
- Precise monospace rhythm

**Preview code snippet:**
```css
.scanlines {
    background: repeating-linear-gradient(
        0deg,
        rgba(0, 255, 65, 0.03),
        rgba(0, 255, 65, 0.03) 1px,
        transparent 1px,
        transparent 2px
    );
    pointer-events: none;
}

.terminal-frame {
    border: 1px solid #30363d;
    background: #161b22;
    padding: var(--content-gap);
}

.prompt::before {
    content: '$';
    color: var(--accent);
    margin-right: 0.5rem;
}
```

---

### 11. Swiss Modern

**Vibe:** Minimal, precise, data-forward

**Best for:** Corporate, product strategy, analytics

**Fonts:**
- Archivo (headings)
- Nunito (body)

**Palette:**
- Base: White #ffffff
- Text: Black #000000
- Accent: Signal red #ff3b30

**Signature elements:**
- Visible grids
- Asymmetry
- Geometric discipline

**Preview code snippet:**
```css
.visible-grid {
    background-image:
        linear-gradient(#e5e5e5 1px, transparent 1px),
        linear-gradient(90deg, #e5e5e5 1px, transparent 1px);
    background-size: 40px 40px;
}

.asymmetric {
    margin-left: clamp(2rem, 10vw, 8rem);
}

.geometric-rule {
    width: 100px;
    height: 4px;
    background: var(--accent);
}
```

---

### 12. Paper & Ink

**Vibe:** Literary, thoughtful, story-driven

**Best for:** Essays, keynote narratives, manifesto decks

**Fonts:**
- Cormorant Garamond (headings)
- Source Serif 4 (body)

**Palette:**
- Base: Warm cream #faf6f0
- Text: Charcoal #2c2c2c
- Accent: Crimson #a93226

**Signature elements:**
- Pull quotes
- Drop caps
- Elegant rules

**Preview code snippet:**
```css
.pull-quote {
    font-family: 'Cormorant Garamond', serif;
    font-size: var(--title-size);
    color: var(--accent);
    border-left: 4px solid var(--accent);
    padding-left: var(--content-gap);
    font-style: italic;
}

.drop-cap::first-letter {
    font-size: 3.5em;
    float: left;
    margin-right: 0.1em;
    line-height: 0.8;
}

.elegant-rule {
    height: 2px;
    background: linear-gradient(
        90deg,
        transparent,
        var(--accent),
        transparent
    );
}
```

---

## Direct Selection Prompts

If user already knows the style they want, let them pick directly:

"Which preset would you like?
- Bold Signal
- Electric Studio
- Creative Voltage
- Dark Botanical
- Notebook Tabs
- Pastel Geometry
- Split Pastel
- Vintage Editorial
- Neon Cyber
- Terminal Green
- Swiss Modern
- Paper & Ink"

Skip preview generation unless they want to see options first.

---

## Animation Feel Mapping

| Feeling | Motion Direction |
|---------|------------------|
| **Dramatic / Cinematic** | Slow fades, parallax, large scale-ins |
| **Techy / Futuristic** | Glow, particles, grid motion, scramble text |
| **Playful / Friendly** | Springy easing, rounded shapes, floating motion |
| **Professional / Corporate** | Subtle 200-300ms transitions, clean slides |
| **Calm / Minimal** | Very restrained movement, whitespace-first |
| **Editorial / Magazine** | Strong hierarchy, staggered text/image interplay |

**Implementation tips:**

```css
/* Dramatic fade */
.reveal {
    opacity: 0;
    transform: translateY(2rem);
    transition: opacity 1.2s ease, transform 1.2s ease;
}
.reveal.active {
    opacity: 1;
    transform: translateY(0);
}

/* Techy scramble */
@keyframes scramble {
    0% { clip-path: inset(50% 50% 50% 50%); }
    100% { clip-path: inset(0 0 0 0); }
}

/* Playful float */
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* Professional slide */
.reveal {
    opacity: 0;
    transition: opacity 0.3s ease;
}
.reveal.active {
    opacity: 1;
}
```

---

## CSS Gotchas

### Negating Functions

**❌ WRONG - Browsers ignore silently:**
```css
right: -clamp(28px, 3.5vw, 44px);
margin-left: -min(10vw, 100px);
```

**✅ CORRECT:**
```css
right: calc(-1 * clamp(28px, 3.5vw, 44px));
margin-left: calc(-1 * min(10vw, 100px));
```

**Why:** Browsers don't support negating math functions directly. Use `calc(-1 * ...)` instead.

---

## Validation Sizes

Test presentations at minimum:

### Desktop
- 1920x1080 (Full HD)
- 1440x900 (Laptop)
- 1280x720 (HD)

### Tablet
- 1024x768 (iPad portrait)
- 768x1024 (iPad landscape)

### Mobile
- 375x667 (iPhone SE portrait)
- 414x896 (iPhone 11 portrait)
- 667x375 (iPhone SE landscape)
- 896x414 (iPhone 11 landscape)

---

## Anti-Patterns

### ❌ Don't Use These

**1. Generic startup gradients**
```css
/* Don't do this */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**2. Inter/Roboto as default voice**
```css
/* Unless user wants utilitarian neutrality */
font-family: 'Inter', sans-serif;
```

**3. Bullet walls**
```html
<!-- Don't cram 10+ bullets into one slide -->
<ul>
    <li>Point 1</li>
    <li>Point 2</li>
    ...
    <li>Point 12</li>
</ul>
```

**4. Scrolling code blocks**
```css
/* More than 10 lines = split into multiple slides */
.code-block {
    max-height: 50vh;
    overflow-y: auto; /* Never do this in slides */
}
```

**5. Fixed-height content boxes**
```css
/* Breaks on short screens */
.box {
    height: 400px; /* Use max-height instead */
}
```

---

## Quick Reference

### Font Sources

**Google Fonts:**
- Archivo, Archivo Black
- Space Grotesk, Space Mono
- Manrope
- Syne
- Cormorant, Cormorant Garamond
- Bodoni Moda
- Plus Jakarta Sans, Outfit
- Fraunces
- JetBrains Mono
- Clash Display, Satoshi
- Nunito
- Source Serif 4
- DM Sans

**Fontshare:**
- All fonts are free and no tracking required

### Color Tools

- **Contrast:** https://contrast-ratio.com/
- **Palettes:** https://coolors.co/
- **Gradients:** https://cssgradient.io/

### Inspiration

- [zarazhangrui](https://github.com/zarazhangrui) - Original inspiration
- [Awwwards](https://www.awwwards.com/) - Design trends
- [Brutal Websites](https://brutalwebsites.com/) - Bold typography
- [SiteInspire](https://www.siteinspire.net/) - Web design patterns
