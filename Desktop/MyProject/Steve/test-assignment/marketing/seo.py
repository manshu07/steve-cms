"""
SEO payload builder for pages and posts.
Provides intelligent fallbacks for Open Graph and Twitter Card meta tags.
"""

import re
from django.utils.text import Truncator


def extract_first_image(html):
    """Extract the first image src from HTML content."""
    if not html:
        return None
    match = re.search(r'<img[^>]+src="([^"]+)"', html)
    if not match:
        return None
    return match.group(1).strip()


def extract_first_paragraph(html, limit=160):
    """Extract and truncate the first paragraph from HTML content."""
    if not html:
        return ''
    match = re.search(r'<p[^>]*>(.*?)</p>', html, flags=re.I | re.S)
    if not match:
        return ''
    raw = re.sub(r'<[^>]+>', '', match.group(1)).strip()
    return Truncator(raw).chars(limit)


def build_seo_payload(obj, request=None):
    """
    Build SEO payload for a page or post.

    Implements intelligent fallback chain:
    - Title: seo_title → title
    - Description: seo_description → first paragraph from HTML
    - Image: og_image → twitter_image → primary_image → cover_image → first img in HTML

    IMPORTANT: Checks both body_html and blocks_html for content extraction.
    """
    # Check body_html first (legacy), then blocks_html (new blocks system)
    html = getattr(obj, 'body_html', '') or ''
    if not html:
        html = getattr(obj, 'blocks_html', '') or ''

    # Build title with fallback
    title = obj.seo_title or obj.title if hasattr(obj, 'seo_title') else obj.title

    # Build description with fallback
    description = obj.seo_description if hasattr(obj, 'seo_description') else ''
    if not description:
        description = extract_first_paragraph(html)

    # Build OG title with fallback
    og_title = obj.og_title if hasattr(obj, 'og_title') else ''
    og_title = og_title or title

    # Build OG description with fallback
    og_description = obj.og_description if hasattr(obj, 'og_description') else ''
    og_description = og_description or description

    # Build image with fallback chain
    image = None
    if hasattr(obj, 'og_image') and obj.og_image:
        image = obj.og_image
    elif hasattr(obj, 'twitter_image') and obj.twitter_image:
        image = obj.twitter_image
    elif hasattr(obj, 'primary_image') and obj.primary_image:
        image = obj.primary_image
    elif hasattr(obj, 'cover_image') and obj.cover_image:
        image = obj.cover_image
    else:
        image = extract_first_image(html)

    payload = {
        'title': title,
        'description': description,
        'og_title': og_title,
        'og_description': og_description,
        'image': image,
    }

    # Add URL if request is provided
    if request and hasattr(obj, 'get_absolute_url'):
        payload['url'] = request.build_absolute_uri(obj.get_absolute_url())
        # Make relative image URLs absolute
        if payload.get('image') and not payload['image'].startswith('http'):
            payload['image'] = request.build_absolute_uri(payload['image'])

    return payload
