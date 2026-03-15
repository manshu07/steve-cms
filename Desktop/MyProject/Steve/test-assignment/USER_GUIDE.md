# BeyondCode Page Builder - User Guide

## Welcome to the Page Builder

The drag/drop page builder empowers you to create beautiful, responsive pages without coding. This guide will walk you through all the features and help you build your first page.

---

## 🎯 Getting Started

### Accessing the Builder

1. Log in to your BeyondCode CMS account
2. Navigate to **Pages** in the sidebar
3. Click **Edit** on any existing page, or **Create New Page**
4. The page builder will open automatically

### Builder Interface Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Builder Toolbar                           │
│  [Desktop] [Tablet] [Mobile]  [Undo] [Redo]  [Save] [Publish] │
├──────────┬──────────────────────────────────┬──────────────────┤
│          │                                  │                  │
│ Palette │          Canvas                   │   Properties     │
│          │                                  │                  │
│ Components (drag from here)              │ (edit here)      │
│          │                                  │                  │
│ • Heading │    ┌─────────────────────────┐   │                  │
│ • Text    │    │                         │   │                  │
│ • Button  │    │   Your Page Content     │   │                  │
│ • Image   │    │                         │   │                  │
│ • ...     │    └─────────────────────────┘   │                  │
│          │                                  │                  │
└──────────┴──────────────────────────────────┴──────────────────┘
```

---

## 🧩 Using Components

### Available Components

#### **Content Components**

**Heading**
- Add titles and subtitles (H1-H6)
- Customize text and alignment (left, center, right)
- Perfect for page sections and content hierarchy

**Text Paragraph**
- Add rich text content
- Customize padding and spacing
- Great for articles and descriptions

**Quote**
- Add testimonials and quotes
- Include author attribution
- Choose alignment for visual impact

#### **Form Components**

**Button**
- Create call-to-action buttons
- Choose styles: Primary, Secondary, or Text
- Add links (with option to open in new tab)

**Form Container**
- Build contact forms and surveys
- Customize form title and submit button text
- Add success messages for submissions

#### **Layout Components**

**Container**
- Create boxed or full-width sections
- Set background colors
- Control padding for spacing

**Columns**
- Create 2 or 3 column layouts
- Adjust gap between columns
- Drag other components into columns

**Divider**
- Add horizontal or vertical separators
- Customize thickness and color
- Great for visual separation

**Spacer**
- Add vertical spacing between sections
- Set exact height (e.g., "20px", "40px")
- Helps with layout precision

#### **Media Components**

**Image**
- Upload and display images
- Set width and alignment
- Add alt text for accessibility

---

## 🖱️ Drag and Drop Basics

### Adding Components

1. **Find the component** in the Palette (left sidebar)
2. **Click and drag** the component to the Canvas (center area)
3. **Drop it** where you want it to appear
4. The component will be added and automatically selected

### Reordering Components

1. **Click and hold** the drag handle (appears on hover/selection)
2. **Drag** the component to a new position
3. **Release** to drop it in place

### Selecting Components

- **Click** any component to select it
- Selected components show a blue border and drag handle
- The Properties panel (right sidebar) will show editable options

---

## ⚙️ Editing Properties

### Property Panel (Right Sidebar)

When you select a component, the Properties panel shows all editable settings:

**Text Content:**
- Type directly into text fields
- Select from dropdown menus (alignment, heading levels, etc.)

**Styles:**
- **Grid Span:** Control width (1-12 columns)
- **Padding:** Add internal spacing (e.g., "20px")
- **Margin:** Add external spacing (e.g., "20px 0")
- **Background:** Set background color (e.g., "#ffffff", "#f0f0f0")

**Special Properties:**
- **Buttons:** Edit text, style, link URL
- **Images:** Upload new image, set alt text, width, alignment
- **Forms:** Customize title, button text, success message

---

## 📱 Responsive Preview

### Switching Viewports

Click the viewport buttons in the toolbar to preview different screen sizes:

- **Desktop** 🖥️ (1200px width) - Default view
- **Tablet** 📱 (768px width) - iPad and tablets
- **Mobile** 📱 (375px width) - Smartphones

### Best Practices

- Start with **Desktop** view for building
- Check **Mobile** view to ensure content fits
- Adjust grid spans for mobile (use smaller spans on mobile)
- Test images and buttons on all viewports

---

## 💾 Saving and Publishing

### Auto-Save

The builder automatically saves your work every 3 seconds after you stop making changes. You'll see:
- A **progress bar** at the top when there are unsaved changes
- A **success notification** when auto-save completes

### Manual Save

1. Click the **Save** button in the toolbar
- Or press `Ctrl+S` (Windows/Linux) or `Cmd+S` (Mac)
- You'll see a success notification when saved

### Publishing

1. Make sure all changes are saved (no progress bar showing)
2. Click the **Publish** button in the toolbar
3. Confirm publishing
4. Your page will go live immediately!

---

## ⌨️ Keyboard Shortcuts

Speed up your workflow with these shortcuts:

| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` / `Cmd+Z` | Undo last action |
| `Ctrl+Y` / `Cmd+Y` | Redo undone action |
| `Ctrl+C` / `Cmd+C` | Copy selected component |
| `Ctrl+V` / `Cmd+V` | Paste component |
| `Ctrl+D` / `Cmd+D` | Duplicate selected component |
| `Ctrl+S` / `Cmd+S` | Save page |
| `Delete` | Remove selected component |
| `Escape` | Clear selection |

---

## 🎨 Tips and Best Practices

### Creating Effective Pages

1. **Start with a plan** - Sketch your page layout first
2. **Use headings** - Create clear hierarchy with H1, H2, H3
3. **Add breathing room** - Use Spacers between sections
4. **Break up text** - Use multiple Text Paragraphs instead of one long text
5. **Make it mobile-friendly** - Always check mobile view
6. **Add CTAs** - Use Buttons to guide user actions
7. **Use quotes** - Build trust with testimonials
8. **Organize with containers** - Group related content

### Layout Tips

- **12-Column Grid:** Think of the canvas as 12 columns
  - Full width = 12 columns
  - Half width = 6 columns
  - Third width = 4 columns
- **Containers:** Use to group content with consistent styling
- **Columns:** Great for side-by-side content
- **Spacers:** Add visual breathing room

### Common Page Structures

**Landing Page:**
```
1. Heading (H1) - Hero section
2. Text Paragraph - Introduction
3. Spacer (40px)
4. Columns (2) - Features/benefits
5. Spacer (40px)
6. Quote - Testimonial
7. Spacer (40px)
8. Button - Call to action
```

**About Page:**
```
1. Heading (H1) - Page title
2. Container - Bio section
   - Image
   - Heading (H2)
   - Text Paragraph
3. Spacer (40px)
4. Columns (2) - Team members
5. Spacer (40px)
6. Divider
7. Heading (H2) - Mission
8. Text Paragraph
```

---

## 🐛 Troubleshooting

### Common Issues

**Component won't delete:**
- Make sure it's selected (blue border showing)
- Try pressing the Delete key instead of clicking delete button
- Refresh the page if stuck

**Image not uploading:**
- Check file size (max 5MB)
- Ensure file is an image (JPG, PNG, GIF)
- Check your internet connection
- Try again in a few moments

**Changes not saving:**
- Check for the progress bar at the top (if visible, it's saving)
- Wait a few seconds for auto-save to complete
- Try manually clicking Save
- Refresh the page if needed

**Canvas looks wrong:**
- Try switching viewports (Desktop → Tablet → Mobile)
- Check if grid spans are too wide for mobile
- Resize browser window to full screen
- Clear browser cache and refresh

---

## 📚 Advanced Features

### Templates

**Coming Soon:** Save your page layouts as templates and reuse them for future pages!

### Asset Library

Access all your uploaded images in the Image component:
1. Select an Image component
2. Click "Upload Image" or browse your library
3. Search and filter your uploaded images
4. Click to select and use instantly

### Keyboard Navigation

Navigate the builder quickly:
- `Tab` - Move between sections
- `Arrow Keys` - Navigate through components (coming soon)
- `Enter` - Edit selected component
- `Escape` - Exit editing mode

---

## 🆘 Need Help?

### Getting Support

1. **Check the FAQ** - Most common questions answered here
2. **Contact Support** - Email support@beyondcode.com
3. **Video Tutorials** - Watch step-by-step guides
4. **Community Forum** - Connect with other users

### Reporting Bugs

Found an issue? Please report:
1. What you were trying to do
2. What happened instead
3. Browser and device information
4. Screenshot (if applicable)

---

## 🎓 Next Steps

**For Beginners:**
1. Try the sample templates
2. Build your first simple page (1 heading, 1 text, 1 button)
3. Experiment with different layouts
4. Save and publish your page

**For Advanced Users:**
1. Master the Columns component for complex layouts
2. Use Containers for consistent branding
3. Optimize for mobile responsiveness
4. Create templates for common layouts

---

## 📖 Additional Resources

- **Video Tutorials:** [Link to tutorials]
- **Component Library:** [Link to component showcase]
- **Best Practices Guide:** [Link to guide]
- **API Documentation:** [Link for developers]

---

**Version:** 1.0
**Last Updated:** March 2026
**Happy Building!** 🚀
