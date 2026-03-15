"""
Public views for the marketing site.
Handles homepage, pages, blog, sitemap, and robots.txt.
"""

from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Page, Post, NavMenu, Footer, Category
from .seo import build_seo_payload


def marketing_home(request):
    """Render the homepage. Tries CMS page first, falls back to hardcoded template."""
    # Try to get CMS homepage
    home_page = Page.objects.filter(slug='home').first()

    if home_page and home_page.is_published:
        # Use CMS-based homepage with consistent nav/footer
        nav = NavMenu.objects.filter(name='Primary').first()
        footer = Footer.objects.first()
        return render(request, 'marketing/page.html', {
            'page': home_page,
            'nav_menu': nav,
            'footer': footer,
            'seo': build_seo_payload(home_page, request=request),
        })

    # Fallback to hardcoded template
    nav = NavMenu.objects.filter(name='Primary').first()
    footer = Footer.objects.first()
    return render(request, 'marketing/home.html', {
        'nav_menu': nav,
        'footer': footer,
        'seo': {
            'title': 'BeyondCode AI | Collections Automation for EU Lenders',
            'description': 'Turn collections backlogs into predictable throughput. 100% contact-attempt coverage with audit-ready evidence logs within 40 business days.',
            'og_title': 'BeyondCode AI | Collections Automation for EU Lenders',
            'og_description': 'Turn collections backlogs into predictable throughput. 100% contact-attempt coverage with audit-ready evidence logs within 40 business days.',
            'image': None,
            'url': request.build_absolute_uri('/'),
        },
    })


def page_detail(request, slug):
    """Render a single page with publish gate."""
    page = get_object_or_404(Page, slug=slug)
    if not page.is_published:
        raise Http404()
    nav = NavMenu.objects.filter(name='Primary').first()
    footer = Footer.objects.first()
    return render(request, 'marketing/page.html', {
        'page': page,
        'nav_menu': nav,
        'footer': footer,
        'seo': build_seo_payload(page, request=request),
    })


def blog_index(request):
    """Render the blog index with published posts and category filter."""
    posts = Post.objects.filter(status__in=['published', 'scheduled']).order_by('-publish_at')
    posts = [post for post in posts if post.is_published]
    categories = Category.objects.all()  # For category filter chips
    nav = NavMenu.objects.filter(name='Primary').first()
    footer = Footer.objects.first()
    return render(request, 'marketing/blog_index.html', {
        'posts': posts,
        'categories': categories,
        'nav_menu': nav,
        'footer': footer,
        'seo': {
            'title': 'BeyondCode AI Blog',
            'description': 'Insights on AI-powered debt collection, compliance, and operational efficiency for EU lenders.',
            'og_title': 'BeyondCode AI Blog',
            'og_description': 'Insights on AI-powered debt collection, compliance, and operational efficiency for EU lenders.',
            'image': None,
        },
    })


def blog_post_detail(request, slug):
    """Render a single blog post with publish gate."""
    post = get_object_or_404(Post, slug=slug)
    if not post.is_published:
        raise Http404()
    nav = NavMenu.objects.filter(name='Primary').first()
    footer = Footer.objects.first()
    return render(request, 'marketing/blog_post.html', {
        'post': post,
        'nav_menu': nav,
        'footer': footer,
        'seo': build_seo_payload(post, request=request),
    })


def sitemap_xml(request):
    """Google-compliant XML sitemap listing all published pages and posts."""
    now = timezone.now()
    base = request.build_absolute_uri('/').rstrip('/')

    urls = []

    # Homepage
    urls.append({
        'loc': f'{base}/',
        'changefreq': 'weekly',
        'priority': '1.0',
    })

    # Blog index
    urls.append({
        'loc': f'{base}/blog/',
        'changefreq': 'daily',
        'priority': '0.8',
    })

    # Published pages
    pages = Page.objects.filter(
        status__in=['published', 'scheduled'],
    ).order_by('title')
    for page in pages:
        if not page.is_published:
            continue
        urls.append({
            'loc': f'{base}/{page.slug}/',
            'lastmod': page.updated_at.strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.7',
        })

    # Published posts
    posts = Post.objects.filter(
        status__in=['published', 'scheduled'],
    ).order_by('-publish_at')
    for post in posts:
        if not post.is_published:
            continue
        urls.append({
            'loc': f'{base}/blog/{post.slug}/',
            'lastmod': post.updated_at.strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.6',
        })

    # Build XML
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for entry in urls:
        lines.append('  <url>')
        lines.append(f'    <loc>{entry["loc"]}</loc>')
        if 'lastmod' in entry:
            lines.append(f'    <lastmod>{entry["lastmod"]}</lastmod>')
        lines.append(f'    <changefreq>{entry["changefreq"]}</changefreq>')
        lines.append(f'    <priority>{entry["priority"]}</priority>')
        lines.append('  </url>')
    lines.append('</urlset>')

    xml = '\n'.join(lines)
    return HttpResponse(xml, content_type='application/xml')


def robots_txt(request):
    """Serve robots.txt with sitemap reference."""
    base = request.build_absolute_uri('/').rstrip('/')
    content = (
        'User-agent: *\n'
        'Allow: /\n'
        'Disallow: /cms/\n'
        'Disallow: /admin/\n'
        f'\nSitemap: {base}/sitemap.xml\n'
    )
    return HttpResponse(content, content_type='text/plain')
