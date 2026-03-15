---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
origin: ECC
---

# Frontend Slides Skill

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser.

Inspired by the visual exploration approach showcased in work by [zarazhangrui](https://github.com/zarazhangrui).

## Purpose
Transform topics, notes, or PowerPoint files into stunning HTML presentations that are viewport-optimized, accessible, and production-ready.

## When to Use This Skill

**Auto-activates when:**
- Creating a talk deck, pitch deck, workshop deck, or internal presentation
- Converting `.ppt` or `.pptx` slides into an HTML presentation
- Improving an existing HTML presentation's layout, motion, or typography
- Exploring presentation styles with a user who doesn't know their design preference

**Keywords that trigger:**
- presentation, slides, deck, talk, pitch
- PowerPoint, PPT, PPTX, convert
- HTML presentation, web slides
- keynote, workshop, conference

---

## Non-Negotiables

### 1. Zero Dependencies
- Default to one self-contained HTML file
- Inline CSS and JS
- No external frameworks unless user explicitly requests

### 2. Viewport Fit is Mandatory
- Every slide must fit inside one viewport
- No internal scrolling within slides
- Content overflow = split into more slides

### 3. Show, Don't Tell
- Use visual previews instead of abstract style questionnaires
- Generate 3 single-slide previews for style selection
- Let users see and choose rather than describe

### 4. Distinctive Design
- Avoid generic purple-gradient decks
- Avoid Inter-on-white template-looking slides
- Each deck should have visual personality

### 5. Production Quality
- Code is commented and organized
- Accessible (semantic HTML, keyboard nav, ARIA)
- Responsive (mobile, tablet, desktop, landscape)
- Performant (smooth animations, respects reduced motion)

---

## Workflow

### Step 1: Detect Mode

Choose one path:

**New Presentation**
- User has a topic, notes, or full draft
- Build from scratch

**PPT/PPTX Conversion**
- User has PowerPoint slides
- Extract content, rebuild in HTML

**Enhancement**
- User already has HTML slides
- Improve layout, motion, typography

---

### Step 2: Discover Content

Ask only the minimum:

**Purpose:**
- Pitch deck (investors, sales)
- Teaching (workshop, tutorial)
- Conference talk (keynote, breakout)
- Internal update (team, company)

**Length:**
- Short: 5-10 slides
- Medium: 10-20 slides
- Long: 20+ slides

**Content State:**
- Finished copy (ready to design)
- Rough notes (need structure)
- Topic only (need both)

**If user has content, ask them to paste it before styling.**

---

### Step 3: Discover Style

**Default to visual exploration.**

If user already knows desired preset, skip previews and use it directly.

**Otherwise:**

1. **Ask: What feeling should the deck create?**
   - Impressed / Confident
   - Energized / Excited
   - Focused / Calm
   - Inspired / Moved

2. **Generate 3 single-slide preview files**
   - Location: `.ecc-design/slide-previews/`
   - Each preview must be self-contained HTML
   - Show typography, color, motion clearly
   - Stay under ~100 lines of slide content

3. **Ask: Which preview to keep or what elements to mix?**

Use preset guide in `STYLE_PRESETS.md` for mood mapping.

---

### Step 4: Build the Presentation

**Output file name:**
- `presentation.html` (default)
- `[presentation-name].html` (if user specifies)

**Use `assets/` folder only when:**
- Extracting images from PPT/PPTX
- User supplies images/logos

**Required structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>
    <!-- Fonts from Google Fonts or Fontshare -->
    <style>
        /* Viewport-safe CSS base (from STYLE_PRESETS.md) */
        /* Theme custom properties */
        /* Slide-specific styles */
        /* Animation styles */
    </style>
</head>
<body>
    <main>
        <section class="slide" data-slide="1">
            <div class="slide-content">
                <!-- Slide content -->
            </div>
        </section>
        <!-- More slides -->
    </main>

    <nav class="nav-dots">
        <!-- Navigation dots -->
    </nav>

    <div class="keyboard-hint">
        <!-- Navigation hint -->
    </div>

    <script>
        // Presentation controller
        // Keyboard navigation
        // Touch/swipe navigation
        // Mouse wheel navigation
        // Intersection Observer for reveals
        // Reduced motion support
    </script>
</body>
</html>
```

---

### Step 5: Enforce Viewport Fit

**This is a hard gate.**

#### Golden Rule
```
Each slide = exactly one viewport height.
Too much content = split into more slides.
Never scroll inside a slide.
```

#### Rules

1. **Every slide must have:**
   ```css
   .slide {
       height: 100vh;
       height: 100dvh;
       overflow: hidden;
   }
   ```

2. **All type and spacing must scale with `clamp()`**
   ```css
   font-size: clamp(1rem, 2.5vw, 1.5rem);
   padding: clamp(1rem, 4vw, 4rem);
   ```

3. **When content doesn't fit → split into multiple slides**
   - Never squeeze text below readable sizes
   - Never allow scrollbars inside a slide

4. **Use density limits from STYLE_PRESETS.md**
   - Title: 1 heading + 1 subtitle + optional tagline
   - Content: 1 heading + 4-6 bullets or 2 paragraphs
   - Feature grid: 6 cards max
   - Code: 8-10 lines max

---

### Step 6: Validate

**Check at these sizes:**
- Desktop: 1920x1080, 1280x720
- Tablet: 768x1024
- Mobile: 375x667, 667x375

**If browser automation is available:**
- Verify no slide overflows
- Test keyboard navigation
- Check reduced motion support

---

### Step 7: Deliver

**At handoff:**
1. Delete temporary preview files (unless user wants to keep them)
2. Open the deck with platform-appropriate opener
3. Summarize:
   - File path
   - Preset used
   - Slide count
   - Easy theme customization points

**Platform openers:**
- macOS: `open presentation.html`
- Linux: `xdg-open presentation.html`
- Windows: `start "" presentation.html`

---

## PPT/PPTX Conversion

### Extraction Workflow

1. **Prefer `python3` with `python-pptx`**
   ```bash
   pip install python-pptx
   ```

2. **Extract from presentation:**
   - Text content per slide
   - Speaker notes
   - Images/assets

3. **If `python-pptx` unavailable:**
   - Ask: Install it or use manual/export-based workflow?

4. **After extraction:**
   - Run same style-selection workflow as new presentation
   - Preserve slide order
   - Preserve speaker notes

**Keep conversion cross-platform.** Don't rely on macOS-only tools when Python can do the job.

---

## Implementation Requirements

### HTML/CSS

- Use inline CSS and JS unless user explicitly wants multi-file
- Fonts from Google Fonts or Fontshare
- Prefer:
  - Atmospheric backgrounds
  - Strong type hierarchy
  - Clear visual direction
  - Abstract shapes, gradients, grids, noise, geometry
- Avoid illustrations (unless explicitly requested)

### JavaScript

**Must include:**
- Keyboard navigation (arrow keys, space)
- Touch/swipe navigation
- Mouse wheel navigation
- Progress indicator or slide index
- Reveal-on-enter animation triggers

**Example controller structure:**
```javascript
class PresentationController {
    constructor() {
        this.slides = document.querySelectorAll('.slide');
        this.currentSlide = 0;
        this.setupNavigation();
        this.setupObserver();
    }

    setupNavigation() {
        // Keyboard
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown' || e.key === ' ') this.next();
            if (e.key === 'ArrowUp') this.prev();
        });

        // Wheel
        document.addEventListener('wheel', (e) => {
            if (e.deltaY > 0) this.next();
            if (e.deltaY < 0) this.prev();
        });

        // Touch
        let touchStartY = 0;
        document.addEventListener('touchstart', (e) => {
            touchStartY = e.touches[0].clientY;
        });
        document.addEventListener('touchend', (e) => {
            const touchEndY = e.changedTouches[0].clientY;
            if (touchStartY - touchEndY > 50) this.next();
            if (touchEndY - touchStartY > 50) this.prev();
        });
    }

    setupObserver() {
        // Intersection Observer for reveal animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                }
            });
        }, { threshold: 0.5 });

        this.slides.forEach(slide => observer.observe(slide));
    }

    next() {
        if (this.currentSlide < this.slides.length - 1) {
            this.currentSlide++;
            this.goToSlide(this.currentSlide);
        }
    }

    prev() {
        if (this.currentSlide > 0) {
            this.currentSlide--;
            this.goToSlide(this.currentSlide);
        }
    }

    goToSlide(index) {
        this.slides[index].scrollIntoView({ behavior: 'smooth' });
        this.updateProgress();
    }

    updateProgress() {
        // Update dots or slide counter
    }
}
```

---

## Accessibility

### Semantic Structure

```html
<main>
    <section class="slide" aria-label="Slide 1: Title">
        <div class="slide-content">
            <h1>Presentation Title</h1>
        </div>
    </section>
</main>

<nav class="nav-dots" aria-label="Slide navigation">
    <button aria-label="Go to slide 1">1</button>
    <button aria-label="Go to slide 2">2</button>
</nav>
```

### Requirements

- Use semantic elements (`main`, `section`, `nav`)
- Maintain readable contrast ratios
- Support keyboard-only navigation
- Respect `prefers-reduced-motion`
- Include ARIA labels where needed

---

## Content Density Limits

Use these maxima unless user explicitly asks for denser slides AND readability holds:

| Slide Type | Limit |
|------------|-------|
| Title | 1 heading + 1 subtitle + optional tagline |
| Content | 1 heading + 4-6 bullets or 2 short paragraphs |
| Feature grid | 6 cards max |
| Code | 8-10 lines max |
| Quote | 1 quote + attribution |
| Image | 1 image constrained by viewport |

**When content exceeds limits → split into multiple slides**

---

## Anti-Patterns

### ❌ Avoid These

1. **Generic startup gradients**
   - Purple-on-white templates
   - No visual identity

2. **System-font decks**
   - Unless intentionally editorial

3. **Long bullet walls**
   - More than 6 bullets per slide
   - Tiny text to fit everything

4. **Code blocks that need scrolling**
   - More than 10 lines of code
   - Split into multiple slides instead

5. **Fixed-height content boxes**
   - Break on short screens
   - Use viewport-relative units instead

6. **Invalid negated CSS functions**
   ```css
   /* ❌ WRONG - browsers ignore silently */
   right: -clamp(28px, 3.5vw, 44px);
   margin-left: -min(10vw, 100px);

   /* ✅ CORRECT */
   right: calc(-1 * clamp(28px, 3.5vw, 44px));
   margin-left: calc(-1 * min(10vw, 100px));
   ```

---

## Quick Reference

### File Structure

```
project-root/
├── presentation.html          # Main deck
├── assets/                    # Images (if needed)
│   ├── slide-1-image.png
│   └── logo.svg
└── .ecc-design/              # Temporary previews
    └── slide-previews/
        ├── preview-1.html
        ├── preview-2.html
        └── preview-3.html
```

### Mood to Preset Quick Mapping

| Mood | Use Presets |
|------|-------------|
| Impressed / Confident | Bold Signal, Electric Studio, Dark Botanical |
| Excited / Energized | Creative Voltage, Neon Cyber, Split Pastel |
| Calm / Focused | Notebook Tabs, Paper & Ink, Swiss Modern |
| Inspired / Moved | Dark Botanical, Vintage Editorial, Pastel Geometry |

### Animation Feel

| Feeling | Motion Direction |
|---------|------------------|
| Dramatic | Slow fades, parallax, large scale-ins |
| Techy | Glow, particles, grid motion, scramble text |
| Playful | Springy easing, rounded shapes, floating motion |
| Professional | Subtle 200-300ms transitions, clean slides |
| Calm | Very restrained movement, whitespace-first |
| Editorial | Strong hierarchy, staggered text/image interplay |

---

## Related ECC Skills

- **frontend-patterns** - Component and interaction patterns around the deck
- **liquid-glass-design** - When presentation borrows Apple glass aesthetics
- **e2e-testing** - For automated browser verification of final deck

---

## Deliverable Checklist

Before final handoff, verify:

- [ ] Presentation runs from local file in browser
- [ ] Every slide fits viewport without scrolling
- [ ] Style is distinctive and intentional
- [ ] Animation is meaningful, not noisy
- [ ] Reduced motion is respected
- [ ] File paths and customization points explained

---

## Origin

This skill is based on the "Frontend Slides" skill from ECC (Exa
Computer Corp), inspired by the visual exploration approach of
[zarazhangrui](https://github.com/zarazhangrui).
