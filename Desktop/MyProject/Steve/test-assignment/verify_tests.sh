#!/bin/bash
# Quick verification script for the test suite
# This script runs smoke tests and verifies critical functionality

set -e  # Exit on error

echo "🧪 Running Test Suite Verification"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Run from Django project root."
    exit 1
fi

# Check Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python not found"
    exit 1
fi

echo "✅ Environment check passed"
echo ""

# Check dependencies
echo "📦 Checking dependencies..."
python -c "import django; print(f'Django version: {django.VERSION}')" || {
    echo "❌ Django not installed. Run: pip install django"
    exit 1
}
echo "✅ Dependencies OK"
echo ""

# Run smoke tests
echo "🔥 Running smoke tests..."
python run_tests.py smoke || {
    echo ""
    echo "❌ Smoke tests failed!"
    echo ""
    echo "Smoke tests are fast tests that catch critical issues."
    echo "These failures indicate show-stopper bugs that must be fixed."
    exit 1
}
echo ""
echo "✅ Smoke tests passed"
echo ""

# Verify model fields
echo "🔍 Verifying model field integrity..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_cms.settings')
import django
django.setup()

from marketing.models import MediaAsset

# Create test asset
asset = MediaAsset(file='https://example.com/test.jpg', alt_text='Test')

# Check for correct field
assert hasattr(asset, 'created_at'), '❌ MediaAsset missing created_at field'

# Check for wrong field
assert not hasattr(asset, 'uploaded_at'), '❌ MediaAsset should not have uploaded_at field'

print('✅ Model field integrity verified')
" || {
    echo "❌ Model field verification failed"
    exit 1
}
echo ""

# Verify templates exist
echo "📄 Verifying CMS templates exist..."
templates=(
    "marketing/templates/marketing/cms/dashboard.html"
    "marketing/templates/marketing/cms/page_list.html"
    "marketing/templates/marketing/cms/page_form.html"
    "marketing/templates/marketing/cms/post_list.html"
    "marketing/templates/marketing/cms/post_form.html"
    "marketing/templates/marketing/cms/navigation.html"
)

missing_templates=()
for template in "${templates[@]}"; do
    if [ ! -f "$template" ]; then
        missing_templates+=("$template")
    fi
done

if [ ${#missing_templates[@]} -gt 0 ]; then
    echo "❌ Missing templates:"
    for template in "${missing_templates[@]}"; do
        echo "  - $template"
    done
    exit 1
fi

echo "✅ All CMS templates exist"
echo ""

# Verify URL configuration
echo "🔗 Verifying URL configuration..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_cms.settings')
import django
django.setup()

from django.urls import reverse

critical_urls = [
    'marketing-home',
    'robots-txt',
    'sitemap',
    'cms-dashboard',
    'cms-page-list',
    'cms-post-list',
]

for url_name in critical_urls:
    try:
        url = reverse(url_name)
        print(f'  ✅ {url_name}: {url}')
    except Exception as e:
        print(f'  ❌ {url_name}: {e}')
        exit(1
" || {
    echo "❌ URL configuration verification failed"
    exit 1
}
echo ""

# Success message
echo "=================================="
echo "✅ ALL VERIFICATIONS PASSED!"
echo "=================================="
echo ""
echo "The test suite is properly configured and catching issues."
echo ""
echo "Next steps:"
echo "  1. Run full test suite: python run_tests.py"
echo "  2. Run with coverage: python run_tests.py coverage"
echo "  3. Install pre-commit: pre-commit install"
echo "  4. Push to GitHub to enable CI/CD"
echo ""
echo "Happy testing! 🎉"
