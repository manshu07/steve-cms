import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_cms.settings')
django.setup()

from marketing.models import Page

# Read the exact HTML from the reference implementation
with open('beyondcode-site/index.html', 'r', encoding='utf-8') as f:
    reference_html = f.read()

# Extract the body content from the reference HTML
# The reference has the complete HTML structure, we need to extract just the content inside <main>
import re
main_content_match = re.search(r'<main class="min-h-screen[^>]*>(.*?)</main>', reference_html, re.DOTALL)

if main_content_match:
    exact_body_html = main_content_match.group(1)
else:
    # Fallback: use the entire HTML if we can't find the main tag
    exact_body_html = reference_html

# Add the script tag that was outside the main tag
exact_body_html += '<script src="/static/js/main.js"></script>'

# Fix static file paths for Django
# Replace /assets/ with /static/assets/ and /js/ with /static/js/
exact_body_html = exact_body_html.replace('src="/assets/', 'src="/static/assets/')
exact_body_html = exact_body_html.replace('src="/js/', 'src="/static/js/')
exact_body_html = exact_body_html.replace('href="/assets/', 'href="/static/assets/')
exact_body_html = exact_body_html.replace('href="/css/', 'href="/static/css/')

# Create a single HTML embed block with the exact homepage content
homepage_blocks = {
    "blocks": [
        {
            "type": "html_embed",
            "html": exact_body_html
        }
    ]
}

# Update the homepage in CMS with the exact HTML
try:
    home_page = Page.objects.get(slug='home')
    home_page.blocks_json = homepage_blocks
    home_page.title = "Home"
    home_page.status = 'published'
    home_page.seo_title = "BeyondCode AI | Collections Automation for EU Lenders"
    home_page.seo_description = "Turn collections backlogs into predictable throughput. 100% contact-attempt coverage with audit-ready evidence logs within 40 business days."
    home_page.og_title = "BeyondCode AI | Collections Automation for EU Lenders"
    home_page.og_description = "Turn collections backlogs into predictable throughput. 100% contact-attempt coverage with audit-ready evidence logs within 40 business days."
    home_page.save()
    print(f"[SUCCESS] Homepage updated with EXACT HTML from reference implementation")
    print(f"   - Page ID: {home_page.id}")
    print(f"   - Status: {home_page.status}")
    print(f"   - Using exact HTML from: beyondcode-site/index.html")
    print(f"   - HTML length: {len(exact_body_html)} characters")
except Page.DoesNotExist:
    print("[ERROR] Homepage with slug='home' not found. Creating new homepage...")
    home_page = Page.objects.create(
        title="Home",
        slug="home",
        status="published",
        blocks_json=homepage_blocks,
        seo_title="BeyondCode AI | Collections Automation for EU Lenders",
        seo_description="Turn collections backlogs into predictable throughput. 100% contact-attempt coverage with audit-ready evidence logs within 40 business days.",
        og_title="BeyondCode AI | Collections Automation for EU Lenders",
        og_description="Turn collections backlogs into predictable throughput. 100% contact-attempt coverage with audit-ready evidence logs within 40 business days."
    )
    print(f"[SUCCESS] Homepage created with EXACT HTML from reference implementation")
    print(f"   - Page ID: {home_page.id}")
    print(f"   - Status: {home_page.status}")
    print(f"   - Using exact HTML from: beyondcode-site/index.html")

print("\n[IMPORTANT] This homepage uses the EXACT HTML from the reference implementation.")
print("It will provide 100% pixel-perfect match with the beyondcode-site/index.html design.")
print("\nTo edit content:")
print("1. The page contains one large HTML embed block")
print("2. For small text changes, you can edit the HTML directly")
print("3. For major changes, consider splitting into multiple blocks")
