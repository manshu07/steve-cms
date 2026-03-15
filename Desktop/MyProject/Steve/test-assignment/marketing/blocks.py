"""
Server-side block renderer (JSON → HTML).
Renders all 13 CMS block types to HTML for display on public pages.
"""

from html import escape

from .renderers import render_editorjs


def render_blocks(payload):
    """
    Render blocks JSON to HTML.

    Accepts either {blocks: [...]} or a raw list for backward compatibility.
    """
    if not payload:
        return ''

    # Handle both {blocks: [...]} and raw [...] formats
    blocks = payload.get('blocks', []) if isinstance(payload, dict) else payload

    html = ''
    for block in blocks:
        block_type = block.get('type')
        if block_type == 'rich_text':
            html += _rich_text(block)
        elif block_type == 'code':
            html += _code(block)
        elif block_type == 'html_embed':
            html += _html_embed(block)
        elif block_type == 'callout':
            html += _callout(block)
        elif block_type == 'cta':
            html += _cta(block)
        elif block_type == 'feature_grid':
            html += _feature_grid(block)
        elif block_type == 'comparison_table':
            html += _comparison_table(block)
        elif block_type == 'table':
            html += _table(block)
        elif block_type == 'faq':
            html += _faq(block)
        elif block_type == 'quote':
            html += _quote(block)
        elif block_type == 'logo_cloud':
            html += _logo_cloud(block)
        elif block_type == 'pricing_table':
            html += _pricing_table(block)
        elif block_type == 'image_gallery':
            html += _image_gallery(block)
        elif block_type == 'button':
            html += _button(block)

    return html


def _code(block):
    """
    Trusted raw HTML/JS block.

    This is intended for CMS admins to embed trusted snippets (e.g. clickwrap embed).
    It is wrapped in markers that the sanitizer preserves.
    """
    raw = block.get('html', '')
    if not raw:
        return ''
    return f"<!--TRUSTED_CODE_START-->{raw}<!--TRUSTED_CODE_END-->"


def _html_embed(block):
    """Render HTML embed block (for videos, iframes, or custom HTML)."""
    html = block.get('html', '')
    if not html:
        return ''

    # Return the HTML exactly as provided - no modifications
    # This allows for pixel-perfect reproduction of reference implementations
    return html


def _rich_text(block):
    """Render rich text block with EditorJS content."""
    content = block.get('content', {})
    if not content:
        return ''

    rendered = render_editorjs(content)

    # Check if this is the hero section (has "Bring Your Money Home" heading)
    if 'Bring Your Money Home' in rendered:
        # Render hero section with full homepage design
        hero_html = '''
        <section class="relative overflow-hidden">
            <header class="relative z-20 flex items-center justify-between px-6 md:px-12 lg:px-20 py-5 max-w-7xl mx-auto">
                <div class="flex items-center gap-3">
                    <img src="/static/assets/logo-icon.png" alt="BeyondCode AI" class="h-9">
                    <span class="font-bold text-foreground text-lg tracking-tight">BeyondCode</span>
                </div>
                <div class="flex items-center gap-3">
                    <a href="#how-it-works" class="items-center justify-center gap-2 whitespace-nowrap rounded-lg font-semibold ring-offset-background transition-all duration-300 h-11 px-6 py-2 hidden md:inline-flex text-muted-foreground hover:text-foreground text-sm">How it works</a>
                    <a href="https://calendly.com/henri-beyondcode/ai-collections-demo" target="_blank" class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-semibold ring-offset-background transition-all duration-300 hover:shadow-lg h-11 bg-primary text-primary-foreground hover:bg-primary/90 text-sm px-5 py-2.5">Book a Quick Demo</a>
                </div>
            </header>
            <div class="relative z-10 text-center px-6 pt-8 pb-6 md:pt-12 md:pb-8 max-w-4xl mx-auto">
                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-accent text-accent-foreground text-sm font-medium rounded-full mb-8">
                    <span class="w-2 h-2 rounded-full bg-primary"></span>
                    AI-Powered Debt Collection Platform
                </div>
                ''' + rendered + '''
                <div class="py-6">
                    <p class="text-center text-muted-foreground text-sm font-medium tracking-wide uppercase mb-6">Trusted by EU-regulated financial institutions</p>
                    <div class="flex flex-wrap items-center justify-center gap-x-10 gap-y-4 px-6">
                        <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">BONDORA</span>
                        <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">RAHA24</span>
                        <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">BB-FINANCE</span>
                        <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">HYBA FINANCE</span>
                        <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">THEMIS LAW BUREAU</span>
                        <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">BALTASAR LEASING</span>
                    </div>
                </div>
            </div>
        </section>
        '''
        return hero_html

    # Check if this is "One Platform" section
    if 'One Platform for Compliant AI Collections' in rendered:
        return f'''
        <section class="section-padding bg-background">
            <div class="max-w-6xl mx-auto px-6">
                <div class="text-center mb-8">
                    <h2 class="text-3xl md:text-4xl font-bold text-foreground mb-4">One Platform for Compliant AI Collections</h2>
                    <p class="text-muted-foreground text-lg max-w-2xl mx-auto">Unify your outreach, compliance, and analytics in one platform—saving time and cutting costs.</p>
                </div>
                <div class="grid md:grid-cols-3 gap-6">
                    <div class="rounded-xl p-7 border transition-all bg-card text-card-foreground border-border hover:border-primary/30 hover:shadow-md">
                        <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-accent">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5 text-primary"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"></path></svg>
                        </div>
                        <h3 class="text-lg font-bold mb-2">Automated Outreach at Scale</h3>
                        <p class="text-sm leading-relaxed text-muted-foreground">Every debtor on your list gets contacted on time, every cycle. Scale from hundreds to thousands of calls without adding headcount.</p>
                    </div>
                    <div class="rounded-xl p-7 border transition-all bg-primary text-primary-foreground border-primary shadow-lg">
                        <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-primary-foreground/20">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5 text-primary-foreground"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5,19 5a1 1 0 0 1 1 1z"></path></svg>
                        </div>
                        <h3 class="text-lg font-bold mb-2">GDPR-Compliant by Design</h3>
                        <p class="text-sm leading-relaxed text-primary-foreground/80">Calling windows, retry rules, and consent guardrails enforced automatically. Audit-ready evidence logs for every interaction.</p>
                    </div>
                    <div class="rounded-xl p-7 border transition-all bg-card text-card-foreground border-border hover:border-primary/30 hover:shadow-md">
                        <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-accent">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5 text-primary"><path d="M3 3v16a2 2 0 0 0 2 2h16"></path><path d="M18 17V9"></path><path d="M13 17V5"></path><path d="M8 17v-3"></path></svg>
                        </div>
                        <h3 class="text-lg font-bold mb-2">Predictable Recovery Operations</h3>
                        <p class="text-sm leading-relaxed text-muted-foreground">Turn collections into measurable weekly output with real-time analytics, coverage reports, and structured outcome tracking.</p>
                    </div>
                </div>
            </div>
        </section>
        '''

    return _wrap('div', rendered, 'cms-prose section-padding')


def _callout(block):
    """Render callout block matching homepage design."""
    title = escape(block.get('title', ''))
    body = escape(block.get('body', ''))

    # Convert markdown-like formatting to HTML
    import re
    body_html = body

    # Handle bold text with **
    body_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', body_html)

    # Handle bullet points
    lines = body_html.split('\n')
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('•'):
            formatted_lines.append(f'<li>{line[1:].strip()}</li>')
        elif line.startswith('-'):
            formatted_lines.append(f'<li>{line[1:].strip()}</li>')
        else:
            if line:
                formatted_lines.append(f'<p>{line}</p>')

    body_content = ''.join(formatted_lines)

    return _wrap(
        'section',
        _wrap('div',
            _wrap('span', title, 'inline-flex items-center gap-2 px-4 py-1.5 bg-accent text-accent-foreground text-sm font-medium rounded-full mb-6') +
            _wrap('h2', 'Real Results From a Live Portfolio', 'text-3xl md:text-4xl font-bold text-foreground mb-4') +
            _wrap('p', 'Measurable impact from a single month of automated AI collection on an EU-regulated portfolio.', 'text-muted-foreground text-lg max-w-xl mx-auto') +
            _wrap('div', body_content, 'grid grid-cols-2 md:grid-cols-5 gap-4'),
            'max-w-6xl mx-auto px-6 text-center'
        ),
        'section-padding bg-secondary/50'
    )


def _cta(block):
    """Render CTA block with title, body, and button."""
    title = escape(block.get('title', ''))
    body = escape(block.get('body', ''))
    label = escape(block.get('button_label', ''))
    url = escape(block.get('button_url', ''))
    secondary_label = escape(block.get('secondary_button_label', ''))
    secondary_url = escape(block.get('secondary_button_url', ''))

    buttons = ''
    if label and url:
        buttons += f'<a href="{url}" class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-semibold ring-offset-background transition-all duration-300 hover:shadow-lg h-11 bg-primary text-primary-foreground hover:bg-primary/90 px-8 py-6 text-base">{label}</a>'
    if secondary_label and secondary_url:
        buttons += f'<a href="{secondary_url}" class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-semibold ring-offset-background transition-all duration-300 border bg-transparent hover:border-primary/50 h-11 px-8 py-6 text-base border-border text-foreground hover:bg-secondary">{secondary_label}</a>'

    return _wrap(
        'section',
        _wrap('div',
            _wrap('h2', title, 'text-3xl md:text-4xl font-bold text-foreground mb-4') +
            _wrap('p', body, 'text-muted-foreground text-lg max-w-2xl mx-auto mb-10') +
            _wrap('div', buttons, 'flex flex-col sm:flex-row items-center justify-center gap-4'),
            'max-w-6xl mx-auto px-6 text-center'
        ),
        'section-padding bg-background'
    )


def _button(block):
    """Render standalone button block with configurable style and behavior."""
    label = escape(block.get('label', 'Click Me'))
    url = escape(block.get('url', ''))
    style = escape(block.get('style', 'primary'))
    open_new_tab = block.get('open_new_tab', False)
    icon = escape(block.get('icon', ''))

    # Map style to CSS classes
    style_classes = {
        'primary': 'bg-primary text-primary-foreground hover:bg-primary/90',
        'secondary': 'border border-border bg-transparent text-foreground hover:bg-secondary hover:border-secondary',
        'ghost': 'bg-transparent text-muted-foreground hover:text-foreground hover:bg-secondary',
        'destructive': 'bg-destructive text-destructive-foreground hover:bg-destructive/90'
    }

    css_class = style_classes.get(style, style_classes['primary'])

    # Build target attribute
    target = ' target="_blank" rel="noopener noreferrer"' if open_new_tab else ''

    # Add icon if provided
    icon_html = ''
    if icon:
        icon_html = f'<span class="mr-2">{icon}</span>'

    # Build button HTML
    button_html = f'<a href="{url}"{target} class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-semibold ring-offset-background transition-all duration-300 hover:shadow-lg h-11 px-8 py-2.5 text-base {css_class}">{icon_html}{label}</a>'

    # Wrap in a centered container
    return _wrap('div', button_html, 'text-center py-6')


def _feature_grid(block):
    """Render feature grid block with cards matching homepage design."""
    items = block.get('items', [])
    cards = ''.join(
        _wrap(
            'div',
            _wrap('div', '', 'w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-accent') +
            _wrap('h3', escape(item.get('title', '')), 'text-lg font-bold mb-2') +
            _wrap('p', escape(item.get('body', '')), 'text-sm leading-relaxed text-muted-foreground'),
            'rounded-xl p-7 border transition-all bg-card text-card-foreground border-border hover:border-primary/30 hover:shadow-md'
        )
        for item in items
    )
    return _wrap(
        'section',
        _wrap('div',
            _wrap('div', 'Transform Your Debt Collection With Our Compliant AI Solution', 'text-3xl md:text-4xl font-bold text-foreground mb-4') +
            _wrap('p', 'Everything you need to automate, scale, and audit your collection operations—in one platform.', 'text-muted-foreground text-lg max-w-2xl mx-auto mb-8'),
            'text-center mb-8'
        ) +
        _wrap('div', cards, 'grid sm:grid-cols-2 lg:grid-cols-4 gap-5'),
        'max-w-6xl mx-auto px-6 section-padding bg-background'
    )


def _comparison_table(block):
    """Render comparison table block with headers and rows."""
    headers = block.get('headers', [])
    rows = block.get('rows', [])
    head_cells = ''.join(_wrap('th', escape(header)) for header in headers)
    head = _wrap('thead', _wrap('tr', head_cells))
    body_rows = ''.join(
        _wrap('tr', ''.join(_wrap('td', escape(cell)) for cell in row))
        for row in rows
    )
    body = _wrap('tbody', body_rows)
    return _wrap('table', head + body, 'cms-comparison')


def _table(block):
    """Render generic table block with headers and rows."""
    headers = block.get('headers', [])
    rows = block.get('rows', [])
    head_cells = ''.join(_wrap('th', escape(header)) for header in headers)
    head = _wrap('thead', _wrap('tr', head_cells)) if headers else ''
    body_rows = ''.join(
        _wrap('tr', ''.join(_wrap('td', escape(cell)) for cell in row))
        for row in rows
    )
    body = _wrap('tbody', body_rows)
    return _wrap('table', head + body, 'cms-table')


def _faq(block):
    """Render FAQ block with question/answer pairs."""
    items = block.get('items', [])
    entries = ''.join(
        _wrap(
            'div',
            _wrap('h4', escape(item.get('question', ''))) +
            _wrap('p', escape(item.get('answer', ''))),
            'cms-faq-item'
        )
        for item in items
    )
    return _wrap('div', entries, 'cms-faq')


def _quote(block):
    """Render quote block with quote text and author."""
    quote = escape(block.get('quote', ''))
    author = escape(block.get('author', ''))
    inner = _wrap('blockquote', quote)
    if author:
        inner += _wrap('p', author, 'cms-quote-author')
    return _wrap('div', inner, 'cms-quote')


def _logo_cloud(block):
    """Render logo cloud block matching homepage design."""
    logos = block.get('logos', [])
    items = ''.join(
        _wrap('span', escape(logo.get("alt", "")), 'text-muted-foreground/60 font-bold text-sm tracking-widest uppercase')
        for logo in logos
    )
    return _wrap(
        'div',
        _wrap('p', 'Trusted by EU-regulated financial institutions', 'text-center text-muted-foreground text-sm font-medium tracking-wide uppercase mb-6') +
        _wrap('div', items, 'flex flex-wrap items-center justify-center gap-x-10 gap-y-4 px-6'),
        'py-6'
    )


def _pricing_table(block):
    """Render pricing table block with plan cards."""
    plans = block.get('plans', [])
    cards = ''
    for plan in plans:
        features = ''.join(_wrap('li', escape(feature)) for feature in plan.get('features', []))
        card = (
            _wrap('h4', escape(plan.get('title', ''))) +
            _wrap('p', escape(plan.get('price', '')), 'cms-price') +
            _wrap('ul', features)
        )
        cards += _wrap('div', card, 'cms-pricing-card')
    return _wrap('div', cards, 'cms-pricing')


def _image_gallery(block):
    """Render image gallery block with title, layout, and images."""
    title = escape(block.get('title', ''))
    layout = block.get('layout', 'grid')
    images = block.get('images', [])

    header = _wrap('h3', title, 'cms-gallery-title') if title else ''

    items = ''
    for img in images:
        src = escape(img.get('src', ''))
        alt = escape(img.get('alt', ''))
        caption = escape(img.get('caption', ''))
        inner = f'<img src="{src}" alt="{alt}" loading="lazy">'
        if caption:
            inner += _wrap('span', caption, 'cms-gallery-caption')
        items += _wrap('figure', inner, 'cms-gallery-item')

    layout_class = f'cms-gallery cms-gallery-{layout}'
    return _wrap('div', header + _wrap('div', items, layout_class), 'cms-gallery-wrap')


def _wrap(tag, content, class_name=None):
    """Build an HTML tag with optional class attribute."""
    attrs = f' class="{class_name}"' if class_name else ''
    return f'<{tag}{attrs}>{content}</{tag}>'
